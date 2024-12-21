import argparse
import os
from pathlib import Path
import requests
from tqdm import tqdm
import shutil


# Specify the path to the urls.txt file here
URLS_FILE_PATH = "../urls.txt"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", "-r", type=str, required=True, help="data root path"
    )
    return parser.parse_args()

def download_url(url, out_dir, filename):
    out_path = os.path.join(out_dir, filename)
    # Uncomment this if you want to skip already downloaded files
    if os.path.exists(out_path):
        print(f"Skipping {filename} (already downloaded)")
        return True

    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            with open(out_path, 'wb') as file, tqdm(
                desc=filename,
                total=total_size,
                unit='B',
                unit_scale=True
            ) as progress_bar:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                    progress_bar.update(len(chunk))

        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return False

def extract_archive(file_path, out_dir):
    """Extract the given archive and place the files in the specified directory."""
    try:
        shutil.unpack_archive(file_path, out_dir)
        print(f"Extracted: {file_path}")
        os.remove(file_path)  # Remove the archive after extraction
        print(f"Removed archive: {file_path}")
    except Exception as e:
        print(f"Error extracting {file_path}: {e}")

def download(args):
    out_root = Path(args.root) / "raw_audios"
    out_root.mkdir(exist_ok=True, parents=True)

    urls_file = URLS_FILE_PATH
    if not os.path.exists(urls_file):
        print(f"Error: {urls_file} not found.")
        return

    while True:
        # Read the first line from urls.txt
        with open(urls_file, "r") as f:
            lines = f.readlines()
        
        if not lines:
            print("All URLs have been processed.")
            break

        # Extract the first URL from the file
        first_line = lines[0].strip()
        if not first_line:
            # Remove empty lines
            lines.pop(0)
            with open(urls_file, "w") as f:
                f.writelines(lines)
            continue

        filename, url = first_line.split(": ")
        filename = filename.strip()
        url = url.strip()

        tar_path = out_root / filename

        # Download the file
        success = download_url(url, out_root.as_posix(), filename)

        if success:
            # Extract the archive and remove the .tar file
            extract_archive(tar_path, out_root.as_posix())

            # Remove the first line from urls.txt after successful download
            lines.pop(0)
            with open(urls_file, "w") as f:
                f.writelines(lines)
        else:
            print(f"Failed to download {filename}. Retrying later...")
            break

def main():
    args = get_args()
    download(args)

if __name__ == '__main__':
    main()
