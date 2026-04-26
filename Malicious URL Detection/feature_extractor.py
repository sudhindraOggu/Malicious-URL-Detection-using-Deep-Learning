import re
import socket
import requests
from urllib.parse import urlparse

def extract_features(url):
    features = []

    parsed = urlparse(url)
    hostname = parsed.netloc

    # 1 IP Address
    try:
        socket.inet_aton(hostname)
        features.append(-1)
    except:
        features.append(1)

    # 2 URL Length
    features.append(1 if len(url) < 54 else 0 if len(url) <= 75 else -1)

    # 3 Shortening
    features.append(-1 if re.search(r"bit\.ly|tinyurl|t\.co", url) else 1)

    # 4 @ symbol
    features.append(-1 if "@" in url else 1)

    # 5 //
    features.append(-1 if "//" in url[7:] else 1)

    # 6 Hyphen
    features.append(-1 if "-" in hostname else 1)

    # 7 Subdomain
    dots = hostname.count(".")
    features.append(1 if dots == 1 else 0 if dots == 2 else -1)

    # 8 HTTPS
    features.append(1 if url.startswith("https") else -1)

    # 9–12 basic placeholders
    features += [0, 0]
    features.append(1 if parsed.port in [None, 80, 443] else -1)
    features.append(-1 if "https" in hostname else 1)

    # -------- content-based --------
    try:
        response = requests.get(url, timeout=3)
        content = response.text
        redirects = len(response.history)
    except:
        content = ""
        redirects = 0

    features.append(1 if "src" in content else 0)
    features.append(1 if "<a" in content else 0)
    features.append(1 if "<link" in content else 0)
    features.append(-1 if "about:blank" in content else 1)
    features.append(-1 if "mailto:" in content else 1)
    features.append(1 if hostname in url else -1)
    features.append(-1 if redirects > 2 else 1)
    features.append(-1 if "onmouseover" in content else 1)
    features.append(-1 if "event.button==2" in content else 1)
    features.append(-1 if "alert(" in content else 1)
    features.append(-1 if "<iframe" in content else 1)

    # Remaining placeholders
    features += [0] * 7

    return features