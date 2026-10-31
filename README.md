\# Smart Home Energy Saving Assistant

Samsung Innovation Campus - Gen AI Project



\*\*Problem:\*\* Indian households waste electricity on appliances left on in empty rooms and on peak-tariff usage.

\*\*For:\*\* a family living in a 2BHK flat.



\## What it does

1\. Simulates 7 days of hourly appliance data (`datasets/generate\_data.py` -> `datasets/usage.csv`)

2\. Applies 6 If-Then rules with time-of-day tariff (Rs 4 / 6 / 9 per kWh) - `notebooks/engine.py`

3\. Ranks alerts: priority = 50% savings + 30% comfort ease + 20% confidence

4\. Gen AI turns the top alerts into short friendly tips - `notebooks/llm\_tips.py` (template fallback if no API key)

5\. Streamlit dashboard + alert feed - `notebooks/app.py`



\## Folder structure

\- `notebooks/` - source scripts (app, rules engine, Gen AI tips)

\- `prompts/` - prompt log (`prompt\_log.md`)

\- `datasets/` - data generator, test script, generated data

\- `outputs/` - sample outputs (`alerts.csv`) and UI screenshots



\## Setup and run

Run all commands from this main folder.



pip install -r requirements.txt

python datasets/generate\_data.py

python notebooks/engine.py        # writes outputs/alerts.csv

streamlit run notebooks/app.py



\## APIs used

Anthropic API (optional) for the AI tips. No key is included in this project.

To enable it, set your own key first (PowerShell):

$env:ANTHROPIC\_API\_KEY="your\_key\_here"

Without a key, the app uses built-in template tips and still works fully.



\## Dependencies

See requirements.txt

