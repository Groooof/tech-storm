from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from pydantic import PostgresDsn


def convert_database_url(base_url: PostgresDsn, *, is_async: bool = True) -> str:
    params = base_url.hosts()[0]
    host = f"{params['host']}:{params['port']}" if params.get("port") else params["host"]
    return f"postgresql{'+asyncpg' * is_async}://{params['username']}:{params['password']}@{host}{base_url.path}"


def truncate_str(value: str, max_length: int = 256) -> str:
    return f'{value[:max_length]}...' if len(value) > max_length else value


def convert_to_msc(value: datetime) -> datetime:
    tz = ZoneInfo('Europe/Moscow')
    return value.astimezone(tz)


def datetime_to_str(value: datetime, with_tz=False) -> str:
    fmt = '%Y-%m-%d %H:%M:%S'
    fmt += '%z' if with_tz else ''
    return value.strftime(fmt)


def add_utc_tz(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC)


def non_empty_str(v: str) -> str:
    assert v, 'Value mustn`t be empty!'
    return v


def empty_str_to_none(v: str) -> str | None:
    return v or None


def add_plus_to_phone(value: str):
    return '+' + value if value.startswith('7') else value


def convert_seconds_to_mmss_fmt(value: int) -> str:
    minutes, seconds = divmod(value, 60)
    return f"{minutes:02}:{seconds:02}"
