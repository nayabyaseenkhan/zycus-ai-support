from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "knowledge-base"


def load_knowledge_base() -> list[dict]:
    """Load all Markdown knowledge-base documents."""

    documents = []

    for file_path in KNOWLEDGE_BASE_PATH.rglob("*.md"):
        relative_path = file_path.relative_to(KNOWLEDGE_BASE_PATH)

        category = (
            relative_path.parts[0]
            if relative_path.parts
            else "unknown"
        )

        content = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "content": content,
                "source": str(relative_path),
                "category": category,
            }
        )

    return documents


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[str]:
    """Split text into overlapping chunks."""

    if not text.strip():
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - chunk_overlap

    return chunks


def load_knowledge_base_chunks(
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[dict]:
    """Load KB documents and split them into chunks."""

    documents = load_knowledge_base()
    chunks = []

    for document in documents:
        text_chunks = chunk_text(
            document["content"],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for chunk_index, content in enumerate(text_chunks):
            chunks.append(
                {
                    "content": content,
                    "source": document["source"],
                    "category": document["category"],
                    "chunk_index": chunk_index,
                }
            )

    return chunks