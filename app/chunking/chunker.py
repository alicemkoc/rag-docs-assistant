from pathlib import Path
import json


CLEANED_DATA_DIR = Path("data/cleaned")
CHUNKS_DATA_DIR = Path("data/chunks")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def ensure_chunks_dir() -> None:
    CHUNKS_DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_text(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def split_text(text: str) -> list:
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + CHUNK_SIZE
        chunk_text = text[start:end]

        chunks.append({"text": chunk_text, "start_char": start, "end_char": end})

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def build_chunk_objects(chunks: list, source_file: str) -> list:
    chunk_objects = []

    for i, chunk in enumerate(chunks):
        chunk_objects.append(
            {
                "chunk_id": f"{source_file}_{i}",
                "text": chunk["text"],
                "metadata": {
                    "source": source_file,
                    "start_char": chunk["start_char"],
                    "end_char": chunk["end_char"],
                },
            }
        )

    return chunk_objects


def save_chunks(chunks: list, output_path: Path) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)


def process_file(file_path: Path) -> Path:
    text = load_text(file_path)
    raw_chunks = split_text(text)
    chunk_objects = build_chunk_objects(raw_chunks, file_path.stem)

    output_path = CHUNKS_DATA_DIR / f"{file_path.stem}.json"
    save_chunks(chunk_objects, output_path)

    return output_path


def run() -> None:
    ensure_chunks_dir()

    text_files = sorted(CLEANED_DATA_DIR.glob("*.txt"))

    if not text_files:
        print("No cleaned text files found")
        return

    for file_path in text_files:
        print(f"Chunking: {file_path}")
        output_path = process_file(file_path)
        print(f"Saved: {output_path}")


if __name__ == "__main__":
    run()
