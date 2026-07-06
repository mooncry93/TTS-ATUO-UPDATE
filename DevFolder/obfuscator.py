import os
import zlib
import base64

def obfuscate_file(src_path, dest_path):
    """
    Obfuscates a Python file by compressing with zlib and encoding in base64.
    Creates a self-executing stub that runs the code in memory.
    """
    if not os.path.exists(src_path):
        print(f"[OBFUSCATOR] Source file not found: {src_path}")
        return False
        
    with open(src_path, "r", encoding="utf-8") as f:
        source_code = f.read()
        
    # Compress and encode
    compressed = zlib.compress(source_code.encode("utf-8"), 9)
    encoded = base64.b64encode(compressed).decode("utf-8")
    
    # Generate self-executing stub
    stub = f"""# Obfuscated by Digital_TTS Obfuscator
import zlib
import base64
exec(zlib.decompress(base64.b64decode(b"{encoded}")).decode("utf-8"), globals())
"""
    
    # Write to destination
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(stub)
        
    print(f"[OBFUSCATOR] Obfuscated: {os.path.basename(src_path)} -> {os.path.basename(dest_path)}")
    return True
