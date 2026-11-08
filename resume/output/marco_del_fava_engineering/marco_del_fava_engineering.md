---
title: Marco Del Fava
author: Marco Del Fava
lang: en
---

# Marco Del Fava

**Research Software & Neural Data**

M.S. Biomedical Engineering student | UC Davis | Human intracranial electrophysiology

mdelfava@ucdavis.edu | 707-637-6544 | Sacramento, CA

[GitHub](https://github.com/BarkBarkBarkBarkBarkBarkBark)
[LinkedIn](https://www.linkedin.com/in/marc-del-fava)

## Engineering Summary

Biomedical Engineering M.S. student and neuroscience researcher at UC Davis. I build Python acquisition and data-integrity workflows and use coding agents with profiling, debugging, and regression tests.

## Technical Skills

**Scientific Programming:** Python, NumPy, Pandas, scikit-learn, pytest, Git, Linux, Docker; MATLAB


**Neural Data & Acquisition:** Neuralynx, Intan RHD, DarkHorse MED, Neo, SpikeInterface, Kilosort4, MountainSort5


**Engineering Methods:** Scientific data parsing, metadata validation and repair, waveform analysis, experimental synchronization, profiling, regression tests



## Research Experience

**Research Volunteer**, UC Davis Health — Z-Lab (Dr. Jie Zheng) — Jul 2025 - Present

- Work with human intracranial electrophysiology recordings, developing Python workflows to prepare, process, and analyze single-neuron data.

## Selected Engineering Projects

### Neural Data Formats and Integrity


- Adapted a Neo-backed MED reader to skip corrupt parity channels whose metadata caused standard readers to abort, allowing processing without modifying source recordings.

- Evaluated signal fidelity across 20 million samples on one channel (32 kHz; 625 s), comparing original CSC and compressed MED recordings. Measured a maximum amplitude difference of 0.5 µV, with exact agreement after whole-microvolt source rounding. [Reader code](https://github.com/BarkBarkBarkBarkBarkBarkBark/DHN_validation/blob/496c2326f000037698f7b92b4b3a4139c3a70d13/sort_med/sorting_tools/med_utils.py) · [Validation notebook](https://github.com/BarkBarkBarkBarkBarkBarkBark/DHN_validation/blob/496c2326f000037698f7b92b4b3a4139c3a70d13/sort_med/evidence/8_7_filetype_comparison.ipynb)



### Neural Acquisition and Experimental Synchronization


- Built Python workflows for processing Intan recordings through SpikeInterface, including probe mapping, channel checks, spike sorting, waveform extraction, and quality metrics.

- Developed synchronization software to align PsychoPy behavioral events with RHX recordings, using matched event labels and affine clock fitting to characterize drift between recording systems. [Processing notebook](https://github.com/BarkBarkBarkBarkBarkBarkBark/zlab_sorting_script/blob/3ff216ac593166687ae2260ccb705ea1322cf9f1/notebooks/sort_intan.ipynb)



### Debugging Agent-Generated Software


- Investigated a performance regression in Hosaka, a command-line software platform, where agent-generated schema validation made listing seven records take approximately ten seconds.

- Used execution timing logs to identify repeated validation as the bottleneck, then introduced content-based caching and regression tests to preserve checks for changed or invalid schemas.



## Additional Professional Experience

**IT Administrator**, First Step Communities — Jul 2021 - Present

- Maintain network and IT infrastructure across multiple shelter sites, including routing/VLAN segmentation, Microsoft 365 administration, and troubleshooting.

**Analyst**, Eurofins Test America — Oct 2019 - Jun 2021

- Prepared soil and water samples using solvent extraction in a high-throughput environmental testing laboratory, following established quality assurance procedures.


## Education

**M.S. Biomedical Engineering**, University of California, Davis — 2026–Present

**M.S. Psychology**, Arizona State University — 2023

**B.S. Neuroscience, Physiology, and Behavior**, University of California, Davis — 2017

