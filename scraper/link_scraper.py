# ==========================================
# File: scraper/link_scraper.py
# Mengambil link artikel dari halaman berita.
# Dirancang agar bisa bekerja di berbagai situs
# berita tanpa hardcode ke satu website.
# ==========================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import time
import re

# Digunakan untuk mengambil isi artikel dari URL yang ditemukan
from scraper.content_scraper import scrape_multiple_articles


# ==========================================
# KONFIGURASI FILTER LINK
# ==========================================

# Kata kunci yang biasanya muncul pada halaman
# non-artikel seperti video, kategori, atau iklan.
URL_BLACKLIST_KEYWORDS = [
    "video", "foto", "gallery", "galeri",
    "infografis", "podcast", "live",
    "20detik", "tv",
    "indeks", "category", "kategori",
    "topik", "tag", "label",
    "lipsus",
    "author", "penulis",
    "search", "pencarian",
    "login", "signup", "register",
    "sitemap",
    "pubads", "doubleclick", "googleads",
    "ads", "adservice", "click.php",
]

# Pola URL yang umum digunakan oleh artikel berita
ARTICLE_URL_PATTERNS = [
    r"/read/\d{4}/\d{2}/\d{2}/\d+/",   # Kompas
    r"/d-\d{5,}/",                     # Detik
    r"/\d{8}\d{6}-\d+-\d+/",           # CNN Indonesia
    r"/read/\d{6,}/",                  # Tempo
    r"/\d{4}/\d{2}/\d{2}/\d+/",        # Tribun / Okezone
    r"/\d{4}-\d{2}-\d{2}/",            # BBC style
    r"/\d{8}/[a-z0-9\-]+",
    r"/berita/\d{6,}/",                # Antara
]

# Ekstensi file yang pasti bukan artikel
NON_ARTICLE_EXTENSIONS = (
    ".jpg", ".jpeg", ".png", ".gif", ".webp",
    ".pdf", ".zip", ".mp4", ".mp3",
    ".css", ".js",
)


# ==========================================
# MEMBUAT SELENIUM DRIVER
# ==========================================

def create_driver(headless: bool = True) -> webdriver.Chrome:
    """Membuat Selenium Chrome WebDriver."""
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Mengurangi deteksi otomatisasi
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    return webdriver.Chrome(options=chrome_options)


# ==========================================
# UTILITAS FILTER URL
# ==========================================

def _has_blacklisted_keyword(url: str) -> bool:
    """Cek apakah URL mengandung kata kunci yang dilarang."""
    parsed = urlparse(url)
    target = (parsed.netloc + parsed.path).lower()
    return any(keyword in target for keyword in URL_BLACKLIST_KEYWORDS)


def _matches_article_pattern(url: str) -> bool:
    """Cek apakah URL cocok dengan pola artikel."""
    return any(re.search(pattern, url) for pattern in ARTICLE_URL_PATTERNS)


def _is_valid_http_url(url: str) -> bool:
    """Pastikan URL adalah http/https."""
    return bool(url) and url.startswith(("http://", "https://"))


def _has_non_article_extension(url: str) -> bool:
    """Cek apakah URL mengarah ke file non-artikel."""
    path = urlparse(url).path.lower()
    return path.endswith(NON_ARTICLE_EXTENSIONS)


def _is_same_domain(url: str, base_url: str) -> bool:
    """Pastikan link berasal dari domain yang sama."""
    base_domain = urlparse(base_url).netloc
    link_domain = urlparse(url).netloc

    def root_domain(netloc: str) -> str:
        parts = netloc.split(".")
        return ".".join(parts[-2:]) if len(parts) >= 2 else netloc

    return root_domain(link_domain) == root_domain(base_domain)


def looks_like_article(url: str, base_url: str = "") -> bool:
    """
    Menentukan apakah sebuah URL kemungkinan
    merupakan halaman artikel berita.
    """
    if not _is_valid_http_url(url):
        return False

    if _has_non_article_extension(url):
        return False

    if _has_blacklisted_keyword(url):
        return False

    if base_url and not _is_same_domain(url, base_url):
        return False

    if not _matches_article_pattern(url):
        return False

    return True


# ==========================================
# MENGAMBIL LINK ARTIKEL
# ==========================================

def get_article_links(driver: webdriver.Chrome, url: str, limit: int = 5) -> list[str]:
    """Mengambil sejumlah link artikel dari halaman berita."""

    print(f"[LinkScraper] Membuka halaman: {url}")
    driver.get(url)

    time.sleep(3)

    anchors = driver.find_elements(By.TAG_NAME, "a")

    seen_urls = set()
    valid_links = []

    for anchor in anchors:
        href = anchor.get_attribute("href")

        if href and href not in seen_urls and looks_like_article(href, base_url=url):
            seen_urls.add(href)
            valid_links.append(href)

            if len(valid_links) >= limit:
                break

    print(f"[LinkScraper] Ditemukan {len(valid_links)} link artikel")
    for link in valid_links:
        print(f"  → {link}")

    return valid_links


# ==========================================
# INTEGRASI LINK SCRAPER + CONTENT SCRAPER
# ==========================================

def run_full_scraper(url: str, limit: int = 5) -> list[dict]:
    """
    Mengambil link artikel lalu mengekstrak
    judul, tanggal, dan isi artikel.
    """

    driver = create_driver()

    try:
        links = get_article_links(driver, url, limit)

        if not links:
            print("[LinkScraper] Tidak ada link artikel ditemukan.")
            return []

        articles = scrape_multiple_articles(driver, links)

        return articles

    finally:
        driver.quit()


# ==========================================
# TESTING TANPA GUI
# ==========================================

if __name__ == "__main__":

    test_url = "https://nasional.kompas.com/"

    hasil = run_full_scraper(test_url, limit=5)

    print("\n=== HASIL SCRAPING ===\n")

    if not hasil:
        print("Tidak ada artikel berhasil di-scrape.")
    else:
        for i, artikel in enumerate(hasil, start=1):
            print(f"[{i}] Judul   : {artikel.get('title', '-')}")
            print(f"    Tanggal : {artikel.get('date', '-')}")
            print(f"    Link    : {artikel.get('link', '-')}")
            isi = artikel.get('content', '')
            print(f"    Isi     : {isi[:150]}{'...' if len(isi) > 150 else ''}\n")