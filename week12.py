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


class CleanCSVSaver:
    def __init__(self, input_filepath: str, output_filepath: str = "prices_clean.csv"):
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.cleaner = PriceCleaner()

    def save(self) -> pd.DataFrame:
        df = pd.read_csv(self.input_filepath, dtype={"price": str})
        df["price_raw"] = df["price"].fillna("")
        df["price_clean"] = self.cleaner.clean_series(df["price"])
        df["parse_error"] = df["price_clean"].isna()
        df_out = df.drop(columns=["price"])
        df_out.to_csv(self.output_filepath, index=False, encoding="utf-8")
        print(f"Saved: {self.output_filepath}")
        print(df_out[["price_raw", "price_clean", "parse_error"]].to_string(index=False))
        return df_out


if __name__ == "__main__":
    saver = CleanCSVSaver("prices_raw.csv", "prices_clean.csv")
    saver.save()