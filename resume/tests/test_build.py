"""
test_build.py — Tests for the resume build pipeline.

Covers:
  - YAML loading
  - Required field validation
  - Markdown rendering (presence of key content)
  - Profile filtering behavior
  - Output filename sanitization
  - Output file creation
"""

from pathlib import Path

import pytest

from scripts.build_resume import (
    apply_profile,
    fmt_date,
    get_output_stem,
    load_yaml,
    render_resume,
    validate_resume,
)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def resume_data():
    return load_yaml(DATA_DIR / "base_resume.yaml")


@pytest.fixture
def profiles():
    return load_yaml(DATA_DIR / "role_profiles.yaml")


# ── YAML loading ──────────────────────────────────────────────────────────────

def test_yaml_loads(resume_data):
    assert isinstance(resume_data, dict)
    assert "personal" in resume_data


def test_profiles_yaml_loads(profiles):
    assert isinstance(profiles, dict)
    assert "neuroengineering" in profiles
    assert "data_analytics" in profiles


def test_canonical_skills_have_migrated_to_text_mappings(resume_data):
    for group in resume_data["skills"]:
        assert all(isinstance(item, dict) and item.get("text") for item in group["items"])


def test_snippets_yaml_loads():
    snippets = load_yaml(DATA_DIR / "cover_letter_snippets.yaml")
    assert isinstance(snippets, dict)
    assert "opener" in snippets


# ── Validation ────────────────────────────────────────────────────────────────

def test_valid_resume_passes(resume_data):
    validate_resume(resume_data)  # must not raise


def test_missing_name_raises():
    data = {
        "personal": {"contact": {"email": "test@test.com"}},
        "summary": {},
        "skills": [],
        "experience": [],
        "education": [],
    }
    with pytest.raises(ValueError, match="name"):
        validate_resume(data)


def test_missing_email_raises():
    data = {
        "personal": {"name": "Test User", "contact": {}},
        "summary": {},
        "skills": [],
        "experience": [],
        "education": [],
    }
    with pytest.raises(ValueError, match="email"):
        validate_resume(data)


def test_missing_top_level_field_raises():
    data = {"personal": {"name": "Test", "contact": {"email": "t@t.com"}}}
    with pytest.raises(ValueError, match="Missing required"):
        validate_resume(data)


# ── Date formatting ───────────────────────────────────────────────────────────

def test_fmt_date_year_month():
    assert fmt_date("2021-07") == "Jul 2021"


def test_fmt_date_year_only():
    assert fmt_date("2023") == "2023"


def test_fmt_date_present():
    assert fmt_date("present") == "Present"
    assert fmt_date("Present") == "Present"


def test_fmt_date_none():
    assert fmt_date(None) == ""


# ── Output naming ─────────────────────────────────────────────────────────────

def test_output_stem_sanitized():
    stem = get_output_stem("Marco Del Fava", "neuroengineering", "cv")
    assert " " not in stem
    assert stem.startswith("neuroengineering_cv_")


def test_output_stem_handles_spaces():
    stem = get_output_stem("Marco Del Fava", "data analytics", "resume")
    assert "data_analytics" in stem


# ── Rendering ────────────────────────────────────────────────────────────────

def test_render_contains_name(resume_data, profiles):
    md = render_resume(resume_data, profiles["neuroengineering"])
    assert "Marco Del Fava" in md


def test_render_contains_standard_sections(resume_data, profiles):
    md = render_resume(resume_data, profiles["neuroengineering"])
    assert "## Research Profile" in md
    assert "## Research Experience" in md
    assert "## Education" in md
    assert "## Technical Skills" in md


def test_render_contains_contact_info(resume_data, profiles):
    md = render_resume(resume_data, profiles["neuroengineering"])
    assert "mdelfava@ucdavis.edu" in md
    assert "Sacramento" in md


def test_neuroengineering_includes_zlab(resume_data, profiles):
    md = render_resume(resume_data, profiles["neuroengineering"])
    assert "Z-Lab" in md


def test_neuroengineering_includes_spike_sorting(resume_data, profiles):
    md = render_resume(resume_data, profiles["neuroengineering"])
    assert "spike sorting" in md.lower() or "kilosort" in md.lower()


def test_data_analytics_excludes_volunteer(resume_data, profiles):
    md = render_resume(resume_data, profiles["data_analytics"])
    assert "Z-Lab" not in md


def test_data_analytics_summary_variant(resume_data, profiles):
    md = render_resume(resume_data, profiles["data_analytics"])
    assert "shelter" in md.lower() or "400+" in md


def test_bullet_count_capped(resume_data, profiles):
    """Neuroengineering profile caps bullets at max_bullets_per_role."""
    filtered = apply_profile(resume_data, profiles["neuroengineering"])
    max_bullets = profiles["neuroengineering"]["max_bullets_per_role"]
    for job in filtered["experience"]:
        assert len(job["bullets"]) <= max_bullets


def test_skill_categories_ordered(resume_data, profiles):
    """Skill categories in output should follow profile's defined order."""
    profile = profiles["neuroengineering"]
    filtered = apply_profile(resume_data, profile)
    rendered_cats = [s["category"] for s in filtered["skills"]]
    expected = [c for c in profile["skill_categories"] if c in rendered_cats]
    assert rendered_cats == expected


# ── Output file creation ──────────────────────────────────────────────────────

def test_output_markdown_file_created(resume_data, profiles, tmp_path):
    md = render_resume(resume_data, profiles["neuroengineering"])
    out = tmp_path / "test_resume.md"
    out.write_text(md, encoding="utf-8")
    assert out.exists()
    assert out.stat().st_size > 200


def test_output_markdown_readable(resume_data, profiles, tmp_path):
    md = render_resume(resume_data, profiles["neuroengineering"])
    out = tmp_path / "test_resume.md"
    out.write_text(md, encoding="utf-8")
    contents = out.read_text(encoding="utf-8")
    assert "Marco Del Fava" in contents
    assert "## Additional Professional Experience" in contents


def test_section_order_and_research_not_duplicated(resume_data, profiles):
    md = render_resume(resume_data, profiles["neuroengineering"])
    headings = [
        "# Marco Del Fava", "## Research Profile", "## Research Experience",
        "## Selected Projects", "## Education", "## Technical Skills",
        "## Additional Professional Experience", "## Certifications",
    ]
    positions = [md.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert md.count("Z-Lab") == 1
    assert "IT Administrator**, First Step Communities" in md
    assert "IT Administrator for First Step" not in md


@pytest.mark.parametrize("profile_key", [
    "neuroengineering", "data_analytics", "clinical_research", "default",
])
def test_all_profiles_render_normalized_content(resume_data, profiles, profile_key):
    md = render_resume(resume_data, profiles[profile_key])
    assert "{'text':" not in md
    assert "'evidence':" not in md
    assert "\\HeaderTwoColumn" not in md
    assert "https://https://" not in md
    assert "ucd_python_badge" not in md


def test_legacy_skill_and_project_items_normalized(resume_data, profiles):
    resume_data["skills"][0]["items"] = [
        "Legacy skill", {"text": "Current skill"}, {
            "text": "Evidenced skill", "evidence": "github.com/owner/repo",
        },
    ]
    resume_data["projects"][0]["bullets"] = ["Legacy contribution"]
    filtered = apply_profile(resume_data, profiles["neuroengineering"])
    assert filtered["skills"][0]["items"][0] == {"text": "Legacy skill"}
    assert filtered["skills"][0]["items"][2]["evidence"] == "https://github.com/owner/repo"
    md = render_resume(resume_data, profiles["neuroengineering"])
    assert "Legacy skill" in md and "Current skill" in md and "Legacy contribution" in md
    assert "{'text':" not in md


def test_profile_does_not_mutate_canonical_data(resume_data, profiles):
    import copy
    original = copy.deepcopy(resume_data)
    apply_profile(resume_data, profiles["neuroengineering"])
    assert resume_data == original


@pytest.mark.parametrize("item", [
    {"text": ""}, {"evidence": "https://github.com/owner/repo"}, 12,
    {"text": "Bad URL", "evidence": "javascript:alert(1)"},
    {"text": "Bad URL", "evidence": "http://github.com/owner/repo"},
])
def test_invalid_skill_items_raise(resume_data, profiles, item):
    resume_data["skills"][0]["items"] = [item]
    with pytest.raises(ValueError):
        apply_profile(resume_data, profiles["neuroengineering"])


def test_confirmed_dates_and_defensible_claims(resume_data, profiles):
    filtered = apply_profile(resume_data, profiles["neuroengineering"])
    assert filtered["education"][0]["graduation_date"] == "Fall 2026 - Present"
    assert filtered["research"][0]["start_date"] == "2025-07"
    md = render_resume(resume_data, profiles["neuroengineering"])
    for unsupported in [
        "recently admitted", "incoming", "I look forward", "BCI-adjacent",
        "2 million", "improving manual curation", "sub-millisecond",
    ]:
        assert unsupported.lower() not in md.lower()
    assert "putative O-Sort unit labels" in md
    assert "hardware bench validation remains pending" in md
    assert "not demonstrated human concept selectivity or causality" in md


def test_projects_have_problem_two_bullets_status_and_sources(resume_data, profiles):
    filtered = apply_profile(resume_data, profiles["neuroengineering"])
    assert [project["id"] for project in filtered["projects"]] == [
        "intan", "sorting", "semantic", "neuralynx",
    ]
    for project in filtered["projects"]:
        assert project["problem"] and project["status"] and project["links"]
        assert len(project["bullets"]) == 2


def test_latex_preserves_header_typography_and_evidence(resume_data, profiles):
    md = render_resume(resume_data, profiles["neuroengineering"], output_format="latex")
    assert r"\ResumeName{Marco Del Fava}" in md
    assert r"\HeaderProfileLink{linkedin.png}{https://www.linkedin.com/in/marc-del-fava}" in md
    assert r"\EvidenceLink{https://github.com/" in md
    assert md.count(r"\newpage") == 1
    assert r"\newpage" not in render_resume(resume_data, profiles["neuroengineering"])
    tex = (ROOT / "templates/resume.tex").read_text()
    assert r"\fontsize{11pt}{13pt}" in tex
    assert "margin=0.7in" in tex and r"\usepackage{microtype}" in tex


def test_explicit_output_name_stable_and_failure_not_success(resume_data, profiles, tmp_path, monkeypatch):
    from scripts import build_resume as builder
    monkeypatch.setattr(builder, "to_docx", lambda *args: True)
    monkeypatch.setattr(builder, "to_pdf", lambda *args: False)
    with pytest.raises(RuntimeError, match="PDF build failed"):
        builder.build_resume(
            resume_data, profiles["neuroengineering"], "fixed_cv", tmp_path,
        )
    assert (tmp_path / "fixed_cv/fixed_cv.md").is_file()
    assert not (tmp_path / "fixed_cv/fixed_cv.pdf.md").exists()
