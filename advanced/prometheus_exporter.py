from flask import Flask, Response
from core.dmarc_parser import parse_dmarc_gzip

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    try:
        records = parse_dmarc_gzip('data/sample_report.xml.gz')
        output = []
        for r in records:
            ip = r.get("source_ip", "unknown")
            count = r.get("count", 0)
            disposition = r.get("disposition", "none")
            output.append(f'dmarc_reports_total{{ip="{ip}",disposition="{disposition}"}} {count}')
        return Response("\n".join(output), mimetype='text/plain')
    except Exception as e:
        return Response(f"# Error: {str(e)}", mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
