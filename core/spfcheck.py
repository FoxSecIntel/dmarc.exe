import sys
import dns.resolver
import re

MAX_DNS_LOOKUPS = 10

def fetch_spf_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                if isinstance(txt_string, bytes):
                    txt_string = txt_string.decode()
                if txt_string.startswith("v=spf1"):
                    return txt_string
    except Exception as e:
        print(f"[!] Error fetching SPF record for {domain}: {e}")
    return None

def parse_spf_record(record):
    mechanisms = record.split()
    includes = [m.split(':')[1] for m in mechanisms if m.startswith('include:')]
    ip4s = [m.split(':')[1] for m in mechanisms if m.startswith('ip4:')]
    ip6s = [m.split(':')[1] for m in mechanisms if m.startswith('ip6:')]
    all_mech = [m for m in mechanisms if m.endswith('all')]
    return {
        'raw': record,
        'includes': includes,
        'ip4': ip4s,
        'ip6': ip6s,
        'all': all_mech
    }

def resolve_includes(includes, seen=None, depth=0):
    if seen is None:
        seen = set()
    results = []
    if depth > MAX_DNS_LOOKUPS:
        results.append(f"[!] Max include depth reached at {includes}")
        return results
    for domain in includes:
        if domain in seen:
            continue
        seen.add(domain)
        record = fetch_spf_record(domain)
        if record:
            results.append(f"[+] {domain}: {record}")
            parsed = parse_spf_record(record)
            results += resolve_includes(parsed['includes'], seen, depth + 1)
        else:
            results.append(f"[!] No SPF found for included domain: {domain}")
    return results

def main():
    if len(sys.argv) != 2:
        print("Usage: python spfcheck.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    print(f"\n=== SPF Check for {domain} ===")
    record = fetch_spf_record(domain)

    if not record:
        print("[!] No SPF record found.")
        return

    parsed = parse_spf_record(record)

    print(f"\n[SPF Record] {parsed['raw']}")
    print("\n[IP4 Addresses]")
    for ip in parsed['ip4']:
        print(f"  - {ip}")

    print("\n[IP6 Addresses]")
    for ip in parsed['ip6']:
        print(f"  - {ip}")

    print("\n[Includes]")
    for inc in parsed['includes']:
        print(f"  - {inc}")

    print("\n[ALL Mechanism]")
    for a in parsed['all']:
        print(f"  - {a}")

    print("\n[Resolved Includes]")
    resolved = resolve_includes(parsed['includes'])
    for line in resolved:
        print(f"  {line}")

if __name__ == "__main__":
    main()

