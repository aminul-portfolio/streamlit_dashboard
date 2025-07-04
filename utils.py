# utils.py

import pandas as pd
import io
from streamlit import cache_data

@cache_data
def load_data(file_path):
    """Load trading data from CSV and cache it."""
    return pd.read_csv(file_path)

def filter_dataframe(df, symbol=None, trade_type=None):
    """Return filtered dataframe."""
    filtered = df.copy()
    if symbol and symbol != "All":
        filtered = filtered[filtered["Symbol"] == symbol]
    if trade_type and trade_type != "All":
        filtered = filtered[filtered["Type"] == trade_type]
    return filtered

def generate_csv(df):
    """Encode dataframe to CSV bytes."""
    return df.to_csv(index=False).encode("utf-8")

def generate_excel(df):
    """Encode dataframe to Excel bytes."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Report")
    buffer.seek(0)
    return buffer
