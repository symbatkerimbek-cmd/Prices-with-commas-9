import csv
import os


class CSVCreator:
    """Создаёт тестовый файл prices_raw.csv с ценами в формате строк."""

    def __init__(self, filename: str = "prices_raw.csv"):
        self.filename = filename

    def generate_data(self) -> list[dict]:
        """Возвращает список строк с тестовыми данными."""
        return [
            {"product": "Яблоки",    "price": "12,5",       "category": "Фрукты"},
            {"product": "Бананы",    "price": "89,99",      "category": "Фрукты"},
            {"product": "Молоко",    "price": "1 234,56",   "category": "Молочные"},
            {"product": "Хлеб",      "price": "45,0",       "category": "Выпечка"},
            {"product": "Масло",     "price": "250,75",     "category": "Молочные"},
            {"product": "Сыр",       "price": "1 100,0",    "category": "Молочные"},
            {"product": "Курица",    "price": "320,5",      "category": "Мясо"},
            {"product": "Говядина",  "price": "2 450,99",   "category": "Мясо"},
            {"product": "Картофель", "price": "35,25",      "category": "Овощи"},
            {"product": "Морковь",   "price": "28,0",       "category": "Овощи"},
            {"product": "Томаты",    "price": "abc",        "category": "Овощи"},   # плохая строка
            {"product": "Огурцы",    "price": "",           "category": "Овощи"},   # пустая строка
            {"product": "Рис",       "price": "110,50",     "category": "Крупы"},
            {"product": "Гречка",    "price": "95,0",       "category": "Крупы"},
            {"product": "Макароны",  "price": "N/A",        "category": "Крупы"},   # плохая строка
            {"product": "Сахар",     "price": "75,99",      "category": "Бакалея"},
            {"product": "Соль",      "price": "22,5",       "category": "Бакалея"},
            {"product": "Кофе",      "price": "3 200,0",   "category": "Напитки"},
            {"product": "Чай",       "price": "450,25",     "category": "Напитки"},
            {"product": "Вода",      "price": "55,0",       "category": "Напитки"},
        ]

    def save(self) -> None:
        """Сохраняет данные в CSV файл."""
        data = self.generate_data()
        fieldnames = ["product", "price", "category"]

        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        print(f"[OK] Файл '{self.filename}' создан. Строк: {len(data)}")
        print(f"     Путь: {os.path.abspath(self.filename)}")


if __name__ == "__main__":
    creator = CSVCreator("prices_raw.csv")
    creator.save()