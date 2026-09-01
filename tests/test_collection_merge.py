from src.collection import (
    ar5iv_document_is_usable,
    canonical_source_url,
    document_needs_refresh,
    discover_arxiv_papers,
    merge_documents,
)
from src.evaluate import EVAL_JUDGMENTS
from src.source_seeds import CURATED_SOURCE_URLS


class FakeResponse:
    status = 200

    def __init__(self, identifiers):
        entries = "".join(
            f"<entry><id>https://arxiv.org/abs/{identifier}v2</id></entry>"
            for identifier in identifiers
        )
        self.body = (
            '<feed xmlns="http://www.w3.org/2005/Atom">'
            f"{entries}</feed>"
        ).encode("utf-8")


class FakeArxivClient:
    def __init__(self):
        self.starts = []

    def get(self, _url, params, timeout):
        assert timeout == 30
        self.starts.append(params["start"])
        pages = {
            0: ["1000.00001", "1000.00002"],
            2: ["1000.00003"],
        }
        return FakeResponse(pages.get(params["start"], []))


def test_curated_seeds_cover_every_fixed_qrel_source():
    expected = {
        canonical_source_url(url)
        for judgment in EVAL_JUDGMENTS
        for url in judgment["relevant_sources"]
    }
    curated = {canonical_source_url(url) for url in CURATED_SOURCE_URLS}
    assert expected <= curated


def test_arxiv_discovery_paginates_and_normalizes_versions():
    client = FakeArxivClient()
    results = discover_arxiv_papers(
        "all:test", max_results=4, client=client, page_size=2
    )
    assert client.starts == [0, 2]
    assert results == [
        "https://arxiv.org/abs/1000.00001",
        "https://arxiv.org/abs/1000.00002",
        "https://arxiv.org/abs/1000.00003",
    ]


def test_collection_merge_preserves_existing_canonical_source():
    existing = [{"url": "https://arxiv.org/abs/1234.56789v2", "title": "existing"}]
    additions = [
        {"url": "https://www.arxiv.org/abs/1234.56789", "title": "duplicate"},
        {"url": "https://example.com/article/?tracking=yes", "title": "new"},
    ]
    merged = merge_documents(existing, additions)
    assert [document["title"] for document in merged] == ["existing", "new"]


def test_collection_merge_replaces_broken_ar5iv_record_with_pdf():
    existing = [
        {
            "url": "https://arxiv.org/abs/1707.06347",
            "title": "[1707.06347] Untitled Document",
            "markdown": "See pages 1-last of <ppo-min.pdf> " * 30,
            "fetch_method": "ar5iv",
        }
    ]
    pdf = {
        "url": "https://arxiv.org/abs/1707.06347",
        "title": "Proximal Policy Optimization Algorithms",
        "markdown": "Proximal policy optimization full paper text. " * 30,
        "fetch_method": "pdf",
    }

    assert document_needs_refresh(existing[0])
    assert not document_needs_refresh(pdf)
    assert merge_documents(existing, [pdf]) == [pdf]


def test_ar5iv_conversion_shell_triggers_pdf_fallback():
    conversion_shell = (
        "See pages 1-last of <ppo-min.pdf>\n"
        "Conversion report Report an issue View original on arXiv " * 20
    )
    assert not ar5iv_document_is_usable(
        "[1707.06347] Untitled Document", conversion_shell
    )


def test_ar5iv_paper_content_is_usable():
    paper = "Abstract self-attention transformer architecture evidence. " * 20
    assert ar5iv_document_is_usable("Attention Is All You Need", paper)
