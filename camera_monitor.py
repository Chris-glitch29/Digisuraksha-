import cv2
import psutil
import datetime

# Log file
log_file = "camera_access_log.txt"

def log_event(message):
    with open(log_file, "a") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")
    print(f"[ALERT] {message}")

def check_camera():
    cap = cv2.VideoCapture(0)  # Try to access default camera
    if cap.isOpened():
        log_event("Camera is accessible (possibly in use)")
        cap.release()
    else:
        log_event("Camera is NOT accessible (no active use)")

def check_processes():
    suspicious = []
    camera_keywords = ["zoom", "teams", "skype", "discord", "chrome", "firefox"]
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pname = proc.info['name'].lower()
            if any(word in pname for word in camera_keywords):
                suspicious.append(pname)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if suspicious:
        log_event(f"Processes that may be using camera: {list(set(suspicious))}")

if __name__ == "__main__":
    print("🔍 Camera Security Monitor Running... Press CTRL+C to stop.\n")
    while True:
        try:
            check_camera()
            check_processes()
            
            # Run every 10 seconds
            import time
            time.sleep(10)

        except KeyboardInterrupt:
            print("\n❌ Stopped by user.")
            break

Dependencies required :
pip install opencv-python psutil

Run the script:
python camera_monitor.py
