import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")

KEYWORDS = [
    "xray", "v2ray", "clash", "sing-box",
    "config", "yaml", "protocol"
]

def fetch():
    url = "https://api.github.com/search/repositories?q=v2ray+clash+sing-box"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        text = ""
        for item in data.get("items", []):
            text += item.get("full_name", "") + "\n"
            text += item.get("description", "") + "\n"

        return text
    except:
        return ""

# 👇 你写的逻辑（保留并优化）
def analyze_repo(text):
    signals = []

    for line in text.split("\n"):
        if any(k in line.lower() for k in KEYWORDS):
            signals.append(line.strip())

    return list(set(signals))[:50]

def send_email(body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = f"网络技术情报 {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(EMAIL, PASS)
        s.send_message(msg)

if __name__ == "__main__":
    raw = fetch()
    result = analyze_repo(raw)

    if not result:
        body = "今日未检测到相关技术更新"
    else:
        body = "【技术情报】\n\n" + "\n".join(result)

    send_email(body)
