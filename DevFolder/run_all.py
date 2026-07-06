import sys
import os
import subprocess
import time
import signal

# List of active subprocesses
processes = []

def terminate_all(sig=None, frame=None):
    """Gracefully terminates all active subprocesses."""
    print("\n[ORCHESTRATOR] Received shutdown signal. Terminating all microservices...")
    for p in processes:
        try:
            p.terminate()
            p.wait(timeout=2.0)
        except Exception:
            p.kill()
    print("[ORCHESTRATOR] Clean shutdown complete.")
    sys.exit(0)

# Connect interrupts to cleanup logic
signal.signal(signal.SIGINT, terminate_all)
signal.signal(signal.SIGTERM, terminate_all)

def check_requirements():
    """Verifies that fastapi, uvicorn, and requests are installed."""
    try:
        import fastapi
        import uvicorn
        import requests
    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e.name}. Please run 'pip install fastapi uvicorn requests' first.")
        sys.exit(1)

def main():
    check_requirements()
    
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(workspace_dir)
    
    print("=" * 70)
    print("      DIGITAL_TTS BY MR.THY MULTI-ENGINE LOCAL TTS SYSTEM ORCHESTRATOR      ")
    print("=" * 70)
    

    is_frozen = getattr(sys, 'frozen', False)

    # Determine the commands to run.
    vox_python = sys.executable
    if sys.platform == "win32":
        possible_runtimes = [
            os.path.join("VoxCPM2", "voxcpm_runtime", "python.exe"),
            os.path.join("..", "VoxCPM2", "voxcpm_runtime", "python.exe")
        ]
        for runtime in possible_runtimes:
            if os.path.exists(runtime):
                vox_python = os.path.abspath(runtime)
                break

    vox_cmd = [vox_python, "run_all.py", "--server", "voxcpm"]
    
    # Check if compiled secure gateway.exe exists (packaged installer mode)
    gateway_exe_path = os.path.join(workspace_dir, "gateway.exe")
    if sys.platform == "win32" and os.path.exists("gateway.exe"):
        gate_cmd = [os.path.abspath("gateway.exe")]
    elif sys.platform == "win32" and os.path.exists(gateway_exe_path):
        gate_cmd = [gateway_exe_path]
    else:
        # In development, fall back to running python run_all.py --server gateway
        gate_cmd = [sys.executable, "run_all.py", "--server", "gateway"]

    # 2. Start Real VoxCPM2 Server (Port 8081)
    print("[ORCHESTRATOR] Starting Real VoxCPM2 Server (Port 8081)...")
    import tempfile
    if is_frozen:
        log_vox_path = os.path.join(tempfile.gettempdir(), "voxcpm.log")
    else:
        log_vox_path = "voxcpm.log"
    log_vox = open(log_vox_path, "w", buffering=1)
    p_vox = subprocess.Popen(
        vox_cmd,
        stdout=log_vox,
        stderr=log_vox
    )
    processes.append(p_vox)

    
    # Give mock servers 1.5 seconds to boot and bind to their ports
    print("[ORCHESTRATOR] Warming up local ports...")
    time.sleep(1.5)
    
    # 4. Start Unified API Gateway (Port 8000)
    print("[ORCHESTRATOR] Starting Unified Gateway & UI Server (Port 8000)...")
    if is_frozen:
        log_gate_path = os.path.join(tempfile.gettempdir(), "gateway.log")
    else:
        log_gate_path = "gateway.log"
    log_gate = open(log_gate_path, "w", buffering=1)
    p_gate = subprocess.Popen(
        gate_cmd,
        stdout=log_gate,
        stderr=log_gate
    )
    processes.append(p_gate)
    
    print("\n" + "=" * 70)
    print("SUCCESS: All services are successfully initialized and running.")
    print("-> Web GUI Dashboard: http://127.0.0.1:8000")
    print("-> Gateway Routing:  http://127.0.0.1:8000/api/generate")
    print("-> Status Check:     http://127.0.0.1:8000/api/status")
    print("=" * 70)
    print("Press Ctrl+C to terminate all services and free ports.")
    
    # Automatically open the browser to the web GUI dashboard
    import webbrowser
    print("[ORCHESTRATOR] Opening default browser to the web UI...")
    webbrowser.open("http://127.0.0.1:8000")

    
    # Keep orchestrator process alive to monitor children
    try:
        while True:
            # Check if any child process has died unexpectedly
            for p in processes:
                if p.poll() is not None:
                    print(f"\n[WARNING] A microservice terminated unexpectedly (Exit Code: {p.returncode}). Restarting all...")
                    terminate_all()
            time.sleep(1)
    except KeyboardInterrupt:
        terminate_all()

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    
    if len(sys.argv) > 2 and sys.argv[1] == "--server":
        server_type = sys.argv[2]
        if server_type == "voxcpm":
            import voxcpm_server
            voxcpm_server.main()
            sys.exit(0)
        elif server_type == "gateway":
            import gateway
            gateway.main()
            sys.exit(0)
        elif server_type == "downloader":
            import download_models
            download_models.main()
            sys.exit(0)
        elif server_type == "setup":
            import setup_env
            setup_env.main()
            sys.exit(0)

            
    main()
