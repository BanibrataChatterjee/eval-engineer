"""Install the Eval Engineer skill into Codex and Claude Code projects."""

from __future__ import annotations

import argparse
import shutil
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Iterator, Sequence


SKILL_NAME = "eval-engineer"
REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/metrics.md",
    "references/tokenomics-rca.md",
    "scripts/summarize_debug_packet.py",
    "scripts/compare_tokenomics_packets.py",
)


class InstallError(RuntimeError):
    """Raised when installation cannot proceed safely."""


@dataclass(frozen=True)
class Destination:
    agent: str
    scope: str
    path: Path


def _repo_skill_source() -> Path | None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "skills" / SKILL_NAME
        if (candidate / "SKILL.md").is_file():
            return candidate
    return None


@contextmanager
def _skill_source() -> Iterator[Path]:
    local_source = _repo_skill_source()
    if local_source is not None:
        yield local_source
        return

    bundled = resources.files("eval_engineer_installer").joinpath(
        "bundled",
        SKILL_NAME,
    )
    with resources.as_file(bundled) as bundled_path:
        yield bundled_path


def _validate_skill_dir(path: Path) -> None:
    missing = [relative for relative in REQUIRED_FILES if not (path / relative).is_file()]
    if missing:
        formatted = ", ".join(missing)
        raise InstallError(f"{path} is missing required skill files: {formatted}")


def _selected_agents(target: str) -> list[str]:
    if target == "both":
        return ["codex", "claude"]
    return [target]


def _destinations(target: str, scope: str, project_dir: Path) -> list[Destination]:
    project_dir = project_dir.expanduser().resolve()
    destinations: list[Destination] = []
    for agent in _selected_agents(target):
        if scope == "project":
            base = project_dir / (".agents" if agent == "codex" else ".claude") / "skills"
        elif agent == "codex":
            base = Path.home() / ".agents" / "skills"
        else:
            base = Path.home() / ".claude" / "skills"
        destinations.append(Destination(agent=agent, scope=scope, path=base / SKILL_NAME))
    return destinations


def _copy_ignore(_directory: str, names: list[str]) -> set[str]:
    ignored = {".DS_Store", "__pycache__"}
    return {name for name in names if name in ignored or name.endswith(".pyc")}


def _remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def install(args: argparse.Namespace) -> int:
    destinations = _destinations(args.target, args.scope, args.project_dir)
    with _skill_source() as source:
        _validate_skill_dir(source)

        for destination in destinations:
            if args.dry_run:
                print(f"would install {destination.agent} {destination.scope}: {destination.path}")
                continue

            if destination.path.exists() or destination.path.is_symlink():
                if not args.force:
                    raise InstallError(
                        f"{destination.path} already exists; rerun with --force to replace it"
                    )
                _remove_existing(destination.path)

            destination.path.parent.mkdir(parents=True, exist_ok=True)
            if args.link:
                if _repo_skill_source() is None:
                    raise InstallError("--link requires running from a source checkout")
                destination.path.symlink_to(source)
            else:
                shutil.copytree(source, destination.path, ignore=_copy_ignore)

            _validate_skill_dir(destination.path)
            print(f"installed {destination.agent} {destination.scope}: {destination.path}")

    if not args.dry_run:
        print("restart Codex or Claude Code if the skills directory was not already watched")
    return 0


def check(args: argparse.Namespace) -> int:
    destinations = _destinations(args.target, args.scope, args.project_dir)
    for destination in destinations:
        _validate_skill_dir(destination.path)
        print(f"ok {destination.agent} {destination.scope}: {destination.path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="eval-engineer",
        description="Install the Eval Engineer Galileo skill for Codex and Claude Code.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install", help="install the skill")
    add_shared_arguments(install_parser)
    install_parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing installed skill directory",
    )
    install_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print destinations without writing files",
    )
    install_parser.add_argument(
        "--link",
        action="store_true",
        help="symlink from a local source checkout instead of copying files",
    )
    install_parser.set_defaults(func=install)

    check_parser = subparsers.add_parser("check", help="validate an installed skill")
    add_shared_arguments(check_parser)
    check_parser.set_defaults(func=check)

    return parser


def add_shared_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--target",
        choices=("codex", "claude", "both"),
        default="both",
        help="which agent skill location to install into",
    )
    parser.add_argument(
        "--scope",
        choices=("project", "user"),
        default="project",
        help="install into the current project or the user's global skill folder",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="project root for project-scope installs",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except InstallError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
