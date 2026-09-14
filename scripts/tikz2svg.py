#!/usr/bin/env python3
"""Render every tikzpicture in the bootcamp decks to SVG for the website.

For each presentations/<deck>.tex, every balanced
\\begin{tikzpicture}...\\end{tikzpicture} is compiled standalone with the
brand colors from preamble.tex and converted with pdftocairo into
site/static/img/diagrams/<deck>-<nn>.svg. Beamer overlays are neutralised so
the final overlay state is drawn.

Usage: python3 scripts/tikz2svg.py [deck ...]   (default: 0_why .. 7_wallet)
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRES = ROOT / "presentations"
BUILD = ROOT / "build" / "diagrams"
OUT = ROOT / "site" / "static" / "img" / "diagrams"

DEFAULT_DECKS = ["0_why", "1_paradigm", "2_amm", "3_lending",
                 "4_rust", "5_accounts", "6_anchor", "7_wallet"]

HEADER = r"""\documentclass[tikz,border=6pt]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{Archivo}
\renewcommand{\sfdefault}{\rmdefault}
\usepackage{amsmath,amssymb}
\usetikzlibrary{calc,positioning,arrows.meta}
\definecolor{stpldark}{HTML}{0B0E0F}
\definecolor{stplcard}{HTML}{161A1B}
\definecolor{stplborder}{HTML}{1E2526}
\definecolor{stplred}{HTML}{DC143C}
\definecolor{stplwhite}{HTML}{FFFFFF}
\definecolor{stplmuted}{HTML}{8A9BA8}
% Beamer overlay helpers used inside pictures -> draw the final state.
\tikzset{visible on/.style={}, invisible/.style={}}
\newcommand{\pause}{}
\begin{document}
\color{stplwhite}
"""
FOOTER = "\n\\end{document}\n"

BEGIN = r"\begin{tikzpicture}"
END = r"\end{tikzpicture}"


def extract_pictures(tex: str):
    """Yield each top-level tikzpicture source (nesting-aware)."""
    i = 0
    while True:
        start = tex.find(BEGIN, i)
        if start < 0:
            return
        depth, j = 0, start
        while True:
            b = tex.find(BEGIN, j)
            e = tex.find(END, j)
            if e < 0:
                raise ValueError("unbalanced tikzpicture")
            if 0 <= b < e:
                depth += 1
                j = b + len(BEGIN)
            else:
                depth -= 1
                j = e + len(END)
                if depth == 0:
                    yield tex[start:j]
                    break
        i = j


def is_placeholder(src: str) -> bool:
    # \screenshotph in 7_wallet draws a dashed "[ zrzut ekranu ]" box; skip.
    return "zrzut ekranu" in src


def strip_comments(src: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", src)


def render(deck: str) -> list[Path]:
    tex = (PRES / f"{deck}.tex").read_text(encoding="utf-8")
    # Expand \screenshotph before extraction so its picture is recognisable.
    pictures = [p for p in extract_pictures(tex) if not is_placeholder(p)]
    BUILD.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    for n, pic in enumerate(pictures, 1):
        name = f"{deck}-{n:02d}"
        src = BUILD / f"{name}.tex"
        src.write_text(HEADER + strip_comments(pic) + FOOTER, encoding="utf-8")
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", src.name],
            cwd=BUILD, capture_output=True, text=True,
        )
        if r.returncode != 0:
            log = (BUILD / f"{name}.log").read_text(errors="replace")
            err = "\n".join(l for l in log.splitlines() if l.startswith("!"))
            print(f"FAIL {name}\n{err}", file=sys.stderr)
            continue
        svg = OUT / f"{name}.svg"
        subprocess.run(
            ["pdftocairo", "-svg", str(BUILD / f"{name}.pdf"), str(svg)],
            check=True,
        )
        written.append(svg)
        print(f"ok   {svg.relative_to(ROOT)}")
    return written


def main(argv):
    decks = argv or DEFAULT_DECKS
    if not shutil.which("pdflatex") or not shutil.which("pdftocairo"):
        sys.exit("need pdflatex and pdftocairo on PATH")
    total = sum(len(render(d)) for d in decks)
    print(f"{total} diagrams -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1:])
