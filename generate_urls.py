# # import argparse
# # from pathlib import Path

# # from voxpopuli import LANGUAGES, LANGUAGES_V2, YEARS, DOWNLOAD_BASE_URL

# def get_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "--subset", "-s", type=str, required=True,
#         choices=["400k", "100k", "10k", "asr"] + LANGUAGES + LANGUAGES_V2,
#         help="Data subset to generate URLs for"
#     )
#     parser.add_argument(
#         "--output", "-o", type=str, default="urls.txt",
#         help="Output file to save the filenames and URLs"
#     )
#     return parser.parse_args()

# def generate_urls(args):
#     if args.subset in LANGUAGES_V2:
#         languages = [args.subset.split("_")[0]]
#         years = YEARS + [f"{y}_2" for y in YEARS]
#     elif args.subset in LANGUAGES:
#         languages = [args.subset]
#         years = YEARS
#     else:
#         languages = {
#             "400k": LANGUAGES,
#             "100k": LANGUAGES,
#             "10k": LANGUAGES,
#             "asr": ["original"]
#         }.get(args.subset, None)
#         years = {
#             "400k": YEARS + [f"{y}_2" for y in YEARS],
#             "100k": YEARS,
#             "10k": [2019, 2020],
#             "asr": YEARS
#         }.get(args.subset, None)

#     # Generate the list of filenames and URLs
#     url_list = []
#     for l in languages:
#         for y in years:
#             filename = f"{l}_{y}.tar"
#             url = f"{DOWNLOAD_BASE_URL}/audios/{filename}"
#             url_list.append((filename, url))

#     # Save the filenames and URLs to the specified output file
#     with open(args.output, "w") as f:
#         for filename, url in url_list:
#             f.write(f"{filename}: {url}\n")

#     print(f"{len(url_list)} filenames and URLs saved to {args.output}")

# def main():
#     args = get_args()
#     generate_urls(args)

# if __name__ == '__main__':
#     main()
