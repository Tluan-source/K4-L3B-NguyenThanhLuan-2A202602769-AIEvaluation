"""Additional edge cases; the supplied assessment tests remain unchanged."""

import pytest

from template import BenchmarkRunner, EvalResult, LLMJudge, QAPair, rerank_by_overlap


def test_judge_rejects_invalid_scores_and_unknown_criteria():
    judge = LLMJudge(lambda _: '{"accuracy": NaN, "clarity": true, "extra": 1}')
    assert judge.score_response("Q", "A", {"accuracy": "", "clarity": ""})[
        "scores"
    ] == {"accuracy": 0.5, "clarity": 0.5}


def test_judge_clamps_scores_and_parses_fenced_json():
    judge = LLMJudge(lambda _: '```json\n{"scores": {"accuracy": 2, "clarity": -1}}\n```')
    assert judge.score_response("Q", "A", {"accuracy": "", "clarity": ""})[
        "scores"
    ] == {"accuracy": 1.0, "clarity": 0.0}


@pytest.mark.parametrize("current,passed", [(0.75, True), (0.749, False)])
def test_regression_threshold_is_strict(current: float, passed: bool):
    pair = QAPair("Q", "A")
    baseline = EvalResult(pair, "A", 0.8, 0.8, 0.8, True)
    candidate = EvalResult(pair, "A", current, 0.8, 0.8, True)
    assert BenchmarkRunner().run_regression([candidate], [baseline])["passed"] is passed


def test_reranker_preserves_duplicates_and_stable_ties():
    chunks = ["noise", "answer first", "answer second", "noise"]
    assert rerank_by_overlap(chunks, "answer") == [
        "answer first", "answer second", "noise", "noise"
    ]
    assert chunks == ["noise", "answer first", "answer second", "noise"]
