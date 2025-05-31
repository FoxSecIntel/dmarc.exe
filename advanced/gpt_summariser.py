import openai
import configparser

def load_openai_key():
    config = configparser.ConfigParser()
    config.read("config/config.ini")
    return config["OPENAI"]["api_key"]

def summarise_dmarc(findings):
    openai.api_key = load_openai_key()
    prompt = f"""Summarise this DMARC data and highlight any spoofing trends or notable behaviours:\n\n{findings}"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
