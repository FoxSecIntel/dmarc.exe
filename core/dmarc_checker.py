import dns.resolver
import base64

HIDDEN_HASH = "wqhWaWN0b3J5IGlzIG5vdCB3aW5uaW5nIGZvciBvdXJzZWx2ZXMsIGJ1dCBmb3Igb3RoZXJzLiAtIFRoZSBNYW5kYWxvcmlhbsKoCg=="

def decrypt_hidden_message():
    return base64.b64decode(HIDDEN_HASH).decode("utf-8")

def check_dmarc(domain):
    if domain.lower() == "m":
        return f"=== Decrypted Message ===\n{decrypt_hidden_message()}"

    try:
        result = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
        for txt in result:
            record = txt.to_text().replace('"', '')
            if record.startswith('v=DMARC1'):
                tags = record.split(';')
                formatted = "DMARC record found:\n" + "\n".join(f" {tag.strip()}" for tag in tags if tag.strip())
                return formatted
        return "No valid DMARC record found."
    except dns.resolver.NoAnswer:
        return "No DMARC record found (no answer)"
    except dns.resolver.NXDOMAIN:
        return f"Domain {domain} does not exist"
    except dns.exception.Timeout:
        return "DNS query timed out"
    except Exception as e:
        return f"Unexpected error: {e}"

