#!/bin/bash
set -euo pipefail

# Change to the root directory of the project
cd "$(dirname "$0")"/..

echo "Running DMARC daily job..."

# Optional behavior:
# - If DOMAIN is set, run check + parse
# - Otherwise parse-only (safe default for unattended runs)
if [[ -n "${DOMAIN:-}" ]]; then
  python3 main.py "$DOMAIN" --report "${REPORT_PATH:-data/sample_report.xml.gz}"
else
  python3 main.py --parse-only --report "${REPORT_PATH:-data/sample_report.xml.gz}"
fi
