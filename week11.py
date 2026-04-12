import pandas as pd
import numpy as np


class PriceCleaner:
    def clean_series(self, price_series: pd.Series) -> pd.Series:
        cleaned = (
            price_series
            .fillna("")
            .str.strip()
            .str.replace(r"\s+", "", regex=True)
            .str.replace(",", ".", regex=False)
            .replace("", np.nan)
        )
        return pd.to_numeric(cleaned, errors="coerce")


class PriceDataFrame:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.cleaner = PriceCleaner()
        self.df = None

    def build(self) -> pd.DataFrame:
        raw = pd.read_csv(self.filepath, dtype={"price": str})
        raw["price_raw"] = raw["price"].fillna("")
        raw["price_clean"] = self.cleaner.clean_series(raw["price"])
        raw["parse_error"] = raw["price_clean"].isna()
        self.df = raw
        return self.df


if __name__ == "__main__":
    builder = PriceDataFrame("prices_raw.csv")
    builder.build()
    print(builder.df[["price_raw", "price_clean", "parse_error"]].to_string(index=False))