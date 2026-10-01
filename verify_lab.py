"""Offline evidence verification and reproducible reranking experiment."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from evaluate_answers import build_evaluation_artifact, load_evaluation_inputs
from template import BenchmarkRunner, FailureAnalyzer, RAGASEvaluator, rerank_by_overlap


def verify(root: Path) -> dict[str, Any]:
    if (root / "template.py").read_bytes() != (root / "solution/solution.py").read_bytes():
        raise ValueError("template.py and solution/solution.py differ")
    pairs, answers = load_evaluation_inputs(
        root / "golden_dataset.json", root / "artifacts/actual_answers.json"
    )
    evaluator = RAGASEvaluator()
    runner = BenchmarkRunner()
    results = runner.run(pairs, answers.__getitem__, evaluator)
    expected = build_evaluation_artifact(results, runner.generate_report(results), FailureAnalyzer())
    recorded = json.loads((root / "artifacts/benchmark_results.json").read_text(encoding="utf-8"))
    if recorded != expected:
        raise ValueError("Saved benchmark differs from evaluation of the recorded answers")

    actual = json.loads((root / "artifacts/actual_answers.json").read_text(encoding="utf-8"))
    corpus = (root / "data/technology_store").resolve()
    for answer in actual["answers"]:
        for chunk in answer["retrieved_contexts"]:
            source = (corpus / chunk["source_doc"]).resolve()
            if not source.is_relative_to(corpus):
                raise ValueError("Retrieved source escapes corpus")
            source_text = " ".join(source.read_text(encoding="utf-8").split())
            if " ".join(chunk["text"].split()) not in source_text:
                raise ValueError(f"{answer['id']}: retrieved chunk lacks corpus provenance")

    rows: list[dict[str, Any]] = []
    for pair, result in zip(pairs, results, strict=True):
        before = pair.retrieved_contexts
        after = rerank_by_overlap(before, pair.question)
        if Counter(before) != Counter(after):
            raise ValueError("Reranking changed the retrieved set")
        recall_before = evaluator.evaluate_context_recall(before, pair.expected_answer)
        recall_after = evaluator.evaluate_context_recall(after, pair.expected_answer)
        if recall_before != recall_after:
            raise ValueError("Reranking changed recall")
        precision_before = evaluator.evaluate_context_precision(before, pair.expected_answer)
        precision_after = evaluator.evaluate_context_precision(after, pair.expected_answer)
        rows.append({
            "id": pair.metadata["id"],
            "recall_before": recall_before,
            "recall_after": recall_after,
            "precision_before": precision_before,
            "precision_after": precision_after,
            "delta_precision": precision_after - precision_before,
            "gold_faithfulness": result.faithfulness,
            "retrieved_faithfulness": evaluator.evaluate_faithfulness(
                result.actual_answer, "\n\n".join(before)
            ),
        })
    return {
        "query_source": "question only; no expected answer used for reranking",
        "count": len(rows),
        "averages": {
            metric: sum(row[metric] for row in rows) / len(rows)
            for metric in rows[0] if metric != "id"
        },
        "results": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-reranking", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    try:
        report = verify(root)
        path = root / "artifacts/reranking_results.json"
        if args.write_reranking:
            path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        elif json.loads(path.read_text(encoding="utf-8")) != report:
            raise ValueError("Saved reranking experiment differs from reproduced results")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"PASS: {report['count']} recorded answers, benchmark, provenance, and reranking verified")
    print(json.dumps(report["averages"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
