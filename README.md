## Log Anomaly Detection Project

# Log File Anomaly Detection

This project parses application logs and detects several anomaly types:

- Spike Anomaly
- Gap Anomaly
- Event Order Violation
- Out-of-Hours Activity

## Project Flow

Run the entry point → main.py
"python main.py --log logs/sample.log --outdir output"

## Parsing → src/parser.py

- Reads log file line by line.
- Extracts timestamp, activity, and message.
- Converts timestamps to Python datetime.

## Anomaly Detection → src/anomaly_detector.py

- Spike Anomaly → burst of repeated events.
- Gap Anomaly → long inactivity.
- Event Order Violation → e.g., LOGOUT before LOGIN_SUCCESS.
- Out-of-Hours Activity → critical events outside 9–18 hrs.

## Visualization → src/visualizer.py

- Plots event frequencies over time.
- Highlights spike anomalies.

## Report Generation → src/report_generator.py

- output/anomalies.json → structured machine-readable report.
- output/anomalies.md → human-readable explanation.

## Database Persistence → src/db_store.py

- Saves anomalies into output/anomalies.db (SQLite).
- Enables further querying/analysis.

## Output -> logs/sample.log

After running main.py, the output/ directory will contain:

- anomalies.json – structured anomaly data
- anomalies.md – summary report
- spike_plot.png – visualization of spikes
- anomalies.db – SQLite database

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
