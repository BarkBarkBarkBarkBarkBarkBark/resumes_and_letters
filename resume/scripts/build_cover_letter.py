#!/usr/bin/env python3
"""
build_cover_letter.py — Generate a cover letter from YAML snippets.

Usage:
    python scripts/build_cover_letter.py --company "UC Davis" --role "Research Engineer"
    python scripts/build_cover_letter.py --company "Acme" --role "Analyst" --profile data_analytics
    python scripts/build_cover_letter.py --company "Acme" --role "Analyst" --output custom_stem
    python scripts/build_cover_letter.py --company "UC Davis" --role "Lab Manager" --md-only
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

# ── Path constants ────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATES_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output"


# ── YAML loading ──────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── Output naming ─────────────────────────────────────────────────────────────

def _sanitize(s: str) -> str:
    return (
        s.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace(",", "")
        .replace(".", "")
    )


def get_output_stem(name: str, company: str, role: str) -> str:
    return f"{_sanitize(name)}_cover_letter_{_sanitize(company)}_{_sanitize(role)}"


# ── Pandoc helpers ────────────────────────────────────────────────────────────

def _run_pandoc(args: list) -> tuple:
    try:
        result = subprocess.run(
            ["pandoc"] + args,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            return False, result.stderr.strip()
        return True, ""
    except FileNotFoundError:
        return False, "pandoc not found. Install with: brew install pandoc"
    except subprocess.TimeoutExpired:
        return False, "pandoc timed out."


def _to_docx(md_path: Path, docx_path: Path) -> bool:
    ok, err = _run_pandoc([
        str(md_path), "-f", "markdown", "-t", "docx",
        "--standalone", "-o", str(docx_path),
    ])
    if not ok:
        print(f"  [WARN] DOCX failed: {err}")
    return ok


def _to_pdf(md_path: Path, pdf_path: Path) -> bool:
    for engine in ["weasyprint", "wkhtmltopdf", "pdflatex", "xelatex", "lualatex"]:
        ok, _ = _run_pandoc([
            str(md_path), "-f", "markdown", "--standalone",
            f"--pdf-engine={engine}", "-o", str(pdf_path),
        ])
        if ok:
            return True
    print(
        "  [WARN] PDF generation skipped — no supported PDF engine found.\n"
        "         Install: pip install weasyprint   or   brew install wkhtmltopdf"
    )
    return False


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Build a cover letter from YAML snippets.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--company", required=True, help="Target company name")
    parser.add_argument("--role", required=True, help="Target role / position title")
    parser.add_argument(
        "--profile", default=None,
        help="Role profile key (controls opener selection). Default: target_metadata.default_profile",
    )
    parser.add_argument(
        "--output", default=None,
        help="Output filename stem without extension (default: auto-generated)",
    )
    parser.add_argument(
        "--md-only", action="store_true",
        help="Render Markdown only; skip DOCX and PDF",
    )
    args = parser.parse_args()

    resume_data = load_yaml(DATA_DIR / "base_resume.yaml")
    snippets = load_yaml(DATA_DIR / "cover_letter_snippets.yaml")
    profiles = load_yaml(DATA_DIR / "role_profiles.yaml")

    meta = resume_data.get("target_metadata", {})
    profile_key = args.profile or meta.get("default_profile", "default")
    profile = profiles.get(profile_key, profiles.get("default", {}))

    opener_key = profile.get("cover_letter_opener", "neuroengineering")
    opener_variants = snippets.get("opener", {})
    opener_template = opener_variants.get(opener_key) or opener_variants.get("neuroengineering", "")
    opener = opener_template.format(role=args.role, company=args.company)

    closer_key = "research" if profile_key in ("neuroengineering", "clinical_research") else "default"
    closer = snippets.get("closer", {}).get(closer_key, snippets.get("closer", {}).get("default", ""))

    ctx = {
        "name": resume_data["personal"]["name"],
        "contact": resume_data["personal"]["contact"],
        "company": args.company,
        "role": args.role,
        "profile_key": profile_key,
        "opener": opener,
        "research_background": snippets.get("research_background", ""),
        "projects_background": snippets.get("projects_background", ""),
        "data_systems_background": snippets.get("data_systems_background", ""),
        "lab_background": snippets.get("lab_background", ""),
        "closer": closer,
    }

    # For analytics profile, omit the neuro-specific research_background
    if profile_key == "data_analytics":
        ctx["research_background"] = ""
        ctx["projects_background"] = ""

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("cover_letter.md.j2")
    md_text = template.render(**ctx)

    OUTPUT_DIR.mkdir(exist_ok=True)
    name = resume_data["personal"]["name"]
    stem = args.output or get_output_stem(name, args.company, args.role)
    md_path = OUTPUT_DIR / f"{stem}.md"
    docx_path = OUTPUT_DIR / f"{stem}.docx"
    pdf_path = OUTPUT_DIR / f"{stem}.pdf"

    md_path.write_text(md_text, encoding="utf-8")
    print(f"[OK] Markdown  → {md_path.relative_to(ROOT)}")

    if not args.md_only:
        if _to_docx(md_path, docx_path):
            print(f"[OK] DOCX      → {docx_path.relative_to(ROOT)}")
        if _to_pdf(md_path, pdf_path):
            print(f"[OK] PDF       → {pdf_path.relative_to(ROOT)}")

    print(f"\nDone. Cover letter → {args.company} / {args.role}")


if __name__ == "__main__":
    main()
