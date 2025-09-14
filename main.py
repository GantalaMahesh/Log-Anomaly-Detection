
"""main.py
Entry point: parse logs, detect anomalies, visualize, and generate reports.
This file imports modules from the 'src' package.
"""
from src.parser import parse_file
from src.anomaly_detector import detect_all, detect_spikes
from src.visualizer import plot_spikes
from src.report_generator import generate_json_report, generate_md_report
from src.db_store import save_anomalies
import argparse
from pathlib import Path
import sys
# ensure src is importable
sys.path.insert(0, str(Path(__file__).parent / 'src'))


def main(logpath, outdir, config):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    records, warnings = parse_file(logpath)
    if warnings:
        print("Warnings while parsing:\n", warnings)
    anomalies = detect_all(records, config)
    # Save JSON and md reports
    json_path = outdir / "anomalies.json"
    md_path = outdir / "anomalies.md"
    generate_json_report(anomalies, json_path)
    generate_md_report(anomalies, md_path)
    print(f"Wrote reports to {json_path} and {md_path}")
    # Visualize spikes
    spikes = detect_spikes(records,
                           window_seconds=config.get(
                               'spike_window_seconds', 2),
                           threshold=config.get('spike_threshold', 3))
    plot_path = outdir / "spike_plot.png"
    plot_spikes(records, spikes, outpath=str(plot_path))
    print(f"Spike plot saved to {plot_path}")
    db_path = outdir / 'anomalies.db'
    save_anomalies(db_path, anomalies)
    print(f"Anomalies also saved to database {db_path}")
    return json_path, md_path, plot_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', required=False,
                        default='logs/sample.log', help='Path to log file')
    parser.add_argument('--outdir', required=False,
                        default='output', help='Output directory')
    args = parser.parse_args()
    # config: thresholds; candidates may tune these
    cfg = {
        'spike_window_seconds': 2,
        'spike_threshold': 3,
        'gap_minutes': 30,
        'business_start_hour': 9,
        'business_end_hour': 18,
        'critical_events': ['FILE_DELETE', 'FILE_UPLOAD', 'LOGIN_FAILURE', 'LOGIN_SUCCESS']
    }
    main(args.log, args.outdir, cfg)
