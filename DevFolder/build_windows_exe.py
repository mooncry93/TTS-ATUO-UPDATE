import os
import sys
import shutil
import subprocess

def check_pyinstaller():
    """Checks if PyInstaller is installed in the current environment."""
    try:
        import PyInstaller
        return True
    except ImportError:
        print("[INFO] PyInstaller is not installed. Installing it via pip...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            return True
        except Exception as e:
            print(f"[ERROR] Failed to install PyInstaller: {e}")
            return False

def build_exe():
    if sys.platform != "win32":
        print("=============================================================")
        print("[WARNING] CROSS-COMPILATION CONSTRAINT")
        print("-------------------------------------------------------------")
        print("You are currently running on a non-Windows OS (macOS/Linux).")
        print("To generate a Windows '.exe', you must run this script")
        print("on a Windows machine.")
        print("=============================================================")
        return

    print("=============================================================")
    print("      Digital_TTS Compiler: Building Secure Windows Launcher ")
    print("=============================================================")

    if not check_pyinstaller():
        return

    # Directories for the build output
    dist_dir = "dist"
    build_dir = "build"
    output_launcher_folder = os.path.join(dist_dir, "Digital_TTS_Studio")

    # Clear previous builds
    for path in [dist_dir, build_dir]:
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                print(f"[WARNING] Could not clear '{path}' directory: {e}")

    # Find FFI DLLs in the running compiler python environment
    ffi_dlls = []
    python_dir = os.path.dirname(sys.executable)
    lib_bin = os.path.join(python_dir, "Library", "bin")
    search_dirs = [python_dir, lib_bin]
    for d in search_dirs:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f.lower().startswith("ffi") and f.lower().endswith(".dll"):
                    ffi_dlls.append(os.path.join(d, f))
    print(f"[BUILD] Found FFI DLL dependencies to include: {ffi_dlls}")

    # 1. Run PyInstaller to compile launcher.py into launcher executable folder (onedir)
    print("[BUILD] Compiling launcher source code (launcher.py) to executable folder...")
    pyinstaller_launcher_cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--console",
        "--onedir",
        "--name=Digital_TTS_Studio",
        "--icon=app_icon.ico"
    ]
    for dll in ffi_dlls:
        pyinstaller_launcher_cmd.extend(["--add-binary", f"{dll};."])
    pyinstaller_launcher_cmd.append("launcher.py")

    try:
        subprocess.check_call(pyinstaller_launcher_cmd)
        print("[BUILD] Launcher compilation completed successfully.")
    except Exception as e:
        print(f"[ERROR] Launcher PyInstaller compilation failed: {e}")
        return

    # 2. Run PyInstaller to compile gateway.py into a standalone executable file (onefile)
    print("[BUILD] Compiling gateway and licensing (gateway.py) to secure single-file executable...")
    pyinstaller_gateway_cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--console",
        "--onefile",
        "--name=gateway",
        "--icon=app_icon.ico",
        "--exclude-module=torch",
        "--exclude-module=torchvision",
        "--exclude-module=torchaudio",
        "--exclude-module=scipy",
        "--exclude-module=numba",
        "--exclude-module=pandas",
        "--exclude-module=matplotlib",
        "--exclude-module=sympy",
        "--exclude-module=jinja2",
        "--exclude-module=h5py"
    ]
    for dll in ffi_dlls:
        pyinstaller_gateway_cmd.extend(["--add-binary", f"{dll};."])
    pyinstaller_gateway_cmd.append("gateway.py")

    try:
        subprocess.check_call(pyinstaller_gateway_cmd)
        print("[BUILD] Gateway compilation completed successfully.")
    except Exception as e:
        print(f"[ERROR] Gateway PyInstaller compilation failed: {e}")
        return

    # Copy frontend static files into the launcher build folder
    static_src = "static"
    static_dest = os.path.join(output_launcher_folder, "static")
    print(f"[BUILD] Copying static assets from '{static_src}' to '{static_dest}'...")
    try:
        if os.path.exists(static_dest):
            shutil.rmtree(static_dest)
        shutil.copytree(static_src, static_dest)
    except Exception as e:
        print(f"[ERROR] Failed to copy static UI files: {e}")
        return

    print("\n========================= BUILD SUCCESS =========================")
    print(f"Your compiled Windows application files are located at:")
    print(f"-> Launcher folder: {os.path.abspath(output_launcher_folder)}")
    print(f"-> Secure Gateway:  {os.path.abspath(os.path.join(dist_dir, 'gateway.exe'))}")
    print("-----------------------------------------------------------------")
    print("Files ready for packaging:")
    print("1. 'dist/Digital_TTS_Studio/*' (Launcher launcher + UI static assets)")
    print("2. 'dist/gateway.exe' (Compiled API server and license checker)")
    print("=================================================================")

if __name__ == "__main__":
    build_exe()
