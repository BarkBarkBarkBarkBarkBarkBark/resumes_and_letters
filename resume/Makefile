.PHONY: all install resume resume-neuro resume-analytics resume-clinical \
        cover-letter all-resumes site site-neuro site-analytics test clean profiles

PYTHON := python3

# ── Default target ────────────────────────────────────────────────────────────
all: resume site

# ── Install Python dependencies ───────────────────────────────────────────────
install:
	$(PYTHON) -m pip install -r requirements.txt

# ── Resume builds ─────────────────────────────────────────────────────────────
resume:
	$(PYTHON) scripts/build_resume.py

resume-neuro:
	$(PYTHON) scripts/build_resume.py --profile neuroengineering

resume-analytics:
	$(PYTHON) scripts/build_resume.py --profile data_analytics

resume-clinical:
	$(PYTHON) scripts/build_resume.py --profile clinical_research

# Build all profile variants at once
all-resumes:
	$(PYTHON) scripts/build_resume.py --profile neuroengineering
	$(PYTHON) scripts/build_resume.py --profile data_analytics
	$(PYTHON) scripts/build_resume.py --profile clinical_research

# ── Cover letter ──────────────────────────────────────────────────────────────
# Usage: make cover-letter COMPANY="UC Davis" ROLE="Research Engineer"
cover-letter:
ifndef COMPANY
	$(error COMPANY is required. Usage: make cover-letter COMPANY="Acme" ROLE="Engineer")
endif
ifndef ROLE
	$(error ROLE is required. Usage: make cover-letter COMPANY="Acme" ROLE="Engineer")
endif
	$(PYTHON) scripts/build_cover_letter.py --company "$(COMPANY)" --role "$(ROLE)"

# ── GitHub Pages site ────────────────────────────────────────────────────────
# Builds docs/index.html — commit this file, then set GH Pages source to
# "GitHub Actions" in repo Settings → Pages.
site:
	$(PYTHON) scripts/build_site.py

site-neuro:
	$(PYTHON) scripts/build_site.py --profile neuroengineering

site-analytics:
	$(PYTHON) scripts/build_site.py --profile data_analytics

# ── Tests ─────────────────────────────────────────────────────────────────────
test:
	$(PYTHON) -m pytest tests/ -v

# ── Clean generated outputs ───────────────────────────────────────────────────
clean:
	find output/ -type f ! -name ".gitkeep" -delete
	@echo "Output directory cleaned."

# ── List available profiles ───────────────────────────────────────────────────
profiles:
	$(PYTHON) scripts/build_resume.py --list-profiles

# ── List available profiles ───────────────────────────────────────────────────
profiles:
	$(PYTHON) scripts/build_resume.py --list-profiles
