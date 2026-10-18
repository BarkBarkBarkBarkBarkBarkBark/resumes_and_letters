#!/usr/bin/env python3
"""Build a CV from canonical YAML. Run from the repository root.

python resume/scripts/build_resume.py --profile neuroengineering --output marco_del_fava_cv
"""

import argparse
import copy
import json
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlsplit

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATES_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output"
REQUIRED_TOP_LEVEL = ["personal", "summary", "skills", "experience", "education"]
_MONTH_ABBR = dict(zip(
    [f"{month:02d}" for month in range(1, 13)],
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
))


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as source:
        return yaml.safe_load(source)


def validate_resume(data: dict) -> None:
    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            raise ValueError(f"Missing required top-level field: '{field}'")
    if not data["personal"].get("name"):
        raise ValueError("personal.name is required")
    if not data["personal"].get("contact", {}).get("email"):
        raise ValueError("personal.contact.email is required")


def fmt_date(value) -> str:
    if value is None:
        return ""
    value = str(value).strip()
    if value.lower() == "present":
        return "Present"
    parts = value.split("-")
    if len(parts) == 2:
        year, month = parts
        return f"{_MONTH_ABBR.get(month.zfill(2), month)} {year}"
    return value


def https_url(value: str) -> str:
    value = value.strip()
    if urlsplit(value).scheme not in ("", "https"):
        raise ValueError(f"Expected an HTTPS evidence/profile URL, got: {value!r}")
    if not value.startswith(("http://", "https://")):
        value = "https://" + value
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or any(
        char.isspace() or char in '{}\\' for char in value
    ):
        raise ValueError(f"Expected an HTTPS evidence/profile URL, got: {value!r}")
    return value


def normalize_item(item) -> dict:
    """Accept legacy strings at the boundary; templates always receive text/evidence."""
    if isinstance(item, str):
        item = {"text": item}
    if not isinstance(item, dict) or not isinstance(item.get("text"), str) or not item["text"].strip():
        raise ValueError(f"Expected a nonempty text item, got: {item!r}")
    result = dict(item)
    result["text"] = result["text"].strip()
    if result.get("evidence"):
        result["evidence"] = https_url(result["evidence"])
    return result


def _score_bullet(bullet: dict, prefer: list, deprioritize: list) -> int:
    tags = bullet.get("tags", [])
    return sum(tag in prefer for tag in tags) - sum(tag in deprioritize for tag in tags)


def public_evidence(projects: list) -> dict:
    inventory = load_yaml(DATA_DIR / "evidence_inventory.yaml")["records"]
    selected = {}
    for project in projects:
        for key in project.get("evidence_ids", []):
            if key not in inventory or inventory[key].get("public") is not True:
                raise ValueError(f"Project {project['id']} references unpublished evidence: {key}")
            record = copy.deepcopy(inventory[key])
            revision = record.get("revision")
            if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
                raise ValueError(f"Public evidence requires a full commit SHA: {key}")
            if not record.get("sources"):
                raise ValueError(f"Public evidence requires exact sources: {key}")
            if record.get("maturity") not in ("Implemented", "Validated", "Prototype"):
                raise ValueError(f"Public evidence has an invalid maturity: {key}")
            for field in (
                "measurement_definition", "test_conditions", "verified_result",
                "limitations", "verification",
            ):
                if not record.get(field):
                    raise ValueError(f"Evidence {key} is missing {field}")
            for source in record["sources"]:
                source["url"] = https_url(
                    f"https://github.com/{record['repository']}/"
                    f"{source.get('kind', 'blob')}/{record['revision']}/{source['path']}"
                )
            visual = record.get("visual", {})
            if visual.get("kind") == "bars":
                maximum = visual["maximum"]
                if maximum <= 0 or any(
                    not 0 <= bar["value"] <= maximum for bar in visual["bars"]
                ):
                    raise ValueError(f"Evidence chart values are out of range: {key}")
            selected[key] = record
    return selected


def apply_profile(data: dict, profile: dict) -> dict:
    result = copy.deepcopy(data)
    prefer = profile.get("prefer_tags", [])
    deprioritize = profile.get("deprioritize_tags", [])
    max_bullets = profile.get("max_bullets_per_role", 99)

    def bullets(items: list, limit: int, priorities: Optional[list] = None) -> list:
        normalized = [normalize_item(item) for item in items]
        priorities = prefer if priorities is None else priorities
        if priorities:
            normalized.sort(key=lambda item: _score_bullet(item, priorities, deprioritize), reverse=True)
        return normalized[:limit]

    summaries = result.get("summary", {})
    result["summary_text"] = (
        summaries.get(profile.get("summary_key", "default")) or summaries.get("default", "")
        if isinstance(summaries, dict) else str(summaries)
    )
    contact = result["personal"]["contact"]
    for key in ("github", "linkedin"):
        if contact.get(key):
            contact[key] = https_url(contact[key])

    for job in result.get("experience", []):
        job["bullets"] = bullets(
            job.get("bullets", []), profile.get("max_bullets_per_additional_role", max_bullets),
            profile.get("additional_prefer_tags", prefer),
        )
    volunteers = result.get("volunteer", []) if profile.get("include_volunteer", True) else []
    for entry in volunteers:
        limit = profile.get(
            "max_bullets_per_research_role" if entry.get("section") == "research"
            else "max_bullets_per_additional_role", max_bullets
        )
        entry["bullets"] = bullets(entry.get("bullets", []), limit)
    result["research"] = [entry for entry in volunteers if entry.get("section") == "research"]
    result["volunteer"] = [
        entry for entry in volunteers
        if entry.get("section") != "research" and profile.get("include_supporting_volunteer", True)
    ]

    for group in result.get("skills", []):
        group["items"] = [normalize_item(item) for item in group["items"]]
    categories = profile.get("skill_categories", [])
    if categories:
        groups = {group["category"]: group for group in result["skills"]}
        result["skills"] = [groups[category] for category in categories if category in groups]
    for group in result.get("skills", []):
        group["items"] = group["items"][:profile.get("max_skills_per_category", 99)]
    if not profile.get("include_coursework", False):
        result["coursework"] = []
    if not profile.get("include_certifications", True):
        result["certifications"] = []

    for project in result.get("projects", []):
        project["bullets"] = bullets(
            project.get("bullets", []), profile.get("max_bullets_per_project", max_bullets)
        )
        for link in project.get("links", []):
            link["url"] = https_url(link["url"])
    order = profile.get("project_order", [])
    if order:
        projects = {project["id"]: project for project in result.get("projects", [])}
        result["projects"] = [projects[key] for key in order]
    result["compact"] = profile.get("compact", False)
    result["engineering_focus"] = profile.get("engineering_focus", False)
    result["evidence_records"] = public_evidence(result.get("projects", []))
    result["page_break_before_education"] = profile.get("page_break_before_education", False)
    result["page_break_before_project"] = profile.get("page_break_before_project")
    return result


def latex_escape(value: str) -> str:
    substitutions = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
        "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(substitutions.get(char, char) for char in value)


def template_environment() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        trim_blocks=True, lstrip_blocks=True,
        autoescape=select_autoescape(enabled_extensions=("html.j2",)),
    )
    env.filters["fmt_date"] = fmt_date
    env.filters["latex_escape"] = latex_escape
    return env


def render_resume(data: dict, profile: dict, template_name: str = "resume.md.j2",
                  output_format: str = "markdown") -> str:
    return template_environment().get_template(template_name).render(
        resume=apply_profile(data, profile), output_format=output_format
    )


def _sanitize(value: str) -> str:
    return value.lower().replace(" ", "_").replace("-", "_").replace("/", "_").replace(",", "").replace(".", "")


def get_output_stem(name: str, profile_key: str, doc_type: str = "cv") -> str:
    now = datetime.now()
    return f"{_sanitize(profile_key)}_{_sanitize(doc_type)}_{now.month}-{now.day}-{now:%y-%H%M}"


def _run_pandoc(args: list) -> tuple:
    try:
        proc = subprocess.run(["pandoc"] + args, capture_output=True, text=True, timeout=120)
    except FileNotFoundError:
        return False, "pandoc not found. Install Pandoc before building."
    except subprocess.TimeoutExpired:
        return False, "pandoc timed out."
    return proc.returncode == 0, proc.stderr.strip()


def to_docx(md_path: Path, docx_path: Path) -> bool:
    ok, error = _run_pandoc([str(md_path), "--standalone", "-o", str(docx_path)])
    if not ok:
        print(f"[ERROR] DOCX generation failed: {error}")
    return ok


def to_tex(md_path: Path, tex_path: Path, template_path: Path) -> bool:
    ok, error = _run_pandoc([
        str(md_path), "--standalone", "-t", "latex", "--shift-heading-level-by=-1",
        "--template", str(template_path),
        "-o", str(tex_path),
    ])
    if not ok:
        print(f"[ERROR] TEX generation failed: {error}")
    return ok


def _tex_executable(name: str) -> str:
    executable = shutil.which(name)
    if executable:
        return executable
    candidate = Path("/Library/TeX/texbin") / name
    if candidate.is_file():
        return str(candidate)
    raise FileNotFoundError(f"{name} not found. Install TeX Live/MacTeX with LuaLaTeX and latexmk.")


def to_pdf(md_path: Path, pdf_path: Path, tex_path: Optional[Path] = None,
           template_path: Optional[Path] = None) -> bool:
    tex_path = tex_path or pdf_path.with_suffix(".tex")
    template_path = template_path or TEMPLATES_DIR / "resume.tex"
    if not to_tex(md_path, tex_path, template_path):
        return False
    try:
        latexmk = _tex_executable("latexmk")
        lualatex = _tex_executable("lualatex")
        proc = subprocess.run(
            [latexmk, "-g", "-pdf", f"-pdflatex={lualatex} -interaction=nonstopmode -halt-on-error %O %S",
             tex_path.name],
            cwd=tex_path.parent, capture_output=True, text=True, timeout=300,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        print(f"[ERROR] PDF build failed: {error}")
        return False
    if proc.returncode != 0:
        print(f"[ERROR] LuaLaTeX compilation failed:\n{proc.stdout[-2500:]}\n{proc.stderr[-1000:]}")
        return False
    produced = tex_path.with_suffix(".pdf")
    if not produced.is_file():
        print("[ERROR] LuaLaTeX did not produce a PDF.")
        return False
    if produced != pdf_path:
        produced.replace(pdf_path)
    return True


def build_resume(data: dict, profile: dict, stem: str, output_dir: Path = OUTPUT_DIR,
                 md_only: bool = False) -> Path:
    validate_resume(data)
    filtered = apply_profile(data, profile)
    folder = output_dir / stem
    folder.mkdir(parents=True, exist_ok=True)
    metadata = yaml.safe_dump({
        "title": data["personal"]["name"], "author": data["personal"]["name"], "lang": "en",
    }, sort_keys=False, allow_unicode=True)
    frontmatter = f"---\n{metadata}---\n\n"
    md_path = folder / f"{stem}.md"
    md_path.write_text(frontmatter + render_resume(data, profile), encoding="utf-8")
    (folder / f"{stem}.json").write_text(
        json.dumps(filtered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if not md_only:
        icons = folder / "icons"
        icons.mkdir(exist_ok=True)
        for name in ("github.png", "linkedin.png"):
            shutil.copy2(TEMPLATES_DIR / "icons" / name, icons / name)
        if not to_docx(md_path, folder / f"{stem}.docx"):
            raise RuntimeError("DOCX build failed.")
        pdf_source = folder / f"{stem}.pdf.md"
        pdf_source.write_text(
            frontmatter + render_resume(data, profile, output_format="latex"), encoding="utf-8"
        )
        try:
            if not to_pdf(pdf_source, folder / f"{stem}.pdf"):
                raise RuntimeError("PDF build failed; no publishable CV was produced.")
        finally:
            pdf_source.unlink()
    print(f"[OK] CV artifacts: {folder}")
    return folder


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile")
    parser.add_argument("--data", type=Path, default=DATA_DIR / "base_resume.yaml")
    parser.add_argument("--output", help="Exact output stem; no timestamp is appended.")
    parser.add_argument("--doc-type", default="cv")
    parser.add_argument("--md-only", action="store_true")
    parser.add_argument("--list-profiles", action="store_true")
    args = parser.parse_args()
    profiles = load_yaml(DATA_DIR / "role_profiles.yaml")
    if args.list_profiles:
        for key, profile in profiles.items():
            print(f"{key}: {profile['name']}")
        return
    data = load_yaml(args.data)
    key = args.profile or data.get("target_metadata", {}).get("default_profile", "default")
    if key not in profiles:
        parser.error(f"Unknown profile: {key}. Available: {', '.join(profiles)}")
    stem = _sanitize(args.output) if args.output else get_output_stem(data["personal"]["name"], key, args.doc_type)
    if not stem:
        parser.error("--output must contain a filename stem.")
    try:
        build_resume(data, profiles[key], stem, md_only=args.md_only)
    except (ValueError, RuntimeError) as error:
        parser.exit(1, f"[ERROR] {error}\n")


if __name__ == "__main__":
    main()
