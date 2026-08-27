from src.utils.kb_loader import load_knowledge_base_chunks


def test_kb_chunking():
    print("Testing knowledge-base chunking...\n")

    chunks = load_knowledge_base_chunks()

    print(f"Chunks created: {len(chunks)}")

    assert chunks
    assert len(chunks) >= 9

    for chunk in chunks[:5]:
        assert chunk["content"]
        assert chunk["source"]
        assert chunk["category"]
        assert "chunk_index" in chunk

        print(
            f"✓ {chunk['source']} "
            f"| {chunk['category']} "
            f"| chunk {chunk['chunk_index']}"
        )

    print(
        "\nKnowledge-base chunking test passed successfully!"
    )