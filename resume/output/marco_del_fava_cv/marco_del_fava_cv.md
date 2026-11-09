---
title: Marco Del Fava
author: Marco Del Fava
lang: en
---

# Marco Del Fava

**Research Software & Neural Data**

M.S. Biomedical Engineering student | UC Davis | Human intracranial electrophysiology

[mdelfava@ucdavis.edu](mailto:mdelfava@ucdavis.edu) | 707-637-6544 | Sacramento, CA

[GitHub](https://github.com/BarkBarkBarkBarkBarkBarkBark)
[LinkedIn](https://www.linkedin.com/in/marc-del-fava)

## Research Profile

Biomedical Engineering M.S. student at UC Davis developing Python tools for neuroscience data acquisition, conversion, and validation. I work with human intracranial recordings, including proprietary Neuralynx, Intan, and MED formats. My projects span reader development, metadata repair, signal-integrity testing, and agent-assisted software engineering.

## Technical Skills

**Scientific Programming:** Python, NumPy, Pandas, scikit-learn, pytest, Git, Linux, Docker; MATLAB


**Neural Data & Acquisition:** Neuralynx, Intan RHD, DarkHorse MED, Neo, SpikeInterface, Kilosort4, MountainSort5


**Engineering Methods:** Scientific data parsing, metadata validation and repair, waveform analysis, experimental synchronization, profiling, regression tests



## Research Experience

**Graduate Student**, UC Davis Health — Z-Lab (Dr. Jie Zheng) — Jul 2025 - Present

- Work with human intracranial electrophysiology recordings, developing Python workflows to prepare, process, and analyze single-neuron data.
- Develop event-aligned analyses of responses to repeated spoken narratives, combining sorted spike timestamps, experimental markers, rasters, and peri-stimulus firing rates.
- Support acquisition and spike-processing workflows across recording systems, including channel mapping, signal quality assessment, and synchronization with behavioral experiments.

## Selected Engineering Projects

### Neural Data Formats and Integrity


- Adapted a Neo-backed MED reader to skip corrupt parity channels whose metadata caused standard readers to abort, allowing processing without modifying source recordings.


- Developed validation and repair utilities for Neuralynx recordings with sample-count inconsistencies and missing recording-end metadata that prevented downstream conversion.


- Evaluated signal fidelity across 20 million samples on one channel (32 kHz; 625 s), comparing original CSC and compressed MED recordings. Measured a maximum amplitude difference of 0.5 µV, with exact agreement after whole-microvolt source rounding.




### Neural Acquisition and Experimental Synchronization


- Built Python workflows for processing Intan recordings through SpikeInterface, including probe mapping, channel checks, spike sorting, waveform extraction, and quality metrics.


- Developed synchronization software to align PsychoPy behavioral events with RHX recordings, using matched event labels and affine clock fitting to characterize drift between recording systems.




### Waveform Analysis and Spike Sorting


- Evaluated waveform representations across 38,145 spike snippets and 10 putative O-Sort unit labels, comparing how well different features preserved local waveform structure and supported clustering.


- Found that strong local neighbor consistency did not translate into equivalent global clustering agreement, distinguishing local waveform-feature consistency from whole-dataset clustering behavior.




### Debugging Agent-Generated Software


- Investigated a performance regression in Hosaka, a command-line software platform, where agent-generated schema validation made listing seven records take approximately 70 seconds.


- Used execution timing logs to identify repeated validation as the bottleneck, then introduced content-based caching and regression tests to preserve checks for changed or invalid schemas.




## Additional Professional Experience

**IT Administrator**, First Step Communities — Jul 2021 - Present

- Maintain network and IT infrastructure across multiple shelter sites, including routing/VLAN segmentation, Microsoft 365 administration, and troubleshooting.
- Support longitudinal data collection and analysis of service utilization and housing outcomes, translating operational data into research and reporting workflows.

**Analyst**, Eurofins Test America — Oct 2019 - Jun 2021

- Prepared soil and water samples using solvent extraction in a high-throughput environmental testing laboratory, following established quality assurance procedures.
- Maintained high-accuracy data entry and review in a regulated laboratory environment; supported QA documentation and adherence to standard operating procedures.


## Education

**M.S. Biomedical Engineering**, University of California, Davis — 2026–Present

**M.S. Psychology**, Arizona State University — 2023

**B.S. Neuroscience, Physiology, and Behavior**, University of California, Davis — 2017

## Professional Development & Certifications

**Python for Data Science, Professional Concentration**, UC Davis Continuing and Professional Education — 2025


- [Data Analysis with Matplotlib, Pandas, and Scikit-Learn Python Libraries](https://www.credly.com/badges/505ef11c-58b4-48bd-aa9e-5a21f0247d46/public_url) — UC Davis Continuing and Professional Education (2025-09-18)
- Biomedical Research; Research Administration; GCP Social and Behavioral Research — CITI Program
