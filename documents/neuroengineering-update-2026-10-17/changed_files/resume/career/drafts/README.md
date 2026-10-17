# Application drafts

These drafts were generated from the canonical YAML on October 17, 2026.
Select and tailor a profile for a specific employer before submitting it.

- `marco_del_fava_resume_neuroengineering` is the general research-engineering
  resume, with Markdown, Word, and PDF versions.
- `marco_del_fava_resume_neural_data.md` emphasizes scientific software and data.
- `marco_del_fava_resume_acquisition_validation.md` emphasizes bench testing,
  acquisition integration, and timing.
- `cover_letter_*.md` are examples for a generic Neurotechnology Team. Replace
  the recipient and role through the build arguments and customize the
  employer-specific motivation. No applications have been submitted.

From the `resume/` directory:

```bash
python scripts/build_resume.py --profile neuroengineering --md-only
python scripts/build_resume.py --profile neural_data --md-only
python scripts/build_resume.py --profile acquisition_validation --md-only
python scripts/build_cover_letter.py --company "Company Name" --role "Research Engineer" --profile neuroengineering --md-only
```

Markdown outputs land in `output/`. For Word, the normal resume build uses
`templates/reference.docx` with Pandoc. That reference can be regenerated with
`python scripts/build_reference_docx.py` after installing `python-docx`.
The reviewed PDF here was exported from the Word draft, so both share a layout.
Copy regenerated outputs into this directory when refreshing the committed drafts.
