import os
import sys
import json
import base64
import hashlib
import random
from datetime import datetime

# --- PURE PYTHON RSA UTILITIES ---
def is_prime(n, k=5):
    """Miller-Rabin primality test."""
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=512):
    """Generates a random prime of the specified bit length."""
    while True:
        p = random.getrandbits(bits)
        p |= (1 << (bits - 1)) | 1  # Ensure it is odd and has the exact bit-length
        if is_prime(p):
            return p

def egcd(a, b):
    """Extended Euclidean Algorithm."""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """Modular multiplicative inverse."""
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def generate_keypair(bits=1024):
    """Generates a public/private RSA keypair (n, e, d)."""
    print("Generating primes (this may take a few seconds)...")
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    while p == q:
        q = generate_prime(bits // 2)
        
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modinv(e, phi)
    return n, e, d

# --- CLI PROGRAM ---
def main():
    print("================================================")
    print("      Digital_TTS Master License Key Generator  ")
    print("================================================")
    print("1. Generate Master RSA Keypair")
    print("2. Generate License Key for Client")
    choice = input("Select an option (1/2): ").strip()
    
    keys_file = "master_keys.json"
    
    if choice == "1":
        # Generate new RSA master keypair
        n, e, d = generate_keypair(1024)
        key_data = {
            "n": str(n),
            "e": str(e),
            "d": str(d)
        }
        with open(keys_file, "w") as f:
            json.dump(key_data, f, indent=4)
        print(f"\n[SUCCESS] New keypair saved to '{keys_file}'. Keep this file SECRET!")
        print("\nCopy the following 'n' value and paste it into RSA_N in 'license_verify.py':")
        print("-----------------------------------------------------------------")
        print(f"RSA_N = {n}")
        print("-----------------------------------------------------------------")
        
    elif choice == "2":
        # Generate client license key
        if not os.path.exists(keys_file):
            print(f"\n[ERROR] '{keys_file}' not found. Please generate the keypair first (Option 1).")
            return
            
        with open(keys_file, "r") as f:
            key_data = json.load(f)
            
        n = int(key_data["n"])
        d = int(key_data["d"])
        
        hwid = input("\nEnter Client HWID (e.g. THY-XXXX-XXXX-XXXX-XXXX): ").strip()
        if not hwid.startswith("THY-") or len(hwid) != 19:
            print("[WARNING] The entered HWID does not match the standard format. Proceeding anyway.")
            
        expiry = input("Enter License Expiry Date (YYYY-MM-DD or 'lifetime'): ").strip().lower()
        if expiry != "lifetime":
            try:
                datetime.strptime(expiry, "%Y-%m-%d")
            except ValueError:
                print("[ERROR] Invalid date format. Must be YYYY-MM-DD.")
                return
                
        # 1. Build metadata
        license_metadata = {
            "hwid": hwid,
            "expiry": expiry
        }
        
        data_bytes = json.dumps(license_metadata).encode("utf-8")
        
        # 2. Cryptographic signature
        expected_hash = hashlib.sha256(data_bytes).digest()
        hash_int = int.from_bytes(expected_hash, "big")
        
        # Sign: hash_int^d mod n
        signature_int = pow(hash_int, d, n)
        sig_bytes = signature_int.to_bytes((n.bit_length() + 7) // 8, "big")
        
        # 3. Combined base64 license payload
        combined = data_bytes + b"||" + sig_bytes
        license_key = base64.b64encode(combined).decode("utf-8")
        
        print("\n=================== LICENSE KEY GENERATED ===================")
        print("Copy the license key below and send it to the client:")
        print("-------------------------------------------------------------")
        print(license_key)
        print("-------------------------------------------------------------")
        print("The client will paste this key to activate the application.")
        print("=============================================================")

if __name__ == "__main__":
    main()
