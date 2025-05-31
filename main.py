import sys
from core.dmarc_checker import check_dmarc
from core.dmarc_parser import parse_dmarc_gzip

def main():
    domain = sys.argv[1]
    print("=== DMARC Record Check ===")
    result = check_dmarc(domain)
    print(result)

    print("\n=== DMARC Report Parsing ===")
    report = parse_dmarc_gzip("data/sample_report.xml.gz")
    for record in report:
        print(record)

if __name__ == "__main__":
    main()
