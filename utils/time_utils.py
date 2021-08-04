import datetime


def seconds_since_midnight(now=None):
    if not now:
        now = datetime.datetime.now()

    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elapsed = (now - midnight)
    return elapsed.seconds + elapsed.microseconds/1000000
