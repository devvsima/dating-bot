from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Circle

from data.config import GRAPH_FILE_PATH


class StatsGraph:
    @staticmethod
    def get_day_period(days: int) -> Tuple[datetime, datetime]:
        """Возвращает текущую дату и дату N дней назад"""
        today = datetime.today()
        days_ago = today - timedelta(days=days)
        return today, days_ago

    def create_user_registration_graph(
        self, data: List[dict], path: Path = GRAPH_FILE_PATH, days: int = 30
    ) -> None:
        """Создает график новых пользователей за последние N дней"""
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["date"] = df["timestamp"].dt.date

        today, ago = self.get_day_period(days)
        start_date = datetime(ago.year, ago.month, ago.day)
        end_date = datetime(today.year, today.month, today.day)

        all_dates = pd.date_range(start=start_date, end=end_date).date
        daily_counts = df.groupby("date").size()  # Подсчет всех записей для каждой даты
        daily_counts_full = pd.Series(daily_counts, index=all_dates).fillna(0)

        plt.figure(figsize=(12, 6))
        sns.set_theme(style="whitegrid")

        sns.barplot(
            x=daily_counts_full.index,
            y=daily_counts_full,
            legend=False,
        )

        plt.title(f"User arrivals in the last {days} days", fontsize=16, fontweight="bold")
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Number of new users", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)

        plt.tight_layout()
        plt.savefig(path)
        plt.close()

    def create_gender_pie_chart(
        self, gender_count: Dict[str, int], path: Path = GRAPH_FILE_PATH
    ) -> None:
        """Создает круговую диаграмму по полу пользователей"""
        labels = list(gender_count.keys())
        sizes = list(gender_count.values())
        total_users = sum(sizes)

        colors = ["#2980b9", "#e74c3c"]
        lighter_colors = ["#85c1e9", "#f5b7b1"]
        explode = (0.08, 0.08)

        fig, ax = plt.subplots(figsize=(8, 8), facecolor="#F9F9F9")

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=None,
            explode=explode,
            colors=lighter_colors,
            autopct="%1.1f%%",
            pctdistance=0.82,
            shadow=False,
            startangle=140,
            wedgeprops={"linewidth": 2, "edgecolor": "white", "alpha": 0.9},
            textprops={"fontsize": 14, "color": "black", "fontweight": "bold"},
        )

        center_circle = Circle((0, 0), 0.70, fc="white", edgecolor="gray", linewidth=2, alpha=0.8)
        ax.add_artist(center_circle)

        plt.text(
            0,
            0,
            f"{total_users}",
            ha="center",
            va="center",
            fontsize=20,
            fontweight="bold",
            color="#34495e",
        )

        ax.legend(
            wedges,
            labels,
            title="Gender",
            loc="upper right",
            bbox_to_anchor=(1.2, 1),
            fontsize=12,
            frameon=False,
            labelspacing=1.2,
        )

        plt.title(
            "Distribution of users by gender",
            fontsize=18,
            fontweight="bold",
            color="#2A3D66",
            pad=20,
        )
        plt.savefig(path, dpi=120, bbox_inches="tight", transparent=True)
        plt.close()
