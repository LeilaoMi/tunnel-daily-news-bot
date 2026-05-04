import requests
import re
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")

# 🔥 多真实可访问来源（重点）
SOURCES = [
    "https://www.freeclashnode.com/",
    "https://nodefree.org/",
    "https://clashnode.com/",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
]

PATTERN = r"(vmess://[^\s\"']+|vless://[^\s\"']+|trojan://[^\s\"']+|ss://[^\s\"']+)"

def fetch():
    text = ""

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            text += r.text + "\n"
        except:
            pass

    return text

def extract(text):
    nodes = re.findall(PATTERN, text)
    return list(set(nodes))[:150]

def send(nodes):
    date = datetime.now().strftime("%Y-%m-%d")

    body = f"【节点收集 {date}】\n\n"

    if not nodes:
        body += "未抓到节点（源可能被墙或更新）"
    else:
        for i, n in enumerate(nodes, 1):
            body += f"{i}. {n}\n\n"

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "节点收集日报"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(EMAIL, PASS)
        s.send_message(msg)

if __name__ == "__main__":
    raw = fetch()
    nodes = extract(raw)
    send(nodes)
