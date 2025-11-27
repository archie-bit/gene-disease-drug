import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://ftp.ebi.ac.uk/pub/databases/opentargets/platform/25.09/output/association_by_datasource_direct/"
OUT_DIR = "data/raw/opentargets/association_by_datasource_direct"

def list_parquet_files():
    """Parse FTP directory HTML and extract .parquet file names."""
    print("Fetching directory listing...")
    r = requests.get(BASE_URL)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    parquet_files = []

    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.endswith(".parquet"):
            parquet_files.append(href)

    return parquet_files


def download_file(filename):
    """Download a file in streaming mode."""
    url = BASE_URL + filename
    path = os.path.join(OUT_DIR, filename)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    print(f"Downloading {filename}...")

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print(f"Finished: {filename}")


def main():
    files = list_parquet_files()
    print(f"Found {len(files)} parquet files.")

    for file in files:
        download_file(file)

    print("All files downloaded successfully!")


if __name__ == "__main__":
    main()
