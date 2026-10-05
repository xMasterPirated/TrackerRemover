import sys
import re
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

def resource_path(filename):
    if getattr(sys, "frozen", False): return Path(sys._MEIPASS) / filename
    return Path(__file__).resolve().parent / filename

TRACKERS_PATH = resource_path("trackers")
with open(TRACKERS_PATH, "r", encoding="utf-8") as f:
    trackers_list = [line.strip() for line in f if line.strip()]

pattern = r'https?://[^\s<>"\'\])]+|www\.[^\s<>"\'\])]+'
url_pattern = re.compile(pattern)

def find_urls(text):
    return url_pattern.findall(text)

def get_redirect(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        response = requests.get(url, allow_redirects=True, stream=True, timeout=10)

    return response.url

def remove_trackers(url):
    if "tiktok" in url: url = get_redirect(url)

    parsed = urlparse(url)
    params = [
        (key, value)
        for key, value in parse_qsl(parsed.query)
        if key not in trackers_list
    ]

    return urlunparse(parsed._replace(query=urlencode(params)))