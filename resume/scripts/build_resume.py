#!/usr/bin/env python3
"""
build_resume.py — Generate resume Markdown, DOCX, and PDF from base_resume.yaml.

Usage:
    python scripts/build_resume.py
    python scripts/build_resume.py --profile neuroengineering
    python scripts/build_resume.py --profile data_analytics
    python scripts/build_resume.py --profile neuroengineering --output my_resume
    python scripts/build_resume.py --list-profiles
    python scripts/build_resume.py --md-only
"""

import argparse
import copy
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


# ── Validation ────────────────────────────────────────────────────────────────

REQUIRED_TOP_LEVEL = ["personal", "summary", "skills", "experience", "education"]


def validate_resume(data: dict) -> None:
    """Raise ValueError if required fields are missing."""
    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            raise ValueError(f"Missing required top-level field: '{field}'")
    personal = data["personal"]
    if not personal.get("name"):
        raise ValueError("personal.name is required")
    contact = personal.get("contact", {})
    if not contact.get("email"):
        raise ValueError("personal.contact.email is required")


# ── Date formatting ───────────────────────────────────────────────────────────

_MONTH_ABBR = {
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
    "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
    "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec",
}


def fmt_date(value) -> str:
    """Convert YYYY-MM or YYYY date strings to readable form (e.g. 'Jul 2021')."""
    if value is None:
        return ""
    val = str(value).strip()
    if val.lower() == "present":
        return "Present"
    # Year only
    if val.isdigit() and len(val) == 4:
        return val
    parts = val.split("-")
    if len(parts) == 2:
        year, month = parts
        return f"{_MONTH_ABBR.get(month.zfill(2), month)} {year}"
    return val


# ── Role profile filtering ────────────────────────────────────────────────────

def _score_bullet(bullet: dict, prefer: list, deprioritize: list) -> int:
    """Return a priority score for a bullet based on tag overlap with profile."""
    tags = bullet.get("tags", [])
    score = sum(1 for t in tags if t in prefer)
    score -= sum(1 for t in tags if t in deprioritize)
    return score


def apply_profile(data: dict, profile: dict) -> dict:
    """
    Return a deep copy of data with content filtered per the active role profile:
      - summary_text added (selected variant)
      - experience bullets sorted by tag score, capped at max_bullets_per_role
      - volunteer bullets similarly filtered (or section cleared)
      - skills filtered to profile's skill_categories
      - coursework cleared if include_coursework is False
    """
    result = copy.deepcopy(data)

    prefer = profile.get("prefer_tags", [])
    deprioritize = profile.get("deprioritize_tags", [])
    max_bullets = profile.get("max_bullets_per_role", 99)

    # Select summary variant
    summaries = result.get("summary", {})
    summary_key = profile.get("summary_key", "default")
    if isinstance(summaries, dict):
        result["summary_text"] = summaries.get(summary_key) or summaries.get("default", "")
    else:
        result["summary_text"] = str(summaries)

    # Filter and sort experience bullets
    for job in result.get("experience", []):
        bullets = job.get("bullets", [])
        if prefer:
            bullets = sorted(
                bullets,
                key=lambda b: _score_bullet(b, prefer, deprioritize),
                reverse=True,
            )
        job["bullets"] = bullets[:max_bullets]

    # Filter volunteer section
    if not profile.get("include_volunteer", True):
        result["volunteer"] = []
    else:
        for entry in result.get("volunteer", []):
            bullets = entry.get("bullets", [])
            if prefer:
                bullets = sorted(
                    bullets,
                    key=lambda b: _score_bullet(b, prefer, deprioritize),
                    reverse=True,
                )
            entry["bullets"] = bullets[:max_bullets]

    # Filter skill categories
    skill_categories = profile.get("skill_categories", [])
    if skill_categories:
        # Preserve the order defined in the profile
        ordered = {cat: None for cat in skill_categories}
        for s in result.get("skills", []):
            if s.get("category") in ordered:
                ordered[s["category"]] = s
        result["skills"] = [v for v in ordered.values() if v is not None]

    # Optionally clear coursework
    if not profile.get("include_coursework", False):
        result["coursework"] = []

    # Filter and sort project bullets
    project_bullets = profile.get("max_bullets_per_project", max_bullets)
    projects = result.get("projects", [])
    for project in projects:
        bullets = project.get("bullets", [])
        if prefer:
            bullets = sorted(
                bullets,
                key=lambda b: _score_bullet({"tags": project.get("tags", [])}, prefer, deprioritize),
                reverse=True,
            )
        project["bullets"] = bullets[:project_bullets]

    if prefer and projects:
        projects = sorted(
            projects,
            key=lambda p: _score_bullet({"tags": p.get("tags", [])}, prefer, deprioritize),
            reverse=True,
        )
    result["projects"] = projects

    return result


# ── Rendering ────────────────────────────────────────────────────────────────

def render_resume(data: dict, profile: dict, template_name: str = "resume.md.j2") -> str:
    """Render the resume to a Markdown string using Jinja2."""
    filtered = apply_profile(data, profile)
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["fmt_date"] = fmt_date
    template = env.get_template(template_name)
    return template.render(**filtered)


# ── Output helpers ────────────────────────────────────────────────────────────

def _sanitize(s: str) -> str:
    """Convert a string to a safe filename component."""
    return (
        s.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace(",", "")
        .replace(".", "")
    )


def get_output_stem(name: str, profile_key: str) -> str:
    return f"{_sanitize(name)}_resume_{_sanitize(profile_key)}"


# ── Pandoc helpers ────────────────────────────────────────────────────────────

def _run_pandoc(args: list) -> tuple:
    """Run pandoc with args. Returns (success: bool, error_message: str)."""
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


def to_docx(md_path: Path, docx_path: Path) -> bool:
    ok, err = _run_pandoc([
        str(md_path), "-f", "markdown", "-t", "docx",
        "--standalone", "-o", str(docx_path),
    ])
    if not ok:
        print(f"  [WARN] DOCX failed: {err}")
    return ok


def to_pdf(md_path: Path, pdf_path: Path) -> bool:
    """Try PDF engines in preference order. Return True if any succeeds."""
    engines = ["weasyprint", "wkhtmltopdf", "pdflatex", "xelatex", "lualatex"]
    for engine in engines:
        ok, _ = _run_pandoc([
            str(md_path), "-f", "markdown", "--standalone",
            f"--pdf-engine={engine}", "-o", str(pdf_path),
        ])
        if ok:
            return True
    print(
        "  [WARN] PDF generation skipped — no supported PDF engine found.\n"
        "         Install one of:\n"
        "           pip install weasyprint\n"
        "           brew install wkhtmltopdf\n"
        "           brew install --cask basictex   (pdflatex)\n"
        "         DOCX output is complete and usable."
    )
    return False


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Build resume from YAML source.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--profile", default=None,
        help="Role profile key (see data/role_profiles.yaml). Default: target_metadata.default_profile",
    )
    parser.add_argument(
        "--output", default=None,
        help="Output filename stem without extension (default: auto-generated from name + profile)",
    )
    parser.add_argument(
        "--data", default=None,
        help="Path to resume YAML (default: data/base_resume.yaml)",
    )
    parser.add_argument(
        "--list-profiles", action="store_true",
        help="Print available profiles and exit",
    )
    parser.add_argument(
        "--md-only", action="store_true",
        help="Render Markdown only; skip DOCX and PDF generation",
    )
    args = parser.parse_args()

    profiles = load_yaml(DATA_DIR / "role_profiles.yaml")

    if args.list_profiles:
        print("Available profiles:")
        for key, val in profiles.items():
            print(f"  {key:<22} {val.get('name', '')}")
        sys.exit(0)

    data_path = Path(args.data) if args.data else DATA_DIR / "base_resume.yaml"
    resume_data = load_yaml(data_path)

    try:
        validate_resume(resume_data)
    except ValueError as exc:
        print(f"[ERROR] Validation failed: {exc}")
        sys.exit(1)

    meta = resume_data.get("target_metadata", {})
    profile_key = args.profile or meta.get("default_profile", "default")

    if profile_key not in profiles:
        print(f"[ERROR] Profile '{profile_key}' not found. Run --list-profiles to see options.")
        sys.exit(1)

    profile = profiles[profile_key]
    name = resume_data["personal"]["name"]
    md_text = render_resume(resume_data, profile)

    OUTPUT_DIR.mkdir(exist_ok=True)
    stem = args.output or get_output_stem(name, profile_key)
    md_path = OUTPUT_DIR / f"{stem}.md"
    docx_path = OUTPUT_DIR / f"{stem}.docx"
    pdf_path = OUTPUT_DIR / f"{stem}.pdf"

    md_path.write_text(md_text, encoding="utf-8")
    print(f"[OK] Markdown  → {md_path.relative_to(ROOT)}")

    if not args.md_only:
        if to_docx(md_path, docx_path):
            print(f"[OK] DOCX      → {docx_path.relative_to(ROOT)}")
        if to_pdf(md_path, pdf_path):
            print(f"[OK] PDF       → {pdf_path.relative_to(ROOT)}")

    print(f"\nDone. Profile: {profile.get('name', profile_key)}")


if __name__ == "__main__":
    main()
