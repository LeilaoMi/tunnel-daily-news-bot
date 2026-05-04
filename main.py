import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")

SOURCES = [
    "https://rsshub.app/github/search/vless",
    "https://rsshub.app/github/search/vmess",
    "https://rsshub.app/github/search/clash",
    "https://hnrss.org/frontpage",
]

KEYWORDS = [
    "vless://", "vmess://", "trojan://",
    "ss://", "ssr://",
    "clash", "订阅", "节点", "proxy", "vpn"
]

BAD_WORDS = [
    "广告", "购买", "机场", "客服", "推广", "telegram群"
]

def fetch():
    data = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            data += r.text + "\n"
        except:
            pass
    return data

def extract(text):
    results = []

    for line in text.split("\n"):
        l = line.lower()

        if any(b in line for b in BAD_WORDS):
            continue

        if any(k in l for k in KEYWORDS):
            results.append(line.strip())

    # 去重
    return list(set(results))[:80]

def format_msg(nodes):
    today = datetime.now().strftime("%Y-%m-%d")

    msg = f"【每日节点情报 {today}】\n\n"

    if not nodes:
        msg += "未获取到有效节点（源可能失效）"
        return msg

    for i, n in enumerate(nodes, 1):
        msg += f"{i}. {n}\n\n"

    return msg

def send(body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "每日节点情报"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.yandex.com", 465) as s:
        s.login(EMAIL, PASS)
        s.send_message(msg)

if __name__ == "__main__":
    raw = fetch()
    nodes = extract(raw)
    body = format_msg(nodes)
    send(body)
