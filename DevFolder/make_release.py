import os
import shutil
import sys

def build_customer_release():
    print("=============================================================")
    print("       Digital_TTS Release Packer: Preparing Customer Files   ")
    print("=============================================================")
    
    # 1. Check if the compiled distribution folder exists
    compiled_src = os.path.join("dist", "Digital_TTS_Studio")
    
    if not os.path.exists(compiled_src):
        print("[WARNING] Compiled folder 'dist/Digital_TTS_Studio' not found.")
        print("Please compile the application on Windows first by running:")
        print("👉 python build_windows_exe.py")
        print("\nWe will proceed by creating the template folder structures for you.")
        
    release_dir = os.path.join("..", "For Client")
    if os.path.exists(release_dir):
        try:
            shutil.rmtree(release_dir)
        except Exception as e:
            print(f"[WARNING] Could not clear existing release folder: {e}. Attempting to copy on top of it...")
            
    os.makedirs(release_dir, exist_ok=True)
    
    # 2. Files that MUST remain PRIVATE (Never share these!)
    private_files = ["master_keys.json", "keygen.py", "license.lic", "make_release.py", "build_windows_exe.py", "installer_config.iss"]
    
    # 3. Copy compiled application files to the Release folder
    client_studio_dir = os.path.join(release_dir, "Digital_TTS_Studio")
    if os.path.exists(compiled_src):
        print(f"[PACK] Copying compiled binaries from '{compiled_src}' to '{release_dir}'...")
        shutil.copytree(compiled_src, client_studio_dir, dirs_exist_ok=True)
        gateway_compiled = os.path.join("dist", "gateway.exe")
        if os.path.exists(gateway_compiled):
            print(f"[PACK] Copying compiled gateway executable to '{client_studio_dir}'...")
            shutil.copy2(gateway_compiled, os.path.join(client_studio_dir, "gateway.exe"))
    else:
        # Copy the public source code files to the client folder (allowing source run if not compiled yet)
        print(f"[PACK] Compiled folder not found. Copying public source code files instead...")
        os.makedirs(client_studio_dir, exist_ok=True)
        
        # Copy python files
        public_py_files = ["gateway.py", "license_verify.py", "run_all.py", "voxcpm_server.py"]
        for f in public_py_files:
            if os.path.exists(f):
                shutil.copy2(f, os.path.join(client_studio_dir, f))
                
        # Copy static folder
        shutil.copytree("static", os.path.join(client_studio_dir, "static"), dirs_exist_ok=True)

    # 4. Copy scripts and update release folder to the client package (always required for launcher/setup)
    print(f"[PACK] Packaging update releases and launcher scripts...")
    
    # Copy UPDATE RELEASE directory
    client_update_dir = os.path.join(client_studio_dir, "UPDATE RELEASE")
    if os.path.exists(client_update_dir):
        shutil.rmtree(client_update_dir)
    shutil.copytree("UPDATE RELEASE", client_update_dir, dirs_exist_ok=True)

    # Always copy public scripts to the root of the client folder
    public_scripts_src = [
        "run_all.bat",
        "START_APP.bat",
        "START_APP.command",
        os.path.join("UPDATE RELEASE", "setup.bat"),
        os.path.join("UPDATE RELEASE", "setup.sh")
    ]
    for src in public_scripts_src:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(client_studio_dir, os.path.basename(src)))

    # Always copy run_all.py and voxcpm_server.py (preferring obfuscated files if available)
    obf_run_all = os.path.join("dist_obfuscated", "run_all.py")
    if os.path.exists(obf_run_all):
        print("[PACK] Copying obfuscated run_all.py from dist_obfuscated...")
        shutil.copy2(obf_run_all, os.path.join(client_studio_dir, "run_all.py"))
        # Also copy PyArmor runtime folder
        pyarmor_runtime_src = os.path.join("dist_obfuscated", "pyarmor_runtime_000000")
        if os.path.exists(pyarmor_runtime_src):
            pyarmor_runtime_dest = os.path.join(client_studio_dir, "pyarmor_runtime_000000")
            if os.path.exists(pyarmor_runtime_dest):
                shutil.rmtree(pyarmor_runtime_dest)
            shutil.copytree(pyarmor_runtime_src, pyarmor_runtime_dest, dirs_exist_ok=True)
    else:
        if os.path.exists("run_all.py"):
            shutil.copy2("run_all.py", os.path.join(client_studio_dir, "run_all.py"))
            
    if os.path.exists("voxcpm_server.py"):
        shutil.copy2("voxcpm_server.py", os.path.join(client_studio_dir, "voxcpm_server.py"))

    if os.path.exists("download_models.py"):
        shutil.copy2("download_models.py", os.path.join(client_studio_dir, "download_models.py"))

    # 4. Copy VoxCPM2 resources (including heavy models) if they exist
    voxcpm_src = "VoxCPM2"
    voxcpm_dest = os.path.join(release_dir, "VoxCPM2")
    if os.path.exists(voxcpm_src):
        print(f"[PACK] Copying VoxCPM2 framework files & model weights...")
        os.makedirs(voxcpm_dest, exist_ok=True)
        
        # Copy inference library folder
        sub_lib = os.path.join(voxcpm_src, "VoxCPM-main")
        if os.path.exists(sub_lib):
            shutil.copytree(sub_lib, os.path.join(voxcpm_dest, "VoxCPM-main"), dirs_exist_ok=True)
            
        # Copy compiled model weights folder
        sub_models = os.path.join(voxcpm_src, "models")
        if os.path.exists(sub_models):
            shutil.copytree(sub_models, os.path.join(voxcpm_dest, "models"), dirs_exist_ok=True)
            
        # Copy FFmpeg dependencies
        ffmpeg_file = os.path.join(voxcpm_src, "ffmpeg.exe")
        if os.path.exists(ffmpeg_file):
            shutil.copy2(ffmpeg_file, os.path.join(voxcpm_dest, "ffmpeg.exe"))
    else:
        print("[INFO] No 'VoxCPM2/' directory detected. Client will need to obtain VoxCPM2 components separately.")

    # 5. Copy the Installation Instructions Guide (KHMER)
    guide_src = "INSTALLATION_GUIDE.md"
    if os.path.exists(guide_src):
        print(f"[PACK] Including '{guide_src}' in the release package...")
        shutil.copy2(guide_src, os.path.join(release_dir, guide_src))

    # 6. Create MAC USER release folder with public scripts/sources
    mac_dir = os.path.join(release_dir, "MAC USER")
    print(f"[PACK] Creating macOS release package folder '{mac_dir}'...")
    if os.path.exists(mac_dir):
        shutil.rmtree(mac_dir)
    os.makedirs(mac_dir, exist_ok=True)
    
    # Obfuscate core python files for macOS client safety
    from obfuscator import obfuscate_file
    mac_py_files = ["gateway.py", "license_verify.py", "voxcpm_server.py", "download_models.py"]
    for f in mac_py_files:
        if os.path.exists(f):
            dest_path = os.path.join(mac_dir, f)
            obfuscate_file(f, dest_path)
            
    # Copy plain run_all.py (always plain on macOS to avoid Windows PyArmor runtime incompatibility)
    if os.path.exists("run_all.py"):
        shutil.copy2("run_all.py", os.path.join(mac_dir, "run_all.py"))

    # Copy static assets folder
    shutil.copytree("static", os.path.join(mac_dir, "static"), dirs_exist_ok=True)

    # Copy launcher scripts
    if os.path.exists("START_APP.command"):
        shutil.copy2("START_APP.command", os.path.join(mac_dir, "START_APP.command"))
    if os.path.exists(os.path.join("UPDATE RELEASE", "setup.sh")):
        shutil.copy2(os.path.join("UPDATE RELEASE", "setup.sh"), os.path.join(mac_dir, "setup.sh"))
        
    # Copy UPDATE RELEASE directory containing setup_env.py
    shutil.copytree("UPDATE RELEASE", os.path.join(mac_dir, "UPDATE RELEASE"), dirs_exist_ok=True)

    # 7. Sync UPDATE RELEASE to the parent directory root folder for GitHub
    parent_update_dir = os.path.join("..", "UPDATE RELEASE")
    local_update_dir = "UPDATE RELEASE"
    if os.path.exists(local_update_dir):
        print(f"[PACK] Syncing '{local_update_dir}' to root parent folder '{parent_update_dir}'...")
        if os.path.exists(parent_update_dir):
            try:
                shutil.rmtree(parent_update_dir)
            except Exception:
                pass
        try:
            shutil.copytree(local_update_dir, parent_update_dir, dirs_exist_ok=True)
            print("[PACK] Auto-update setup files synced successfully.")
        except Exception as e:
            print(f"[WARNING] Failed to sync auto-update setup folder to root: {e}")

    print("\n======================= RELEASE PACK COMPLETE =======================")
    print("A clean customer package has been created successfully!")
    print(f"Directory: {os.path.abspath(release_dir)}")
    print("---------------------------------------------------------------------")
    print("📂 WHAT YOU SHOULD GIVE TO YOUR CUSTOMER:")
    print("  Give them the ENTIRE folder 'For Client/'. It contains:")
    print("  ├── Digital_TTS_Studio/   <- Contains Compiled Exe (or public code), static UI, DLLs")
    print("  ├── VoxCPM2/              <- Contains VoxCPM2 framework, code libraries, and models")
    print("  └── INSTALLATION_GUIDE.md <- Khmer instructions for Windows/Mac")
    print("---------------------------------------------------------------------")
    print("🛑 WHAT YOU MUST KEEP SECRET (DO NOT GIVE TO CUSTOMER):")
    print("  The following files in your current workspace contain security/keys:")
    for f in private_files:
        if os.path.exists(f):
            print(f"  ❌ {f} (Contains private signing keys or developer code)")
    print("=====================================================================")

if __name__ == "__main__":
    build_customer_release()
