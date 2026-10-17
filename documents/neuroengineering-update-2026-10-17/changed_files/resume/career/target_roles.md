# Neuroengineering application strategy

Reviewed October 17, 2026. Role rankings below are judgments about fit, not hiring
probabilities. Prioritize employers and teams where the daily work uses human
electrophysiology, Python, acquisition integration, and validation.

## Positioning

Lead with the ability to connect a neural recording system to interpretable,
checked single-unit results. Pair acquisition experience with event alignment,
data handling, and evidence that software preserves the response being studied.
Describe AI-assisted coding through the engineering decisions and validation
that Marco owns.

## Role families and resume variants

| Priority | Job titles to search | Why the experience fits | Profile |
| --- | --- | --- | --- |
| First | Research Engineer; Research Software Engineer; Scientific Programmer; Neuroinformatics Engineer | Human neural data, lab workflows, Python tooling, sorting and PSTHs, experiment integration, and communication with researchers. | `neuroengineering` |
| First | Neural Data Engineer; Scientific Software Developer; Neural Signal Processing Engineer with a Python/data emphasis | Neuralynx/MED handling, SpikeInterface, response checks, event alignment, Linux and automation. Prefer roles that allow development of production software depth. | `neural_data` |
| First | Acquisition Engineer; Research Systems Engineer; Test Engineer; Scientific Applications Engineer; Technical Support Engineer in electrophysiology | DeepArray/Intan bench testing, channel troubleshooting, timing work, laboratory QA, and years supporting operational technical systems. | `acquisition_validation` |
| Selective stretch | BCI Software Engineer; Real-Time Neural Processing Engineer | Relevant acquisition and analysis context with active streaming prototypes. Establish compiled-language ability, performance measurements, and robust interfaces as required by each posting. | `neural_data` |
| Later | Embedded DSP Engineer; FPGA Engineer; Senior BCI/ML Engineer | Current work is adjacent, but the record does not establish embedded production experience, FPGA implementation, senior engineering ownership, or validated decoder performance. | Build evidence before retitling experience. |

Keep remote scientific software/data roles in the search. Acquisition and clinical
hardware positions often specify an on-site location or travel; the concrete
examples below do so. Remote remains a preference, not assumed availability.
The prior compensation goal is at least $40/hour, approximately $83,200/year
at 2,080 paid hours. Verify salary, schedule, student compatibility, travel,
and any animal-work requirement for each opening. Avoid roles requiring hands-on
large-animal experiments. These examples are skill benchmarks, not a declaration
that each satisfies all personal constraints.

## Employer evidence

The following are primary employer postings or employer-hosted documents checked
during this update. Titles and requirements are summarized; verify availability
before applying.

| Example | Relevant requirements | Fit and remaining gap |
| --- | --- | --- |
| [Blackrock Neurotech Neural Data Infrastructure Engineer](https://ats.rippling.com/en-CA/blackrockneurotech/jobs/91ebe665-8784-4195-aae8-03031f7c3f6e) | Acquisition metadata, channel mapping, timestamps, preprocessing, spike processing, drift/artifact checks, versioned datasets, Python and software reliability. On-site Salt Lake City. | Very close match in subject matter. The posting also expects independent operation of large scientific pipelines, strong Python engineering, scientific storage formats, and relevant industry experience. Treat the particular opening as a stretch and a useful skill map. |
| [Paradromics Software Engineer](https://paradromicsinc.applytojob.com/apply/r7CgYCDBNk/Software-Engineer) | BCI data curation, performant decoding software, simulated/real neural-data evaluation, hardware-in-the-loop work, Python plus Rust/C++/C, and three or more years of relevant professional experience. Oakland with regular Austin/Oakland travel. Posted base range $120,000-$150,000. | Good connection to recorded/simulated data and validation. Compiled-language experience, relevant software tenure, and hardware-in-the-loop implementation remain material gaps. Existing nonprofit tenure does not automatically satisfy three years of BCI software engineering. |
| [NeuroNexus Technical Support Engineer](https://www.neuronexus.com/wp-content/uploads/2024/08/Technical-support-engineer-NeuroNexus.pdf) | Probe/hardware/software troubleshooting, microelectrode arrays, acquisition, signal processing, Python/MATLAB, technical documentation, and customer communication. Ann Arbor. | Strong bridge between neural lab work and professional technical support. This is a historical employer-hosted PDF in a 2024 path; current hiring status is unverified. Use the role family, not an assumed live vacancy. |
| [Neuralink Signal Processing Engineer](https://job-boards.greenhouse.io/neuralink/jobs/6681863003) | Neural spike detection and electrode health, on-chip DSP, fixed-point/quantized algorithms, architecture tradeoffs, and three or more years in hardware-constrained DSP. Austin or South San Francisco. | Acquisition and waveform interests overlap. Embedded implementation and SoC optimization make this a later-stage target; do not present exploratory SNN code as equivalent experience. |

## What is most likely to improve an interview

1. **A reproducible acquisition and timing demonstration.** Show the channel map,
   signal-quality checks, raw/event clocks, and measured limitations. The 121/128
   bench result is useful because it is concrete and attributable to a lab test.
2. **A small recorded-data validation package.** Use a synthetic or approved
   de-identified fixture with expected spike/event outputs and a repeat-responsive
   reference case. Include an intentionally shifted marker, channel swap, or
   scaling error so reviewers see that checks detect failures. A response found
   and checked in the same data is a consistency check, not held-out validation.
3. **A replay-based streaming benchmark.** Measure throughput, P50/P95/P99/max
   latency, buffering, and missed/dropped data under a stated channel count and
   sample rate. Keep capture-to-processing latency distinct from physical
   stimulus timing and network API response time.
4. **One small compiled-language contribution if a target role requires it.**
   A measured C++ or Rust reader/detector with Python integration can close a
   specific gap. It is a milestone to build, not a present resume skill.
5. **An upstream contribution after implementation and review.** A MED reader,
   documented validation fixture, or useful SpikeInterface example can give
   external evidence of collaboration. No accepted contribution is currently
   established.

The first three build directly on ongoing work. A broad new deep-learning project
is less urgent than making an existing pipeline easy to run, inspect, and trust.

## Tailoring each application

Choose one profile, then select the two or three accomplishments that match the
actual responsibilities. Keep the current M.S. status, volunteer appointment,
and prototype scope accurate. Retain formal employer titles. Do not insert a
job's requested technology into the skills list solely because it appears in
the posting.

For acquisition roles, lead with channel mapping, grounding, timing, and test
records. For software roles, lead with data formats, reproducible processing,
event alignment, and failure diagnosis. For BCI research roles, connect these
to the semantic-tuning prototype and adaptive-screening direction without
claiming a validated semantic decoder.
