
"""visualizer.py
Plotting functions for spike visualization.
Uses matplotlib (no seaborn).
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import Counter
from datetime import datetime


def plot_spikes(records, spikes, outpath="spike_plot.png", aggregation_minutes=1):
    """Plot event frequency over time and mark spike time ranges.
    - records: list of parsed records
    - spikes: list of spike anomaly dicts produced by detect_spikes
    Saves plot as PNG at outpath.
    """
    if not records:
        return None
    # Create time series count per second
    times = [r["timestamp"] for r in records]
    # aggregate counts per second
    counts = Counter(times)
    # sort
    sorted_times = sorted(counts.keys())
    values = [counts[t] for t in sorted_times]
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(sorted_times, values)  # default colors
    ax.set_xlabel("Time")
    ax.set_ylabel("Event frequency (per timestamp)")
    ax.set_title("Event frequency over time (spike visualization)")
    # mark spikes in red dots (matplotlib default color toggles, do not specify colors)
    for s in spikes:
        # parse time_range like 'start - end' where start and end are reprs
        tr = s.get("time_range")
        if not tr:
            continue
        try:
            start_str, end_str = [p.strip() for p in tr.split("-")]
            start = datetime.fromisoformat(start_str)
            end = datetime.fromisoformat(end_str)
            # find indices in sorted_times in range
            xs = [t for t in sorted_times if start <= t <= end]
            ys = [counts[t] for t in xs]
            if xs:
                ax.scatter(xs, ys)  # default color
        except Exception:
            continue
    # pretty formatting
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    fig.autofmt_xdate()
    plt.tight_layout()
    fig.savefig(outpath)
    plt.close(fig)
    return outpath
