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
        "# Marco Del Fava", "## Research Profile", "## Technical Skills",
        "## Research Experience", "## Selected Engineering Projects",
        "## Additional Professional Experience", "## Education",
        "## Professional Development & Certifications",
    ]
    positions = [md.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert md.count("Z-Lab") == 1
    assert "IT Administrator**, First Step Communities" in md
    assert "IT Administrator for First Step" not in md


@pytest.mark.parametrize("profile_key", [
    "neuroengineering", "engineering", "data_analytics", "clinical_research", "default",
])
def test_all_profiles_render_normalized_content(resume_data, profiles, profile_key):
    md = render_resume(resume_data, profiles[profile_key])
    assert "{'text':" not in md
    assert "'evidence':" not in md
    assert "\\HeaderTwoColumn" not in md
    assert "https://https://" not in md
    assert "ucd_python_badge" not in md


def test_legacy_skill_and_project_items_normalized(resume_data, profiles):
    profile = dict(profiles["neuroengineering"], max_skills_per_category=3)
    resume_data["skills"][0]["items"] = [
        "Legacy skill", {"text": "Current skill"}, {
            "text": "Evidenced skill", "evidence": "github.com/owner/repo",
        },
    ]
    resume_data["projects"][0]["bullets"] = ["Legacy contribution"]
    filtered = apply_profile(resume_data, profile)
    group = next(group for group in filtered["skills"] if group["category"] == resume_data["skills"][0]["category"])
    assert group["items"][0] == {"text": "Legacy skill"}
    assert group["items"][2]["evidence"] == "https://github.com/owner/repo"
    md = render_resume(resume_data, profile)
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
    assert filtered["education"][0]["graduation_date"] == "2026–Present"
    assert filtered["research"][0]["start_date"] == "2025-07"
    md = render_resume(resume_data, profiles["neuroengineering"])
    for unsupported in [
        "recently admitted", "incoming", "I look forward", "BCI-adjacent",
        "2 million", "improving manual curation", "sub-millisecond",
    ]:
        assert unsupported.lower() not in md.lower()
    assert "putative O-Sort unit labels" in md
    assert "affine clock fitting" in md
    assert "Neo-backed MED reader" in md
    assert "content-based caching" in md
    for redundant in ("not independently verified", "not validated", "Work in progress"):
        assert redundant not in md
    for withheld in ("121", "19,991.371", "19,997.824", "22.29 ms", "76.42 ms"):
        assert withheld not in md


def test_projects_have_concise_contributions_and_sources(resume_data, profiles):
    filtered = apply_profile(resume_data, profiles["neuroengineering"])
    assert [project["id"] for project in filtered["projects"]] == [
        "compression", "intan", "sorting", "hosaka",
    ]
    for project in filtered["projects"]:
        assert project["problem"] and project["tools"]
        expected_links = {"compression": 2, "intan": 1, "sorting": 1, "hosaka": 0}
        assert len(project["links"]) == expected_links[project["id"]]
        assert "status" not in project and "maturity" not in project
        assert project["evidence_ids"]
        assert len(project["bullets"]) == (3 if project["id"] == "compression" else 2)


def test_latex_preserves_header_typography_and_evidence(resume_data, profiles):
    md = render_resume(resume_data, profiles["neuroengineering"], output_format="latex")
    assert r"\ResumeName{Marco Del Fava}" in md
    assert r"\ProfileLink{github.png}{https://github.com/" in md
    assert r"\ProfileLink{linkedin.png}{https://www.linkedin.com/in/marc-del-fava}{LinkedIn}" in md
    assert r"\EvidenceLink" not in md and r"\HeaderProfileLink" not in md
    projects = md.split("## Selected Engineering Projects")[1]
    assert r"\ProfileLink" not in projects
    for label in ("Reader code", "Validation notebook", "Processing notebook", "Technical report"):
        assert label not in md
    assert "}{Source}" not in md and "[Source](" not in md
    assert "(continued)" not in md
    assert r"\newpage" in md
    assert r"\newpage" not in render_resume(resume_data, profiles["neuroengineering"])
    tex = (ROOT / "templates/resume.tex").read_text()
    assert r"\fontsize{11pt}{13pt}" in tex
    assert "margin=0.7in" in tex and r"\usepackage{microtype}" in tex


@pytest.mark.parametrize("profile_key", ["neuroengineering", "engineering"])
def test_hosaka_accomplishment_remains_without_a_source_link(resume_data, profiles, profile_key):
    md = render_resume(resume_data, profiles[profile_key], output_format="latex")
    hosaka = md.split("### Debugging Agent-Generated Software")[1].split("## Additional Professional Experience")[0]
    assert "seven records take approximately ten seconds" in hosaka
    assert "content-based caching" in hosaka
    assert r"\ProfileLink" not in hosaka
    assert "hosaka-debugging" not in md
    filtered = apply_profile(resume_data, profiles[profile_key])
    assert filtered["evidence_records"]["hosaka-debugging"]["source_type"] == "owner-report"


def test_profile_urls_are_escaped_only_in_latex(resume_data, profiles):
    url = "https://github.com/owner_name?view=1&mode=raw#profile"
    resume_data["personal"]["contact"]["github"] = url
    latex = render_resume(resume_data, profiles["neuroengineering"], output_format="latex")
    assert r"owner\_name?view=1\&mode=raw\#profile}{GitHub}" in latex
    markdown = render_resume(resume_data, profiles["neuroengineering"])
    assert f"[GitHub]({url})" in markdown


@pytest.mark.parametrize("profile_key", ["neuroengineering", "engineering", "catalystneuro"])
def test_documents_keep_project_text_without_project_links(resume_data, profiles, profile_key):
    filtered = apply_profile(resume_data, profiles[profile_key])
    for output_format in ("markdown", "latex"):
        text = render_resume(resume_data, profiles[profile_key], output_format=output_format)
        for project in filtered["projects"]:
            assert project["name"] in text
            for bullet in project["bullets"]:
                assert bullet["text"] in text
            for link in project["links"]:
                assert link["url"] not in text
                assert link["label"] not in text


def test_graduate_student_title_is_scoped_to_zlab(resume_data, profiles):
    research = apply_profile(resume_data, profiles["neuroengineering"])["research"]
    assert research[0]["role"] == "Graduate Student"
    assert research[0]["start_date"] == "2025-07"
    e5 = next(role for role in resume_data["volunteer"] if "Neuroscience Unit E5" in role["organization"])
    assert e5["role"] == "Research Volunteer"


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


def test_engineering_profile_is_compact_without_changing_claims(resume_data, profiles):
    compact = apply_profile(resume_data, profiles["engineering"])
    full = apply_profile(resume_data, profiles["neuroengineering"])
    assert compact["compact"] and not full["compact"]
    assert len(compact["summary_text"].split()) < len(full["summary_text"].split())
    assert [project["id"] for project in compact["projects"]] == ["compression", "intan", "hosaka"]
    assert len(full["research"][0]["bullets"]) == 3
    assert len(compact["research"][0]["bullets"]) == 1
    full_projects = {project["id"]: project for project in full["projects"]}
    for project in compact["projects"]:
        assert all(bullet in full_projects[project["id"]]["bullets"] for bullet in project["bullets"])
    assert len(compact["projects"][0]["bullets"]) == 2
    assert "0.5 µV" in compact["projects"][0]["bullets"][1]["text"]
    assert compact["certifications"] == []
    assert len(compact["research"]) == 1
    assert all(len(group["items"]) == 1 for group in compact["skills"])
    md = render_resume(resume_data, profiles["engineering"])
    headings = [
        "# Marco Del Fava", "## Engineering Summary", "## Technical Skills",
        "## Research Experience", "## Selected Engineering Projects",
        "## Additional Professional Experience", "## Education",
    ]
    positions = [md.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert "Research Software & Neural Data" in md
    assert "2026–Present" in md
    assert "## Professional Development & Certifications" not in md


def test_engineering_metrics_match_inventory(resume_data, profiles):
    inventory = load_yaml(DATA_DIR / "evidence_inventory.yaml")["records"]
    fidelity = inventory["dhn-fidelity"]["values"]
    control = inventory["dhn-spike-control"]["values"]
    features = inventory["waveform-features"]["values"]
    assert fidelity["frames"] / fidelity["sample_rate_hz"] == fidelity["duration_seconds"] == 625
    assert fidelity["frames"] - fidelity["nonzero_before_rounding"] == 48011
    assert fidelity["frames"] - fidelity["nonzero_after_rounding"] == fidelity["frames"]
    assert fidelity["max_abs_error_after_rounding_uv"] == 0
    union = control["csc_spikes"] + control["med_spikes"] - control["exact_matches"]
    assert control["exact_matches"] / union == control["exact_jaccard"] == 1.0
    assert control["exact_matches"] == 35587
    assert fidelity["max_abs_error_uv"] == 0.5
    assert fidelity["nonzero_before_rounding"] == 19951989
    assert features["spike_snippets"] == 38145 and features["putative_units"] == 10
    assert features["ari"] == 0.3665
    assert features["families"][0] == {
        "name": "event", "knn_purity": features["knn_purity"],
        "matched_accuracy": features["matched_accuracy"], "ari": features["ari"],
    }
    assert [(row["name"], row["knn_purity"], row["matched_accuracy"], row["ari"])
            for row in features["families"][1:]] == [
        ("scalar", 0.9123, 0.5406, 0.3974),
        ("full", 0.9572, 0.5365, 0.4046),
        ("temporal_mad", 0.8367, 0.4301, 0.3125),
    ]
    for key in ("engineering", "neuroengineering"):
        md = render_resume(resume_data, profiles[key])
        for metric in ("20 million", "one channel", "32 kHz", "625 s", "0.5 µV"):
            assert metric in md
        assert "whole-microvolt source rounding" in md
        assert "95.04%" not in md and "54.26%" not in md
        if key == "neuroengineering":
            assert "38,145" in md and "10 putative" in md
            assert "local neighbor consistency" in md and "global clustering agreement" in md
        assert "35,587" not in md
        records = apply_profile(resume_data, profiles[key])["evidence_records"]
        assert records["dhn-spike-control"]["values"] == control
        assert "canonical arrays asserted equal" in records["dhn-spike-control"]["test_conditions"]
        assert "not proof of unrounded fidelity" in records["dhn-spike-control"]["limitations"]
        if key == "neuroengineering":
            assert records["waveform-features"]["values"]["ari"] == 0.3665


@pytest.mark.parametrize("evidence_id", ["intan-timing-withheld", "legacy-professional", "missing"])
def test_unpublished_evidence_cannot_enter_public_profile(resume_data, profiles, evidence_id):
    resume_data["projects"][0]["evidence_ids"] = [evidence_id]
    with pytest.raises(ValueError, match="unpublished evidence"):
        apply_profile(resume_data, profiles["neuroengineering"])


@pytest.mark.parametrize(("field", "value", "message"), [
    ("revision", "main", "full commit SHA"),
    ("sources", [], "exact sources"),
    ("maturity", "Production-ready", "invalid maturity"),
    ("measurement_definition", "", "missing measurement_definition"),
])
def test_invalid_public_evidence_fails_explicitly(resume_data, profiles, monkeypatch, field, value, message):
    from scripts import build_resume as builder
    inventory = load_yaml(DATA_DIR / "evidence_inventory.yaml")
    inventory["records"]["intan-workflow"][field] = value
    monkeypatch.setattr(builder, "load_yaml", lambda path: inventory)
    with pytest.raises(ValueError, match=message):
        apply_profile(resume_data, profiles["neuroengineering"])


@pytest.mark.parametrize("profile_key", ["engineering", "neuroengineering"])
def test_approved_methods_propagate_without_private_data(resume_data, profiles, profile_key):
    md = render_resume(resume_data, profiles[profile_key])
    assert "human intracranial electrophysiology recordings" in md
    assert "routing/VLAN segmentation" in md
    if profile_key == "neuroengineering":
        assert "repeated spoken narratives" in md
        assert "housing outcomes" in md
    assert "500,000" not in md
    assert "6,000" not in md
    records = apply_profile(resume_data, profiles[profile_key])["evidence_records"]
    for key in ("narrative-methods", "systems-methods"):
        assert records[key]["source_type"] == "owner-report"
        assert "revision" not in records[key]


def test_owner_report_cannot_masquerade_as_pinned_source(resume_data, profiles, monkeypatch):
    from scripts import build_resume as builder
    inventory = load_yaml(DATA_DIR / "evidence_inventory.yaml")
    inventory["records"]["narrative-methods"]["revision"] = "a" * 40
    monkeypatch.setattr(builder, "load_yaml", lambda path: inventory)
    with pytest.raises(ValueError, match="Owner-reported evidence"):
        apply_profile(resume_data, profiles["neuroengineering"])


def test_badge_is_in_full_header_not_certification_bullets(resume_data, profiles):
    full = render_resume(resume_data, profiles["neuroengineering"], output_format="latex")
    assert full.index(r"\BeginResumeHeader") < full.index(r"\ResumeName")
    assert full.index(r"\ResumeName") < full.index(r"\EndResumeHeader") < full.index("## Research Profile")
    assert "ucd_python_badge.png" not in full.split("## Professional Development & Certifications")[1]
    compact = render_resume(resume_data, profiles["engineering"], output_format="latex")
    assert r"\BeginResumeHeader" not in compact


def test_new_owner_reports_and_adapter_keep_distinct_provenance(resume_data, profiles):
    records = apply_profile(resume_data, profiles["neuroengineering"])["evidence_records"]
    adapter = records["med-adapter"]
    assert adapter["revision"] == "496c2326f000037698f7b92b4b3a4139c3a70d13"
    assert adapter["sources"][0]["path"] == "sort_med/sorting_tools/med_utils.py"
    for key in ("hosaka-debugging", "neuralynx-repair"):
        assert records[key]["source_type"] == "owner-report"
        assert records[key]["confirmed_on"] == "2026-11-08"
        assert not records[key].get("revision") and not records[key].get("sources")
    assert "No before/after speedup ratio claimed" in records["hosaka-debugging"]["measurement_definition"]
    assert "seven-record" in records["hosaka-debugging"]["test_conditions"]
    assert "approximately ten seconds" in records["hosaka-debugging"]["test_conditions"]
    assert "owner-reported" in records["hosaka-debugging"]["limitations"]


def test_professional_development_is_not_an_academic_degree(resume_data, profiles):
    full = apply_profile(resume_data, profiles["neuroengineering"])
    assert len(full["education"]) == 3
    assert all("Python" not in degree["degree"] for degree in full["education"])
    assert full["professional_development"][0]["name"] == "Python for Data Science, Professional Concentration"
    assert apply_profile(resume_data, profiles["engineering"])["professional_development"] == []


@pytest.mark.parametrize("profile_key", ["neuroengineering", "engineering", "data_analytics", "clinical_research", "default"])
def test_reusable_letter_variants_render_without_stale_claims(resume_data, profiles, profile_key, tmp_path, monkeypatch):
    from scripts import build_cover_letter as letters
    monkeypatch.setattr(letters, "OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(letters, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", [
        "build_cover_letter.py", "--company", "Example Lab", "--role", "Research Engineer",
        "--profile", profile_key, "--output", "letter", "--md-only",
    ])
    letters.main()
    text = (tmp_path / "letter.md").read_text()
    assert "Research Engineer position at Example Lab" in text
    for stale in ("recently admitted", "train classifiers", "real-time spike discrimination",
                  "would be honored", "{role}", "{company}"):
        assert stale not in text
    if profile_key in ("neuroengineering", "engineering"):
        assert "Hosaka" in text and "one-channel comparison" in text
        assert len(text.split()) < 250
    if profile_key == "data_analytics":
        assert "Hosaka" not in text and "MED" not in text
