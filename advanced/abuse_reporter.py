import requests
import configparser

def load_abuseipdb_key():
    config = configparser.ConfigParser()
    config.read("config/config.ini")
    return config["ABUSEIPDB"]["api_key"]

def report_ip_to_abuse(ip):
    api_key = load_abuseipdb_key()
    url = "https://api.abuseipdb.com/api/v2/report"
    headers = {'Key': api_key, 'Accept': 'application/json'}
    data = {
        'ip': ip,
        'categories': '4,5',  # Phishing, spoofing
        'comment': 'Reported via DMARC.exe toolkit'
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()
