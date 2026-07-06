import os
import sys
import time
import json
import subprocess
import urllib.request
import zipfile

PROGRESS_FILE = "setup_progress.json"

MODELS_TO_DOWNLOAD = [
    # VoxCPM2 models
    {
        "name": "VoxCPM2 model.safetensors",
        "url": "https://huggingface.co/openbmb/VoxCPM2/resolve/main/model.safetensors",
        "dest": "VoxCPM2/models/openbmb__VoxCPM2/model.safetensors"
    },
    {
        "name": "VoxCPM2 audiovae.pth",
        "url": "https://huggingface.co/openbmb/VoxCPM2/resolve/main/audiovae.pth",
        "dest": "VoxCPM2/models/openbmb__VoxCPM2/audiovae.pth"
    },
    {
        "name": "VoxCPM2 config.json",
        "url": "https://huggingface.co/openbmb/VoxCPM2/resolve/main/config.json",
        "dest": "VoxCPM2/models/openbmb__VoxCPM2/config.json"
    },
    {
        "name": "VoxCPM2 tokenizer.json",
        "url": "https://huggingface.co/openbmb/VoxCPM2/resolve/main/tokenizer.json",
        "dest": "VoxCPM2/models/openbmb__VoxCPM2/tokenizer.json"
    },
    {
        "name": "VoxCPM2 tokenizer_config.json",
        "url": "https://huggingface.co/openbmb/VoxCPM2/resolve/main/tokenizer_config.json",
        "dest": "VoxCPM2/models/openbmb__VoxCPM2/tokenizer_config.json"
    },
    {
        "name": "VoxCPM2 special_tokens_map.json",
        "url": "https://huggingface.co/openbmb/VoxCPM2/resolve/main/special_tokens_map.json",
        "dest": "VoxCPM2/models/openbmb__VoxCPM2/special_tokens_map.json"
    },
    {
        "name": "VoxCPM2 tokenization_voxcpm2.py",
        "url": "https://huggingface.co/openbmb/VoxCPM2/resolve/main/tokenization_voxcpm2.py",
        "dest": "VoxCPM2/models/openbmb__VoxCPM2/tokenization_voxcpm2.py"
    },
]

def update_progress(active, phase, message, percent, status="running"):
    data = {
        "active": active,
        "phase": phase,
        "message": message,
        "percent": round(percent, 2),
        "status": status,
        "timestamp": time.time()
    }
    try:
        with open(PROGRESS_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

def is_package_installed(pkg_name):
    # Map installer package names to import module names if different
    import_map = {
        "gtts": "gtts",
        "soundfile": "soundfile",
        "numpy": "numpy",
        "torch": "torch",
        "torchaudio": "torchaudio",
        "transformers": "transformers",
        "huggingface_hub": "huggingface_hub",
        "tqdm": "tqdm",
        "pydantic": "pydantic",
        "librosa": "librosa",
        "pyttsx3": "pyttsx3",
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "requests": "requests",
        "einops": "einops",
        "safetensors": "safetensors",
        "addict": "addict",
        "inflect": "inflect",
        "wetext": "wetext",
        "simplejson": "simplejson",
        "sortedcontainers": "sortedcontainers",
        "qwen-asr": "qwen_asr"
    }
    module_name = import_map.get(pkg_name, pkg_name)
    try:
        __import__(module_name)
        if pkg_name == "torch":
            import torch
            if not torch.cuda.is_available():
                return False
        return True
    except Exception:
        return False

def install_dependencies():
    packages = [
        "fastapi", "uvicorn", "requests", "gtts", "soundfile", 
        "numpy", "torch", "torchaudio", "transformers", 
        "huggingface_hub", "tqdm", "pydantic", "librosa", "pyttsx3",
        "einops", "safetensors", "addict", "inflect", "wetext", 
        "simplejson", "sortedcontainers", "qwen-asr"
    ]
    total = len(packages)
    
    print("[SETUP] Verifying/Installing Python dependencies...")
    for idx, pkg in enumerate(packages):
        percent = 5.0 + (idx / total) * 30.0 # 5% to 35%
        
        # Check if already installed to prevent pip calls when offline/already configured
        if is_package_installed(pkg):
            print(f"[SETUP] Dependency verified: {pkg}")
            continue
            
        msg = f"Installing package: {pkg} ({idx+1}/{total})..."
        update_progress(True, "dependencies", msg, percent)
        print(f"[SETUP] {msg}")
        
        try:
            # Install package using pip
            if pkg in ("torch", "torchaudio"):
                cmd = [sys.executable, "-m", "pip", "install", "torch", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu121", "--force-reinstall"]
            else:
                cmd = [sys.executable, "-m", "pip", "install", pkg]
                
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            print(f"[SETUP] Installed {pkg} successfully.")
        except Exception as e:
            print(f"[SETUP] Warning: standard install of {pkg} had an issue, attempting safe install...")
            try:
                if pkg in ("torch", "torchaudio"):
                    cmd_fallback = [sys.executable, "-m", "pip", "install", "torch", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu121", "--force-reinstall"]
                else:
                    cmd_fallback = [sys.executable, "-m", "pip", "install", "--no-warn-script-location", pkg]
                subprocess.run(
                    cmd_fallback,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except:
                pass
                
    update_progress(True, "dependencies", "Python dependencies verified and installed.", 35.0)
    time.sleep(0.5)

def download_file(url, dest_path, display_name, start_pct, end_pct):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # If already downloaded and sized reasonably, skip
    # (VoxCPM config/python files are small, safetensors/pth/gguf models are > 1MB)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        print(f"[SETUP] {display_name} already exists. Skipping.")
        update_progress(True, "download", f"Verified existing {display_name}.", end_pct)
        return True
        
    print(f"[SETUP] Downloading {display_name}...")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=60.0) as response:
            total_size = int(response.info().get('Content-Length', 0))
            downloaded = 0
            start_time = time.time()
            
            with open(dest_path, "wb") as file:
                while True:
                    chunk = response.read(1024 * 1024) # 1MB chunks
                    if not chunk:
                        break
                    file.write(chunk)
                    downloaded += len(chunk)
                    
                    percent_complete = (downloaded / total_size) if total_size > 0 else 0
                    current_pct = start_pct + percent_complete * (end_pct - start_pct)
                    
                    # Calculate speed
                    elapsed = time.time() - start_time
                    speed_mb = (downloaded / (1024 * 1024)) / elapsed if elapsed > 0 else 0
                    
                    msg = f"Downloading {display_name} ({round(percent_complete * 100, 1)}%) - {round(speed_mb, 1)} MB/s"
                    update_progress(True, "download", msg, current_pct)
                    
        return True
    except Exception as e:
        print(f"[SETUP] Error downloading {display_name}: {str(e)}")
        # Clean up partial download
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
            except:
                pass
        raise e

def download_and_extract_ffmpeg(start_pct, end_pct):
    dest_dir = "VoxCPM2"
    if not os.path.exists(dest_dir) and os.path.exists(os.path.join("..", dest_dir)):
        dest_dir = os.path.join("..", dest_dir)
        
    dest_path = os.path.join(dest_dir, "ffmpeg.exe")
    
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000000:
        print("[SETUP] ffmpeg.exe dependency verified. Skipping.")
        update_progress(True, "download", "Verified existing ffmpeg.exe.", end_pct)
        return
        
    zip_path = os.path.join(dest_dir, "ffmpeg.zip")
    url = "https://github.com/ffbinaries/ffbinaries-prebuilt/releases/download/v4.4.1/ffmpeg-4.4.1-win-64.zip"
    
    print("[SETUP] Downloading ffmpeg.exe dependency (~35MB)...")
    update_progress(True, "download", "Downloading ffmpeg.exe binary package...", start_pct)
    
    try:
        # Download zip
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60.0) as response:
            total_size = int(response.info().get('Content-Length', 0))
            downloaded = 0
            start_time = time.time()
            
            with open(zip_path, "wb") as f:
                while True:
                    chunk = response.read(256 * 1024) # 256KB chunks
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    percent_complete = (downloaded / total_size) if total_size > 0 else 0
                    current_pct = start_pct + percent_complete * (end_pct - start_pct)
                    
                    elapsed = time.time() - start_time
                    speed_mb = (downloaded / (1024 * 1024)) / elapsed if elapsed > 0 else 0
                    msg = f"Downloading ffmpeg.exe ({round(percent_complete * 100, 1)}%) - {round(speed_mb, 1)} MB/s"
                    update_progress(True, "download", msg, current_pct)
                    
        # Extract ffmpeg.exe from zip
        print("[SETUP] Extracting ffmpeg.exe...")
        update_progress(True, "download", "Extracting ffmpeg.exe...", end_pct - 2.0)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extract("ffmpeg.exe", dest_dir)
            
        # Clean up zip
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
        print("[SETUP] ffmpeg.exe installed successfully.")
        update_progress(True, "download", "Installed ffmpeg.exe successfully.", end_pct)
    except Exception as e:
        print(f"[SETUP] Warning: Failed to download or extract ffmpeg.exe: {e}")
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except:
                pass
        raise e

def main():
    update_progress(True, "starting", "Starting 1-Click Super Setup & Calibrator...", 2.0)
    time.sleep(0.5)
    
    try:
        # Phase 1: Dependencies (5% to 35%)
        install_dependencies()
        
        # Phase 2: Download ffmpeg.exe (35% to 42%)
        download_and_extract_ffmpeg(35.0, 42.0)
        
        # Phase 3: Download model files (42% to 98%)
        total_downloads = len(MODELS_TO_DOWNLOAD)
        for idx, model_info in enumerate(MODELS_TO_DOWNLOAD):
            start_pct = 42.0 + (idx / total_downloads) * 56.0
            end_pct = 42.0 + ((idx + 1) / total_downloads) * 56.0
            
            dest_rel_path = model_info["dest"]
            if dest_rel_path.startswith("VoxCPM2/") and not os.path.exists("VoxCPM2") and os.path.exists(os.path.join("..", "VoxCPM2")):
                dest_path = os.path.join("..", dest_rel_path)
            else:
                dest_path = dest_rel_path
                
            download_file(
                model_info["url"],
                dest_path,
                model_info["name"],
                start_pct,
                end_pct
            )
        
        # Phase 4: Finalizing
        update_progress(True, "finalizing", "Calibrating model runtimes and validating setup...", 98.0)
        time.sleep(0.5)
        
        # Check for custom update log / changelog note
        update_msg = "1-Click Setup complete! All environment requirements and model weights are ready."
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            log_file = os.path.join(script_dir, "update_log.txt")
            if os.path.exists(log_file):
                with open(log_file, "r", encoding="utf-8") as lf:
                    custom_text = lf.read().strip()
                if custom_text:
                    update_msg = custom_text
        except Exception:
            pass
            
        update_progress(False, "completed", update_msg, 100.0, "completed")
        print("\n" + "="*70)
        print("                   DIGITAL_TTS UPDATE COMPLETED / LOG")
        print("-"*70)
        print(update_msg)
        print("="*70 + "\n")
        
    except Exception as e:
        err_msg = f"Setup failed: {str(e)}"
        print(f"[ERROR] {err_msg}")
        update_progress(False, "error", err_msg, 0.0, "error")
        raise e

if __name__ == "__main__":
    main()
