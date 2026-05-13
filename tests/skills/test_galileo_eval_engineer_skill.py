#!/usr/bin/env python3
"""Behavior checks for the Galileo Eval Engineer skill."""

from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "skills" / "galileo-eval-engineer"
SUMMARIZER = SKILL_DIR / "scripts" / "summarize_debug_packet.py"
ASSETS_DIR = SKILL_DIR / "assets"


def _load_summarizer():
    spec = importlib.util.spec_from_file_location("summarize_debug_packet", SUMMARIZER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class GalileoEvalEngineerSkillTest(unittest.TestCase):
    def test_skill_description_is_portable(self) -> None:
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        match = re.search(r"^description:\s*(.+)$", skill_text, flags=re.MULTILINE)
        self.assertIsNotNone(match)
        description = match.group(1).strip()
        self.assertLessEqual(len(description), 200)
        self.assertIn("AI agents/RAG apps", description)

    def test_skill_does_not_hardcode_reference_fixture(self) -> None:
        banned_terms = [
            "TC-1",
            "tool-calling-support",
            "Brazil",
            "wire_transfer",
            "claude-sonnet-4-6",
        ]
        for path in SKILL_DIR.rglob("*"):
            if path.is_file() and not path.name.startswith("."):
                text = path.read_text(encoding="utf-8")
                for term in banned_terms:
                    self.assertNotIn(term, text, f"{term} leaked into {path}")

    def test_skill_names_baseline_and_verification_packets(self) -> None:
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn(".galileo/current/debug-packet.json", skill_text)
        self.assertIn(".galileo/current/verification-debug-packet.json", skill_text)
        self.assertIn("debug-packet-after.json", skill_text)
        self.assertIn("log streams", skill_text)

    def test_summarizer_handles_generic_rag_packet(self) -> None:
        module = _load_summarizer()
        packet_path = ROOT / "tests" / "skills" / "fixtures" / "generic-rag-debug-packet.json"
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        summary = module.summarize(packet)

        self.assertIn("agent_type: rag", summary)
        self.assertIn("groundedness: 0.42", summary)
        self.assertIn("expected:", summary)
        self.assertIn("actual:", summary)
        self.assertIn("trace-rag-001", summary)

    def test_summarizer_handles_generic_tool_calling_packet(self) -> None:
        module = _load_summarizer()
        packet_path = ROOT / "tests" / "skills" / "fixtures" / "generic-tool-calling-debug-packet.json"
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        summary = module.summarize(packet)

        self.assertIn("agent_type: tool_calling", summary)
        self.assertIn("tool_selection_quality: 0.44", summary)
        self.assertIn("update_crm_record", summary)
        self.assertIn("send_email", summary)
        self.assertIn("trace-tool-001", summary)

    def test_artifact_templates_preserve_grounded_rca_shape(self) -> None:
        expected = {
            "diagnosis-template.md": [
                "RCA Summary",
                "Evidence Source",
                "Evidence Links",
                "Metric Contract",
                "Failure Pattern",
                "Expected Versus Actual",
                "Metric Reading",
                "Uncertainty",
                "Debug packet",
                "Verification packet",
                "Trace IDs",
                "Span IDs",
                "Metrics",
            ],
            "fix-plan-template.md": [
                "Bounded Change",
                "Fix Surface",
                "Evidence Behind The Change",
                "Metric Contract",
                "Editable Files",
                "Non-Goals",
                "Risk",
            ],
            "verification-plan-template.md": [
                "Baseline",
                "Evidence Source",
                "Commands",
                "Verification Mode",
                "Galileo Comparison",
                "Regression Check",
                "Success Criteria",
                "Follow-Up",
                "verification-debug-packet.json",
                "log-stream-origin RCA",
                "metrics",
                "traces",
            ],
        }

        for filename, required_terms in expected.items():
            text = (ASSETS_DIR / filename).read_text(encoding="utf-8")
            for term in required_terms:
                self.assertIn(term, text, f"{term} missing from {filename}")

    def test_rca_recipe_captures_galileo_learning_loop(self) -> None:
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        recipe_text = (SKILL_DIR / "references" / "rca-recipe.md").read_text(encoding="utf-8")

        self.assertIn("references/rca-recipe.md", skill_text)

        required_terms = [
            "Start From Fetched Evidence",
            "Name The Metric Contract",
            "Classify The Fix Surface",
            "Prove One Narrow Improvement",
            "Preserve The Learning",
            "controlled experiment",
            "production log stream",
            "mixed",
            "retriever, ranker, query rewrite, or chunking",
            "deterministic guardrail",
            "adapter or SDK wiring",
            "custom metric or rubric",
            "Choose verification mode from the evidence source",
            "metric/eval gap",
        ]
        for term in required_terms:
            self.assertIn(term, recipe_text)

    def test_galileo_sources_reference_covers_experiments_and_log_streams(self) -> None:
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        source_text = (SKILL_DIR / "references" / "galileo-sources.md").read_text(encoding="utf-8")

        self.assertIn("references/galileo-sources.md", skill_text)

        required_terms = [
            "experiments for controlled sample evals",
            "log streams for production or live-traffic RCA",
            "Normalize both into the same debug-packet contract",
            "Production evidence should often become future controlled evals",
        ]
        for term in required_terms:
            self.assertIn(term, source_text)

    def test_metrics_reference_is_not_agent_metric_only(self) -> None:
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        metrics_text = (SKILL_DIR / "references" / "metrics.md").read_text(encoding="utf-8")

        self.assertIn("references/metrics.md", skill_text)

        required_terms = [
            "choose metrics from the failure contract",
            "Response Quality",
            "RAG And Context Use",
            "Safety, Security, And Style",
            "SQL",
            "Vision",
            "Custom Metrics",
            "fixture-specific, not a general recommendation",
        ]
        for term in required_terms:
            self.assertIn(term, metrics_text)


if __name__ == "__main__":
    unittest.main()
