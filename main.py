def analyze_repo(text):
    signals = []

    keywords = [
        "xray", "v2ray", "clash", "sing-box",
        "config", "yaml", "protocol"
    ]

    for line in text.split("\n"):
        if any(k in line.lower() for k in keywords):
            signals.append(line.strip())

    return list(set(signals))[:50]
