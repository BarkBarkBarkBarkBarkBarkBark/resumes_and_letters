# Marco Del Fava

**[Public portfolio and CV](https://barkbarkbarkbarkbarkbarkbark.github.io/resumes_and_letters/)**

## Neural acquisition, spike processing, and single-neuron response analysis

I'm a biomedical engineering master's student at UC Davis and a research
volunteer in Dr. Jie Zheng's lab, working on human single-unit electrophysiology.
I build research software for neural acquisition and spike analysis. My interests
include Intan acquisition, real-time spike sorting, and semantic selectivity in
single-neuron responses.

Selected work covers Intan file-processing and acquisition integration,
waveform discrimination and experimental online sorting, and semantic analysis
and simulation. The portfolio distinguishes implemented code from developing
hardware integration, proposed experiments, and unvalidated performance claims.

## Resume and portfolio generator

Canonical content lives in [base_resume.yaml](resume/data/base_resume.yaml).
Filtering, ordering, bullet limits, and the CV page break are configured in
[role_profiles.yaml](resume/data/role_profiles.yaml). Do not edit generated files
or copy older templates from the historical `documents/` snapshot into the
active generator.

### Install

Run all commands below **from the repository root**. Python 3.9+, Pandoc,
LuaLaTeX, and latexmk are required for the complete publication build.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r resume/requirements.txt

# macOS: install Pandoc and a TeX distribution with LuaLaTeX/latexmk.
brew install pandoc
brew install --cask mactex-no-gui

# Ubuntu alternative:
# sudo apt-get install pandoc latexmk texlive-luatex \
#   texlive-fonts-recommended texlive-latex-extra
```

The LaTeX template preserves 11-point body text, 13-point leading, 0.7-inch
margins, microtype, and TeX Gyre fonts with Latin Modern fallbacks. There is no
automatic PDF-engine substitution; a missing engine or failed PDF is a build
error, not a successful publication.

### Build and preview

```bash
# Website AND matching PDF, from the same data/profile/template revision:
python resume/scripts/build_site.py --profile neuroengineering

# Serve the generated site; open http://localhost:8000/
python -m http.server 8000 --directory resume/docs

# Exact, stable output name (no timestamp added to --output):
python resume/scripts/build_resume.py --profile neuroengineering --output marco_del_fava_cv

# Markdown and JSON only; no Pandoc or TeX required:
python resume/scripts/build_resume.py --profile neuroengineering --md-only

python resume/scripts/build_resume.py --list-profiles
python -m pytest resume/tests -q
```

PDF integration checks also use Poppler (`brew install poppler` on macOS,
`sudo apt-get install poppler-utils` on Ubuntu). After a site build, these check
the actual two-page PDF, selectable section order, body margins, and evidence
annotations. CI runs them against its freshly built publication directory.

Standalone CV outputs go into `resume/output/<stem>/`: Markdown, JSON,
DOCX, LaTeX, and PDF. Without `--output`, the standalone CLI retains timestamped
output names. The website builder always uses `marco_del_fava_cv` and copies
that exact PDF to `resume/docs/marco_del_fava_cv.pdf`. A custom publication
directory can be selected with `--output-dir`.

The homepage uses ordinary hash links, needs no JavaScript, and prints the CV
once. Header profile links use official GitHub and LinkedIn emblems plus full,
readable URLs. Skill evidence is a small linked GitHub emblem with an accessible
label; skill text remains selectable. The PDF has selectable text and clickable
evidence links; it is not a tagged/PDF-UA document.

### Content and evidence schema

Skills and contribution bullets use mappings:

```yaml
- text: Describe the implementation or evaluation precisely.
  evidence: https://github.com/owner/project/blob/main/path/to/implementation.py
  tags: [technical, research]
```

`evidence` and `tags` are optional. Legacy strings are accepted at the input
boundary and normalized to `text` mappings for all renderers and the JSON export.
Invalid or empty items and non-HTTPS evidence links raise errors. Canonical
skills and project bullets have been migrated to mappings.

Each selected project has an `id`, `name`, `problem`, two `bullets`, `status`,
and `links`. Use the most specific implementation, documentation, or evaluation
artifact available. Label integration as developing until hardware validation is
available. Sampling frequency is not end-to-end latency. Performance claims
require workload, hardware, measurement method, and result.

Enrollment since Fall 2026 and the research-volunteer affiliation since July 2025
were confirmed by Marco. No graduation date or formal research appointment is
inferred. The former waveform-count and curation-efficiency claims are omitted
pending labeling provenance and measured outcomes.

### Publishing

[The single Pages workflow](.github/workflows/deploy.yml) tests the generator,
builds the website and PDF into `_site` from the checked-out commit, and uploads
that exact directory using the official Pages artifact/deployment actions.
Set repository **Settings → Pages → Source → GitHub Actions**. The former
competing `gh-pages` publisher has been removed. No output is selected by
modification time, and no shell substitution is passed as an action input.

The active templates are in `resume/templates/`; official raster emblems are
stored with those templates so both local and CI builds use the same assets.
Historical exports under `documents/` are archives, not build inputs.

### Private cover letters

The public site has no Letter tab and never discovers or embeds cover letters.
The standalone generator remains available for deliberate, private use:

```bash
python resume/scripts/build_cover_letter.py \
  --company "Example Lab" --role "Research Engineer" --md-only
```

Review the separate cover-letter snippets before sending them. They are not
part of the public portfolio build.
