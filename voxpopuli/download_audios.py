import argparse
import os
from pathlib import Path

import requests
from tqdm import tqdm
import shutil

from voxpopuli import LANGUAGES, LANGUAGES_V2, YEARS, DOWNLOAD_BASE_URL


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", "-r", type=str, required=True, help="data root path"
    )
    parser.add_argument(
        "--subset", "-s", type=str, required=True,
        choices=["400k", "100k", "10k", "asr"] + LANGUAGES + LANGUAGES_V2,
        help="data subset to download"
    )
    return parser.parse_args()


def download_url(url, out_dir, filename):
    out_path = os.path.join(out_dir, filename)
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(out_path, 'wb') as file, tqdm(
            desc=filename,
            total=int(response.headers.get('content-length', 0)),
            unit='B',
            unit_scale=True
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                progress_bar.update(len(chunk))


def download(args):
    if args.subset in LANGUAGES_V2:
        languages = [args.subset.split("_")[0]]
        years = YEARS + [f"{y}_2" for y in YEARS]
    elif args.subset in LANGUAGES:
        languages = [args.subset]
        years = YEARS
    else:
        languages = {
            "400k": LANGUAGES,
            "100k": LANGUAGES,
            "10k": LANGUAGES,
            "asr": ["original"]
        }.get(args.subset, None)
        years = {
            "400k": YEARS + [f"{y}_2" for y in YEARS],
            "100k": YEARS,
            "10k": [2019, 2020],
            "asr": YEARS
        }.get(args.subset, None)

    url_list = []
    for l in languages:
        for y in years:
            url_list.append(f"{DOWNLOAD_BASE_URL}/audios/{l}_{y}.tar")

    out_root = Path(args.root) / "raw_audios"
    out_root.mkdir(exist_ok=True, parents=True)
    print(f"{len(url_list)} files to download...")
    for url in tqdm(url_list):
        tar_path = out_root / Path(url).name
        download_url(url, out_root.as_posix(), Path(url).name)
        shutil.unpack_archive(tar_path.as_posix(), out_root.as_posix())
        os.remove(tar_path)


def main():
    args = get_args()
    download(args)


if __name__ == '__main__':
    main()
