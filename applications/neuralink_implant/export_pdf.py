#!/usr/bin/env python3
"""Export the version-controlled Neuralink cover letter to a checked PDF.

Requires pandoc and pdflatex available on PATH. The editable Google Doc is
separate; this exports the Markdown revision in this repository, not Doc edits.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "cover_letter.md"
DESTINATION = HERE / "dist" / "neuralink_implant_cover_letter.pdf"


def build_pdf(source: Path = SOURCE, destination: Path = DESTINATION) -> Path:
    if not source.is_file():
        raise FileNotFoundError(f"Cover-letter source missing: {source}")
    for binary in ("pandoc", "pdflatex"):
        if shutil.which(binary) is None:
            raise RuntimeError(f"Missing {binary}; install it before exporting the PDF")
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "pandoc", str(source), "--from=markdown", "--standalone",
            "--pdf-engine=pdflatex", "-V", "geometry:margin=0.78in",
            "-V", "fontsize=10pt", "-o", str(destination),
        ],
        check=True,
        timeout=120,
    )
    if not destination.is_file() or destination.stat().st_size < 100:
        raise RuntimeError("Pandoc completed without a usable PDF")
    if destination.read_bytes()[:5] != b"%PDF-":
        raise RuntimeError("Output is not a PDF")
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DESTINATION)
    args = parser.parse_args()
    print(f"Verified PDF: {build_pdf(destination=args.output)}")
