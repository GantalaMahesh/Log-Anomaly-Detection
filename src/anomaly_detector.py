
"""anomaly_detector.py
Functions to detect:
 - spike anomalies (same event > X occurrences within Y seconds)
 - gap anomalies (no events for > Z minutes)
 - event order violations (e.g., LOGOUT before LOGIN_SUCCESS)
 - out-of-hours activity (critical events outside business hours)
"""
from collections import defaultdict, deque
from datetime import timedelta, time
import datetime as _dt


def detect_spikes(records, window_seconds=2, threshold=3):
    """Detect spike anomalies per activity.
    Returns list of dicts with keys: type, event, time_range, count, details
    Logic: sliding window per event type using deque of timestamps.
    """
    spikes = []
    events = defaultdict(deque)  # activity -> deque[timestamps]
    for rec in records:
        act = rec["activity"]
        ts = rec["timestamp"]
        dq = events[act]
        dq.append(ts)
        # Pop timestamps older than window
        while dq and (ts - dq[0]).total_seconds() > window_seconds:
            dq.popleft()
        if len(dq) >= threshold:
            # report a spike covering current deque window
            start = dq[0]
            end = dq[-1]
            spikes.append({
                "type": "Spike Anomaly",
                "event": act,
                "time_range": f"{start.isoformat(sep=' ')} - {end.isoformat(sep=' ')}",
                "count": len(dq),
                "details": f"{len(dq)} occurrences of {act} within {window_seconds} seconds"
            })
            # Clear deque to avoid duplicate reports for overlapping windows
            dq.clear()
    return spikes


def detect_gaps(records, gap_minutes=30):
    """Detect gaps where no events recorded for more than gap_minutes.
    Returns list of dicts with type, start, end, duration_minutes.
    """
    gaps = []
    if not records:
        return gaps
    prev = records[0]["timestamp"]
    for rec in records[1:]:
        ts = rec["timestamp"]
        diff = (ts - prev).total_seconds() / 60.0
        if diff > gap_minutes:
            gaps.append({
                "type": "Gap Anomaly",
                "start": prev,
                "end": ts,
                "duration_minutes": diff,
                "details": f"No events for {diff:.2f} minutes between {prev} and {ts}"
            })
        prev = ts
    return gaps


def extract_user_from_message(message):
    """Try to extract 'User X' pattern from message text. Returns user id or None."""
    import re
    m = re.search(r"User\s+([A-Za-z0-9_@.-]+)", message)
    if m:
        return m.group(1)
    m2 = re.search(r"user[:=]\s*([A-Za-z0-9_@.-]+)", message, re.I)
    if m2:
        return m2.group(1)
    return None


def detect_order_violations(records):
    """Detect order violations such as LOGOUT before LOGIN_SUCCESS.
    We'll maintain a simple session state per user: logged_in boolean.
    Returns list of violations with event, user, time, details.
    """
    violations = []
    state = defaultdict(lambda: {"logged_in": False})
    for rec in records:
        act = rec["activity"]
        ts = rec["timestamp"]
        msg = rec["message"]
        user = extract_user_from_message(msg) or "UNKNOWN"
        if act == "LOGIN_SUCCESS":
            state[user]["logged_in"] = True
        elif act == "LOGOUT":
            if not state[user]["logged_in"]:
                violations.append({
                    "type": "Event Order Violation",
                    "event": act,
                    "user": user,
                    "time": ts,
                    "details": f"{user} performed {act} at {ts} without prior LOGIN_SUCCESS"
                })
            else:
                state[user]["logged_in"] = False
        elif act == "LOGIN_FAILURE":
            pass
    return violations


def detect_out_of_hours(records, start_hour=9, end_hour=18, critical_events=None):
    """Detect critical events outside business hours.
    Returns list of dicts with event, time, details.
    critical_events: set/list of activity names considered critical. If None, default to FILE_DELETE, FILE_UPLOAD.
    Business hours are inclusive of start_hour and exclusive of end_hour.
    """
    if critical_events is None:
        critical_events = {"FILE_DELETE", "FILE_UPLOAD",
                           "LOGIN_SUCCESS", "LOGIN_FAILURE"}
    results = []
    for rec in records:
        act = rec["activity"]
        ts = rec["timestamp"]
        if act in critical_events:
            h = ts.time()
            if not (time(start_hour, 0, 0) <= h < time(end_hour, 0, 0)):
                results.append({
                    "type": "Out-of-Hours",
                    "event": act,
                    "time": ts,
                    "details": f"{act} at {ts} is outside business hours ({start_hour}:00-{end_hour}:00)"
                })
    return results


def detect_all(records, config=None):
    """Run all detectors with config dict. Returns combined list of anomalies."""
    if config is None:
        config = {}
    spikes = detect_spikes(records,
                           window_seconds=config.get(
                               "spike_window_seconds", 2),
                           threshold=config.get("spike_threshold", 3))
    gaps = detect_gaps(records, gap_minutes=config.get("gap_minutes", 30))
    orders = detect_order_violations(records)
    ooh = detect_out_of_hours(records,
                              start_hour=config.get("business_start_hour", 9),
                              end_hour=config.get("business_end_hour", 18),
                              critical_events=set(config.get("critical_events", ["FILE_DELETE", "FILE_UPLOAD", "LOGIN_FAILURE", "LOGIN_SUCCESS"])))
    # unify and return
    combined = spikes + gaps + orders + ooh
    # sort by time where applicable

    def get_time(a):
        for k in ("time", "start", "time_range"):
            if k in a:
                val = a[k]
                if isinstance(val, str):
                    # try to parse start of time_range
                    try:
                        parts = val.split("-")
                        return _dt.datetime.fromisoformat(parts[0].strip())
                    except Exception:
                        return None
                return val
        return None
    combined_sorted = sorted(combined, key=lambda x: (
        get_time(x) or _dt.datetime.min))
    return combined_sorted
