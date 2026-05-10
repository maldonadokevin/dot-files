#!/usr/bin/env python3
"""
Symlink dot-files to their target locations.
Shows diffs and asks for confirmation before making any change.
Checks for required tools and offers to install missing ones.
"""

import difflib
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
DIM    = "\033[2m"


def bold(s):   return f"{BOLD}{s}{RESET}"
def red(s):    return f"{RED}{s}{RESET}"
def green(s):  return f"{GREEN}{s}{RESET}"
def yellow(s): return f"{YELLOW}{s}{RESET}"
def cyan(s):   return f"{CYAN}{s}{RESET}"
def dim(s):    return f"{DIM}{s}{RESET}"


# ---------------------------------------------------------------------------
# Tools to check
# Each entry: (display_name, check_fn, install_cmd)
# check_fn returns True if the tool is already available.
# install_cmd is a shell string run via subprocess.
# ---------------------------------------------------------------------------
def _has(cmd: str) -> bool:
    return shutil.which(cmd) is not None

def _has_brew() -> bool:
    return _has("brew")

def _has_uv() -> bool:
    return Path.home().joinpath(".local/bin/uv").exists() or _has("uv")

def _has_rust() -> bool:
    return Path.home().joinpath(".cargo/bin/cargo").exists() or _has("cargo")

def _has_tmux() -> bool:
    return _has("tmux")

TOOLS = [
    (
        "Homebrew",
        _has_brew,
        '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
    ),
    (
        "uv (Python)",
        _has_uv,
        "curl -LsSf https://astral.sh/uv/install.sh | sh",
    ),
    (
        "Rust / cargo",
        _has_rust,
        "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
    ),
    (
        "tmux",
        _has_tmux,
        "brew install tmux",
    ),
]


# ---------------------------------------------------------------------------
# File map: repo-relative source → absolute target
# ---------------------------------------------------------------------------
REPO = Path(__file__).parent.resolve()
HOME = Path.home()
VSCODE_SETTINGS = HOME / "Library/Application Support/Code/User/settings.json"

FILES = [
    (REPO / ".zshrc",               HOME / ".zshrc"),
    (REPO / ".vimrc",               HOME / ".vimrc"),
    (REPO / ".gitconfig",           HOME / ".gitconfig"),
    (REPO / ".gitignore_global",    HOME / ".gitignore_global"),
    (REPO / ".tmux.conf",           HOME / ".tmux.conf"),
    (REPO / "vscode/settings.json", VSCODE_SETTINGS),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def confirm(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} {dim('[y/n]')} ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False


def read_text(path: Path) -> list[str]:
    try:
        return path.read_text(errors="replace").splitlines(keepends=True)
    except OSError:
        return []


def print_diff(src: Path, dst: Path) -> None:
    src_lines = read_text(src)
    dst_lines = read_text(dst)
    diff = list(difflib.unified_diff(
        dst_lines, src_lines,
        fromfile=f"current  {dst}",
        tofile=f"incoming {src}",
    ))
    if not diff:
        print(dim("  (files are identical)"))
        return
    for line in diff:
        if line.startswith("+++") or line.startswith("---"):
            print(bold(line), end="")
        elif line.startswith("+"):
            print(green(line), end="")
        elif line.startswith("-"):
            print(red(line), end="")
        elif line.startswith("@@"):
            print(cyan(line), end="")
        else:
            print(dim(line), end="")


def symlink(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() or dst.is_symlink():
        dst.unlink()
    dst.symlink_to(src)


def run(cmd: str) -> bool:
    """Run a shell command, streaming output. Returns True on success."""
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0


# ---------------------------------------------------------------------------
# Phases
# ---------------------------------------------------------------------------
def check_tools() -> None:
    print(bold("Checking tools\n"))

    for name, is_installed, install_cmd in TOOLS:
        if is_installed():
            print(f"  {green('✓')} {name}")
            continue

        print(f"  {yellow('✗')} {name} {dim('not found')}")
        if confirm(f"    Install {name}?"):
            print()
            ok = run(install_cmd)
            if ok:
                print(green(f"\n    ✓ {name} installed"))
            else:
                print(red(f"\n    ✗ Installation failed — you may need to install {name} manually"))
        else:
            print(dim("    skipped"))

    print()


def link_files() -> None:
    print(bold("Linking dot-files\n"))

    skipped = installed = 0

    for src, dst in FILES:
        label = f"{dim(str(dst.parent) + '/')}{bold(dst.name)}"
        print(f"  {cyan('→')} {label}")

        # Already a correct symlink — nothing to do
        if dst.is_symlink() and dst.resolve() == src:
            print(green("    ✓ already linked, skipping\n"))
            skipped += 1
            continue

        # Target exists — show diff and confirm override
        if dst.exists() or dst.is_symlink():
            print(yellow("    ! target already exists — diff:\n"))
            print_diff(src, dst)
            print()
            if not confirm(yellow("    Override?")):
                print(dim("    skipped\n"))
                skipped += 1
                continue
        else:
            if not confirm("    Create symlink?"):
                print(dim("    skipped\n"))
                skipped += 1
                continue

        symlink(src, dst)
        print(green("    ✓ linked\n"))
        installed += 1

    print(dim("─" * 40))
    print(f"  {green(str(installed))} linked  {dim(str(skipped))} skipped")

    if installed > 0:
        print(dim("\n  Tip: open a new terminal tab to pick up .zshrc changes."))
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    print(bold(f"\nDot-files installer"))
    print(dim(f"Repo: {REPO}\n"))

    check_tools()
    link_files()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(red("\n\nAborted."))
        sys.exit(1)
