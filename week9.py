import pandas as pd
import numpy as np


class PriceMaskFinder:
    """Находит 'плохие' строки — те, где в колонке price нет ни одной цифры."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df: pd.DataFrame | None = None
        self.price_strings: pd.Series | None = None
        self.bad_mask: pd.Series | None = None

    def load(self) -> None:
        """Загружает CSV и получает колонку price как строки."""
        self.df = pd.read_csv(self.filepath, dtype={"price": str})

        if "price" not in self.df.columns:
            raise ValueError("В CSV нет колонки 'price'")

        # NaN заменяем на пустую строку
        self.price_strings = self.df["price"].fillna("")

    def find_bad_rows(self) -> pd.Series:
        """
        Возвращает маску строк, где в price нет ни одной цифры.
        Например:
        'abc' -> True
        '12,500' -> False
        '' -> True
        """
        if self.price_strings is None:
            raise ValueError("Сначала вызови load()")

        self.bad_mask = ~self.price_strings.str.contains(r"\d", regex=True)
        return self.bad_mask

    def show_bad_rows(self) -> None:
        """Печатает найденные плохие строки."""
        if self.df is None or self.bad_mask is None:
            raise ValueError("Сначала вызови load() и find_bad_rows()")

        bad_rows = self.df[self.bad_mask]

        print("Строки, где в price нет цифр:\n")
        print(bad_rows)


# запуск
finder = PriceMaskFinder("prices_raw.csv")
finder.load()
finder.find_bad_rows()
finder.show_bad_rows()