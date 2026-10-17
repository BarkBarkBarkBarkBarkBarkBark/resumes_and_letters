# Neuroengineering resume update

Prepared October 17, 2026 for Marco Del Fava.

The GitHub connection allowed repository reads but rejected a write with HTTP
403 Resource not accessible by integration. No remote branch, pull request, or
website update was created. These files contain the completed local update.

Repository: https://github.com/BarkBarkBarkBarkBarkBarkBark/resumes_and_letters
Base commit: a2df8798a79966bfd71896beb8037c9281a46995
Local update commit: 29ebe4f
Proposed branch: career/neuroengineering-2026-10-17

## Contents

The patch carries all 27 changed or added files, including binary Word and PDF
assets. The changed_files directory mirrors their repository-relative paths.
It includes three targeted resume profiles and example letters, a two-page
reviewed Word/PDF resume, a detailed experience/goals inventory, and a role
strategy grounded in employer requirements.

## Apply with a local coding agent

Work in a clean clone or worktree of the repository. Create the proposed branch
from main and apply the included patch with git am --3way. Do not overwrite
uncommitted work. Resolve any conflicts against the current source YAML and
retain newer user edits. Run python -m pytest resume/tests -q from the repository
root, then rebuild the required profiles from resume/.

The update passed 32 build tests. All six profiles rendered, three example
letters rendered, and both Word/PDF resume pages were visually inspected.
These checks validate the resume system and document layout; experimental
results retain their stated evidence and limitations in the inventory.

## Suggested pull request

Title: Update neuroengineering resumes with acquisition and validation experience

The previous resume described incoming M.S. status and emphasized experimental
sorting prototypes. This update leads with current UC Davis enrollment,
128-channel DeepArray/Intan bench work, human single-unit processing, experiment
synchronization, and response-based pipeline checks.

Adds three role profiles, corresponding letters, reviewed application drafts,
and an inventory separating completed work from ongoing development and goals.
Keeps acquisition/replay and real-time clinical performance at their documented
stage. Validation: 32 tests pass; all profiles/letters rendered; two-page Word
and PDF layouts inspected.
