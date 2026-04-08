# resume-as-code

A plain-text resume system where all content lives in a single YAML file and
outputs are generated programmatically. Edit once, publish everywhere.

---

## Why YAML as the source of truth

| Concern | Solution |
|---|---|
| Version control | YAML diffs cleanly in git — you can see exactly what changed |
| No vendor lock-in | Plain text; no proprietary format to reverse-engineer |
| Role targeting | One file, multiple rendered variants via role profiles |
| Reusability | Cover letter snippets are pulled from the same source |
| Readability | YAML is human-editable without tooling |

---

## Project structure

```
resume/
  data/
    base_resume.yaml          ← edit this; single source of truth
    cover_letter_snippets.yaml ← reusable cover letter paragraphs
    role_profiles.yaml        ← filtering rules per target role type
  templates/
    resume.md.j2              ← Jinja2 Markdown resume template
    cover_letter.md.j2        ← Jinja2 Markdown cover letter template
  scripts/
    build_resume.py           ← CLI: generate resume outputs
    build_cover_letter.py     ← CLI: generate cover letter outputs
  output/                     ← generated files land here (gitignored)
  tests/
    test_build.py             ← pytest suite
  README.md
  requirements.txt
  Makefile
```

---

## Installation

**Requirements:** Python 3.9+, [Pandoc](https://pandoc.org/installing.html)

```bash
# Install Pandoc (macOS)
brew install pandoc

# Install Python dependencies
pip install -r requirements.txt
# or
make install
```

### PDF generation (optional)

Pandoc needs a PDF engine. In order of preference:

```bash
# Option 1 — WeasyPrint (Python, easiest)
pip install weasyprint

# Option 2 — wkhtmltopdf
brew install wkhtmltopdf

# Option 3 — BasicTeX (pdflatex)
brew install --cask basictex
```

If no PDF engine is found, the build still completes with Markdown and DOCX.

---

## Build outputs

```bash
# Default resume (uses target_metadata.default_profile from base_resume.yaml)
python scripts/build_resume.py

# Specific profile
python scripts/build_resume.py --profile neuroengineering
python scripts/build_resume.py --profile data_analytics
python scripts/build_resume.py --profile clinical_research

# Custom output filename
python scripts/build_resume.py --profile neuroengineering --output my_custom_name

# Markdown only (skip DOCX/PDF)
python scripts/build_resume.py --md-only

# List available profiles
python scripts/build_resume.py --list-profiles

# Cover letter
python scripts/build_cover_letter.py --company "UC Davis" --role "Research Engineer"
python scripts/build_cover_letter.py --company "Acme" --role "Data Analyst" --profile data_analytics
```

**Or via Make:**

```bash
make resume                              # default profile
make resume-neuro                        # neuroengineering profile
make resume-analytics                    # data_analytics profile
make all-resumes                         # all profiles at once
make cover-letter COMPANY="UC Davis" ROLE="Research Engineer"
make test                                # run pytest
make clean                              # remove generated outputs
```

**Output files are written to `output/` with sanitized filenames, e.g.:**

```
output/marco_del_fava_resume_neuroengineering.md
output/marco_del_fava_resume_neuroengineering.docx
output/marco_del_fava_resume_neuroengineering.pdf
output/marco_del_fava_cover_letter_uc_davis_research_engineer.docx
```

---

## Editing content

**All content edits happen in `data/base_resume.yaml` only.**

### Add a new bullet to a job

Find the relevant entry under `experience:` or `volunteer:` and add to its `bullets:` list:

```yaml
- text: >
    Describe what you did and the outcome or impact.
  tags: [analytics, technical, python]
```

Tags control which role profile includes this bullet (see [Role targeting](#role-targeting)).

### Update contact info

```yaml
personal:
  name: Marco Del Fava
  contact:
    email: marc.delfava@gmail.com
    phone: "707-637-6544"
    linkedin: linkedin.com/in/yourhandle   # add here
    github: github.com/yourhandle          # add here
```

### Add a new summary variant

```yaml
summary:
  my_new_profile: >
    One paragraph tailored to this application type.
```

Then reference it in a role profile (`data/role_profiles.yaml`):

```yaml
my_new_profile:
  summary_key: my_new_profile
  ...
```

### Add a certification

```yaml
certifications:
  - name: AWS Certified Cloud Practitioner
    issuer: Amazon Web Services
    date: "2025"
```

---

## Role targeting

The system uses **role profiles** to filter and prioritize content without
duplicating it. All profiles read from the same `base_resume.yaml`.

### How it works

1. Each bullet in the YAML has a `tags:` list.
2. Each role profile in `role_profiles.yaml` has `prefer_tags` and `deprioritize_tags`.
3. At build time, bullets are scored by tag overlap, sorted by score, and capped
   at `max_bullets_per_role`.
4. The profile also controls which skill categories appear, whether the volunteer
   section is included, and which summary variant is used.

### Adding a new role profile

Edit `data/role_profiles.yaml`:

```yaml
my_new_role:
  name: "Descriptive Name"
  summary_key: neuroengineering        # or any key in base_resume.yaml summary:
  include_volunteer: true
  include_coursework: false
  prefer_tags: [research, technical, ml]
  deprioritize_tags: [management, operations]
  max_bullets_per_role: 4
  skill_categories:
    - Neural Data & Signal Processing
    - Machine Learning & Data Science
  cover_letter_opener: neuroengineering  # key in cover_letter_snippets.yaml
```

Then build with:

```bash
python scripts/build_resume.py --profile my_new_role
```

---

## Cover letter customization

Cover letter paragraphs live in `data/cover_letter_snippets.yaml`. The template
assembles them automatically based on the active profile.

To add a new opener for a custom profile:

```yaml
opener:
  my_new_role: >
    I am writing to apply for the {role} position at {company}. ...
```

The `{role}` and `{company}` placeholders are filled by the CLI arguments at
build time.

---

## ATS-safe formatting principles used in this repo

The generated Markdown is designed to parse cleanly through automated resume
screening systems (ATS):

| Principle | Implementation |
|---|---|
| Single column | Template has no side-by-side layout |
| No tables | Pandoc DOCX output is table-free |
| Standard section names | Summary, Experience, Education, Skills, Certifications |
| Contact info in body | Not buried in Word header/footer |
| Text-based PDF | Generated via pandoc, not from a screenshot |
| Clean reading order | Top-to-bottom, left-to-right; no floating elements |
| No icons or glyphs | Labels are plain text |
| Consistent date format | "Jul 2021 – Present" |
| Simple bullets | `-` lists only; no nested structures |

---

## Running tests

```bash
make test
# or
python -m pytest tests/ -v
```

Tests cover YAML loading, field validation, date formatting, rendering correctness,
profile filtering behavior, and output file creation.

---

## Publishing to GitHub Pages

The `docs/index.html` file is the GitHub Pages entry point. It is generated from
the same YAML source as the DOCX/PDF outputs and auto-deploys on every push via
GitHub Actions.

### One-time setup

1. Push this repo to GitHub.
2. Go to **Settings → Pages**.
3. Under **Source**, select **GitHub Actions**.
4. That's it — the `.github/workflows/deploy.yml` workflow handles the rest.

Your resume will be live at `https://<your-username>.github.io/<repo-name>/`.

### Build locally

```bash
make site                            # default profile (neuroengineering)
make site-neuro                      # explicit neuroengineering profile
make site-analytics                  # data_analytics profile
python scripts/build_site.py --profile clinical_research
```

The output is written to `docs/index.html`. Commit and push to redeploy.

### How auto-deploy works

Every push to `main` or `master` triggers the workflow in
`.github/workflows/deploy.yml`, which:

1. Installs Python dependencies
2. Runs `python scripts/build_site.py --profile neuroengineering`
3. Uploads `docs/` as a Pages artifact
4. Deploys to `github-pages` environment

You can also trigger a manual rebuild from the **Actions** tab → **Build and
Deploy Resume Site** → **Run workflow**.

---

## Known limitations

- **PDF quality** depends on the installed PDF engine. WeasyPrint produces the most
  reliable output without LaTeX. A custom CSS file can be passed to pandoc for
  better typography if needed.
- **DOCX styling** uses pandoc defaults. For a branded look, create a
  `templates/reference.docx` and pass `--reference-doc templates/reference.docx`
  to the pandoc call in `build_resume.py`.
- **Cover letter paragraphs** are assembled from fixed snippets. For highly
  customized letters, edit `cover_letter_snippets.yaml` directly before building,
  or write the body manually into the rendered Markdown output.
