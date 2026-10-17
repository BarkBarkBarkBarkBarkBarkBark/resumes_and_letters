# Neuroengineering experience and goals

Updated October 17, 2026. This is the working record for future applications and
coding agents. The application text lives in `../data/base_resume.yaml`; this
record explains the evidence, scope, and next milestones behind it.

Marco's target work connects neural acquisition, preprocessing, real-time
interpretation, and validation. The strongest current positioning is a research
engineer or scientific software developer with human single-unit experience,
hands-on acquisition integration, and a professional background in technical
operations. Real-time decoding and adaptive semantic screening are active
development directions.

## How to use the record

Use past tense for implemented work and present tense for work currently underway.
Use "develop," "prototype," and "investigate" to describe active work confidently.
A goal becomes an accomplishment when its evidence exists. An implemented
prototype does not by itself establish reliable live acquisition, clinical use,
decoder accuracy, or a measured latency bound.

Evidence types below distinguish the current user's report, prior project
discussions, the existing resume, and project documentation. The resume build
checks formatting and selection; it does not independently certify experiments.

## Experience inventory

| Area | Status and evidence | Employer-facing wording | Scope to preserve |
| --- | --- | --- | --- |
| UC Davis training | Enrolled in Biomedical Engineering M.S., neuroengineering track, September 2026; current user report and project context. B.S. Neuroscience, Physiology, and Behavior, UC Davis, 2017; M.S. Psychology, ASU, 2023; existing resume. | Biomedical Engineering M.S. student working in Dr. Jie Zheng's Z-Lab. | Degree is in progress. No expected graduation date is established. |
| Human microwire analysis | Ongoing since July 2025 Z-Lab volunteer role; existing resume and current report. Neuralynx data from Behnke-Fried microwires; SpikeInterface, MountainSort5, Kilosort4, and O-Sort workflows. | Process and sort human intracranial single-unit recordings; examine waveform structure and downstream responses. | Preserve volunteer title until a formal appointment changes. Analysis of an existing dataset does not imply personally collecting it. |
| Intan and DeepArray | Completed bench work with continuing integration; retrieved lab-testing context, October 5-9, 2026. Marco co-led 128-channel testing; the lab reported 121 clean test-signal channels, channel-map agreement, and expected behavior of problematic channels. | Co-led 128-channel DeepArray/Intan bench testing, including channel mapping, grounding, filtering, and channel-quality troubleshooting. | Attribute 121/128 to this lab test. It is not human single-unit yield, sensitivity, or a general hardware specification. |
| Experimental timing | Implemented timing tools with ongoing integration; prior project reports describe PsychoPy/RHX TCP/LiveNotes annotations and Cedrus C-Pod TTL integration. | Develop experiment synchronization and characterize clock drift and event-alignment residuals. | Software timestamps, recording-clock alignment, and physical stimulus onset are different measurements. No submillisecond claim is established. |
| Neuralynx to MED comparison | Completed comparisons, ongoing diagnosis; prior reports describe approximately 1-3% spike disagreement and investigation of rounding/precision. | Compare CSC and MED-derived processing to investigate conversion precision and downstream spike-detection discrepancies. | The discrepancy is not a validated converter error rate or evidence that compression is lossy. Quantization is an investigated explanation. |
| Noise and recording stability | Prior project discussions include an approximately 150 Hz periodic artifact with harmonics, common-reference concerns, and interest in long-recording quality changes. | Investigate acquisition artifacts and how preprocessing choices affect single-unit analysis. | No established artifact source, completed long-duration drift study, or proven noise-removal performance is documented. |
| Repeated-story analysis | Implemented Python workflow; October 16-17 user report. Dataset: 10 participants, seven 30-second stories, six repetitions each. Inputs are sorted units and event markers; output includes PSTHs. | Built event-aligned single-unit analysis and reproduced an event-associated response in the same unit across six repetitions. | Responses occurred within a continuous narrative. No independent words or balanced semantic stimulus battery were presented. |
| Response-based pipeline checks | Current work, explicitly reported in this request. A previously identified repeat-responsive unit provides a reference case for analysis. | Check pipeline behavior against known repeatable response patterns in recorded data. | This is a regression/reference case, not independent ground truth for spike identity or proof of concept specificity. |
| NEURON semantic tuning | Implemented simulation prototype, confirmed by current user report and `semantic_neuron` documentation. Sentence similarity controls stochastic synaptic input to one Hodgkin-Huxley compartment with fixed synaptic weights. | Built a seeded NEURON prototype linking embedding similarity to synaptic input and spiking output. | Semantic selectivity is imposed through the input mapping. It is not an emergent semantic representation or validated human-cell model. |
| Dark Horse Neuro integration | Implemented orchestration components and ongoing hardware integration; `dhn_client` documentation and prior troubleshooting. RC/CS writers, SSH launch, diagnostics, NetCom integration, and NRD-to-UDP prototype. | Develop Python tooling for Neuralynx/Dark Horse Neuro acquisition configuration, launch, diagnostics, and replay. | Earlier synthetic streaming succeeded; NRD reception/recording remained unresolved in retrieved reports. Do not call this validated clinical acquisition or completed replay. |
| Waveform discrimination | Existing resume records `spike_discrim`, Numba WeightBank representations, and benchmark tooling. | Prototype waveform representations for spike discrimination and clustering research. | Benchmark metrics and code are not established clinical accuracy or measured end-to-end latency. Keep secondary until artifacts are reviewed. |
| Streaming SNN sorting | Existing resume records experimental `SNNeuro` filtering, gating, STDP, and monitoring code; current user describes real-time pipeline work. | Develop experimental streaming spike-processing tools. | Do not assert validated live single-unit identity, all advertised input formats, or closed-loop human deployment. |
| AI-assisted scientific coding | Current user report and prior project work. Uses coding agents to implement Python pipelines and examines recorded outputs. | Use AI coding agents to accelerate development and evaluate results against experimental reference cases. | Report implemented checks. Automated tests, code review, held-out evaluation, and independent ground truth are distinct evidence. |
| EMU exposure | Existing resume: UC Davis Health Neuroscience Unit E5, December 2022-July 2023. Prepared headboxes and EEG kits, shadowed technologists and observed clinical procedures. | Supported EEG preparation and observed clinical neurophysiology in the EMU. | No EEG technologist credential or independent clinical interpretation is claimed. |
| OR access and acquisition | Working toward OR/UC Davis Health access and participation; October 2026 access requests and current user report. | Contribute to acquisition preparation for planned human neurophysiology experiments. | Access preparation and bench work are not completed intraoperative cases or independent operation of a clinical recording system. |

## Professional experience that supports the transition

**Additional training.** The existing resume records the UC Davis Continuing and
Professional Education Python for Data Science professional concentration in
2025, with a reported 4.0 GPA, plus the Data Analysis with Matplotlib, Pandas, and
Scikit-Learn badge. CITI training includes Biomedical Research, Essentials of
Research Administration, and GCP Social and Behavioral Research Best Practices.
The engineering resume keeps the relevant badge and research training under
certifications rather than presenting the concentration as another degree.

**First Step Communities, Operations Specialist, July 2021-present.** Existing
resume documents Python/SPSS/Excel analysis, outcomes reporting, clinical-partner
data coordination, 40+ standardized forms, workflow automation, and multi-site
Microsoft 365 administration. Recent work also includes network segmentation,
wireless connectivity, camera/NVR integration, and device troubleshooting. For
engineering applications, emphasize operational reliability, integration,
requirements gathering, documentation, and communication with nontechnical users.
The exact organization-wide counts vary by period; retain dated context when using
site or service-volume metrics.

**Clinical-services outcomes research.** Current collaboration with Jeffrey Hoch
and a medical student examines whether clinical social-worker engagement is
associated with housing outcomes. Working data context includes approximately
500,000 service records and 6,000 enrollments. Matching/propensity methods and a
first-author manuscript are being developed. Do not describe this as a published
paper or an established causal intervention effect.

**Eurofins Test America, Analyst, October 2019-June 2021.** Existing resume records
solvent extraction, high-throughput sample workflows, QA documentation, data
review, and standard operating procedures. This supports test and validation
roles through practical laboratory discipline. It does not establish medical
device design-control or regulatory-submission experience.

**California Home Builders Association, Research Intern, July 2023-February
2024.** Existing resume records shelter-village cost estimation and policy
communication. Useful for research coordination and analytical communication;
secondary on a neural engineering resume. Organization/title spelling should
follow employment records when tailoring an application.

**Independent software and embedded projects.** Hosaka, TalkBox, and the Scientific
A.I. Workstation show continued work with Linux, Raspberry Pi/Jetson, interfaces,
and agent-assisted development. Link one relevant project when its installation,
behavior, and demonstration are reproducible. They do not establish FPGA, RTOS,
embedded C/C++, or production inference expertise.

## Specific measurements and interpretation

The reported same-computer timing tests are useful engineering evidence, including
their limitations. Retain the underlying event logs and analysis before quoting
them in an application or portfolio.

| Reported run | Clock estimate | Alignment residuals | Interpretation |
| --- | --- | --- | --- |
| Approximately 3 minutes, 142 events | 19,991.371 samples/s, -431 ppm from nominal 20 kHz | Median -0.476 ms; P95 22.29 ms; maximum 28.60 ms | Demonstrates measurement of clock mismatch and event alignment; not proof of low-latency physical stimulus timing. |
| Approximately 18 minutes, 883 events | 19,997.824 samples/s, -108.8 ppm | Median -4.643 ms; P95 76.42 ms; maximum 98.62 ms; approximately 4-second gap near trials 70-71 | Longer runs exposed drift/discontinuity concerns. Do not report only the short-run median. |

For the repeated story, the response was reported near both mentions of
"sexually aware," in the same unit across the six runs. The reporting criterion
required an increase in a majority of trials. Whether the drive is the phrase,
"aware," acoustics, context, or narrative position remains open. Record the
statistical test, baseline, response window, multiple-comparison correction,
and selection procedure before making a formal significance claim. Reusing a
discovered responsive unit checks software consistency; reserve separate data
for generalization claims.

The [Semantic Neuron documentation](https://github.com/BarkBarkBarkBarkBarkBarkBark/semantic_neuron)
reports seeded repeatability and zero-weight controls, but also documents classic
HH temperature, a single compartment, and imposed similarity-dependent input.
Its best employment value is a transparent test system for a research hypothesis.
The [Dark Horse Neuro orchestration documentation](https://github.com/BarkBarkBarkBarkBarkBarkBark/dhn_client)
supports component implementation, with integration status kept separate.

## Active goals and the evidence needed to promote them

Previously discussed design targets include 30 kHz, 24-bit, 32-channel processing
and detection-to-trigger latency below 5 ms, plus scaling from current
128-channel acquisition work toward larger systems. These are design targets,
not measured supported capacity or latency. Jetson deployment and later FPGA
implementation are development interests. Keep coding-agent demonstrations on
synthetic or institutionally approved data.

| Goal | Honest current wording | Evidence for an accomplishment claim |
| --- | --- | --- |
| Repeatable acquisition bring-up | Developing a documented acquisition and channel-quality workflow. | Channel map, acquisition configuration, test-signal recordings, defect/noise log, and successful repeat runs. |
| Reliable synchronization | Characterizing timing and integrating hardware event markers. | Simultaneous marker recordings; explicit clocks; measured alignment, jitter, drift, discontinuities, and repeat runs. Add a physical onset sensor when claiming stimulus-onset accuracy. |
| Source-format consistency | Investigating CSC/MED processing discrepancies. | Matched channels/samples/timestamps, documented scaling and precision, controlled reprocessing, and explained detection differences. |
| Streaming detection and interpretation | Developing a replay-to-stream processing prototype. | Paced replay, known injected events, throughput and latency distributions, dropped-data/backlog checks, and comparison with offline results. |
| Adaptive semantic screening | Developing adaptive stimulus selection to characterize single-unit tuning. | Predefined response criteria, repeat confirmation, held-out stimuli/trials, comparison with random or fixed screening, and response-versus-presentation-budget results. |
| Memory reinstatement prediction | Planning content-specific reinstatement analysis. | Independent labels, appropriate subject/session splits, baseline comparisons, uncertainty, and held-out predictive performance. |
| Closed-loop intervention | Planning experiments linked to detected or predicted activity. | Working detection-to-trigger chain plus required clinical approvals and supervised experimental evidence. No completed intervention is currently established. |
| OR data collection | Preparing for participation in human intraoperative recordings. | Actual participation, documented responsibilities, supervisor confirmation, and permission to describe aggregate outcomes. |
| Agent-assisted validation | Building checks around AI-assisted scientific implementation. | Versioned reference fixtures, reproducible commands, expected results, deliberate failure cases, and artifacts reviewers can inspect. |

## Claims retained as historical resume material

The older canonical resume reports approximately two million hand-labeled
waveforms, neural-network spike/noise classification, GPU sorting on AWS, and
several streaming/benchmark features. Preserve them as reported experience, but
do not turn them into measured performance improvements without dataset lineage,
evaluation results, or a reviewed demonstration. They remain available in the
source data and are secondary to better-supported recent acquisition and
response-analysis work.

No current record establishes clinical deployment, a production BCI decoder,
hard real-time guarantees, FPGA development, C/C++ proficiency, an accepted
SpikeInterface contribution, or a published thesis/manuscript.

## Updating this record

Add a date, status, concrete personal contribution, repository/artifact link,
measurement context, and remaining limitation for each new accomplishment.
Update the corresponding canonical YAML bullet and rebuild the role profiles.
Keep planned capabilities here until an implementation or measurement supports
stronger language. The application should read confidently without asking the
reader to infer that a prototype is already a deployed system.
