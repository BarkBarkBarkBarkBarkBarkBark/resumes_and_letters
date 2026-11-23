# Neuralink Software Engineer Intern, Implant — application kit

Position: https://job-boards.greenhouse.io/neuralink/jobs/6569018003

## Submission checklist

1. Edit the native Google Doc: https://docs.google.com/document/d/1o7HNRSzbu9Src2gc_PdyeC9Y6yheVhnN1qzOCH-eoZU/edit
2. In Google Docs choose File > Download > PDF Document (.pdf), or run the repository PDF builder on the Markdown source.
3. Submit the PDF with the **engineering** (one-page) resume or research CV, depending on the available attachment fields.
4. Paste three concise, independently substantiated accomplishments into the application form's **Evidence of exceptional ability** fields. These matter more than the cover letter according to the posting.
5. Complete work authorization, graduation year, desired internship season/start date and South San Francisco on-site questions accurately. The job is on-site and the posting says no relocation assistance for interns.

## Proposed evidence-of-exceptional-ability answers

These are bounded examples, not claims of device-level verification or human clinical validation. Check every figure before submitting.

**1. Measured recording conversion integrity.** Evaluated source-to-MED numerical fidelity over 20,000,000 samples from one channel recorded at 32 kHz. The maximum absolute amplitude difference was 0.5 µV; after rounding the source to whole microvolts, the two arrays had zero mismatches. Documented the comparison conditions and what the single-channel test does *not* demonstrate.

**2. Recovered difficult acquisition recordings.** Built a Neo-backed adapter for SpikeInterface that bypasses malformed Neuralynx MED channel metadata that otherwise prevented successful file reads. The adapter filters the affected channels before header parsing while preserving sampling-stream and channel-gain metadata, allowing valid channels to enter an ordinary analysis pipeline. This is a reader and data-integrity fix, not a new compression algorithm.

**3. Diagnosed and regression-tested a software bottleneck.** Traced an approximately 70-second command listing seven records to repeated schema validation during development of Hosaka. Added content-based caching and regression checks to avoid unnecessary repeated validations while checking modified or invalid schemas. The 70-second figure is a pre-fix observation, not a measured post-fix speedup.

A fourth optional example could describe Intan RHD loading, channel/probe checks, filtering, spike sorting and waveform quality metrics, but it has no defensible throughput or validation metric on the current public evidence page. Prefer the three above rather than padding the application.

## Job-to-evidence mapping

- **Design-control verification testing software / manufacturing acceptance:** controlled comparison and documented limitations from MED validation, regression checks from Hosaka.
- **Recorder and monitoring systems:** Intan and Neuralynx acquisition formats, Python and Linux tooling, replay and metadata handling.
- **Production vs research:** observability, repeatable tests, boundary-condition handling, and refusing to generalize a one-channel test to a whole implant.
- **Python, Linux/Unix:** demonstrated; **C or Rust** is requested, but the repository does not substantiate fluency. Do not claim it.
- **Safety-critical software experience:** preferred but not established; say you want to learn regulated-device practices, not that you have medical-device design-control experience.

## Build and test

From repository root with Python 3.9+ and Pandoc installed:

```bash
python -m unittest discover -s applications/neuralink_implant -p 'test_*.py' -v
python applications/neuralink_implant/export_pdf.py
```

The builder runs Pandoc with pdflatex, checks that the produced PDF exists and starts with a PDF signature, and writes to `applications/neuralink_implant/dist/neuralink_implant_cover_letter.pdf`. Install `pandoc` and `pdflatex` first. For the editable canonical version, Google Docs is preferable; its File > Download > PDF route exports the currently edited document, whereas this GitHub builder exports the version-controlled Markdown.

## Technical sources

- [Measurement scope and limitations](../../resume/data/evidence_inventory.yaml)
- [Existing cover-letter generator](../../resume/scripts/build_cover_letter.py)
- [Existing research CV](../../README.md)
