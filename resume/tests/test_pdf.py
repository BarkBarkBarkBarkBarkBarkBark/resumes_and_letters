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
        "Technical Skills", "Selected Engineering Projects", "Research Experience",
        "Education", "Additional Professional Experience",
    ]
    if profile != "engineering":
        headings.append("Certifications")
    positions = [text.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert text.count("Z-Lab") == 1
    assert "##" not in text and "{'text':" not in text
    first_page = text.split("\f")[0]
    assert "Neural Signal Processing & Acquisition" in first_page
    assert "Neural Acquisition and Synchronization" in first_page
    assert "Neural Signal Fidelity and Processing Validation" in first_page
    for claim in ("0.5 uV", "35,587", "95.04%", "54.26%"):
        assert claim in text
    if profile == "engineering":
        assert "Spike Sorting and Waveform Discrimination" in first_page
        assert "First Step Communities" in first_page and "Eurofins" in first_page
        assert "Fall 2026 - Present" in first_page
    assert "narrative-aligned rasters" in text
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


def test_pdf_contains_all_evidence_and_project_links(publication):
    pdf, profile_key, _ = publication
    data = load_yaml(DATA_DIR / "base_resume.yaml")
    profile = load_yaml(DATA_DIR / "role_profiles.yaml")[profile_key]
    filtered = apply_profile(data, profile)
    expected = {
        item["evidence"]
        for group in filtered["skills"] for item in group["items"] if item.get("evidence")
    }
    for project in filtered["projects"]:
        expected.update(item["evidence"] for item in project["bullets"] if item.get("evidence"))
        if not filtered["compact"]:
            expected.update(link["url"] for link in project["links"])
    expected.update(filtered["personal"]["contact"][key] for key in ("github", "linkedin"))
    links = output("pdfinfo", "-url", str(pdf))
    for url in expected:
        assert url in links
