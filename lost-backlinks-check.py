import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# ==== SETTINGS ====
INPUT_FILE = "urls.csv"          # one URL per row, first column
OUTPUT_FILE = "link_check_results.csv"

# Put your target here
TARGET_DOMAIN = "yourdomain.com"
# Optional: if you want to check one exact URL instead of any link to your domain
EXACT_TARGET_URL = ""  # example: "https://yourdomain.com/some-page/"
# ==================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0 Safari/537.36"
}

def normalize_url(url):
    if not url:
        return ""
    return url.strip().rstrip("/")

def matches_target(href):
    href_norm = normalize_url(href)

    if EXACT_TARGET_URL:
        return href_norm == normalize_url(EXACT_TARGET_URL)

    parsed = urlparse(href_norm)
    domain = parsed.netloc.lower().replace("www.", "")
    return domain == TARGET_DOMAIN.lower().replace("www.", "")

def check_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        matched_links = []
        for a in links:
            absolute_href = urljoin(response.url, a["href"])
            if matches_target(absolute_href):
                matched_links.append(absolute_href)

        return {
            "source_url": url,
            "final_url": response.url,
            "status_code": response.status_code,
            "link_found": "YES" if matched_links else "NO",
            "matched_links": " | ".join(sorted(set(matched_links))),
            "error": ""
        }

    except Exception as e:
        return {
            "source_url": url,
            "final_url": "",
            "status_code": "",
            "link_found": "ERROR",
            "matched_links": "",
            "error": str(e)
        }

def main():
    rows = []

    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            url = row[0].strip()
            if not url or url.lower() == "url":
                continue
            rows.append(check_page(url))

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["source_url", "final_url", "status_code", "link_found", "matched_links", "error"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Done. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
