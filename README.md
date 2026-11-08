# Marco Del Fava

**[Engineering portfolio and CV](https://barkbarkbarkbarkbarkbarkbark.github.io/resumes_and_letters/)**

## Research Software & Neural Data

Biomedical Engineering M.S. student at UC Davis, working with human intracranial
electrophysiology in UC Davis Health's Z-Lab. I build Python software for
acquisition formats, data-integrity checks, spike processing, and experimental
synchronization.

Selected work includes a Neo-backed MED reader for SpikeInterface, Neuralynx
metadata validation and repair, Intan processing and event alignment, waveform
feature evaluation, and debugging agent-generated software.

A DarkHorse MED comparison covered 20 million samples from one channel at
32 kHz: maximum amplitude difference was 0.5 uV, with exact agreement after
whole-microvolt source rounding. Methods, measurement definitions, and source
references are on the [technical evidence page](https://barkbarkbarkbarkbarkbarkbark.github.io/resumes_and_letters/evidence.html).

## Canonical content and templates

Edit sources, not generated HTML, Markdown, or PDFs:

- [base_resume.yaml](resume/data/base_resume.yaml): accomplishments, skills,
  projects, education, and contact details.
- [role_profiles.yaml](resume/data/role_profiles.yaml): summary selection,
  project order, skill categories, bullet limits, and compact layout.
- [evidence_inventory.yaml](resume/data/evidence_inventory.yaml): source
  references, measurement definitions, test conditions, results, and limitations.
- [cover_letter_snippets.yaml](resume/data/cover_letter_snippets.yaml): reusable
  application paragraphs, kept out of the public site.
- [resume/templates/](resume/templates/): Jinja HTML/Markdown templates and the
  Pandoc LaTeX template.

The `neuroengineering` profile emphasizes research software and scientific data
for CatalystNeuro; `engineering` is its one-page resume. Analytics, clinical
research, and general profiles retain their own summaries and selections.
The full CV leads with the Z-Lab research role and three consolidated skill
lines, then the flagship formats/integrity and acquisition projects. Its remaining projects,
professional experience, education, and credentials continue on page two.
The one-page resume uses a shorter summary and selects formats, acquisition,
and agent-assisted debugging rather than compressing the full CV verbatim.

The homepage uses plain project sections: purpose, contribution, result, tools,
and an optional source or technical-details link. There are no project diagrams or
maturity badges. Measurement tables and the controlled spike-frame comparison
remain on the evidence page. The full CV has a small Credly-linked UC Davis
badge in its header; the certification section is text-only, and the compact
resume omits the badge. Academic degrees are separate from the Python
professional concentration. GitHub and LinkedIn profile links pair the platform
icons with readable labels. GitHub project references also retain a small icon
beside their "Source" label; skills and ordinary bullets do not carry icons.

## Build and validate

Run commands from the repository root. The full build needs Python 3.9+, Pandoc,
LuaLaTeX, and latexmk. PDF integration tests use Poppler.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r resume/requirements.txt

# macOS system tools:
brew install pandoc poppler
brew install --cask mactex-no-gui

# Ubuntu alternative:
# sudo apt-get install pandoc latexmk texlive-luatex \
#   texlive-fonts-recommended texlive-latex-extra poppler-utils

python -m pytest resume/tests --ignore=resume/tests/test_pdf.py -q
python resume/scripts/build_site.py --profile neuroengineering
python -m pytest resume/tests/test_pdf.py -q

# Local preview:
python -m http.server 8000 --directory resume/docs

# Standalone documents, with stable output names:
python resume/scripts/build_resume.py --profile neuroengineering --output marco_del_fava_cv
python resume/scripts/build_resume.py --profile engineering --output marco_del_fava_engineering

# Markdown/JSON only, without Pandoc or TeX:
python resume/scripts/build_resume.py --profile neuroengineering --md-only
python resume/scripts/build_resume.py --list-profiles
```

Standalone builds write Markdown, JSON, DOCX, LaTeX, and PDF under
`resume/output/<stem>/`. Omit `--output` for a timestamped stem. Build
intermediates are ignored; historical originals are retained.

The site builder generates both exact PDF names, `index.html`, `evidence.html`,
and `evidence_manifest.json` into `resume/docs` or `--output-dir`. It does not
discover files by modification time or copy application letters. A failed
document build prevents publication. The full CV uses 11-point text with
13-point leading; the compact resume uses 10.5/12-point typography. Both use
0.7-inch margins and selectable text with clickable references.

After a layout change, inspect actual desktop/mobile HTML and the first and last
pages of both PDFs. Tests check page counts, reading order, margins, links,
provenance, and factual scope; they do not replace visual review.

## Additional CatalystNeuro profile

The remote changes also provide a separate job-specific CV, without
overwriting the current public portfolio or full research CV:

```bash
python resume/scripts/build_resume.py --profile catalystneuro --output marco_del_fava_catalystneuro
python -m pytest resume/tests --ignore=resume/tests/test_pdf.py -q
```

The resulting PDF and DOCX live under
`resume/output/marco_del_fava_catalystneuro/`. This profile includes
Scientific AI Workstation alongside acquisition, data integrity, and waveform
analysis. The primary `neuroengineering` profile retains the current
four-project selection, including Hosaka.

Both full CVs keep the small UC Davis badge in the header, not inside a
certification bullet. The updated Credly shortcut resolves to the same
credential. The one-page engineering resume continues to omit the badge.

## Evidence and publication

Skills and bullets accept `text`, optional HTTPS `evidence`, and optional `tags`.
Legacy strings are normalized at the input boundary. Projects use `id`, `name`,
`problem`, `bullets`, `tools`, `evidence_ids`, and `links`; profiles select the
records for each output.
Links can set `icon: github` to retain the icon when pointing to technical evidence,
as with the Hosaka debugging account.
Use `hide_on_site: true` to hide a project link on the homepage while retaining its PDF reference.

Only explicitly public inventory records can enter the evidence page, filtered
JSON, or public manifest. Repository evidence requires exact source locations
and full commit revisions. Owner-reported work requires a publication
confirmation and cannot masquerade as commit-pinned code. Neuralynx repair and
Hosaka debugging are approved owner reports. The approximate ten-second,
seven-record Hosaka listing is an owner-reported pre-fix observation, not a
publicly rerun benchmark; no post-fix duration or speedup ratio is claimed.
Private implementations and timing logs are not published.

The 35,587-spike comparison is a controlled check of identical rounded input
arrays. Waveform evidence distinguishes same-label neighbor purity from matched
clustering agreement and ARI. Timing implementation is described without
claiming measured physical onset accuracy or latency.

Do not add source recordings, patient identifiers, private code excerpts,
credentials, or local lab paths. Keep material limitations in technical
documentation rather than repeating them across every public description.

[The single Pages workflow](.github/workflows/deploy.yml) tests the generator,
builds into `_site`, checks the freshly built PDFs using `PORTFOLIO_DIR`, and
publishes that exact directory. CI supplies the source commit; local
working-tree builds leave it empty. Local generation does not deploy the site.
Set **Settings > Pages > Source > GitHub Actions** for publication.
