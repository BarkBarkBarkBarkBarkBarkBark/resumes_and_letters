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
    stem = get_output_stem("Marco Del Fava", "neuroengineering")
    assert " " not in stem
    assert stem == "marco_del_fava_resume_neuroengineering"


def test_output_stem_handles_spaces():
    stem = get_output_stem("Marco Del Fava", "data analytics")
    assert "data_analytics" in stem


# ── Rendering ────────────────────────────────────────────────────────────────

def test_render_contains_name(resume_data, profiles):
    md = render_resume(resume_data, profiles["neuroengineering"])
    assert "Marco Del Fava" in md


def test_render_contains_standard_sections(resume_data, profiles):
    md = render_resume(resume_data, profiles["neuroengineering"])
    assert "## Summary" in md
    assert "## Experience" in md
    assert "## Education" in md
    assert "## Skills" in md


def test_render_contains_contact_info(resume_data, profiles):
    md = render_resume(resume_data, profiles["neuroengineering"])
    assert "marc.delfava@gmail.com" in md
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
    assert "## Experience" in contents
