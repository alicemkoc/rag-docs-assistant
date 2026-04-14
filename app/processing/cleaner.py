from pathlib import Path

from bs4 import BeautifulSoup


RAW_DATA_DIR = Path("data/raw")
CLEANED_DATA_DIR = Path("data/cleaned")


def ensure_cleaned_data_dir() -> None:
    CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_html(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Removes unnecessary tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # Whitespace Cleanning
    lines = [line.strip() for line in text.splitlines()]
    non_empty_lines = [line for line in lines if line]

    return "\n".join(non_empty_lines)


def build_output_path(input_path: Path) -> Path:
    return CLEANED_DATA_DIR / f"{input_path.stem}.txt"


def clean_file(input_path: Path) -> Path:
    html = load_html(input_path)
    cleaned_text = extract_text_from_html(html)
    output_path = build_output_path(input_path)
    output_path.write_text(cleaned_text, encoding="utf-8")
    return output_path


def run() -> None:
    ensure_cleaned_data_dir()

    html_files = sorted(RAW_DATA_DIR.glob("*.html"))

    if not html_files:
        print("No raw HTML files found in data/raw")
        return

    for html_file in html_files:
        print(f"Cleaning: {html_file}")
        output_path = clean_file(html_file)
        print(f"Saved: {output_path}")


if __name__ == "__main__":
    run()
