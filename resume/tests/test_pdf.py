"""Integration checks for a built publication; run after build_site.py."""

import os
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from scripts.build_resume import DATA_DIR, apply_profile, load_yaml

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(params=[("neuroengineering", "marco_del_fava_cv", 2),
                        ("engineering", "marco_del_fava_engineering", 1)])
def publication(request):
    directory = Path(os.environ.get("PORTFOLIO_DIR", ROOT / "docs"))
    profile, stem, pages = request.param
    path = directory / f"{stem}.pdf"
    if not path.is_file():
        if "PORTFOLIO_DIR" in os.environ:
            pytest.fail(f"Publication PDF missing: {path}")
        pytest.skip("Build the portfolio before running PDF integration checks.")
    if not shutil.which("pdfinfo") or not shutil.which("pdftotext"):
        pytest.skip("PDF integration checks require Poppler (pdfinfo and pdftotext).")
    return path, profile, pages


def output(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def test_pdf_has_required_pages_and_selectable_ordered_sections(publication):
    pdf, profile, pages = publication
    metadata = output("pdfinfo", str(pdf))
    assert re.search(rf"^Pages:\s+{pages}$", metadata, re.MULTILINE)
    text = output("pdftotext", "-raw", str(pdf), "-")
    headings = [
        "Marco Del Fava", "Engineering Summary" if profile == "engineering" else "Research Profile",
        "Technical Skills", "Research Experience", "Selected Engineering Projects",
        "Additional Professional Experience", "Education",
    ]
    if profile != "engineering":
        headings.append("Professional Development & Certifications")
    positions = [text.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert text.count("Z-Lab") == 1
    assert "##" not in text and "{'text':" not in text
    first_page = text.split("\f")[0]
    assert "Research Software & Neural Data" in first_page
    assert "Neural Data Formats and Integrity" in first_page
    for claim in ("0.5 µV", "20 million", "one channel", "Hosaka", "content-based caching",
                  "seven records", "approximately ten seconds"):
        assert claim in text
    assert "35,587" not in text
    assert "not independently verified" not in text
    assert "(continued)" not in text
    if profile == "engineering":
        assert "Neural Acquisition and Experimental Synchronization" in first_page
        assert "First Step Communities" in first_page and "Eurofins" in first_page
        assert "2026–Present" in first_page
    else:
        assert "Z-Lab" in first_page and "repeated spoken narratives" in first_page
        assert "38,145" in text and "10 putative" in text
        assert "95.04%" not in text and "54.26%" not in text
        assert "Neural Acquisition and Experimental Synchronization" in first_page
        assert "Waveform Analysis and Spike Sorting" in text.split("\f")[1]
        assert text.index("Education") < text.index("Python for Data Science")
    assert "routing/VLAN segmentation" in text


def test_pdf_body_within_margins(publication):
    pdf, _, page_count = publication
    tree = ET.fromstring(output("pdftotext", "-bbox", str(pdf), "-"))
    ns = {"h": "http://www.w3.org/1999/xhtml"}
    pages = tree.findall(".//h:page", ns)
    assert len(pages) == page_count
    for page in pages:
        words = page.findall("h:word", ns)
        assert words
        for word in words:
            # Microtype may protrude punctuation by less than one point.
            assert float(word.attrib["xMin"]) >= 49.4
            assert float(word.attrib["xMax"]) <= 562.6
            if float(word.attrib["yMin"]) > 750:
                assert word.text in ("1", "2")  # page number, outside the body box
            else:
                assert float(word.attrib["yMin"]) >= 49.4
                assert float(word.attrib["yMax"]) <= 742.6


def test_pdf_contains_readable_project_sources_and_contact_links(publication):
    pdf, profile_key, _ = publication
    data = load_yaml(DATA_DIR / "base_resume.yaml")
    profile = load_yaml(DATA_DIR / "role_profiles.yaml")[profile_key]
    filtered = apply_profile(data, profile)
    expected = {link["url"] for project in filtered["projects"] for link in project["links"]}
    expected.update(filtered["personal"]["contact"][key] for key in ("github", "linkedin"))
    expected.update(cert["credly_url"] for cert in filtered["certifications"] if cert.get("credly_url"))
    links = output("pdfinfo", "-url", str(pdf))
    for url in expected:
        assert url in links
    text = output("pdftotext", "-raw", str(pdf), "-")
    for project in filtered["projects"]:
        for link in project["links"]:
            assert link["label"] in text
    assert not re.search(r"^Source$", text, re.MULTILINE)
    assert "evidence.html#med-adapter" not in links
    assert "evidence.html#hosaka-debugging" not in links
    for artifact in ("med_utils.py", "8_7_filetype_comparison.ipynb"):
        assert artifact in links
