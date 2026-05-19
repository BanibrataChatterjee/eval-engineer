#!/usr/bin/env python3
"""Behavior checks for the policy RAG reference implementation."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_DIR = ROOT / "tests" / "agents" / "policy-rag"
TOKENOMICS_COMPARE = (
    ROOT / "skills" / "eval-engineer" / "scripts" / "compare_tokenomics_packets.py"
)
sys.path.insert(0, str(EXAMPLE_DIR))


def _load_module(name: str, path: Path):
    if str(EXAMPLE_DIR) in sys.path:
        sys.path.remove(str(EXAMPLE_DIR))
    sys.path.insert(0, str(EXAMPLE_DIR))
    for module_name in list(sys.modules):
        if module_name == "agent" or module_name.startswith("agent."):
            del sys.modules[module_name]
        if module_name == "eval" or module_name.startswith("eval."):
            del sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PolicyRagReferenceTest(unittest.TestCase):
    def test_balanced_mode_reduces_cost_tokens_and_latency_without_score_loss(self) -> None:
        evaluate = _load_module("policy_rag_evaluate", EXAMPLE_DIR / "eval" / "evaluate.py")

        baseline = evaluate.run_evaluation(mode="wide")
        verification = evaluate.run_evaluation(mode="balanced")

        self.assertEqual(baseline["overall_score"], 1.0)
        self.assertEqual(verification["overall_score"], 1.0)
        self.assertLess(verification["average_cost"], baseline["average_cost"])
        self.assertLess(verification["average_num_input_tokens"], baseline["average_num_input_tokens"])
        self.assertLess(verification["average_num_total_tokens"], baseline["average_num_total_tokens"])
        self.assertLess(verification["average_latency"], baseline["average_latency"])

    def test_focused_mode_preserves_enterprise_cancellation_policy(self) -> None:
        run_agent = _load_module("policy_rag_run_agent", EXAMPLE_DIR / "agent" / "run_agent.py")

        result = run_agent.answer_question(
            "Can support cancel my enterprise subscription directly?",
            mode="focused",
        )

        self.assertIn("enterprise-cancellation", result["retrieved_document_ids"])
        self.assertIn("assigned account manager", result["answer"])
        self.assertIn("should not cancel", result["answer"])

    def test_balanced_mode_handles_multisource_policy_questions(self) -> None:
        run_agent = _load_module("policy_rag_run_agent", EXAMPLE_DIR / "agent" / "run_agent.py")

        refund = run_agent.answer_question(
            "An enterprise customer wants a $6,000 ACH refund. What has to happen and how long after approval?",
            mode="balanced",
        )
        self.assertIn("billing-refunds", refund["retrieved_document_ids"])
        self.assertIn("refund-exceptions", refund["retrieved_document_ids"])
        self.assertIn("billing ticket", refund["answer"])
        self.assertIn("account manager approval", refund["answer"])
        self.assertIn("7-14 business days", refund["answer"])

        legal_hold = run_agent.answer_question(
            "Can an admin export data for legal hold, or does compliance need to handle it?",
            mode="balanced",
        )
        self.assertIn("security-data", legal_hold["retrieved_document_ids"])
        self.assertIn("privacy-export", legal_hold["retrieved_document_ids"])
        self.assertIn("legal hold", legal_hold["answer"])
        self.assertIn("compliance", legal_hold["answer"])

    def test_focused_mode_is_rejected_for_harder_tokenomics_suite(self) -> None:
        compare = _load_module("compare_tokenomics_packets", TOKENOMICS_COMPARE)
        evaluate = _load_module("policy_rag_evaluate", EXAMPLE_DIR / "eval" / "evaluate.py")

        baseline = evaluate.to_debug_packet(evaluate.run_evaluation(mode="wide"), run_name="wide-hard-baseline")
        focused = evaluate.to_debug_packet(evaluate.run_evaluation(mode="focused"), run_name="focused-risky-candidate")

        result = compare.compare(baseline, focused, ["average_local_answer_score"])

        self.assertLess(focused["aggregate_metrics"]["average_cost"], baseline["aggregate_metrics"]["average_cost"])
        self.assertLess(focused["aggregate_metrics"]["average_local_answer_score"], 1.0)
        self.assertEqual(result["decision"], "reject: quality regressed")

    def test_balanced_mode_is_kept_for_harder_tokenomics_suite(self) -> None:
        compare = _load_module("compare_tokenomics_packets", TOKENOMICS_COMPARE)
        evaluate = _load_module("policy_rag_evaluate", EXAMPLE_DIR / "eval" / "evaluate.py")

        baseline = evaluate.to_debug_packet(evaluate.run_evaluation(mode="wide"), run_name="wide-hard-baseline")
        balanced = evaluate.to_debug_packet(evaluate.run_evaluation(mode="balanced"), run_name="balanced-candidate")

        result = compare.compare(baseline, balanced, ["average_local_answer_score"])

        self.assertLess(balanced["aggregate_metrics"]["average_cost"], baseline["aggregate_metrics"]["average_cost"])
        self.assertEqual(balanced["aggregate_metrics"]["average_local_answer_score"], 1.0)
        self.assertEqual(result["decision"], "keep-candidate: cost evidence improved and quality did not regress")
        self.assertIn("enterprise_refund", result["segments"])

    def test_curated_hard_packets_reject_risky_and_keep_balanced_candidate(self) -> None:
        compare = _load_module("compare_tokenomics_packets", TOKENOMICS_COMPARE)
        fixture_dir = EXAMPLE_DIR / "galileo" / "fixtures"
        baseline = json.loads(
            (fixture_dir / "hard-wide-baseline-debug-packet.json").read_text(encoding="utf-8")
        )
        risky = json.loads(
            (fixture_dir / "hard-focused-risky-debug-packet.json").read_text(encoding="utf-8")
        )
        balanced = json.loads(
            (fixture_dir / "hard-balanced-verification-debug-packet.json").read_text(encoding="utf-8")
        )

        rejected = compare.compare(baseline, risky, ["average_local_answer_score"])
        kept = compare.compare(baseline, balanced, ["average_local_answer_score"])

        self.assertEqual(rejected["decision"], "reject: quality regressed")
        self.assertLess(
            rejected["segments"]["enterprise_refund"]["quality"]["average_local_answer_score"]["delta"],
            0,
        )
        self.assertEqual(
            kept["decision"],
            "keep-candidate: cost evidence improved and quality did not regress",
        )
        self.assertEqual(
            kept["segments"]["enterprise_refund"]["quality"]["average_local_answer_score"]["delta"],
            0.0,
        )

    def test_curated_galileo_packets_keep_focused_candidate(self) -> None:
        compare = _load_module("compare_tokenomics_packets", TOKENOMICS_COMPARE)
        baseline = json.loads(
            (EXAMPLE_DIR / "galileo" / "fixtures" / "wide-baseline-debug-packet.json").read_text(
                encoding="utf-8"
            )
        )
        verification = json.loads(
            (EXAMPLE_DIR / "galileo" / "fixtures" / "focused-verification-debug-packet.json").read_text(
                encoding="utf-8"
            )
        )

        result = compare.compare(
            baseline,
            verification,
            ["average_completeness_gpt", "average_groundedness", "average_context_relevance"],
        )

        self.assertEqual(result["decision"], "keep-candidate: cost evidence improved and quality did not regress")
        self.assertLess(result["cost"]["average_cost"]["delta"], 0)
        self.assertEqual(result["quality"]["average_completeness_gpt"]["delta"], 0.0)


if __name__ == "__main__":
    unittest.main()
