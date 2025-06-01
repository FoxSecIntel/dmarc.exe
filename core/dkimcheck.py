import sys
import dns.resolver
import base64

COMMON_SELECTORS = [
    "default", "selector1", "selector2", "google", "google._domainkey",
    "smtp", "mail", "dkim", "api", "sendgrid", "mandrill", "mailgun"
]

def fetch_dkim_record(domain, selector):
    dkim_domain = f"{selector}._domainkey.{domain}"
    try:
        answers = dns.resolver.resolve(dkim_domain, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                if isinstance(txt_string, bytes):
                    txt_string = txt_string.decode()
                if txt_string.startswith("v=DKIM1"):
                    return txt_string, dkim_domain
    except Exception:
        pass
    return None, dkim_domain

def parse_dkim_record(record):
    tags = {}
    for part in record.split(';'):
        if '=' in part:
            k, v = part.strip().split('=', 1)
            tags[k.strip()] = v.strip()
    return tags

def check_key_validity(p_value):
    try:
        decoded = base64.b64decode(p_value + '==', validate=True)
        return len(decoded) >= 128  # minimum 1024-bit key
    except Exception:
        return False

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python dkimcheck.py <domain> [selector]")
        sys.exit(1)

    domain = sys.argv[1]
    selectors = [sys.argv[2]] if len(sys.argv) == 3 else COMMON_SELECTORS

    found_any = False

    for selector in selectors:
        record, full_domain = fetch_dkim_record(domain, selector)
        print(f"\n=== Checking {full_domain} ===")

        if not record:
            print("  ❌ No DKIM record found.")
            continue

        print(f"  ✅ DKIM record found: {record}")
        parsed = parse_dkim_record(record)

        for k, v in parsed.items():
            print(f"    {k} = {v}")

        if 'p' in parsed:
            is_valid = check_key_validity(parsed['p'])
            print(f"    [Key] {'✅ Valid key' if is_valid else '❌ Invalid/weak key'}")
        else:
            print("    ❌ No public key (p=) found in record.")

        found_any = True

    if not found_any:
        print("\n[!] No DKIM records found with common selectors.")

if __name__ == "__main__":
    main()

