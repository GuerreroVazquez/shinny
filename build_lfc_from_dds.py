import pandas as pd
from pathlib import Path

DDS_DIR = Path("data/DDS")
OUTPUT_FILE = Path("data/lfc_from_dds.csv")
PREFIX = "RNAseq_abundances_adjusted_combat_inmose_"
SUFFIX = "_DDS"
GLOB_PATTERN = f"{PREFIX}*{SUFFIX}.csv"

SKIP = {"MO", "male.vs.female_Young"}

dds_files = sorted(DDS_DIR.glob(GLOB_PATTERN))

print(f"Found {len(dds_files)} DDS files")

lfc_data = None

for fpath in dds_files:
    comparison = fpath.stem.removeprefix(PREFIX).removesuffix(SUFFIX)

    if comparison in SKIP:
        print(f"  Skipping: {comparison} (duplicate)")
        continue

    print(f"  Reading: {comparison}")

    df = pd.read_csv(fpath, index_col=0)
    df = df[df["padj"] < 0.05]
    lfc_series = df["log2FoldChange"].rename(comparison)

    if lfc_data is None:
        lfc_data = lfc_series.to_frame()
    else:
        lfc_data = lfc_data.join(lfc_series, how="outer")

lfc_data.index.name = None
lfc_data = lfc_data.round(2)
lfc_data.to_csv(OUTPUT_FILE)
print(f"\nSaved consolidated LFC file: {OUTPUT_FILE}")
print(f"Shape: {lfc_data.shape}")
