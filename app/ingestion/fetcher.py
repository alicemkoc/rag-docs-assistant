from pathlib import Path
from urllib.parse import urlparse

import requests


RAW_DATA_DIR = Path("data/raw")

URLS = [
    "https://docs.langchain.com/oss/python/langchain/overview",
    "https://docs.langchain.com/oss/python/langchain/rag",
    "https://docs.langchain.com/oss/python/langchain/knowledge-base",
]


def ensure_raw_data_dir() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def build_output_filename(url: str) -> Path:
    parsed = urlparse(url)
    slug = parsed.path.rstrip("/").split("/")[-1] or "index"
    return RAW_DATA_DIR / f"{slug}.html"


def fetch_page(url: str, timeout: int = 20) -> str:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def save_html(html: str, output_path: Path) -> None:
    output_path.write_text(html, encoding="utf-8")


def run() -> None:
    ensure_raw_data_dir()

    for url in URLS:
        print(f"Fetching: {url}")
        try:
            html = fetch_page(url)
            output_path = build_output_filename(url)
            save_html(html, output_path)
            print(f"Saved: {output_path}")
        except requests.RequestException as exc:
            print(f"Failed to fetch {url}: {exc}")


if __name__ == "__main__":
    run()
