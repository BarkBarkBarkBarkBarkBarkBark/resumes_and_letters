---
title: Marco Del Fava
author: Marco Del Fava
lang: en
---

# Marco Del Fava

**Neural Signal Processing & Acquisition**

Biomedical Engineering M.S. | UC Davis | Human Intracranial Electrophysiology

mdelfava@ucdavis.edu | 707-637-6544 | Sacramento, CA

[GitHub](https://github.com/BarkBarkBarkBarkBarkBarkBark)
[LinkedIn](https://www.linkedin.com/in/marc-del-fava)

## Research Profile

Developing and validating software for human intracranial electrophysiology, including multichannel neural acquisition, signal processing, spike sorting, and experimental synchronization. Experienced in Python-based neural data pipelines, acquisition hardware integration, and quantitative evaluation against recorded data.

## Technical Skills

**Neural Data & Signal Processing**

- SpikeInterface, Kilosort4, MountainSort5; waveform features and unit matching [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/DHN_validation/blob/496c2326f000037698f7b92b4b3a4139c3a70d13/sort_med/evidence/Strict_Comparison_of_Sorted_Spikes.ipynb)

- Offline waveform discrimination and afferent clustering [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/spike_discrim/blob/a697e68898c688ccc5dfe23ced78dbc6494ca1c1/docs/clustering_results.md)



**Neural Acquisition & Tooling**

- Intan RHD, Neuralynx CSC, MED; probe mapping and acquisition configuration [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/zlab_sorting_script/blob/3ff216ac593166687ae2260ccb705ea1322cf9f1/notebooks/sort_intan.ipynb)

- DHN-AQ RC/CS configuration, SSH orchestration, and NRD replay prototypes [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/dhn_client/tree/c4b0420a2f43aaca2367a7034a5deef7019528ee/src/darkhorse_neuralynx)



**Machine Learning & Data Science**

- Python (NumPy, Pandas, scikit-learn, PyTorch, Numba); MATLAB

- Sentence embeddings and seeded NEURON simulation prototypes [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/semantic_neuron/blob/349fe4be084a5b49b4b2037995a137ee6f83994b/neuronlib.py)



**General Technical**

- Git, Linux, SSH, shell scripting, Docker, and AWS GPU workflows

- Microsoft 365 administration; SQL and PostgreSQL




## Selected Engineering Projects

### Neural Acquisition and Timing — Implemented

- Built Intan RHD ingestion, probe/channel checks, and SpikeInterface/Kilosort4 processing with waveform and quality-metric extraction. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/zlab_sorting_script/blob/3ff216ac593166687ae2260ccb705ea1322cf9f1/notebooks/sort_intan.ipynb)

- Implemented queued PsychoPy/RHX event synchronization, exact-label joins, and affine clock fitting to analyze clock drift and alignment residuals.



*Acquisition workflow and clock-alignment software implemented; timing performance not independently verified.*

[Intan processing notebook](https://github.com/BarkBarkBarkBarkBarkBarkBark/zlab_sorting_script/blob/3ff216ac593166687ae2260ccb705ea1322cf9f1/notebooks/sort_intan.ipynb)

### Neural Compression Validation — Validated

- Evaluated DarkHorse Neuro compression on 20 million samples (one channel, 32 kHz; 625 s); maximum source-to-MED difference was 0.5 uV, with zero mismatches after rounding source values to whole microvolts. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/DHN_validation/blob/496c2326f000037698f7b92b4b3a4139c3a70d13/sort_med/evidence/8_7_filetype_comparison.ipynb)

- Controlled MountainSort5 comparison of rounded inputs preserved all 35,587 spike frames for the compared unit (exact Jaccard 1.0). [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/DHN_validation/blob/496c2326f000037698f7b92b4b3a4139c3a70d13/sort_med/evidence/Strict_Comparison_of_Sorted_Spikes.ipynb)



*Offline validation on a bounded single-channel slice; archived outputs reviewed, not a new raw-data rerun.*

[Waveform fidelity evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/DHN_validation/blob/496c2326f000037698f7b92b4b3a4139c3a70d13/sort_med/evidence/8_7_filetype_comparison.ipynb) · [Controlled spike comparison](https://github.com/BarkBarkBarkBarkBarkBarkBark/DHN_validation/blob/496c2326f000037698f7b92b4b3a4139c3a70d13/sort_med/evidence/Strict_Comparison_of_Sorted_Spikes.ipynb)

### Spike Sorting and Neural Processing — Validated

- Implemented waveform-feature evaluation across 38,145 spike snippets and 10 putative O-Sort unit labels; event-family KNN purity at k=5 was 95.04%. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/spike_discrim/blob/a697e68898c688ccc5dfe23ced78dbc6494ca1c1/docs/clustering_results.md)

- Measured 54.26% Hungarian-matched KMeans accuracy (ARI 0.3665) for that feature family; neighborhood purity is not sorter accuracy or biological ground truth. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/spike_discrim/blob/a697e68898c688ccc5dfe23ced78dbc6494ca1c1/src/spike_discrim/benchmarking/afferent_clustering.py)



*Offline feature validation; streaming detection and competitive-learning sorting in SNNeuro remain prototypes.*

[Discrimination results](https://github.com/BarkBarkBarkBarkBarkBarkBark/spike_discrim/blob/a697e68898c688ccc5dfe23ced78dbc6494ca1c1/docs/clustering_results.md) · [O-Sort membership comparison](https://github.com/BarkBarkBarkBarkBarkBarkBark/osort_medd_comparison/blob/4d5e94e7c3a637e9efdda8e35d7a8c0494f20a1d/codes/compare_osort_membership.m) · [Streaming prototype](https://github.com/BarkBarkBarkBarkBarkBarkBark/SNNeuro/blob/c2eecb76d4d47ad4966ee117e10fd9585e0f48a8/src/snn_agent/core/pipeline.py)

### Single-neuron analysis and adaptive-search development — Prototype

- Implemented a seeded NEURON prototype mapping sentence similarity to stochastic input rates, with fixed synaptic weights. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/semantic_neuron/blob/349fe4be084a5b49b4b2037995a137ee6f83994b/neuronlib.py)

- Added seeded stimulus windows, presynaptic event recording, voltage traces, and output spike times for reproducible simulated response analysis. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/semantic_neuron/blob/349fe4be084a5b49b4b2037995a137ee6f83994b/neuronlib.py)



*Simulation implemented; adaptive human stimulus selection and semantic selectivity are not validated.*

[Simulation implementation](https://github.com/BarkBarkBarkBarkBarkBarkBark/semantic_neuron/blob/349fe4be084a5b49b4b2037995a137ee6f83994b/neuronlib.py)

### Supporting acquisition work - Neuralynx / Dark Horse Neuro — Prototype

- Implemented DHN-AQ RC/CS configuration writers and SSH launch orchestration. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/dhn_client/tree/c4b0420a2f43aaca2367a7034a5deef7019528ee/src/darkhorse_neuralynx/dhn_client)

- Developed an NRD-to-UDP replay prototype for DHN-AQ ingestion. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/dhn_client/blob/c4b0420a2f43aaca2367a7034a5deef7019528ee/src/darkhorse_neuralynx/pegasus_bridge/nrd_stream.py)



*Prototype implemented; hardware reception and recording validation remain in progress.*

[Acquisition implementation](https://github.com/BarkBarkBarkBarkBarkBarkBark/dhn_client/tree/c4b0420a2f43aaca2367a7034a5deef7019528ee/src/darkhorse_neuralynx)

## Research Experience

**Research Volunteer**, UC Davis Health — Z-Lab (Dr. Jie Zheng) — Jul 2025 - Present

- Develop research workflows connecting acquisition, spike processing, and downstream single-neuron response analysis.
- Analyze human epilepsy microwire recordings using O-Sort and SpikeInterface, with attention to waveform structure and unit curation.


## Education

**M.S. Biomedical Engineering**, University of California, Davis — Fall 2026 - Present

**Python for Data Science, Professional Concentration**, UC Davis Continuing and Professional Education — 2025

**M.S. Psychology**, Arizona State University — 2023

**B.S. Neuroscience, Physiology, and Behavior**, University of California, Davis — 2017

## Additional Professional Experience

**IT Administrator**, First Step Communities — Jul 2021 - Present

- Managed IT infrastructure, device provisioning, and reporting automation.

**Analyst**, Eurofins Test America — Oct 2019 - Jun 2021

- Supported analytical laboratory QA, data review, and standard operating procedures.

## Certifications

- [Data Analysis with Matplotlib, Pandas, and Scikit-Learn Python Libraries](https://www.credly.com/badges/505ef11c-58b4-48bd-aa9e-5a21f0247d46/public_url) — UC Davis Continuing and Professional Education (2025-09-18)
- Biomedical Research; Research Administration; GCP Social and Behavioral Research — CITI Program
