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

## Engineering Summary

Developing and validating software for human intracranial electrophysiology, including multichannel neural acquisition, signal processing, spike sorting, and experimental synchronization. Experienced in Python-based neural data pipelines, acquisition hardware integration, and quantitative evaluation against recorded data.

## Technical Skills

**Neural Data & Signal Processing:** SpikeInterface, Kilosort4, MountainSort5; waveform features and unit matching [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/DHN_validation/blob/496c2326f000037698f7b92b4b3a4139c3a70d13/sort_med/evidence/Strict_Comparison_of_Sorted_Spikes.ipynb)


**Neural Acquisition & Tooling:** Intan RHD, Neuralynx CSC, MED; probe mapping and acquisition configuration [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/zlab_sorting_script/blob/3ff216ac593166687ae2260ccb705ea1322cf9f1/notebooks/sort_intan.ipynb)


**Machine Learning & Data Science:** Python (NumPy, Pandas, scikit-learn, PyTorch, Numba); MATLAB



## Selected Engineering Projects

### Neural Acquisition and Synchronization — Implemented

- Built Intan RHD ingestion, probe/channel checks, and SpikeInterface/Kilosort4 processing with waveform and quality-metric extraction. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/zlab_sorting_script/blob/3ff216ac593166687ae2260ccb705ea1322cf9f1/notebooks/sort_intan.ipynb)

- Implemented queued PsychoPy/RHX event synchronization, exact-label joins, and affine clock fitting to analyze clock drift and alignment residuals.



### Neural Signal Fidelity and Processing Validation — Validated

- Evaluated DarkHorse Neuro compression on 20 million samples (one channel, 32 kHz; 625 s); maximum source-to-MED difference was 0.5 uV, with zero mismatches after rounding source values to whole microvolts. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/DHN_validation/blob/496c2326f000037698f7b92b4b3a4139c3a70d13/sort_med/evidence/8_7_filetype_comparison.ipynb)

- Controlled MountainSort5 comparison of rounded inputs preserved all 35,587 spike frames for the compared unit (exact Jaccard 1.0). [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/DHN_validation/blob/496c2326f000037698f7b92b4b3a4139c3a70d13/sort_med/evidence/Strict_Comparison_of_Sorted_Spikes.ipynb)



### Spike Sorting and Waveform Discrimination — Validated

- Implemented waveform-feature evaluation across 38,145 spike snippets and 10 putative O-Sort unit labels; event-family KNN purity at k=5 was 95.04%. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/spike_discrim/blob/a697e68898c688ccc5dfe23ced78dbc6494ca1c1/docs/clustering_results.md)

- Measured 54.26% Hungarian-matched KMeans accuracy (ARI 0.3665) for that feature family; neighborhood purity is not sorter accuracy or biological ground truth. [Evidence](https://github.com/BarkBarkBarkBarkBarkBarkBark/spike_discrim/blob/a697e68898c688ccc5dfe23ced78dbc6494ca1c1/src/spike_discrim/benchmarking/afferent_clustering.py)



## Research Experience

**Research Volunteer**, UC Davis Health — Z-Lab (Dr. Jie Zheng) — Jul 2025 - Present

- Analyze human intracranial single units with O-Sort/SpikeInterface; develop narrative-aligned rasters and peri-stimulus firing-rate workflows.


## Education

**M.S. Biomedical Engineering**, University of California, Davis — Fall 2026 - Present

**Python for Data Science, Professional Concentration**, UC Davis Continuing and Professional Education — 2025

**M.S. Psychology**, Arizona State University — 2023

**B.S. Neuroscience, Physiology, and Behavior**, University of California, Davis — 2017

## Additional Professional Experience

**IT Administrator**, First Step Communities — Jul 2021 - Present

- Administer multi-site networks, routing/VLAN segmentation, Microsoft 365/Exchange Online, and camera/recording systems; troubleshoot infrastructure and support longitudinal service-utilization and housing-outcome research.

**Analyst**, Eurofins Test America — Oct 2019 - Jun 2021

- Supported analytical laboratory QA, data review, and standard operating procedures.

