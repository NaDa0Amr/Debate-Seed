import inspect

import pytest

from src.clean import relevance_check
from src.evaluate import (
    _ndcg_at_k,
    _result_matches,
    audit_corpus_coverage,
    compute_metrics,
    run_evaluation,
)
from src.retrieve import (
    _console_safe,
    _limit_per_source,
    _rrf_fuse,
    _validate_index_identity,
    _validate_top_k,
)
from src.run_pipeline import timed
from src.settings import (
    EMBEDDING_MODEL,
    EMBEDDING_MODEL_REVISION,
    PIPELINE_VERSION,
    PREPROCESSING_VERSION,
)


def test_cleaner_keeps_a_document_with_one_specific_topic_term():
    _, strong_hits = relevance_check("FlashAttention improves transformer memory efficiency.")
    assert strong_hits == 1


def test_cleaner_normalizes_hyphenated_topic_phrases():
    _, strong_hits = relevance_check("Mixture-of-Experts routing")
    assert strong_hits >= 1


def test_retrieval_limits_chunks_per_source():
    results = [
        {"chunk_id": "a1", "url": "https://example/a"},
        {"chunk_id": "a2", "url": "https://example/a"},
        {"chunk_id": "b1", "url": "https://example/b"},
    ]
    assert [item["chunk_id"] for item in _limit_per_source(results, 1)] == ["a1", "b1"]


def test_rrf_preserves_contextual_text_for_reranking():
    vector_results = [{
        "chunk_id": "a1",
        "text": "evidence",
        "embedding_text": "Document title: Paper\n\nevidence",
    }]
    result = _rrf_fuse(vector_results, [])[0]
    assert result["embedding_text"] == "Document title: Paper\n\nevidence"


def test_source_limit_normalizes_arxiv_versions_and_trailing_slashes():
    results = [
        {"chunk_id": "a1", "url": "https://arxiv.org/abs/1234.56789v2/"},
        {"chunk_id": "a2", "url": "https://www.arxiv.org/abs/1234.56789"},
    ]
    assert [item["chunk_id"] for item in _limit_per_source(results, 1)] == ["a1"]


def test_text_hints_do_not_create_relevance():
    expected = {
        "relevant_sources": ["https://arxiv.org/abs/1234.56789"],
        "relevant_chunks": [{"url": "https://arxiv.org/abs/1234.56789", "hint": "attention"}],
    }
    unrelated = {
        "url": "https://arxiv.org/abs/9999.99999",
        "title": "Attention",
        "text": "attention attention",
    }
    assert not _result_matches(unrelated, expected)


def test_ndcg_uses_fixed_qrels_for_ideal_ranking():
    expected = {
        "relevant_sources": [
            "https://arxiv.org/abs/1111.11111",
            "https://arxiv.org/abs/2222.22222",
        ]
    }
    results = [{"url": "https://arxiv.org/abs/1111.11111"}]
    assert 0 < _ndcg_at_k(results, expected, k=5) < 1


def test_precision_at_k_uses_k_and_duplicate_sources_count_once():
    expected = {"relevant_sources": ["https://arxiv.org/abs/1111.11111"]}
    results = [
        {"url": "https://arxiv.org/abs/1111.11111"},
        {"url": "https://arxiv.org/abs/1111.11111v2"},
    ]
    metrics = compute_metrics(results, expected, k=5)
    assert metrics["precision_at_k"] == 0.2
    assert metrics["relevant_in_top_k"] == 1


def test_corpus_coverage_separates_missing_qrels():
    judgments = [{
        "query_id": "q1",
        "relevant_sources": ["https://example/a", "https://example/b"],
    }]
    coverage = audit_corpus_coverage(judgments, {"https://example/a"})
    assert coverage["available_qrel_sources"] == 1
    assert coverage["fully_covered_queries"] == 0
    assert coverage["mean_source_recall_ceiling"] == 0.5


def test_evaluation_allows_a_diagnostic_run_by_default():
    parameter = inspect.signature(run_evaluation).parameters["allow_incomplete_corpus"]
    assert parameter.default is True


def test_retrieval_defaults_to_evaluated_hybrid_only_mode():
    from src.retrieve import retrieve

    assert inspect.signature(retrieve).parameters["rerank"].default is False


def test_candidate_pool_cannot_be_smaller_than_top_k():
    with pytest.raises(ValueError, match="candidate_pool"):
        _validate_top_k(5, 4)


def test_retrieval_rejects_incompatible_index_identity():
    manifest = {
        "embedding_models": [EMBEDDING_MODEL],
        "embedding_model_revisions": [EMBEDDING_MODEL_REVISION],
        "preprocessing_versions": [PREPROCESSING_VERSION],
        "pipeline_versions": [PIPELINE_VERSION],
        "missing_identity_columns": [],
    }
    _validate_index_identity(manifest)
    with pytest.raises(RuntimeError, match="incompatible"):
        _validate_index_identity({**manifest, "preprocessing_versions": ["old"]})


def test_pipeline_timer_does_not_report_success_after_failure(capsys):
    with pytest.raises(ValueError):
        with timed("broken step"):
            raise ValueError("boom")
    output = capsys.readouterr().out
    assert "[FAILED] broken step" in output
    assert "[OK] broken step" not in output


def test_console_safe_replaces_unsupported_characters(monkeypatch):
    class LegacyStdout:
        encoding = "cp1252"

    monkeypatch.setattr("src.retrieve.sys.stdout", LegacyStdout())
    assert _console_safe("result ‣ section") == "result ? section"
