import os
import sys
import time
import torch
import soundfile as sf
import asyncio
import threading
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# Add VoxCPM-main/src to Python path so we can import voxcpm modules
def resolve_path(rel_path):
    base_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
    cwd_path = os.path.abspath(rel_path)
    if os.path.exists(cwd_path):
        return cwd_path
    path1 = os.path.join(base_dir, rel_path)
    if os.path.exists(path1):
        return path1
    path2 = os.path.join(os.path.dirname(base_dir), rel_path)
    if os.path.exists(path2):
        return path2
    return path1

voxcpm_src = resolve_path("VoxCPM2/VoxCPM-main/src")
sys.path.insert(0, voxcpm_src)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global last_request_time
    last_request_time = time.time()
    asyncio.create_task(idle_cleanup_loop())
    print("[VoxCPM Server] Daemon running in lazy-load mode (RAM: cold, CPU: smooth).")
    yield

app = FastAPI(title="Real VoxCPM2 Inference Daemon", lifespan=lifespan)

# Load model weights on demand
model_path = resolve_path("VoxCPM2/models/openbmb__VoxCPM2")
model = None
model_lock = threading.Lock()
generation_lock = threading.Lock()
active_requests = 0
active_lock = threading.Lock()
last_request_time = 0.0

def load_model():
    global model
    with model_lock:
        if model is not None:
            return
        try:
            # Limit CPU threads to prevent thread contention during parallel runs
            torch.set_num_threads(4)
            import gc
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            elif hasattr(torch, "mps") and torch.backends.mps.is_available():
                torch.mps.empty_cache()

            if torch.cuda.is_available():
                device = "cuda"
            elif torch.backends.mps.is_available():
                device = "mps"
            else:
                device = "cpu"
                
            print(f"[VoxCPM Server] Initializing model on device: {device} (Lazy Loading)...")
            from voxcpm import VoxCPM
            
            model = VoxCPM.from_pretrained(
                model_path,
                load_denoiser=False,
                local_files_only=True,
                optimize=True,
                device=device
            )
            print("[VoxCPM Server] Real VoxCPM2 model loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to load VoxCPM2 model: {e}")
            import traceback
            traceback.print_exc()

def unload_model():
    global model
    if model is not None:
        print("[VoxCPM Server] Unloading model to release memory...")
        del model
        model = None
        
        # Run garbage collection
        import gc
        gc.collect()
        
        # Purge PyTorch Cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        if hasattr(torch, "mps") and torch.backends.mps.is_available():
            torch.mps.empty_cache()
        print("[VoxCPM Server] Memory successfully purged (CPU and VRAM cooled).")

async def idle_cleanup_loop():
    global last_request_time, model, active_requests
    while True:
        await asyncio.sleep(5)
        # Only check idle timeout if there are no active requests in flight
        if model is not None and active_requests == 0:
            idle_time = time.time() - last_request_time
            # 10 minutes idle unload limit
            if idle_time > 600.0:
                print(f"[VoxCPM Server] Idle timeout reached ({idle_time:.1f}s). Releasing resources...")
                unload_model()

@app.post("/cleanup")
async def voxcpm_cleanup():
    unload_model()
    return {"status": "success", "message": "VoxCPM2 memory and VRAM purged successfully."}

@app.post("/synthesize")
def voxcpm_synthesize(data: dict):
    global model, last_request_time, active_requests
    with active_lock:
        active_requests += 1
    last_request_time = time.time()
    
    try:
        # Load model on demand
        load_model()
        if model is None:
            return JSONResponse(
                status_code=503,
                content={"detail": "VoxCPM2 model failed to initialize."}
            )
            
        text = data.get("text", "")
        cfg_value = float(data.get("cfg_value", 2.0))
        low_spec_mode = bool(data.get("low_spec_mode", False))
        
        # If low-spec mode is enabled (checked in UI settings by default),
        # reduce diffusion timesteps to speed up older GPUs/CPUs by 40%
        default_steps = 6 if low_spec_mode else 10
        inference_timesteps = int(data.get("inference_timesteps", default_steps))
        
        reference_wav_path = data.get("reference_wav_path")
        prompt_text = data.get("prompt_text")
        
        # Construct kwargs for model generation
        kw = {
            "text": text,
            "cfg_value": cfg_value,
            "inference_timesteps": inference_timesteps,
            "normalize": False
        }
        
        if reference_wav_path and os.path.exists(reference_wav_path):
            kw["reference_wav_path"] = reference_wav_path
            if prompt_text:
                kw["prompt_wav_path"] = reference_wav_path
                kw["prompt_text"] = prompt_text
                
        print(f"[VoxCPM Server] Synthesizing: '{text[:50]}...' | Low-Spec Mode: {low_spec_mode}")
        
        # Generate speech (thread-safe lock to prevent KV cache collision)
        with generation_lock:
            wav_data = model.generate(**kw)
        
        # Ensure it's a 1D numpy array
        import numpy as np
        if isinstance(wav_data, torch.Tensor):
            wav_data = wav_data.cpu().numpy()
        wav_data = np.squeeze(wav_data)
        
        # Extract correct sample rate
        sr = getattr(model, 'sample_rate', None)
        if sr is None and hasattr(model, 'tts_model'):
            sr = getattr(model.tts_model, 'sample_rate', 24000)
        elif sr is None:
            sr = 24000
            
        # Write file with a unique name to prevent race conditions during concurrent runs
        import uuid
        out_filename = f"voxcpm_output_{uuid.uuid4().hex}.wav"
        out_path = os.path.abspath(out_filename)
        sf.write(out_path, wav_data, sr)
        
        # Release memory immediately if low spec mode is active and no other requests are in flight
        if low_spec_mode:
            with active_lock:
                if active_requests <= 1:
                    unload_model()
            
        return {"status": "success", "file_path": out_path}
        
    except Exception as e:
        print(f"[ERROR] Synthesis failed: {e}")
        import traceback
        traceback.print_exc()
        if active_requests <= 1:
            unload_model()
        return JSONResponse(
            status_code=500,
            content={"detail": f"VoxCPM synthesis error: {str(e)}"}
        )
    finally:
        with active_lock:
            active_requests -= 1
        last_request_time = time.time()

def main():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8081, log_level="warning")

if __name__ == "__main__":
    main()

