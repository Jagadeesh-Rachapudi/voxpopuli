import os
import subprocess
import time
import signal

def check_jobs():
    try:
        result = subprocess.run(
            ["ps", "aux"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in result.stdout.splitlines():
            if "python download_audios.py" in line and "nohup" in line:
                return True
        return False
    except Exception as e:
        print(f"Error checking jobs: {e}")
        return False

def start_download():
    try:
        command = "nohup python download_audios.py --root ../voxpopuli > download_log.txt 2>&1 &"
        os.system(command)
        print("Started download_audios.py script.")
    except Exception as e:
        print(f"Error starting download: {e}")

def handle_exit(signum, frame):
    print("Received exit signal. Stopping monitoring but leaving background jobs running.")
    exit(0)

def main():
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    while True:
        if not check_jobs():
            print("No active jobs found. Restarting download_audios.py...")
            start_download()
        else:
            print("Active job found. No action needed.")
        time.sleep(300)

if __name__ == "__main__":
    main()
