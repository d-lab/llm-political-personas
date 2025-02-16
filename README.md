# LLM Political Personas

This repository contains the code to replicate the experiments and results from [our paper](https://arxiv.org/abs/2412.14843) "Mapping and Influencing the Political Ideology of Large Language Models using Synthetic Personas" (WWW '25) [![DOI](https://zenodo.org/badge/925494468.svg)](https://doi.org/10.5281/zenodo.14879668)

## Overview

We investigate how synthetic personas affect LLMs' political orientations using the Political Compass Test (PCT). The code allows you to:
- Run PCT evaluations on multiple LLMs using persona-based prompting
- Analyze political compass distributions across different models and conditions
- Visualize results through heatmaps and statistical analyses
- Examine the effects of explicit ideological descriptors on model behavior

## Data

Download the required datasets from our [Zenodo repository](https://doi.org/10.5281/zenodo.14816664) and follow the placement instructions in the repository's README [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14816665.svg)](https://doi.org/10.5281/zenodo.14816665)


The data should be organized as follows:
```
data/
└── processed/
    ├── Llama-3.1-8B-Instruct/
    │   ├── base/
    │   ├── right_authoritarian_personas/
    │   └── left_libertarian_personas/
    ├── Mistral-7B-Instruct-v0.3/
    ├── Qwen2.5-7B-Instruct/
    └── zephyr-7b-beta/
└── raw/
```

## Acknowledgments

This work is partially supported by the Australian Research Council (ARC) Training Centre for Information Resilience (Grant No. IC200100022) and by an ARC Future Fellowship Project (Grant No. FT240100022).
