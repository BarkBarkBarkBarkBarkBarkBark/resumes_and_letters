from html.parser import HTMLParser
import json
from pathlib import Path

import pytest

from scripts import build_site as site
from scripts.build_resume import DATA_DIR, apply_profile, load_yaml, template_environment


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.links.append(attrs)
        if tag == "img":
            self.images.append(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])


@pytest.fixture
def content():
    data = load_yaml(DATA_DIR / "base_resume.yaml")
    profile = load_yaml(DATA_DIR / "role_profiles.yaml")["neuroengineering"]
    return data, profile


def render_site(content):
    data, profile = content
    return template_environment().get_template("resume.html.j2").render(
        resume=apply_profile(data, profile), pdf_url="marco_del_fava_cv.pdf",
        source_commit="abc123",
    )


def test_site_has_real_navigation_and_accessible_evidence(content):
    html = render_site(content)
    parser = PageLinks()
    parser.feed(html)
    hrefs = [link.get("href", "") for link in parser.links]
    for href in hrefs:
        if href.startswith("#"):
            assert href[1:] in parser.ids
    assert "#selected-projects" in hrefs
    assert "marco_del_fava_cv.pdf" in hrefs
    assert "marco_del_fava_engineering.pdf" in hrefs
    assert "mailto:mdelfava@ucdavis.edu" in hrefs
    assert all("alt" in image for image in parser.images)
    evidence = [link for link in parser.links if link.get("class") == "evidence"]
    assert evidence and all(link.get("aria-label", "").startswith("Source evidence:") for link in evidence)
    for forbidden in ("onclick=", "<script", "tab-panel", "Quick snapshot", "Letter</", "{'text':"):
        assert forbidden not in html
    assert "@media print" in html
    assert html.count('id="research-title"') == 1
    assert html.count('id="skills-title"') == 1


def test_html_escapes_content_and_supports_legacy_strings(content):
    data, profile = content
    data["skills"][0]["items"] = ["Legacy skill", {"text": "<script>alert('x')</script>"}]
    html = render_site((data, profile))
    assert "Legacy skill" in html
    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html
    assert "{'text':" not in html


def test_publication_copies_exact_pdf_and_never_discovers_letters(content, tmp_path, monkeypatch):
    data, profile = content
    source = tmp_path / "build"
    source.mkdir()
    expected_pdf = b"%PDF-1.4\nmatching artifact\n"
    (source / f"{site.CV_STEM}.pdf").write_bytes(expected_pdf)
    (source / f"{site.ENGINEERING_STEM}.pdf").write_bytes(b"%PDF-engineering\n")
    (source / "newest_cover_letter.md").write_text("PRIVATE LETTER")
    calls = []

    def build(data_arg, profile_arg, stem):
        calls.append((data_arg, profile_arg, stem))
        return source

    monkeypatch.setattr(site, "build_resume", build)
    output = site.build_site(data, profile, tmp_path / "public", "abc123")
    assert (output / f"{site.CV_STEM}.pdf").read_bytes() == expected_pdf
    html = (output / "index.html").read_text()
    assert "PRIVATE LETTER" not in html and "abc123" in html
    engineering = load_yaml(DATA_DIR / "role_profiles.yaml")["engineering"]
    assert calls == [(data, profile, site.CV_STEM), (data, engineering, site.ENGINEERING_STEM)]
    assert (output / f"{site.ENGINEERING_STEM}.pdf").read_bytes() == b"%PDF-engineering\n"
    assert sorted(path.name for path in output.iterdir()) == [
        ".nojekyll", "assets", "evidence.html", "evidence_manifest.json", "index.html",
        f"{site.CV_STEM}.pdf", f"{site.ENGINEERING_STEM}.pdf",
    ]
    assert sorted(path.name for path in (output / "assets").iterdir()) == ["github.png", "linkedin.png"]
    manifest = json.loads((output / "evidence_manifest.json").read_text())
    assert manifest["source_commit"] == "abc123"
    assert manifest["records"] == apply_profile(data, profile)["evidence_records"]
    assert "intan-timing-withheld" not in manifest["records"]
    assert "legacy-professional" not in manifest["records"]


def test_failed_pdf_build_does_not_publish(content, tmp_path, monkeypatch):
    data, profile = content

    def fail(*args):
        raise RuntimeError("PDF failed")

    monkeypatch.setattr(site, "build_resume", fail)
    with pytest.raises(RuntimeError, match="PDF failed"):
        site.build_site(data, profile, tmp_path / "public")
    assert not (tmp_path / "public/index.html").exists()


def test_only_one_pages_workflow_and_no_mtime_selection():
    workflows = Path(__file__).resolve().parents[2] / ".github/workflows"
    assert not (workflows / "deploy_resume_pages.yml").exists()
    workflow = (workflows / "deploy.yml").read_text()
    assert "build_site.py" in workflow and "path: _site" in workflow
    assert "build_cover_letter.py" not in workflow
    assert "$(" not in workflow and "ls -1t" not in workflow


def test_featured_projects_precede_affiliation_and_have_four_answers(content):
    html = render_site(content)
    assert html.index('id="selected-projects"') < html.index('id="research-title"')
    assert html.index('id="intan"') < html.index('id="compression"') < html.index('id="sorting"')
    assert html.count("<dt>Technical approach</dt>") == 4
    assert html.count("<dt>Evaluation scope</dt>") == 4
    assert html.count("<dt>Finding / implementation</dt>") == 4
    assert html.count('class="project-visual"') == 4
    assert "19,951,989" in html
    assert "95.04%" in html and "54.26%" in html
    assert "0.3665" in html
    assert 'id="figure-B2"' not in html
    assert html.index('id="sorting"') < html.index('id="narrative"') < html.index('id="skills-title"')
    assert "Neural Signal Processing &amp; Acquisition" in html
    assert "Engineering Resume · 1 page" in html
    assert "not a latency measurement" in html
    parser = PageLinks()
    parser.feed(html)
    # No recording-derived images or external image requests.
    assert {image["src"] for image in parser.images} <= {"assets/github.png", "assets/linkedin.png"}


def test_evidence_page_exports_only_approved_records(content):
    data, profile = content
    records = apply_profile(data, profile)["evidence_records"]
    html = template_environment().get_template("evidence.html.j2").render(records=records)
    assert "intan-timing-withheld" not in html
    assert "legacy-professional" not in html
    assert "ZLab2024" not in html
    assert "raw-data rerun" in html
    assert "Mean error, compression ratio" in html
    parser = PageLinks()
    parser.feed(html)
    for key, record in records.items():
        assert key in parser.ids
        if record.get("source_type") == "owner-report":
            assert "revision" not in record and "sources" not in record
            assert record["confirmed_on"] in html
            continue
        assert len(record["revision"]) == 40
        for source in record["sources"]:
            assert f"/{record['revision']}/" in source["url"]
            assert source["url"] in html
    main = PageLinks()
    main.feed(render_site(content))
    for link in main.links:
        if link.get("href", "").startswith("evidence.html#"):
            assert link["href"].split("#")[1] in parser.ids


def test_figures_have_provenance_and_detail_page_preserves_scope(content):
    data, profile = content
    records = apply_profile(data, profile)["evidence_records"]
    html = template_environment().get_template("evidence.html.j2").render(records=records)
    parser = PageLinks()
    parser.feed(html)
    for record in records.values():
        if record.get("visual"):
            assert f"figure-{record['visual']['figure_id']}" in parser.ids
            assert record["visual"]["caption"] in html
    assert len(parser.ids) == len(set(parser.ids))
    for claim in ("35,587 exact frame matches", "35,587 / 35,587 = 1.0",
                  "83.67%", "0.4046", "C2 contingency", "Owner-reported",
                  "No public source commit", "No service-record"):
        assert claim in html
    assert "semantic tuning" in html
    assert "evidence_manifest.json" in html


def test_second_pdf_failure_does_not_publish(content, tmp_path, monkeypatch):
    data, profile = content
    source = tmp_path / "build"
    source.mkdir()
    (source / f"{site.CV_STEM}.pdf").write_bytes(b"%PDF\n")

    def build(data_arg, profile_arg, stem):
        if stem == site.ENGINEERING_STEM:
            raise RuntimeError("Engineering PDF failed")
        return source

    monkeypatch.setattr(site, "build_resume", build)
    with pytest.raises(RuntimeError, match="Engineering PDF failed"):
        site.build_site(data, profile, tmp_path / "public")
    assert not (tmp_path / "public").exists()
