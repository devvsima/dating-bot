import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime

from database.service.stats import get_users_registration_data, get_users_invite
from data.config import DIR


invites_photo_path = rf'{DIR}/photo/invites_graph.png'
registration_photo_path = rf'{DIR}/photo/registration_graph.png'

def get_or_create_invites_graph(path=invites_photo_path) -> str:
    create_user_invite_graph(path)
    return path

def create_user_invite_graph(path) -> None:
    plt.style.use(['dark_background'])
    users, invites = get_users_invite()
    print(invites)
    plt.pie(invites, labels=users)
    plt.xlabel('Users')
    plt.ylabel('Number of Invites')
    plt.title('Invites per User')

    plt.savefig(path)

def get_or_create_registration_graph(data=get_users_registration_data(), path=registration_photo_path) -> str:
    create_user_registration_graph(data, path)
    return path

def create_user_registration_graph(data, path):
    df = pd.DataFrame(data)

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    df['date'] = df['timestamp'].dt.date
    from .date import get_mounth_period
    today, ago = get_mounth_period()
    start_date = datetime(int(ago.year), int(ago.month), int(ago.day))
    end_date = datetime(int(today.year), int(today.month), int(today.day))
    all_dates = pd.date_range(start=start_date, end=end_date).date

    daily_counts = df.groupby('date')['username'].nunique()

    daily_counts_full = pd.Series(daily_counts, index=all_dates).fillna(0)

    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")  # Установка стиля Seaborn

    # Создаем бар график
    sns.barplot(x=daily_counts_full.index, y=daily_counts_full, palette='Blues_d')

    plt.title('Приход пользователей за 30 дней', fontsize=16, fontweight='bold')
    plt.xlabel('Дата', fontsize=12)
    plt.ylabel('Количество уникальных пользователей', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(path)
