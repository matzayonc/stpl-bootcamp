#!/usr/bin/env python3
"""Strip adjacent visually-identical pages from a Beamer PDF.

Beamer's auto-overlay (`\\beamerdefaultoverlayspecification{<+->}`) advances
the overlay counter once per container environment (block, alertblock,
exampleblock, column). With `setbeamercovered=invisible`, the overlay
where an empty container opens renders nothing new — a dead click.

This script renders every page to a low-res raster, hashes it, and rewrites
the PDF (in place) keeping only the first page of each adjacent-identical run.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def page_hashes(pdf: Path, dpi: int = 50) -> list[str]:
    with tempfile.TemporaryDirectory() as td:
        prefix = Path(td) / "p"
        subprocess.run(
            ["pdftoppm", "-r", str(dpi), str(pdf), str(prefix)],
            check=True,
        )
        files = sorted(Path(td).glob("p-*.ppm"), key=lambda p: int(p.stem.split("-")[1]))
        return [hashlib.md5(f.read_bytes()).hexdigest() for f in files]


def keep_indices(hashes: list[str]) -> list[int]:
    keep = []
    prev = None
    for i, h in enumerate(hashes, start=1):
        if h != prev:
            keep.append(i)
        prev = h
    return keep


def dropped_indices(hashes: list[str], keep: list[int]) -> list[int]:
    keep_set = set(keep)
    return [i for i in range(1, len(hashes) + 1) if i not in keep_set]


def dedupe(pdf: Path) -> tuple[int, int, list[int]]:
    hashes = page_hashes(pdf)
    total = len(hashes)
    keep = keep_indices(hashes)
    dropped = total - len(keep)
    if dropped == 0:
        return total, 0, []

    dropped_pages = dropped_indices(hashes, keep)
    page_list = ",".join(str(i) for i in keep)
    with tempfile.NamedTemporaryFile(suffix=".pdf", dir=pdf.parent, delete=False) as tmp:
        out_path = Path(tmp.name)
    try:
        subprocess.run(
            ["qpdf", str(pdf), "--pages", str(pdf), page_list, "--", str(out_path)],
            check=True,
        )
        shutil.move(out_path, pdf)
    except Exception:
        out_path.unlink(missing_ok=True)
        raise
    return total, dropped, dropped_pages


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: dedupe_overlays.py <pdf> [<pdf> ...]", file=sys.stderr)
        return 2
    rc = 0
    for arg in argv[1:]:
        pdf = Path(arg)
        if not pdf.is_file():
            print(f"skip: {pdf} (not a file)", file=sys.stderr)
            rc = 1
            continue
        total, dropped, dropped_pages = dedupe(pdf)
        if dropped:
            page_list = ",".join(str(i) for i in dropped_pages)
            print(f"{pdf.name}: {total} pages, dropped {dropped} (pre-dedup indices: {page_list})")
        else:
            print(f"{pdf.name}: {total} pages, dropped 0")
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
