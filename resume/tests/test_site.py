from html.parser import HTMLParser
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
    assert calls == [(data, profile, site.CV_STEM)]
    assert sorted(path.name for path in output.iterdir()) == [
        ".nojekyll", "assets", "index.html", f"{site.CV_STEM}.pdf",
    ]


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
