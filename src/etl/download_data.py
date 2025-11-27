import os
import gzip
import shutil
import requests

RAW_DIR = "data/raw"

DATASETS = {
    "clinvar": {
        "folder": "clinvar",
        "files": {
            "variant_summary.txt.gz": "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz"
        }
    },
    "dgidb":{
        "folder": "dgidb",
        "files": {
            "interactions.tsv": "https://www.dgidb.org/data/interactions.tsv"
        }
    },  
    "ncbi": {
        "folder": "ncbi",
        "files": {
            "gene_info.gz": "https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz"
        }
    },
}

def download_file(url, out_path):
    print(f"Downloading: {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(out_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Saved: {out_path}")

def ensure_directories():
    for dataset in DATASETS.values():
        folder = os.path.join(RAW_DIR, dataset["folder"])
        os.makedirs(folder, exist_ok=True)

def download_datasets():
    ensure_directories()
    for dataset_name, dataset in DATASETS.items():
        print(f"\n=== Downloading {dataset_name} ===")
        
        folder = os.path.join(RAW_DIR, dataset["folder"])
        
        for filename, url in dataset["files"].items():
            out_path = os.path.join(folder, filename)
            download_file(url, out_path)

    print("\nDrugBank data must be downloaded manually.")
    print("Place DrugBank CSV files inside: data/raw/drugbank/")

if __name__ == "__main__":
    download_datasets()
