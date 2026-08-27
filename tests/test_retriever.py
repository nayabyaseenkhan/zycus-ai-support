from src.triage.retriever import KnowledgeBaseRetriever


def test_retriever():
    print("Testing knowledge-base retriever...\n")

    retriever = KnowledgeBaseRetriever()

    queries = [
        "authentication and SSO problems",
        "billing and subscription plans",
        "getting started with the product",
    ]

    for query in queries:
        print(f"Query: {query}")

        results = retriever.search(
            query,
            top_k=2,
        )

        assert results
        assert len(results) <= 2

        for result in results:
            assert result["source"]
            assert result["content"]
            assert "score" in result

            print(
                f"  ✓ {result['source']} "
                f"(score={result['score']:.3f})"
            )

        print()

    print("Retriever test passed successfully!")