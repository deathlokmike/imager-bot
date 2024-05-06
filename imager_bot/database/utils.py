from datetime import datetime, timezone


def naive_utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)
