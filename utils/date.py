from datetime import datetime, timedelta

def get_mounth_period():
    today = datetime.today()
    days_ago_30 = today - timedelta(days=30)
    return today, days_ago_30