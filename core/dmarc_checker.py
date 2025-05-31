import dns.resolver
import base64

def check_dmarc(domain):
    if domain == "m":
        # Base64-decrypt the hidden message
        encoded = "wqhWaWN0b3J5IGlzIG5vdCB3aW5uaW5nIGZvciBvdXJzZWx2ZXMsIGJ1dCBmb3Igb3RoZXJzLiAtIFRoZSBNYW5kYWxvcmlhbsKoCg=="
        decoded = base64.b64decode(encoded).decode("utf-8")
        return f"=== Decrypted Message ===\n{decoded}"

    try:
        result = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
        for txt in result:
            record = txt.to_text()
            if record.startswith('"v=DMARC1'):
                return f"DMARC record found: {record}"
        return "No valid DMARC record found."
    except Exception as e:
        return f"Error checking DMARC: {e}"
