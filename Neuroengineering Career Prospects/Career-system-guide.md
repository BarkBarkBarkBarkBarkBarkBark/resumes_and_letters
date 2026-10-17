# Active Mac-sync configuration — updated 2026-10-17

The authoritative prospects destination is the existing Mac-synced **Neuroengineering Career Prospects.xlsx** (Drive ID `1OfabvpCFAgig-derS6QzmVIdZLh6MHOO`) in https://drive.google.com/drive/folders/1lyhqMqGog6ACG6pCwGJnM7_01YqqOLjZ. The BCI Job Watch task now points here. Keep this file as Excel. Fetch the latest bytes, edit with the Spreadsheets skill, then replace the same file using Drive update_file. Recheck modification time before replacement and verify the saved file afterward. Do not update the former native Sheet or create a second master. The associated skills JSON remains at the existing linked Drive file until it is explicitly migrated.

Each run also updates alumni and core technical contacts from LinkedIn/public professional sources, including when there are no new jobs. Record `contact_type=uc_davis_alumni`, `core_technical`, or `both` in People.notes. Leave unverified education, titles and emails blank or clearly labeled. Profile expertise is not automatically an employer requirement or a skill the user possesses. Preserve the existing notification policy and do not send outreach.

---

# Neuroengineering career prospects

The working directory is [Neuroengineering Career Prospects](https://docs.google.com/spreadsheets/d/1OfabvpCFAgig-derS6QzmVIdZLh6MHOO/edit?usp=drivesdk&ouid=117259898969272321259&rtpof=true&sd=true). The [Drive folder](https://drive.google.com/drive/folders/1lyhqMqGog6ACG6pCwGJnM7_01YqqOLjZ) groups the directory, skills catalog and handoff files.

## One owner for each kind of information

| Information | Editable master | Relationship |
|---|---|---|
| Companies, people, jobs, interviews and outreach | Mac-synced Excel workbook | Stable IDs connect records across tabs. |
| Experience and evidence for each skill | [Drive skills JSON](https://drive.google.com/file/d/1A12E9qnKHaKAgozwAzKb7y9CePyw88FJ/view?usp=drivesdk) | Keep the existing 875 skill IDs and schema. |
| Published resume and recruiter-facing evidence | Existing resume repository and project repositories | Publish reviewed claims and GitHub evidence links from the skills catalog. |
| Downloadable prospects JSON | Export snapshot | Refresh from the workbook before editing or importing. It is not a second editable master. |
| SkillIndex tab | Reference snapshot | Regenerate from the skills JSON. Do not edit experience here. |

This setup does not install a background bidirectional Drive/GitHub sync. The scheduled job agent maintains the synced Excel workbook. Project updates change the authoritative skills JSON, then an agent can publish the reviewed result to the resume repository. Replacing the Drive JSON must preserve its file ID. Avoid simultaneous writers, reread immediately before replacement and preserve unrelated edits.

## Record structure

| Tab / JSON key | Primary key | Purpose |
|---|---|---|
| Companies / companies | company_id | Business focus, careers page, public general contact, interview route, refresh date. |
| People / people | person_id | Company association, exact role when verified, UC Davis evidence, LinkedIn, public professional email and source. |
| Jobs / jobs | job_id | Official posting, role, location, pay, experience threshold, work mode and animal-work expectations. |
| JobSkills / job_skills | job_skill_id | One job-to-skill mapping per row, with required/preferred/responsibility/example/alternative classification. |
| Interviews / interviews | interview_id | One skill insight per row from an actual conversation, including how to demonstrate it. |
| Outreach / outreach_events | event_id | Append-only history of actual requests, replies, meetings and follow-ups. |
| Projects / learning_projects | project_id | Proposed or active work, skill IDs, acceptance evidence and eventual GitHub links. |
| SkillProposals / skill_proposals | proposal_id | Unmatched employer terms awaiting alias/category review. No experience is implied. |
| Runs / run_log | run_id | What the recurring agent read, added or failed to save. |

Use UUIDs for new person, company, interview, project and event IDs, with the existing type prefix. Existing readable seed IDs remain unchanged. For jobs, prefer employer plus ATS posting ID. Deduplicate people by normalized LinkedIn URL and companies by canonical website domain. A person changing employers keeps their person_id. Before changing company_id, preserve the dated previous affiliation in the person's notes. A job posting disappearing becomes closed or unverified; do not delete its requirements history.

Blank means unknown. A published professional email needs the page on which it was explicitly published. Never infer email patterns or use a contact broker's masked email. General company inboxes belong to Companies, not People. A matching company-filter result is a lead, not proof of an exact role or hiring authority. Historical and unverified associations stay labeled. The seed list is a starting set, not a full employee directory.

## Daily job agent

Keep the existing BCI Job Watch schedule and notification behavior. On each run:

1. Read metadata and the relevant ID columns before writing. Resolve exact tabs and headers. Use bounded ranges and preserve formulas, formatting and user notes.
2. Search official employer postings. Upsert new jobs by employer/ATS ID. Retain first_seen_at and refresh last_verified_at. Mark genuine closures only after checking the official source; access failure is not closure.
3. Map each job requirement to an existing skill_id. Required and preferred qualifications differ from responsibilities and format examples. Preserve one-of language alternatives in alternative_group.
4. Add unfamiliar terms to SkillProposals rather than making near-duplicate skills. Do not alter proficiency, accomplishment statements, evidence or resume eligibility based on a job advertisement.
5. On every run, research up to three UC Davis alumni or core technical people in neurotech, even without new jobs. Prioritize alumni, acquisition and neural-data engineers, BCI software engineers, research scientists, technical leads and relevant hiring managers. Distinguish alumni from non-alumni and cite the current role. Use LinkedIn to resolve identities and record a specific informational-interview topic. Retain sources and uncertainty. An unverified lead can be useful without being called a confirmed current employee.
6. Write updates and a run-log entry, then read back the changed records. Report unsaved changes accurately. Keep the existing meaningful-new-job bulletin behavior. Do not send outreach or apply for jobs.

## Project-to-skills updates

When an implementation is complete, record the repository, commit-pinned code/test/report links, measurement conditions and limitations. Review exactly which skill IDs it supports. Update skill, status, evidence_ids and resume_text to match that evidence. Source review demonstrates that code exists; it does not prove a runtime, hardware or biological claim. A proposed project remains proposed until there is an implementation.

Use resume_include explicitly. Set recruiter_visible only when an eligible claim has a checked public evidence document. Preserve scope such as prototype, replay, bench, live hardware and maintained deployment. Do not infer all related skills from one implementation. Merge new taxonomy entries from SkillProposals only after checking existing IDs and aliases; new entries start empty and resume_include=false.

## Informational interview strategy

Start with two carefully researched requests per week. Lead with the shared UC Davis connection, current master's work and one concrete question about the person's verified work. Ask for 15–20 minutes. Ask for advice before asking for a referral.

- Which two or three skills make a new engineer useful in the first 90 days?
- What project, benchmark or code artifact would convince you someone can do that work?
- What acquisition, preprocessing or real-time failures do strong engineers know how to diagnose?
- Which of my projects would you deepen, and what would you learn next?
- Which team handles human recordings or software without requiring large-animal experimental work?

Afterward, record each skill insight separately with its skill_id, whether it is a paraphrase or your interpretation, a suggested project and acceptance evidence. Build one useful proof of ability, then follow up with the result. Do not publish private conversation notes or attribute quotations without permission.

The practical goal is three strong demonstrations: reliable recording-to-response analysis; a measured streaming/replay pipeline; and one validated model or adaptive experiment. Let actual team feedback determine which deserves the most effort. The full taxonomy is a reference, not a demand to learn 875 skills.

## Initial findings and limitations

The initial set contains seven companies, six alumni or alumni leads, four observed postings, 35 job-skill mappings and four proposed projects. Elias Hamlin and Yi Lu are Neuralink profile leads; exact current titles remain unavailable. Kushaal Rao has a university-documented UC Davis connection; his reported Bridge affiliation needs confirmation. Kimiko Nakajima is a historical Paradromics alumni lead, with current employment unconfirmed. Roman Kazantsev's UC Davis connection is a secondary-source lead needing primary verification. No personal email was verified in the reviewed sources.

Neuralink's observed full-time Next Gen posting asks for four or more years of academic or industry experience. Its preferred methods include NEURON, stimulation modeling and instrumentation. Its internship explicitly includes NHP experiments and lists $35/hour. The directory preserves these constraints instead of treating every neuroengineer title as the same job.

## Programmatic checks and exports

Arrays in Sheet cells use JSON array syntax. Dates in JSON use ISO strings; workbook dates are typed dates. Empty cells export as empty strings or null according to the schema. Ignore the Start tab for record ingestion and regenerate SkillIndex from the canonical skill catalog.

Validate a full JSON export before importing or using it to update the resume workflow:

```bash
python validate_prospects.py prospects.json neuroengineering_skills.json
```

The validator checks duplicate IDs, company/person/job/skill references, duplicate LinkedIn and job URLs, alternative groups, public-email provenance and empty skill proposals. It also applies prospects.schema.json if jsonschema is installed. Schema validity is a structural check, not factual verification. Reread latest synced workbook before every update; never restore this seed snapshot over newer entries.

The package includes the initial JSON export, schema, validator, automation instructions and the existing skills schema. It excludes patient data, private correspondence and any purported interview that has not happened.

