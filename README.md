# 📬 DMARC.exe

**Barbell-style DMARC toolkit** — combining dead-simple, reliable scripts with advanced, experimental features like GPT analysis and Prometheus dashboards.

> Lightweight. Brutal. Flexible. Just like a good kettlebell workout.

---

## 🧱 Core Features (Low Risk, High Certainty)

- ✅ Check if a domain has a valid DMARC record
- ✅ Parse zipped DMARC XML aggregate reports
- ✅ CLI-compatible and self-contained

## 🚀 Advanced Features (High Risk, High Reward)

- 🚀 Prometheus-style `/metrics` export
- 🚀 AbuseIPDB auto-takedown script
- 🚀 GPT-powered DMARC forensic summariser

---

## 🗂 Repo Structure

dmarc.exe  
├── core/  
│ ├── dmarc_parser.py # Parses .gz XML reports  
│ └── dmarc_checker.py # Checks DMARC TXT DNS record  
├── advanced/  
│ ├── prometheus_exporter.py # Flask app for /metrics  
│ ├── abuse_reporter.py # Auto-abuse IP reporting  
│ └── gpt_summariser.py # Uses GPT to summarise findings  
├── data/ # Put sample reports here  
├── config/  
│ └── config.ini # API keys and secrets (excluded from git)  
├── scripts/  
│ ├── run_daily.sh # Cron/automation entry point  
│ └── cron_example.txt # Crontab example  
├── main.py # Demo runner  
├── requirements.txt  
├── .gitignore  
└── README.md  

---

## 🧪 Usage

### Install dependencies

Use Python 3.10+ and install the required packages:

```bash
pip install -r requirements.txt

from core.dmarc_checker import check_dmarc
print(check_dmarc("example.com"))

from core.dmarc_parser import parse_dmarc_gzip
records = parse_dmarc_gzip("data/sample_report.xml.gz")
print(records)
```

## Goals
Give threat intel and mail engineers rapid insight into spoofing attacks

Enable visibility and automation at any scale — even cron

Experiment with AI, not depend on it
