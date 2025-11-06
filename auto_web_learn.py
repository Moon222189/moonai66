import requests
from bs4 import BeautifulSoup

def fetch_text_from_url(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            paragraphs = soup.find_all("p")
            lines = []
            for p in paragraphs:
                text = p.get_text().strip()
                if text:
                    lines.append(text)
            return lines
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return []
