from pathlib import Path
import pandas as pd
from ucimlrepo import fetch_ucirepo

def main():
    print("Fetching UCI Student Performance dataset (ID 320)...")
    dataset = fetch_ucirepo(id=320)

    features = dataset.data.features
    targets = dataset.data.targets
    combined = features.join(targets)

    folder = Path(__file__).resolve().parent
    combined.to_csv(folder / "student_performance.csv", index=False)
    features.to_csv(folder / "student_performance_features.csv", index=False)
    targets.to_csv(folder / "student_performance_targets.csv", index=False)

    print(f"Saved combined dataset: {len(combined):,} rows, {len(combined.columns)} columns")
    print("Files created:")
    print(folder / "student_performance.csv")
    print(folder / "student_performance_features.csv")
    print(folder / "student_performance_targets.csv")
    print("\nFirst five rows:")
    print(combined.head())

if __name__ == "__main__":
    main()
