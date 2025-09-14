## Log Anomaly Detection Project

# Log File Anomaly Detection

This project parses application logs and detects several anomaly types:

- Spike Anomaly
- Gap Anomaly
- Event Order Violation
- Out-of-Hours Activity

## Project Structure

- `src/parser.py` - parse logs
- `src/anomaly_detector.py` - detection logic
- `src/visualizer.py` - plotting spikes
- `src/report_generator.py` - JSON and Markdown reports
- `src/db_store.py` - saved detected anomalies in SQLite
- `main.py` - entry point
- `logs/sample.log` - sample data
- `output/` - generated artifacts after running main.py

## How to run

1. Create virtual environment and install requirements:
   ```
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Run:
   ```
   python main.py --log logs/sample.log --outdir output
   ```

The `output` directory will contain `anomalies.json`, `anomalies.md`, and `spike_plot.png`.
