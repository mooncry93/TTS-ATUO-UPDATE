import os
import sys
import time
import json
import requests

PROGRESS_FILE = "download_progress.json"

MODELS_TO_DOWNLOAD = []

def update_progress(downloading, filename, percent, speed, downloaded_bytes, total_bytes, status="downloading", error_msg=""):
    data = {
        "downloading": downloading,
        "filename": filename,
        "percent": round(percent, 2),
        "speed_mbps": round(speed, 2),
        "bytes_downloaded": downloaded_bytes,
        "total_bytes": total_bytes,
        "status": status,
        "error": error_msg
    }
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)

def download_file(url, dest_path, display_name):
    # Ensure dest folder exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Check if already downloaded
    if os.path.exists(dest_path):
        # Double check size if possible or skip
        print(f"[DOWNLOADER] {display_name} already exists. Skipping.")
        return True
        
    print(f"[DOWNLOADER] Starting download of {display_name}...")
    
    try:
        response = requests.get(url, stream=True, timeout=30.0)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        start_time = time.time()
        last_update_time = start_time
        last_downloaded = 0
        
        filename = os.path.basename(dest_path)
        
        with open(dest_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024): # 1MB chunks
                if not chunk:
                    continue
                file.write(chunk)
                downloaded += len(chunk)
                
                # Calculate progress metrics
                now = time.time()
                elapsed = now - start_time
                interval_elapsed = now - last_update_time
                
                # Update every 0.5 seconds or at completion
                if interval_elapsed >= 0.5 or downloaded == total_size:
                    percent = (downloaded / total_size) * 100 if total_size > 0 else 0
                    
                    # Interval speed
                    bytes_diff = downloaded - last_downloaded
                    speed_mbps = (bytes_diff / (1024 * 1024)) / interval_elapsed if interval_elapsed > 0 else 0
                    
                    update_progress(
                        downloading=True,
                        filename=filename,
                        percent=percent,
                        speed=speed_mbps,
                        downloaded_bytes=downloaded,
                        total_bytes=total_size,
                        status="downloading"
                    )
                    
                    last_update_time = now
                    last_downloaded = downloaded
                    
        return True
        
    except Exception as e:
        print(f"[DOWNLOADER] Failed to download {display_name}: {str(e)}")
        update_progress(
            downloading=False,
            filename=os.path.basename(dest_path),
            percent=0,
            speed=0,
            downloaded_bytes=0,
            total_bytes=0,
            status="error",
            error_msg=str(e)
        )
        # Clean up partial download
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
            except:
                pass
        return False

def main():
    # Initial status
    update_progress(
        downloading=True,
        filename="Warming up...",
        percent=0,
        speed=0,
        downloaded_bytes=0,
        total_bytes=0,
        status="starting"
    )
    
    # Process queue
    success = True
    for item in MODELS_TO_DOWNLOAD:
        success = download_file(item["url"], item["dest"], item["name"])
        if not success:
            break
            
    if success:
        print("[DOWNLOADER] All models downloaded successfully.")
        update_progress(
            downloading=False,
            filename="Completed",
            percent=100,
            speed=0,
            downloaded_bytes=0,
            total_bytes=0,
            status="completed"
        )
    else:
        print("[DOWNLOADER] Model download failed.")

if __name__ == "__main__":
    main()
