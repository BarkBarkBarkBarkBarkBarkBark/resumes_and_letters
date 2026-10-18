# Marco Del Fava

**[Public portfolio and CV](https://barkbarkbarkbarkbarkbarkbark.github.io/resumes_and_letters/)**

## Neural Signal Processing & Acquisition

**Biomedical Engineering M.S. | UC Davis | Human Intracranial Electrophysiology**

I develop neural acquisition and signal-processing software, characterize system
behavior, and validate processing against recorded electrophysiology. Featured
work leads with Intan acquisition/timing software, independent DarkHorse Neuro
compression evaluation, and offline waveform processing.

The compression evaluation compared 20 million samples on one 32 kHz channel
(625 seconds): maximum source-to-MED difference was 0.5 uV, with exact agreement
after rounding the source to whole microvolts. A controlled MountainSort5
comparison of equal rounded inputs preserved 35,587 spike frames for the compared
unit. These are archived single-channel results, not a fresh raw-data rerun or a
claim that I implemented the compression algorithm.

## Resume and portfolio generator

Canonical content lives in [base_resume.yaml](resume/data/base_resume.yaml).
Filtering, ordering, bullet limits, and compact layout selection are configured in
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
# Website, full research CV, and one-page engineering resume:
python resume/scripts/build_site.py --profile neuroengineering

# Serve the generated site; open http://localhost:8000/
python -m http.server 8000 --directory resume/docs

# Exact, stable output name (no timestamp added to --output):
python resume/scripts/build_resume.py --profile neuroengineering --output marco_del_fava_cv
python resume/scripts/build_resume.py --profile engineering --output marco_del_fava_engineering

# Markdown and JSON only; no Pandoc or TeX required:
python resume/scripts/build_resume.py --profile neuroengineering --md-only

python resume/scripts/build_resume.py --list-profiles
python -m pytest resume/tests -q
```

PDF integration checks also use Poppler (`brew install poppler` on macOS,
`sudo apt-get install poppler-utils` on Ubuntu). After a site build, these check
the actual one-page engineering resume and two-page research CV, selectable
section order, body margins, and evidence annotations. CI runs generator tests
first, then the PDF checks against its freshly built publication directory.

Standalone CV outputs go into `resume/output/<stem>/`: Markdown, JSON,
DOCX, LaTeX, and PDF. Without `--output`, the standalone CLI retains timestamped
output names. The website builder always uses `marco_del_fava_cv` and copies
that exact PDF to `resume/docs/marco_del_fava_cv.pdf`. It also builds the
`engineering` profile into `marco_del_fava_engineering.pdf` and generates
`evidence.html` from explicitly public inventory records. Neither PDF is
published if either build fails. A custom publication directory can be selected
with `--output-dir`.

The homepage uses ordinary hash links and needs no JavaScript. Three featured
engineering cards precede research affiliations and answer what was built,
tested, observed, and where the evidence lives. Visuals are architecture diagrams
and charts redrawn from aggregate results, not stock images or recording-derived
waveforms. The download links are the authoritative paginated documents; browser
printing is a readable portfolio, not a substitute for their page-count checks.
Header profile links use official GitHub and LinkedIn emblems plus full,
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

Each selected project has an `id`, `name`, `problem`, two `bullets`, `maturity`,
`status`, `evidence_ids`, and `links`. Featured projects also have a `tested`
description. The compact profile selects the same three project records and
claims as the full CV, without supporting prototypes, repeated project links,
or certifications. Compact PDF text is 10.5 points with 12-point leading and the
same 0.7-inch margins; the full CV retains 11/13-point typography.

### Evidence inventory and publication boundary

[evidence_inventory.yaml](resume/data/evidence_inventory.yaml) is an internal
generator input, not a copied public artifact. Keep it safe for source control:
no credentials, source recordings, patient identifiers, private code excerpts, or
local laboratory paths. Each record identifies the repository, exact file/cell,
commit, measurement definition, conditions, reviewed result, verification method,
and limitations. Projects refer to records by `evidence_ids`. The generator
rejects missing/unpublished evidence references and public records without
full-length commit revisions. Only records marked `public: true` may enter the
site, public evidence report, and filtered JSON.

Maturity labels describe the scope of the evidence, not deployment readiness:

- **Validated:** an evaluation with inspectable archived results. The report
  explicitly says when the review did not rerun original recordings.
- **Implemented:** source-inspected software; no numerical performance implied.
- **Prototype:** implementation without demonstrated acquisition or online
  performance.

The DHN fidelity result is **not bit-exact relative to unrounded CSC**. Mean error,
compression ratio, file-size reduction, and encoder configuration behavior were
not established by the reviewed outputs and are not claimed. The exact spike
match is a rounded-input control, not proof that unrounded conversion preserves
all sorted units.

Waveform-feature results distinguish 95.04% KNN-k5 neighborhood purity from
54.26% Hungarian-matched KMeans accuracy (ARI 0.3665), on 38,145 snippets with
10 putative O-Sort labels. These are offline label-agreement metrics, not
biological ground truth, held-out classification accuracy, or streaming latency.

The private Intan timing implementation was inspected, but the reported
recording-level measurements and bench-test channel count had no source logs or
report in the inspected revision. At Marco's direction those numbers are omitted.
The timing model fits relative RHX sample indices against monotonic flip-callback
time; signed residuals use the fitted slope, while P95 and maximum use absolute
residuals. Neither is physical stimulus-onset jitter or closed-loop latency.
No private repository link, raw timing log, bench recording, or waveform figure
is exported. Aggregate charts were approved; recording-derived imagery was not.

Enrollment since Fall 2026 and the research-volunteer affiliation since July 2025
were confirmed by Marco. No graduation date or formal research appointment is
inferred. The former unsubstantiated waveform-count and curation-efficiency claims remain
omitted. The new snippet count is scoped specifically to the public offline
feature report, not overall data processed or a curation improvement.

### Publishing

[The single Pages workflow](.github/workflows/deploy.yml) tests the generator,
builds the website and both PDFs into `_site` from the checked-out commit, and uploads
that exact directory using the official Pages artifact/deployment actions.
Set repository **Settings → Pages → Source → GitHub Actions**. The former
competing `gh-pages` publisher has been removed. No output is selected by
modification time, and no shell substitution is passed as an action input.
Local generation does not deploy the site; review, commit, and push separately.
GitHub evidence paths were checked at their pinned revisions and Credly returned
HTTP 200 during this update. LinkedIn returned HTTP 999 to automated requests;
its profile remains a manual browser verification item.

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
