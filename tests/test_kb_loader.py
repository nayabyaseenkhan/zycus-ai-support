from src.utils.kb_loader import load_knowledge_base


def test_kb_loader():
    documents = load_knowledge_base()

    print(
        f"Knowledge-base documents loaded: "
        f"{len(documents)}"
    )

    assert len(documents) == 9

    for document in documents:
        assert document["content"]
        assert document["source"]
        assert document["category"]

        print(
            f"✓ {document['source']} "
            f"({document['category']})"
        )

    print(
        "\nKnowledge-base loader test passed successfully!"
    )