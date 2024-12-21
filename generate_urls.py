from pathlib import Path
from voxpopuli import LANGUAGES, LANGUAGES_V2, YEARS, DOWNLOAD_BASE_URL

def generate_urls():
    subset = "10k"
    output = "10k_urls_full"

    languages = LANGUAGES
    years = [2019, 2020]  # Specific to the 10k subset

    # Generate the list of filenames and URLs
    url_list = []
    for l in languages:
        for y in years:
            filename = f"{l}_{y}.tar"
            url = f"{DOWNLOAD_BASE_URL}/audios/{filename}"
            url_list.append((filename, url))

    # Save the filenames and URLs to the specified output file
    with open(output, "w") as f:
        for filename, url in url_list:
            f.write(f"{filename}: {url}\n")

    print(f"{len(url_list)} filenames and URLs saved to {output}")

def main():
    generate_urls()

if __name__ == "__main__":
    main()
