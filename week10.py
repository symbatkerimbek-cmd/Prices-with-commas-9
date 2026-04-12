"""
Задача 10: Функция — убрать пробелы, заменить запятую на точку,
astype(float) для валидных строк.
"""

import pandas as pd
import numpy as np


class PriceCleaner:
    """Очищает строковые цены: пробелы → убрать, запятая → точка, → float."""

    def clean_series(self, price_series: pd.Series) -> pd.Series:
        """
        Принимает Series строк, возвращает Series float (NaN для невалидных).

        Шаги:
        1. Убираем все пробелы (включая неразрывные).
        2. Заменяем запятую на точку.
        3. Конвертируем в float; ошибки → NaN (errors='coerce').
        """
        cleaned = (
            price_series
            .fillna("")  # NaN → пустая строка
            .str.strip()  # убираем крайние пробелы
            .str.replace(r"\s+", "", regex=True)  # убираем все внутренние пробелы
            .str.replace(",", ".", regex=False)  # запятая → точка
            .replace("", np.nan)  # пустая строка → NaN
        )
        # Конвертируем; всё что не число → NaN
        return pd.to_numeric(cleaned, errors="coerce")

    def demo(self) -> None:
        """Демонстрирует работу функции на примерах."""
        examples = pd.Series([
            "12,5",
            "1 234,56",
            "250,75",
            "abc",
            "",
            "N/A",
            "3 200,0",
            "0,99",
        ])

        result = self.clean_series(examples)

        print("[Задача 10] Демонстрация очистки:")
        for raw, clean in zip(examples, result):
            status = "OK" if not pd.isna(clean) else "ОШИБКА"
            print(f"  {str(raw):15s} → {str(clean):10s}  [{status}]")


if __name__ == "__main__":
    cleaner = PriceCleaner()
    cleaner.demo()