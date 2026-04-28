import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from week11 import PriceDataFrame

class PriceHistogram:

    def __init__(self, input_filepath: str, output_filepath: str = "price_histogram.png"):
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self._df_builder = PriceDataFrame(input_filepath)

    def plot(self) -> None:
        df = self._df_builder.build()

        valid = df[~df["parse_error"]]["price_clean"]
        errors = df[df["parse_error"]]

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle("Анализ колонки price", fontsize=14, fontweight="bold")

        ax1 = axes[0]
        counts = [len(valid), len(errors)]
        labels = [f"Валидные\n({len(valid)} шт.)", f"Ошибки парсинга\n({len(errors)} шт.)"]
        colors = ["#4CAF50", "#F44336"]
        bars = ax1.bar(labels, counts, color=colors, edgecolor="white", linewidth=1.5)

        for bar, count in zip(bars, counts):
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.1,
                str(count),
                ha="center", va="bottom", fontsize=12, fontweight="bold"
            )

        ax1.set_title("Качество данных")
        ax1.set_ylabel("Количество строк")
        ax1.set_ylim(0, max(counts) * 1.25)
        ax1.grid(axis="y", alpha=0.3)
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)


        ax2 = axes[1]
        ax2.hist(valid, bins=10, color="#2196F3", edgecolor="white", linewidth=0.8, alpha=0.85)
        ax2.set_title("Распределение price_clean")
        ax2.set_xlabel("Цена (руб.)")
        ax2.set_ylabel("Количество товаров")
        ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        ax2.grid(axis="y", alpha=0.3)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)

        stats_text = (
            f"Среднее: {valid.mean():,.1f} руб.\n"
            f"Медиана: {valid.median():,.1f} руб.\n"
            f"Мин: {valid.min():,.1f}  Макс: {valid.max():,.1f}"
        )
        ax2.text(
            0.97, 0.97, stats_text,
            transform=ax2.transAxes,
            ha="right", va="top",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", edgecolor="gray", alpha=0.8)
        )

        plt.tight_layout()
        plt.savefig(self.output_filepath, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"[Задача 13] Гистограмма сохранена: '{self.output_filepath}'")
        print(f"  Валидных значений : {len(valid)}")
        print(f"  Среднее           : {valid.mean():,.2f} руб.")
        print(f"  Медиана           : {valid.median():,.2f} руб.")


if __name__ == "__main__":
    hist = PriceHistogram("prices_raw.csv", "price_histogram.png")
    hist.plot()
