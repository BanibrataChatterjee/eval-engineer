#!/usr/bin/env python3
"""Installer checks for the Eval Engineer skill CLI."""

from __future__ import annotations

import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from eval_engineer_installer import cli  # noqa: E402


def run_cli(args: list[str]) -> int:
    with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
        return cli.main(args)


class EvalEngineerInstallerTest(unittest.TestCase):
    def test_project_install_copies_codex_and_claude_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "sample-project"
            project_dir.mkdir()

            result = run_cli(["install", "--project-dir", str(project_dir)])

            self.assertEqual(result, 0)
            for base in (project_dir / ".agents", project_dir / ".claude"):
                skill_dir = base / "skills" / cli.SKILL_NAME
                self.assertTrue((skill_dir / "SKILL.md").is_file())
                self.assertTrue((skill_dir / "references" / "tokenomics-rca.md").is_file())
                self.assertTrue((skill_dir / "scripts" / "summarize_debug_packet.py").is_file())
                self.assertEqual(skill_dir.name, "eval-engineer")

    def test_project_install_requires_force_for_existing_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "sample-project"
            project_dir.mkdir()

            first = run_cli(["install", "--target", "codex", "--project-dir", str(project_dir)])
            second = run_cli(["install", "--target", "codex", "--project-dir", str(project_dir)])

            self.assertEqual(first, 0)
            self.assertEqual(second, 1)

    def test_check_validates_installed_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "sample-project"
            project_dir.mkdir()

            install_result = run_cli(["install", "--target", "claude", "--project-dir", str(project_dir)])
            check_result = run_cli(["check", "--target", "claude", "--project-dir", str(project_dir)])

            self.assertEqual(install_result, 0)
            self.assertEqual(check_result, 0)


if __name__ == "__main__":
    unittest.main()
