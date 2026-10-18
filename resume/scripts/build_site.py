#!/usr/bin/env python3
"""Build the public portfolio and matching PDF together, without cover letters.

python resume/scripts/build_site.py --profile neuroengineering
"""

import argparse
import shutil
from pathlib import Path

if __package__:
    from .build_resume import (
        DATA_DIR, ROOT, TEMPLATES_DIR, apply_profile, build_resume, load_yaml,
        template_environment,
    )
else:
    from build_resume import (
        DATA_DIR, ROOT, TEMPLATES_DIR, apply_profile, build_resume, load_yaml,
        template_environment,
    )

DOCS_DIR = ROOT / "docs"
CV_STEM = "marco_del_fava_cv"


def build_site(data: dict, profile: dict, docs_dir: Path = DOCS_DIR,
               source_commit: str = "") -> Path:
    # Publish only explicitly generated artifacts, never files selected by mtime.
    folder = build_resume(data, profile, CV_STEM)
    docs_dir.mkdir(parents=True, exist_ok=True)
    assets = docs_dir / "assets"
    assets.mkdir(exist_ok=True)
    for name in ("github.png", "linkedin.png"):
        shutil.copy2(TEMPLATES_DIR / "icons" / name, assets / name)
    shutil.copy2(folder / f"{CV_STEM}.pdf", docs_dir / f"{CV_STEM}.pdf")
    html = template_environment().get_template("resume.html.j2").render(
        resume=apply_profile(data, profile),
        pdf_url=f"{CV_STEM}.pdf", source_commit=source_commit,
    )
    (docs_dir / "index.html").write_text(html, encoding="utf-8")
    (docs_dir / ".nojekyll").touch()
    print(f"[OK] Portfolio and matching PDF: {docs_dir}")
    return docs_dir


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile")
    parser.add_argument("--data", type=Path, default=DATA_DIR / "base_resume.yaml")
    parser.add_argument("--output-dir", type=Path, default=DOCS_DIR)
    parser.add_argument("--source-commit", default="")
    args = parser.parse_args()
    data = load_yaml(args.data)
    profiles = load_yaml(DATA_DIR / "role_profiles.yaml")
    key = args.profile or data.get("target_metadata", {}).get("default_profile", "default")
    if key not in profiles:
        parser.error(f"Unknown profile: {key}")
    try:
        build_site(data, profiles[key], args.output_dir, args.source_commit)
    except (ValueError, RuntimeError, OSError) as error:
        parser.exit(1, f"[ERROR] Publication build failed: {error}\n")


if __name__ == "__main__":
    main()
