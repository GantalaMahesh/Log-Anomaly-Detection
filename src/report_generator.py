
"""report_generator.py
Generate JSON machine-readable anomaly report and a human-readable markdown summary.
"""
import json
from datetime import datetime


def serialize(obj):
    """Helper to convert datetime objects"""
    if isinstance(obj, datetime):
        return obj.isoformat(sep=' ')
    raise TypeError


def generate_json_report(anomalies, outpath):
    """Write anomalies list to outpath as pretty JSON."""
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(anomalies, f, default=serialize, indent=2)
    return outpath


def generate_md_report(anomalies, outpath):
    lines = ["# Anomaly Report\n"]
    if not anomalies:
        lines.append("No anomalies detected.\n")
    for i, a in enumerate(anomalies, start=1):
        lines.append(f"## {i}. {a.get('type')}")
        for k, v in a.items():
            lines.append(f"- **{k}**: {v}")
        # sensible English description if not present
        if 'description' in a:
            lines.append(f"- **Explanation**: {a['description']}")
        elif 'details' in a:
            lines.append(f"- **Explanation**: {a['details']}")
        lines.append('\n')
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return outpath
