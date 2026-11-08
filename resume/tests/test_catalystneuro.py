"""Verify role-specific content and the visible Credly badge in PDF source."""

from pathlib import Path

from scripts.build_resume import apply_profile, latex_escape, load_yaml, render_resume

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CREDLY = "https://www.credly.com/badges/505ef11c-58b4-48bd-aa9e-5a21f0247d46/public_url"


def test_catalystneuro_cv_keeps_general_cv_unchanged():
    data = load_yaml(DATA / "base_resume.yaml")
    profiles = load_yaml(DATA / "role_profiles.yaml")
    tailored = apply_profile(data, profiles["catalystneuro"])
    general = apply_profile(data, profiles["neuroengineering"])
    assert tailored["personal"]["headline"] == "Research Software Engineering | Neuroscience Data Pipelines"
    assert general["personal"]["headline"] == "Research Software & Neural Data"
    assert [p["id"] for p in tailored["projects"]] == ["intan", "compression", "saw", "sorting"]
    assert [p["id"] for p in general["projects"]] == ["compression", "intan", "sorting", "hosaka"]
    assert [group["category"] for group in tailored["skills"]] == profiles["catalystneuro"]["skill_categories"]
    assert "saw-agent-workflow" in tailored["evidence_records"]
    assert len(tailored["certifications"]) == 1
    assert tailored["certifications"][0]["credly_url"] == CREDLY
    assert len(general["certifications"]) == 2
    md = render_resume(data, profiles["catalystneuro"])
    for name in ("Scientific AI Workstation", "PsychoPy", "RHX", "20 million samples",
                 "Data Analysis with Matplotlib", "Z-Lab"):
        assert name in md
    assert "NWB" not in md and "DANDI" not in md


def test_badge_is_embedded_as_clickable_image_in_both_research_cvs():
    data = load_yaml(DATA / "base_resume.yaml")
    profiles = load_yaml(DATA / "role_profiles.yaml")
    icon = ROOT / "templates/icons/ucd_python_badge.png"
    assert icon.is_file() and icon.stat().st_size > 10000
    for name in ("catalystneuro", "neuroengineering"):
        latex = render_resume(data, profiles[name], output_format="latex")
        assert r"\BeginResumeHeader{" + latex_escape(CREDLY) + r"}{ucd_python_badge.png}" in latex
        assert r"\CredentialBadge" not in latex
        assert "UC Davis Continuing and Professional Education" in latex
    assert r"\newcommand{\BeginResumeHeader}" in (ROOT / "templates/resume.tex").read_text()
