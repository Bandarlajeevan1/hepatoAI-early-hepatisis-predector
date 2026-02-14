"""
Script to download and prepare Hepatitis and ILPD datasets from UCI ML Repository.
"""
import os
import requests
import pandas as pd
from pathlib import Path

# Dataset URLs
HEPATITIS_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/hepatitis/hepatitis.data"
ILPD_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/liver-disorders/bupa.data"

# Feature names
HEPATITIS_COLUMNS = [
    "class",
    "age",
    "sex",
    "steroid",
    "antivirals",
    "fatigue",
    "malaise",
    "anorexia",
    "liver_big",
    "liver_firm",
    "spleen_palpable",
    "spider_web",
    "ascites",
    "varices",
    "bilirubin",
    "alk_phosphatase",
    "sgot",
    "sgpt",
    "albumin",
    "protime",
    "histology",
]

ILPD_COLUMNS = [
    "mcv",
    "alkphos",
    "sgpt",
    "sgot",
    "gammagt",
    "alb",
    "total_bilirubin",
    "direct_bilirubin",
    "TP",
    "albumin_ratio",
    "class",
]


def download_dataset(url: str, filename: str, data_dir: str = "backend/data") -> str:
    """
    Download dataset from URL and save as CSV.

    Args:
        url: Dataset URL
        filename: Output filename (without path)
        data_dir: Directory to save file

    Returns:
        Path to saved file
    """
    os.makedirs(data_dir, exist_ok=True)
    filepath = os.path.join(data_dir, filename)

    if os.path.exists(filepath):
        print(f"✓ {filename} already exists")
        return filepath

    try:
        print(f"Downloading {filename} from {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"✓ Downloaded {filename} ({len(response.content)} bytes)")
        return filepath
    except Exception as e:
        print(f"✗ Failed to download {filename}: {e}")
        return None


def prepare_hepatitis(filepath: str) -> bool:
    """Prepare hepatitis dataset."""
    try:
        print("\nPreparing Hepatitis dataset...")
        df = pd.read_csv(filepath, header=None, names=HEPATITIS_COLUMNS)

        # Handle missing values (indicated by "?")
        df = df.replace("?", None)
        df[["class"]] = df[["class"]] - 1  # Convert 1,2 → 0,1
        
        # Convert to numeric (missing values become NaN)
        numeric_cols = [col for col in df.columns if col != "class"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        print(f"  - Shape: {df.shape}")
        print(f"  - Missing values: {df.isnull().sum().sum()}")
        print(f"  - Classes: {df['class'].value_counts().to_dict()}")

        # Save as clean CSV
        clean_path = filepath.replace(".data", "_clean.csv")
        df.to_csv(clean_path, index=False)
        print(f"  ✓ Saved clean dataset to {clean_path}")
        return True
    except Exception as e:
        print(f"  ✗ Error preparing Hepatitis dataset: {e}")
        return False


def prepare_ilpd(filepath: str) -> bool:
    """Prepare ILPD (Liver Disorders) dataset."""
    try:
        print("\nPreparing ILPD dataset...")
        df = pd.read_csv(filepath, header=None, names=ILPD_COLUMNS)

        # Class values: convert to 0 (no disease), 1 (disease)
        df["class"] = (df["class"] == 1).astype(int)

        # Convert to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        print(f"  - Shape: {df.shape}")
        print(f"  - Missing values: {df.isnull().sum().sum()}")
        print(f"  - Classes: {df['class'].value_counts().to_dict()}")

        # Save as clean CSV
        clean_path = filepath.replace(".data", "_clean.csv")
        df.to_csv(clean_path, index=False)
        print(f"  ✓ Saved clean dataset to {clean_path}")
        return True
    except Exception as e:
        print(f"  ✗ Error preparing ILPD dataset: {e}")
        return False


def main():
    """Download and prepare all datasets."""
    print("=" * 60)
    print("Hepatitis Detection - Dataset Downloader")
    print("=" * 60)

    data_dir = "backend/data"

    # Download Hepatitis dataset
    hep_file = download_dataset(HEPATITIS_URL, "hepatitis.data", data_dir)
    if hep_file:
        prepare_hepatitis(hep_file)

    # Download ILPD dataset
    ilpd_file = download_dataset(ILPD_URL, "bupa.data", data_dir)
    if ilpd_file:
        # Rename for consistency
        new_path = os.path.join(data_dir, "ilpd.data")
        if ilpd_file != new_path:
            os.rename(ilpd_file, new_path)
        prepare_ilpd(new_path)

    print("\n" + "=" * 60)
    print("Dataset preparation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
