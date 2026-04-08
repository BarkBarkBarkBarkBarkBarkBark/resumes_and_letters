#!/usr/bin/env python3
"""
build_site.py — Generate docs/index.html for GitHub Pages from base_resume.yaml.

The output is a self-contained HTML file with inline CSS.
Commit docs/ to your repo, then enable GitHub Pages in Settings → Pages
with source set to "GitHub Actions" (uses .github/workflows/deploy.yml).

Usage:
    python scripts/build_site.py
    python scripts/build_site.py --profile neuroengineering
    python scripts/build_site.py --profile data_analytics
"""

import argparse
import sys
from datetime import date
from pathlib import Path

# Allow importing sibling scripts
sys.path.insert(0, str(Path(__file__).parent))

from build_resume import (  # noqa: E402
    DATA_DIR,
    TEMPLATES_DIR,
    apply_profile,
    fmt_date,
    load_yaml,
    validate_resume,
)
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"


def main():
    parser = argparse.ArgumentParser(
        description="Build docs/index.html for GitHub Pages.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--profile", default=None,
        help="Role profile key (default: target_metadata.default_profile)",
    )
    parser.add_argument(
        "--data", default=None,
        help="Path to resume YAML (default: data/base_resume.yaml)",
    )
    args = parser.parse_args()

    data_path = Path(args.data) if args.data else DATA_DIR / "base_resume.yaml"
    resume_data = load_yaml(data_path)

    try:
        validate_resume(resume_data)
    except ValueError as exc:
        print(f"[ERROR] Validation failed: {exc}")
        sys.exit(1)

    profiles = load_yaml(DATA_DIR / "role_profiles.yaml")
    meta = resume_data.get("target_metadata", {})
    profile_key = args.profile or meta.get("default_profile", "default")

    if profile_key not in profiles:
        print(f"[ERROR] Profile '{profile_key}' not found. Available: {', '.join(profiles)}")
        sys.exit(1)

    profile = profiles[profile_key]
    filtered = apply_profile(resume_data, profile)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["fmt_date"] = fmt_date
    template = env.get_template("resume.html.j2")

    html = template.render(
        **filtered,
        build_date=date.today().strftime("%B %-d, %Y"),
    )

    DOCS_DIR.mkdir(exist_ok=True)

    index = DOCS_DIR / "index.html"
    index.write_text(html, encoding="utf-8")

    nojekyll = DOCS_DIR / ".nojekyll"
    if not nojekyll.exists():
        nojekyll.write_text("", encoding="utf-8")

    print(f"[OK] Site      → docs/index.html")
    print(f"     Profile:    {profile.get('name', profile_key)}")
    print(f"     Size:       {index.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
