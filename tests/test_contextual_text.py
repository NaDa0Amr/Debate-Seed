from src.chunk import chunk_document
from src.contextual_text import build_contextual_text


def test_contextual_text_prefixes_title_and_section_without_changing_body():
    body = "Evidence about sparse expert routing."
    contextual = build_contextual_text(
        body,
        title="  Mixture   of Experts  ",
        headers={"h2": "Routing", "h3": "Load balancing"},
    )
    assert contextual == (
        "Document title: Mixture of Experts\n"
        "Section: Routing > Load balancing\n\n"
        + body
    )


def test_chunk_hash_changes_when_document_context_changes():
    markdown = "## Evidence\n\n" + ("state space sequence evidence " * 12)
    first = chunk_document(
        {"url": "https://example/a", "title": "Mamba", "markdown": markdown}, 0
    )[0]
    second = chunk_document(
        {"url": "https://example/a", "title": "Transformer", "markdown": markdown}, 0
    )[0]
    assert first["text"] == second["text"]
    assert first["embedding_text"].startswith("Document title: Mamba")
    assert first["content_hash"] != second["content_hash"]
