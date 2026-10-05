import re
import requests
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

pattern = r'https?://[^\s<>"\'\])]+|www\.[^\s<>"\'\])]+'
url_pattern = re.compile(pattern)

with open("trackers", "r") as f: tl = f.readlines()
trackers_list = [tracker.strip().replace("\n", "") for tracker in tl]

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