import numpy as np
import pandas as pd


def create_chunk(size: int, start_id: int) -> pd.DataFrame:
    """Core engine to create a clean DataFrame chunk."""
    df = pd.DataFrame(
        {
            "mandt": np.random.randint(100, 999, size),  # SAP Client ID
            "bukrs": np.random.choice(["PL01", "DE01", "US01"], size),  # Company code
            "vbeln": [f"4000{i:06d}" for i in range(start_id, start_id + size)],  # Sales document number
            "matnr": [f"MAT-{i}" for i in range(1000, 1000 + size)],  # Material ID
            "netwr": np.random.uniform(10.0, 5000.0, size),  # Net Value
            "waerk": "PLN",  # Currency
            "erdat": pd.Timestamp("2026-01-01") + pd.to_timedelta(np.random.randint(0, 31536000, size), unit="s"),
            "ernam": np.random.choice(["USER_AP", "USER_BATCH", "SYSTEM"], size),
        }
    )
    return df


def inject_defects(df: pd.DataFrame, ratio: float) -> pd.DataFrame:
    """Injects data quality issues into a DataFrame."""
    if ratio <= 0:
        return df

    num_dirty = int(len(df) * ratio)
    dirty_indices = np.random.choice(df.index, num_dirty, replace=False)

    # Simple defects
    df.loc[np.random.choice(dirty_indices, size=len(dirty_indices) // 2, replace=False), "netwr"] = np.nan
    df.loc[np.random.choice(dirty_indices, size=len(dirty_indices) // 4, replace=False), "mandt"] = -1

    return df
