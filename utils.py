import tomllib


def read_config():
    with open('config.toml', 'rb') as f:
        config = tomllib.load(f)
    return config

from datetime import datetime, timedelta

def get_week_date(i):
    base_date = datetime(2025, 9, 1)
    target_date = base_date + timedelta(weeks=i)
    return target_date.strftime('%Y-%m-%d')