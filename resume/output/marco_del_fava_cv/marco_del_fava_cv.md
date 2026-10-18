---
title: Marco Del Fava
author: Marco Del Fava
lang: en
---

# Marco Del Fava

mdelfava@ucdavis.edu | 707-637-6544 | Sacramento, CA

[https://github.com/BarkBarkBarkBarkBarkBarkBark](https://github.com/BarkBarkBarkBarkBarkBarkBark)

[https://www.linkedin.com/in/marc-del-fava](https://www.linkedin.com/in/marc-del-fava)


## Research Profile

Biomedical Engineering M.S. student at UC Davis and research volunteer in Dr. Jie Zheng's lab, working on human single-unit electrophysiology. Builds research software for neural acquisition and spike analysis, with interests in Intan acquisition, real-time spike sorting, and semantic selectivity in single-neuron responses.

## Research Experience

**Research Volunteer**, UC Davis Health — Z-Lab (Dr. Jie Zheng) — Jul 2025 - Present

- Develop research workflows connecting acquisition, spike processing, and downstream single-neuron response analysis.
- Analyze human epilepsy microwire recordings using O-Sort and SpikeInterface, with attention to waveform structure and unit curation.

## Selected Projects

### Intan acquisition and experiment synchronization

Connect neural recordings to reproducible processing and experiment timing.

- Implemented Intan RHD loading, probe configuration, and SpikeInterface/Kilosort4 processing in zlab_sorting_script. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/zlab_sorting_script/blob/main/notebooks/sort_intan.ipynb)

- Developing Intan RHX/DeepArray acquisition and event-synchronization integration; hardware bench validation remains pending.



*Status: File-processing workflow implemented; live acquisition and timing integration in progress.*

[Intan workflow](https://github.com/BarkBarkBarkBarkBarkBarkBark/zlab_sorting_script/blob/main/readme.md)

### Waveform discrimination and online sorting research

Preserve unit-specific waveform information while investigating streaming analysis.

- Implemented WeightBank waveform representations in spike_discrim; evaluated post-hoc clustering against putative O-Sort unit labels. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/spike_discrim/blob/main/docs/clustering_results.md)

- Developed synthetic streaming/detection infrastructure in realtime-sorter-mvp and experimental competitive-learning sorting in SNNeuro. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/SNNeuro/blob/main/src/snn_agent/core/pipeline.py)



*Status: Discrimination evaluated offline; online unit sorting remains experimental, without validated end-to-end latency.*

[Discrimination results](https://github.com/BarkBarkBarkBarkBarkBarkBark/spike_discrim/blob/main/docs/clustering_results.md) · [Streaming, not unit sorting](https://github.com/BarkBarkBarkBarkBarkBarkBark/realtime-sorter-mvp) · [Experimental sorter](https://github.com/BarkBarkBarkBarkBarkBarkBark/SNNeuro/blob/main/src/snn_agent/core/dec_layer.py)

### Single-neuron response analysis and semantic tuning

Investigate relationships between stimulus meaning and single-neuron responses.

- Implemented a seeded NEURON prototype mapping sentence similarity to stochastic input rates, with fixed synaptic weights. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/semantic_neuron/blob/main/neuronlib.py)

- Developed semantic-trajectory tooling in ZEmbeddings; exploring stimulus-aligned response analysis and adaptive stimulus selection. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/ZEmbeddings/tree/main/src/zembeddings)



*Status: Simulation and text analysis implemented; adaptive experiments proposed, not demonstrated human concept selectivity or causality.*

[Simulation and limitations](https://github.com/BarkBarkBarkBarkBarkBarkBark/semantic_neuron#limitations) · [Semantic text analysis](https://github.com/BarkBarkBarkBarkBarkBarkBark/ZEmbeddings)

### Supporting acquisition work - Neuralynx / Dark Horse Neuro

Configure acquisition sessions and replay archived Neuralynx recordings.

- Implemented DHN-AQ RC/CS configuration writers and SSH launch orchestration. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/dhn_client/tree/main/src/darkhorse_neuralynx/dhn_client)

- Developed an NRD-to-UDP replay prototype for DHN-AQ ingestion. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/dhn_client/blob/main/src/darkhorse_neuralynx/pegasus_bridge/nrd_stream.py)



*Status: Prototype implemented; hardware reception and recording validation remain in progress.*

[Acquisition implementation](https://github.com/BarkBarkBarkBarkBarkBarkBark/dhn_client)


## Education

**M.S. Biomedical Engineering**, University of California, Davis — Fall 2026 - Present

**Python for Data Science, Professional Concentration**, UC Davis Continuing and Professional Education — 2025

**M.S. Psychology**, Arizona State University — 2023

**B.S. Neuroscience, Physiology, and Behavior**, University of California, Davis — 2017

## Technical Skills

**Neural Data & Signal Processing**

- Waveform features, spike-vs-noise evaluation, and afferent clustering [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/spike_discrim/blob/main/docs/clustering_results.md)

- SpikeInterface preprocessing, Kilosort4, and manual unit curation workflows [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/zlab_sorting_script/blob/main/readme.md)



**Neural Acquisition & Tooling**

- Intan RHD loading and probe-aware sorting workflows [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/zlab_sorting_script/blob/main/notebooks/sort_intan.ipynb)

- DHN-AQ RC/CS configuration, SSH orchestration, and NRD replay prototypes [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/dhn_client/tree/main/src/darkhorse_neuralynx)



**Machine Learning & Data Science**

- Python (NumPy, Pandas, scikit-learn, PyTorch, Numba); MATLAB

- Sentence embeddings and seeded NEURON simulation prototypes [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/semantic_neuron/blob/main/neuronlib.py)



**General Technical**

- Git, Linux, SSH, shell scripting, Docker, and AWS GPU workflows

- Microsoft 365 administration; SQL and PostgreSQL





## Additional Professional Experience

**IT Administrator**, First Step Communities — Jul 2021 - Present

- Managed Microsoft 365 IT infrastructure across 4 shelter sites, including user provisioning, device management, and systems coordination.

**Analyst**, Eurofins Test America — Oct 2019 - Jun 2021

- Maintained high-accuracy data entry and review in a regulated laboratory environment; supported QA documentation and adherence to standard operating procedures.

## Certifications

- [Data Analysis with Matplotlib, Pandas, and Scikit-Learn Python Libraries](https://www.credly.com/badges/505ef11c-58b4-48bd-aa9e-5a21f0247d46/public_url) — UC Davis Continuing and Professional Education (2025-09-18)
- Biomedical Research; Research Administration; GCP Social and Behavioral Research — CITI Program
