import requests
import re
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")

SOURCES = [
    "https://api.github.com/search/code?q=vmess",
    "https://api.github.com/search/code?q=vless",
    "https://api.github.com/search/code?q=trojan",
]

PATTERN = r"(vmess://[^\s]+|vless://[^\s]+|trojan://[^\s]+|ss://[^\s]+)"

def fetch():
    text = ""

    headers = {"Accept": "application/vnd.github+json"}

    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json()

            for item in data.get("items", []):
                if "text_matches" in item:
                    for m in item["text_matches"]:
                        text += m.get("fragment", "") + "\n"

        except:
            pass

    return text

def extract(text):
    return list(set(re.findall(PATTERN, text)))[:100]

def send(nodes):
    date = datetime.now().strftime("%Y-%m-%d")

    body = f"【节点收集 {date}】\n\n"

    if not nodes:
        body += "未获取到节点（GitHub限流或无匹配结果）"
    else:
        for i, n in enumerate(nodes, 1):
            body += f"{i}. {n}\n\n"

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "节点收集"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(EMAIL, PASS)
        s.send_message(msg)

if __name__ == "__main__":
    raw = fetch()
    nodes = extract(raw)
    send(nodes)
