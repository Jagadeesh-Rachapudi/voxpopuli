import os
import subprocess
import time

def check_jobs():
    """Check if there are any active jobs running the download script."""
    try:
        # Check for running jobs using `ps` and `grep`
        result = subprocess.run(
            ["ps", "aux"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Filter for the download_audios.py process
        for line in result.stdout.splitlines():
            if "python download_audios.py" in line and "nohup" in line:
                return True  # Found a running job
        return False
    except Exception as e:
        print(f"Error checking jobs: {e}")
        return False

def start_download():
    """Start the download_audios.py script using nohup."""
    try:
        # Command to run the download_audios.py script with nohup
        command = "nohup python download_audios.py --root ../voxpopuli > download_log.txt 2>&1 &"
        os.system(command)
        print("Started download_audios.py script.")
    except Exception as e:
        print(f"Error starting download: {e}")

def main():
    while True:
        # Check for active jobs
        if not check_jobs():
            print("No active jobs found. Restarting download_audios.py...")
            start_download()
        else:
            print("Active job found. No action needed.")
        # Wait for 5 minutes before checking again
        time.sleep(300)

if __name__ == "__main__":
    main()
