import dns.resolver

def check_dmarc(domain):
    try:
        result = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
        for txt in result:
            record = txt.to_text()
            if record.startswith('"v=DMARC1'):
                return f"DMARC record found: {record}"
        return "No valid DMARC record found."
    except Exception as e:
        return f"Error checking DMARC: {e}"
