import os
import sys
import subprocess
import hashlib
import json
import base64
import uuid
from datetime import datetime

# --- HARDCODED MASTER RSA PUBLIC KEY (n, e) ---
# We will populate these values shortly after generating them via keygen.py
# Modulus (n) as a decimal integer or hex, and Exponent (e) = 65537
RSA_N = 71994847009419654198890424317799696172712974090219423424341340975275784983644509861903767267806382243240906942198398099718989327287768345141242034355848014239571123802198951423502466806124479640775988274631650397754391868448338459527485136220432121760447031679031581472955264566923537232944106854306211726121
RSA_E = 65537

# --- ONLINE VALIDATION SYSTEM (GOOGLE SHEETS) ---
# Paste your published Web App macro link from Google Sheets here!
GOOGLE_SHEET_CSV_URL = "https://script.google.com/macros/s/AKfycbwRaX5Ky2MMHW95lTp0XyZKnOxD2Sl9wx7t_vNkCsvWUfrRKANpwp9Lcop0TSk741uZ/exec"

def get_raw_uuid():
    """Queries the OS-specific unique motherboard or hardware UUID."""
    uuid_str = ""
    try:
        if sys.platform == "win32":
            # Windows: Query motherboard UUID
            cmd = "wmic csproduct get uuid"
            output = subprocess.check_output(cmd, shell=True).decode().split()
            if len(output) >= 2:
                uuid_str = output[1].strip()
        elif sys.platform == "darwin":
            # macOS: Query IOPlatformUUID
            cmd = "ioreg -rd1 -c IOPlatformExpertDevice"
            output = subprocess.check_output(cmd, shell=True).decode()
            for line in output.split("\n"):
                if "IOPlatformUUID" in line:
                    parts = line.split("=")
                    if len(parts) >= 2:
                        uuid_str = parts[1].replace('"', '').strip()
                        break
        else:
            # Linux: Query machine-id or product_uuid
            for path in ["/sys/class/dmi/id/product_uuid", "/etc/machine-id"]:
                if os.path.exists(path):
                    with open(path, "r") as f:
                        uuid_str = f.read().strip()
                        break
    except Exception:
        pass
    
    # Filter out common placeholders or invalid outputs
    invalid_uuids = {"", "to be filled by o.e.m.", "00000000-0000-0000-0000-000000000000", "unknown"}
    if uuid_str.lower() in invalid_uuids:
        return ""
    return uuid_str

def get_mac_address():
    """Fallback: Generates a stable hardware identifier based on the network MAC address."""
    try:
        node = uuid.getnode()
        # uuid.getnode() returns a random 48-bit number if MAC lookup fails.
        # Check if the returned node is universal/stable.
        if (node >> 40) & 1 == 0:
            return f"MAC-{node}"
    except Exception:
        pass
    return ""

def calculate_hwid():
    """Generates a stable, unique 16-character Hardware ID formatted as THY-XXXX-XXXX-XXXX-XXXX."""
    raw_id = get_raw_uuid()
    if not raw_id:
        raw_id = get_mac_address()
    if not raw_id:
        # Final fallback: computer hostname
        import socket
        raw_id = f"HOST-{socket.gethostname()}"
        
    # Generate SHA-256 hash of the raw hardware trait
    hasher = hashlib.sha256(raw_id.encode("utf-8"))
    hex_digest = hasher.hexdigest().upper()
    
    # Group the first 16 characters into blocks of 4
    blocks = [hex_digest[i:i+4] for i in range(0, 16, 4)]
    return "THY-" + "-".join(blocks)

def verify_license(license_key_str):
    """
    Decodes and validates the RSA signature on a license key.
    Returns: (is_valid: bool, expiry_date: str, message: str)
    """
    global RSA_N, RSA_E
    if RSA_N == 0:
        return False, "", "Public key is not initialized."
        
    try:
        # 1. Decode combined license key from Base64
        combined_bytes = base64.b64decode(license_key_str.strip().encode("utf-8"))
        
        # 2. Split by separator b"||"
        if b"||" not in combined_bytes:
            return False, "", "Invalid license key format structure."
            
        data_bytes, sig_bytes = combined_bytes.split(b"||", 1)
        
        # 3. Deserialize license dictionary metadata
        license_metadata = json.loads(data_bytes.decode("utf-8"))
        hwid = license_metadata.get("hwid", "")
        expiry = license_metadata.get("expiry", "")
        
        # 4. Verify signature cryptographically using RSA
        signature_int = int.from_bytes(sig_bytes, "big")
        
        # S^e mod n
        decrypted_hash_int = pow(signature_int, RSA_E, RSA_N)
        
        # Calculate expected hash
        expected_hash = hashlib.sha256(data_bytes).digest()
        expected_hash_int = int.from_bytes(expected_hash, "big")
        
        if decrypted_hash_int != expected_hash_int:
            return False, "", "Cryptographic signature validation failed."
            
        # 5. Check if HWID matches current machine
        local_hwid = calculate_hwid()
        if hwid != local_hwid:
            return False, "", f"License is registered for another machine ({hwid})."
            
        # 6. Check Expiration Date
        if expiry != "lifetime":
            try:
                expiry_dt = datetime.strptime(expiry, "%Y-%m-%d")
                if datetime.now() > expiry_dt:
                    return False, expiry, f"License expired on {expiry}."
            except ValueError:
                return False, "", "Invalid date format in license."
                
        return True, expiry, "License is valid and active."
        
    except Exception as e:
        return False, "", f"Verification error: {str(e)}"

def get_license_file_path():
    """
    Returns the absolute path to the local license.lic file.
    To avoid license loss during updates, we store it in the user's home directory.
    Fallback to local directory if home directory is not writable.
    """
    home_dir = os.path.expanduser("~")
    app_dir = os.path.join(home_dir, ".digital_tts")
    try:
        os.makedirs(app_dir, exist_ok=True)
        # Verify write permission
        test_file = os.path.join(app_dir, ".write_test")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        return os.path.join(app_dir, "license.lic")
    except Exception:
        # Fallback to local file in current working directory
        return "license.lic"

def check_local_license():
    """
    Checks if a valid 'license.lic' file exists in the persistent directory or CWD.
    Returns: (is_valid: bool, hwid: str, expiry: str, message: str)
    """
    local_hwid = calculate_hwid()
    lic_file = get_license_file_path()
    
    # Legacy Migration check: if a local license exists in CWD but not in the persistent directory
    legacy_lic = "license.lic"
    if os.path.exists(legacy_lic) and lic_file != legacy_lic and not os.path.exists(lic_file):
        try:
            import shutil
            shutil.copy2(legacy_lic, lic_file)
            print(f"[LICENSING] Migrated legacy local license from {legacy_lic} to {lic_file}")
        except Exception as e:
            print(f"[LICENSING] Failed to migrate legacy license: {e}")
            
    if not os.path.exists(lic_file):
        # As final fallback check legacy file
        if os.path.exists(legacy_lic):
            lic_file = legacy_lic
        else:
            return False, local_hwid, "", "License file 'license.lic' not found."
        
    try:
        with open(lic_file, "r") as f:
            lic_key = f.read().strip()
        is_valid, expiry, msg = verify_license(lic_key)
        return is_valid, local_hwid, expiry, msg
    except Exception as e:
        return False, local_hwid, "", f"Failed to read license: {str(e)}"

def check_online_status(license_key):
    """
    Checks the status of the license key online using the Google Apps Script Web App API.
    Returns: (is_blocked: bool, message: str)
    """
    if not GOOGLE_SHEET_CSV_URL:
        return False, "Online validation server not configured. Running in secure offline mode."
        
    try:
        import urllib.request
        import urllib.parse
        import json
        
        # Build query parameters for Google Apps Script Web App
        url = f"{GOOGLE_SHEET_CSV_URL}?key={urllib.parse.quote(license_key.strip())}"
        
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        response = urllib.request.urlopen(req, timeout=4.0)
        data = json.loads(response.read().decode('utf-8'))
        
        status = data.get("status", "").lower()
        message = data.get("message", "License is verified.")
        
        if status in ("revoked", "blocked", "inactive", "not_found"):
            return True, f"License has been deactivated or removed by admin (Status: {status})."
            
        return False, "License status verified and active."
        
    except Exception as e:
        print(f"[LICENSING] Web App connection failed (falling back to offline check): {e}")
        return False, "Validation server offline. Running in secure offline mode."
