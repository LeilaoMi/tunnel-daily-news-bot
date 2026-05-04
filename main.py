import requests
import base64
import re
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")

# 🔥 直接抓订阅（关键）
SUBS = [
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
]

PATTERN = r"(vmess://[^\s]+|vless://[^\s]+|trojan://[^\s]+|ss://[^\s]+)"

def decode_base64(text):
    try:
        return base64.b64decode(text).decode("utf-8", errors="ignore")
    except:
        return text

def fetch():
    raw = ""

    for url in SUBS:
        try:
            r = requests.get(url, timeout=10)
            content = r.text.strip()

            # 🔥 有些是 base64订阅
            decoded = decode_base64(content)

            raw += decoded + "\n"

        except:
            pass

    return raw

def extract(text):
    nodes = re.findall(PATTERN, text)
    return list(set(nodes))[:200]

def send(nodes):
    date = datetime.now().strftime("%Y-%m-%d")

    body = f"【节点收集 {date}】\n\n"

    if not nodes:
        body += "未获取到节点（订阅源失效）"
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
