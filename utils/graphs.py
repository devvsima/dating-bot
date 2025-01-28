import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime, timedelta

from database.service.stats import get_all_users_registration_data

from data.config import IMAGES_DIR

registration_photo_path = f'{IMAGES_DIR}/registration_graph.png'


def get_day_period(days: int = 30):
    """Возращает текущую дату, и дату 30 дней назад"""
    today = datetime.today()
    days_ago = today - timedelta(days)
    return today, days_ago

async def get_or_create_registration_graph(data=None, path=registration_photo_path) -> str:
    """Создает график регистрации пользователей и возращает путь к фотографии графика"""
    if data is None:
        data = await get_all_users_registration_data()
    create_user_registration_graph(data, path)
    return path

def create_user_registration_graph(data, path):
    """Создает график новых пользователей в заданом периоде"""
    df = pd.DataFrame(data)

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    df['date'] = df['timestamp'].dt.date
    today, ago = get_day_period(30)
    start_date = datetime(int(ago.year), int(ago.month), int(ago.day))
    end_date = datetime(int(today.year), int(today.month), int(today.day))
    all_dates = pd.date_range(start=start_date, end=end_date).date

    daily_counts = df.groupby('date')['username'].nunique()

    daily_counts_full = pd.Series(daily_counts, index=all_dates).fillna(0)

    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")  # Установка стиля Seaborn

    sns.barplot(
        x=daily_counts_full.index,
        y=daily_counts_full,
        palette='Blues_d',
        hue=daily_counts_full.index,
        legend=False
    )

    plt.title('Приход пользователей за 30 дней', fontsize=16, fontweight='bold')
    plt.xlabel('Дата', fontsize=12)
    plt.ylabel('Количество уникальных пользователей', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(path)
