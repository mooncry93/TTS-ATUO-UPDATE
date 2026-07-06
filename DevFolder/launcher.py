import os
import sys
import subprocess
import ctypes
import time

def show_error(title, message):
    if sys.platform == "win32":
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)
    else:
        print(f"[{title}] {message}", file=sys.stderr)

def main():
    print("=========================================================")
    print("             Digital_TTS Studio Launcher                 ")
    print("=========================================================")
    print()
    
    # 1. Determine local paths
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    venv_dir = os.path.join(script_dir, "venv")
    venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
    
    # 2. Check if virtual environment exists
    venv_exists = os.path.exists(venv_python)
    
    if not venv_exists:
        print("[LAUNCHER] Local virtual environment (venv) not found.")
        print("[LAUNCHER] Verifying system Python installation...")
        
        # Verify python is available in system PATH and is version 3.12
        python_found = False
        version_ok = False
        found_version = ""
        
        try:
            # Check if python exists and get version
            res = subprocess.run(["python", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            found_version = res.stdout.decode().strip() or res.stderr.decode().strip()
            python_found = True
            
            # Check if it is Python 3.12
            version_res = subprocess.run(["python", "-c", "import sys; print(sys.version_info[:2] == (3, 12))"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            if version_res.stdout.decode().strip() == "True":
                version_ok = True
        except Exception:
            pass
            
        if not python_found:
            show_error(
                "Python Missing",
                "Python is not installed or not added to your system PATH.\n\n"
                "Please install Python 3.12.x from python.org.\n"
                "Make sure to check the box 'Add Python to PATH' during installation."
            )
            sys.exit(1)
            
        if not version_ok:
            show_error(
                "Python Version Mismatch",
                f"Your system has {found_version} installed.\n\n"
                "This application requires Python 3.12.x to run securely.\n"
                "Please install Python 3.12.x from python.org and ensure it is set as your default python."
            )
            sys.exit(1)
            
        print("[LAUNCHER] Creating local Python virtual environment (venv)...")
        print("[LAUNCHER] This will take a moment...")
        try:
            subprocess.run(["python", "-m", "venv", "venv"], check=True)
            print("[LAUNCHER] Virtual environment created successfully.")
        except Exception as e:
            show_error("Venv Error", f"Failed to create virtual environment: {str(e)}")
            sys.exit(1)
            
    # 3. Run setup_env.py to verify/install dependencies and download model files
    print("[LAUNCHER] Validating environment and checking model files...")
    venv_python_abs = os.path.abspath(venv_python)
    setup_env_abs = os.path.abspath(os.path.join("UPDATE RELEASE", "setup_env.py"))
    
    if not os.path.exists(setup_env_abs):
        show_error("Setup Error", f"Cannot find setup_env.py in 'UPDATE RELEASE'")
        sys.exit(1)
        
    try:
        # Run setup_env.py inside the venv
        subprocess.run([venv_python_abs, setup_env_abs], check=True)
    except Exception as e:
        show_error("Setup Error", "Environment setup or model download failed. Please check the logs in the console.")
        input("\nPress Enter to exit...")
        sys.exit(1)
        
    # 4. Launch the application orchestrator
    print("\n[LAUNCHER] Starting all microservices...")
    run_all_abs = os.path.abspath("run_all.py")
    if not os.path.exists(run_all_abs):
        show_error("Execution Error", f"Cannot find run_all.py in '{script_dir}'")
        sys.exit(1)
        
    try:
        # Run run_all.py using venv python
        res = subprocess.run([venv_python_abs, run_all_abs])
        if res.returncode != 0:
            show_error("Execution Error", f"Application orchestrator terminated with exit code {res.returncode}.")
            input("\nPress Enter to exit...")
            sys.exit(res.returncode)
    except KeyboardInterrupt:
        print("\n[LAUNCHER] Launcher terminated by user.")
    except Exception as e:
        show_error("Execution Error", f"Failed to launch orchestrator: {str(e)}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
