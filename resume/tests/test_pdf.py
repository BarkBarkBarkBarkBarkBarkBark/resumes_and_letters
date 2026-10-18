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


@pytest.fixture
def pdf():
    directory = Path(os.environ.get("PORTFOLIO_DIR", ROOT / "docs"))
    path = directory / "marco_del_fava_cv.pdf"
    if not path.is_file():
        pytest.skip("Build the portfolio before running PDF integration checks.")
    if not shutil.which("pdfinfo") or not shutil.which("pdftotext"):
        pytest.skip("PDF integration checks require Poppler (pdfinfo and pdftotext).")
    return path


def output(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def test_pdf_has_two_pages_and_selectable_ordered_sections(pdf):
    metadata = output("pdfinfo", str(pdf))
    assert re.search(r"^Pages:\s+2$", metadata, re.MULTILINE)
    text = output("pdftotext", "-raw", str(pdf), "-")
    headings = [
        "Marco Del Fava", "Research Profile", "Research Experience", "Selected Projects",
        "Education", "Technical Skills", "Additional Professional Experience", "Certifications",
    ]
    positions = [text.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert text.count("Z-Lab") == 1
    assert "##" not in text and "{'text':" not in text
    first_page = text.split("\f")[0]
    assert "Dr. Jie Zheng" in first_page and "semantic tuning" in first_page


def test_pdf_body_within_margins(pdf):
    tree = ET.fromstring(output("pdftotext", "-bbox", str(pdf), "-"))
    ns = {"h": "http://www.w3.org/1999/xhtml"}
    pages = tree.findall(".//h:page", ns)
    assert len(pages) == 2
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


def test_pdf_contains_all_evidence_and_project_links(pdf):
    data = load_yaml(DATA_DIR / "base_resume.yaml")
    profile = load_yaml(DATA_DIR / "role_profiles.yaml")["neuroengineering"]
    filtered = apply_profile(data, profile)
    expected = {
        item["evidence"]
        for group in filtered["skills"] for item in group["items"] if item.get("evidence")
    }
    for project in filtered["projects"]:
        expected.update(item["evidence"] for item in project["bullets"] if item.get("evidence"))
        expected.update(link["url"] for link in project["links"])
    expected.update(filtered["personal"]["contact"][key] for key in ("github", "linkedin"))
    links = output("pdfinfo", "-url", str(pdf))
    for url in expected:
        assert url in links
