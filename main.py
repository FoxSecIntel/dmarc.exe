import argparse
from urllib.parse import urlparse

from core.dmarc_checker import check_dmarc
from core.dmarc_parser import parse_dmarc_gzip


def _validate_domain(domain: str) -> str:
    domain = domain.strip()
    if not domain:
        raise ValueError("Domain cannot be empty")

    if "://" in domain:
        raise ValueError("Please provide a bare domain (e.g. example.com), not a URL")

    parsed = urlparse(f"//{domain}")
    if parsed.path not in ("", "/") or parsed.query or parsed.fragment:
        raise ValueError("Domain must not include a path, query, or fragment")

    hostname = parsed.hostname or ""
    if hostname != domain.lower() and hostname != domain:
        raise ValueError("Invalid domain format")

    # Allow special internal trigger domains used by downstream logic.
    if domain.lower() in {"m", "tag"}:
        return domain

    if "." not in domain:
        raise ValueError("Domain should include a TLD (e.g. example.com), or be one of: m, tag")

    return domain


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a domain's DMARC record and/or parse a DMARC report."
    )
    parser.add_argument("domain", nargs="?", help="Domain to check (e.g. example.com)")
    parser.add_argument(
        "--report",
        default="data/sample_report.xml.gz",
        help="Path to DMARC report gzip file (default: data/sample_report.xml.gz)",
    )

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--check-only", action="store_true", help="Only run DMARC record check")
    mode_group.add_argument("--parse-only", action="store_true", help="Only parse the DMARC report")

    args = parser.parse_args()

    run_check = not args.parse_only
    run_parse = not args.check_only

    if run_check and not args.domain:
        parser.error("domain is required unless --parse-only is used")

    if run_check:
        try:
            domain = _validate_domain(args.domain)
            print("=== DMARC Record Check ===")
            result = check_dmarc(domain)
            print(result)
        except Exception as exc:
            print(f"DMARC check failed: {exc}")
            return 1

    if run_parse:
        try:
            if run_check:
                print("\n=== DMARC Report Parsing ===")
            else:
                print("=== DMARC Report Parsing ===")
            report = parse_dmarc_gzip(args.report)
            for record in report:
                print(record)
        except Exception as exc:
            print(f"DMARC report parsing failed: {exc}")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
