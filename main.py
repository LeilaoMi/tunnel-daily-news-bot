import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os
import re

EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")

# 🔥 多源（关键：扩大范围）
SOURCES = [
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    "https://www.freeclashnode.com/",
]

# 🔥 节点特征（弱过滤）
PATTERNS = [
    r"vmess://[A-Za-z0-9+/=]+",
    r"vless://[^\s]+",
    r"trojan://[^\s]+",
    r"ss://[^\s]+",
    r"ssr://[^\s]+",
    r"https?://[^\s]*clash[^\s]*",
]

def fetch():
    text = ""

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            text += r.text + "\n"
        except:
            pass

    return text

def extract_nodes(text):
    nodes = []

    for pattern in PATTERNS:
        matches = re.findall(pattern, text)
        nodes.extend(matches)

    # 去重
    return list(set(nodes))[:100]

def format_msg(nodes):
    date = datetime.now().strftime("%Y-%m-%d")

    msg = f"【节点收集 {date}】\n\n"

    if not nodes:
        msg += "未抓到节点（源失效或被限制）"
    else:
        for i, n in enumerate(nodes, 1):
            msg += f"{i}. {n}\n\n"

    return msg

def send(body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = "每日节点收集"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(EMAIL, PASS)
        s.send_message(msg)

if __name__ == "__main__":
    raw = fetch()
    nodes = extract_nodes(raw)
    send(format_msg(nodes))
