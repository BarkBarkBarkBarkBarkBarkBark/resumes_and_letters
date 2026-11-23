"""Unit tests for the Neuralink application PDF exporter and factual scope."""
from pathlib import Path
import importlib.util
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("export_pdf", HERE / "export_pdf.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class CoverLetterTests(unittest.TestCase):
    def test_letter_contains_role_and_specific_evidence(self):
        text = (HERE / "cover_letter.md").read_text(encoding="utf-8")
        for phrase in ("Software Engineer Intern, Implant", "20 million", "0.5 µV",
                       "one channel", "three-month", "regression"):
            self.assertIn(phrase, text)

    def test_no_unsubstantiated_claims(self):
        text = (HERE / "cover_letter.md").read_text(encoding="utf-8").lower()
        for phrase in ("fda approved", "certified", "100% spike", "c/rust expert",
                       "medical-device verification experience"):
            self.assertNotIn(phrase, text)

    @patch.object(mod.shutil, "which", return_value="/usr/bin/fake")
    @patch.object(mod.subprocess, "run")
    def test_export_command_and_pdf_signature(self, run, which):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "cover_letter.pdf"
            def write_pdf(args, **kwargs):
                self.assertIn("--pdf-engine=pdflatex", args)
                self.assertTrue(kwargs["check"])
                out.write_bytes(b"%PDF-1.7\n" + b"x" * 128)
            run.side_effect = write_pdf
            self.assertEqual(mod.build_pdf(destination=out), out)

    @patch.object(mod.shutil, "which", return_value=None)
    def test_missing_dependency_fails_closed(self, which):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(RuntimeError, "Missing pandoc"):
                mod.build_pdf(destination=Path(tmp) / "a.pdf")


if __name__ == "__main__":
    unittest.main()
