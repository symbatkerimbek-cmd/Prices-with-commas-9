
import pandas as pd
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()


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


class PriceService:
    def __init__(self):
        self.cleaner = PriceCleaner()

    def process(self, df: pd.DataFrame) -> dict:
        df["price_clean"] = self.cleaner.clean_series(df["price"])
        df["parse_error"] = df["price_clean"].isna()
        return {
            "total": len(df),
            "cleaned_ok": int((~df["parse_error"]).sum()),
            "errors": int(df["parse_error"].sum()),
        }


service = PriceService()


@app.post("/clean-prices")
async def clean_prices(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(pd.io.common.BytesIO(content), dtype={"price": str})
    result = service.process(df)
    return JSONResponse(content=result)
