import argparse
from core.dmarc_checker import check_dmarc
from core.dmarc_parser import parse_dmarc_gzip


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check a domain's DMARC record and parse a sample DMARC report."
    )
    parser.add_argument("domain", help="Domain to check (e.g. example.com)")
    args = parser.parse_args()

    print("=== DMARC Record Check ===")
    result = check_dmarc(args.domain)
    print(result)

    print("\n=== DMARC Report Parsing ===")
    report = parse_dmarc_gzip("data/sample_report.xml.gz")
    for record in report:
        print(record)


if __name__ == "__main__":
    main()
