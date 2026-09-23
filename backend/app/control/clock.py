"""Clock-time parsing for absolute-time capture (F-14, dialogue pack 5).

The patient gives a clock time, roughly. The controller computes the interval to
now and reads it back for confirmation. Both the stated time and the confirmed
interval are stored. Nothing here decides urgency: elapsed time never
de-escalates (S-5).
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta

TIME_RE = re.compile(r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm|a\.m\.|p\.m\.|o'clock)?\b", re.I)
WORDS = {
    "midnight": 0, "midday": 12, "noon": 12, "lunchtime": 12, "lunch": 12, "breakfast": 8, "dinner": 18, "tea time": 18,
    "dawn": 6, "first thing": 7, "this morning": 8, "in the morning": 8, "morning": 9, "afternoon": 15, "evening": 19,
    "tonight": 20, "last night": 22, "bedtime": 22, "the news": 18,
}
DAY_BACK = {"yesterday": 1, "last night": 1, "the day before yesterday": 2, "two days ago": 2, "three days ago": 3, "a week ago": 7}


def parse_clock(text: str, now: datetime) -> datetime | None:
    """Return the most recent datetime matching the words, or None."""
    t = text.lower()
    hour: int | None = None
    minute = 0
    m = TIME_RE.search(t)
    if m:
        hour = int(m.group(1))
        minute = int(m.group(2) or 0)
        suffix = (m.group(3) or "").replace(".", "")
        if suffix == "o'clock":
            suffix = ""
        if hour > 24 or (hour == 24 and minute) or (suffix in ("am", "pm") and hour > 12):
            hour = None
        elif suffix == "pm" and hour < 12:
            hour += 12
        elif suffix == "am" and hour == 12:
            hour = 0
        elif not suffix and hour <= 12:
            # no am/pm: take the word context, else the most recent occurrence
            if any(w in t for w in ("evening", "tonight", "afternoon", "night", "dinner", "tea", "bed")) and hour < 12:
                hour += 12
    if hour is None:
        for w, h in sorted(WORDS.items(), key=lambda kv: -len(kv[0])):
            if w in t:
                hour = h
                break
    if hour is None:
        return None
    days_back = 0
    for w, d in DAY_BACK.items():
        if w in t:
            days_back = max(days_back, d)
    for i, day in enumerate(("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")):
        if re.search(r"\b" + day + r"\b", t):
            back = (now.weekday() - i) % 7
            days_back = max(days_back, back)
            if back == 0 and now.replace(hour=hour % 24, minute=minute) > now:
                days_back = 7
            break
    dt = now.replace(hour=hour % 24, minute=minute, second=0, microsecond=0) - timedelta(days=days_back)
    if dt > now and days_back == 0 and not m:
        dt -= timedelta(days=1)
    elif dt > now and days_back == 0 and m and not (m.group(3) or "").strip():
        # "6" with no am/pm and in the future: assume the earlier reading (or yesterday)
        alt = dt - timedelta(hours=12)
        dt = alt if alt <= now else dt - timedelta(days=1)
    elif dt > now and days_back == 0:
        dt -= timedelta(days=1)
    return dt


def describe_interval(minutes: int) -> str:
    if minutes < 60:
        return f"{max(minutes, 1)} minutes"
    hours = minutes / 60
    if hours < 48:
        h = round(hours)
        return f"{h} hour" + ("" if h == 1 else "s")
    d = round(hours / 24)
    return f"{d} days"
