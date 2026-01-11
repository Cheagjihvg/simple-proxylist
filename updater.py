import requests
import json
import os
import shutil
import random
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from datetime import datetime

# =============================
# CONFIG
# =============================
CONFIG_FILE = "config.json"
OUTPUT_FILE = "proxy.txt"
TIMEOUT = 10
MAX_WORKERS = 20
VALID_STATUS = range(200, 400)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

# =============================
# THREAD-SAFE STORAGE
# =============================
unique_proxies = set()

# =============================
# LOAD CONFIG
# =============================
def load_proxy_sources():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError("config.json not found")

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    urls = data.get("proxy_sources", [])
    return list(set(urls))

# =============================
# BACKUP CONFIG
# =============================
def backup_config():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"config_backup_{timestamp}.json"
    shutil.copy(CONFIG_FILE, backup_name)
    print(f"📦 Backup created: {backup_name}")

# =============================
# SAVE CONFIG
# =============================
def save_proxy_sources(valid_urls):
    backup_config()
    data = {"proxy_sources": sorted(valid_urls)}
    tmp_file = CONFIG_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_file, CONFIG_FILE)
    print(f"✔ config.json updated with {len(valid_urls)} valid sources")

# =============================
# URL CHECK
# =============================
def is_valid_url_format(url):
    try:
        r = urlparse(url)
        return r.scheme in ("http", "https") and r.netloc
    except:
        return False

def check_url(url):
    if not is_valid_url_format(url):
        return url, False, "Invalid format"
    try:
        r = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": random.choice(user_agents)})
        if r.status_code in VALID_STATUS:
            return url, True, f"OK ({r.status_code})"
        return url, False, f"Status {r.status_code}"
    except requests.exceptions.Timeout:
        return url, False, "Timeout"
    except requests.exceptions.ConnectionError:
        return url, False, "Connection error"
    except Exception as e:
        return url, False, str(e)

def validate_urls(urls):
    valid, dead = [], []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(check_url, url) for url in urls]
        for f in as_completed(futures):
            url, ok, msg = f.result()
            print(("✓" if ok else "✗"), url, msg)
            if ok:
                valid.append(url)
            else:
                dead.append(url)
    return valid, dead

# =============================
# EXTRACT PROXIES
# =============================
def extract_proxies(text):
    return set(re.findall(r"\b\d{1,3}(?:\.\d{1,3}){3}:\d{1,5}\b", text))

def fetch_proxies(url):
    try:
        resp = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": random.choice(user_agents)})
        if resp.status_code not in VALID_STATUS:
            return set()
        return extract_proxies(resp.text)
    except:
        return set()

# =============================
# DOWNLOAD PROXIES
# =============================
def download_all_proxies(sources):
    print(f"🔄 Downloading proxies from {len(sources)} sources...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_proxies, url): url for url in sources}
        for f in as_completed(futures):
            url = futures[f]
            try:
                proxies = f.result()
                new_count = 0
                with open(OUTPUT_FILE, "a") as out:
                    for p in proxies:
                        if p not in unique_proxies:
                            unique_proxies.add(p)
                            out.write(p + "\n")
                            new_count += 1
                if new_count:
                    print(f"✔ [{url}] Added {new_count} new proxies")
            except Exception as e:
                print(f"✗ [{url}] Error: {e}")

# =============================
# MAIN
# =============================
if __name__ == "__main__":
    # 1️⃣ Validate config.json URLs
    print("🔄 Auto-validating proxy sources...")
    proxy_urls = load_proxy_sources()
    valid_urls, dead_urls = validate_urls(proxy_urls)
    print(f"\n✅ Valid: {len(valid_urls)}, ❌ Dead: {len(dead_urls)}")
    if valid_urls:
        save_proxy_sources(valid_urls)

    # 2️⃣ Remove old proxy file
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    # 3️⃣ Download proxies
    download_all_proxies(valid_urls)

    print(f"\n📌 Total unique proxies collected: {len(unique_proxies)}")
    print(f"📌 Saved to {OUTPUT_FILE}")
