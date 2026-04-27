from pathlib import Path
import json

from sentence_transformers import SentenceTransformer


CHUNKS_DIR = Path("data/chunks")
VECTORSTORE_DIR = Path("data/vectorstore")

MODEL_NAME = "all-MiniLM-L6-v2"


def ensure_vectorstore_dir():
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)


def load_chunks(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_embeddings(data, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def run():
    ensure_vectorstore_dir()

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    chunk_files = sorted(CHUNKS_DIR.glob("*.json"))

    if not chunk_files:
        print("No chunk files found")
        return

    for file_path in chunk_files:
        print(f"Embedding: {file_path}")

        chunks = load_chunks(file_path)

        texts = [chunk["text"] for chunk in chunks]

        embeddings = model.encode(texts, show_progress_bar=True)

        enriched_chunks = []

        for chunk, emb in zip(chunks, embeddings):
            chunk_copy = chunk.copy()
            chunk_copy["embedding"] = emb.tolist()
            enriched_chunks.append(chunk_copy)

        output_path = VECTORSTORE_DIR / file_path.name
        save_embeddings(enriched_chunks, output_path)

        print(f"Saved: {output_path}")


if __name__ == "__main__":
    run()
