
"""parser.py
Functions to parse log files into structured records.
Each line expected: TIMESTAMP, ACTIVITY, MESSAGE
TIMESTAMP format: YYYY-MM-DD HH:MM:SS
"""
from datetime import datetime
import re

TIMESTAMP_FORMATS = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S,%f"]


def parse_line(line):
    """Parse a single log line into (timestamp: datetime, activity: str, message: str).
    Returns None for malformed lines.
    """
    if not line or not line.strip():
        return None
    # Try splitting by first two commas
    parts = [p.strip() for p in line.strip().split(",", 2)]
    if len(parts) < 3:
        # malformed
        return None
    ts_str, activity, message = parts
    # normalize activity
    activity = activity.upper()
    # parse timestamp with supported formats
    ts = None
    for fmt in TIMESTAMP_FORMATS:
        try:
            ts = datetime.strptime(ts_str, fmt)
            break
        except Exception:
            continue
    if ts is None:
        # Try if timestamp contains comma for milliseconds
        try:
            ts = datetime.fromisoformat(ts_str)
        except Exception:
            return None
    return {"timestamp": ts, "activity": activity, "message": message}


def parse_file(path):
    """Read file and return list of parsed records sorted by timestamp.
    Skips malformed lines but returns a list of warnings for them.
    """
    records = []
    warnings = []
    with open(path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, start=1):
            parsed = parse_line(line)
            if parsed is None:
                warnings.append({"line": i, "content": line.strip()})
            else:
                records.append(parsed)
    records.sort(key=lambda r: r["timestamp"])
    return records, warnings
