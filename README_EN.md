# Mashup-Benchmark

[中文](README.md)

Mashup-Benchmark is a long-video automatic editing benchmark for evaluating short-form mashup, highlight, and music-driven video editing systems.

This repository uses the Chinese README as the default entry point. When the benchmark structure, data protocol, evaluation metrics, or usage workflow changes, update both `README.md` and `README_EN.md` so the Chinese and English versions stay aligned with each other and with the current project implementation. Figures, diagrams, and paper-style illustrations can use English labels only.

![Mashup-Benchmark Overview](docs/assets/mashup_benchmark_overview.png)

## Dataset

- 10 hour-scale source videos: 3 sports broadcasts, 3 documentary episodes, and 4 feature films.
- 40 video-prompt tasks: each source video has 4 task types: event, character, emotion, and narrative.
- 11 BGM tracks from Mixkit, assigned by task mood and genre.
- Default target output length: 60 seconds.
- Default target shot length: 4 seconds.

The canonical task file is `data/tasks/mashup_benchmark.jsonl`. Each line is one video-prompt-audio task.

## Directory Layout

```text
Mashup-Benchmark/
  data/
    tasks/mashup_benchmark.jsonl # Canonical 40-task JSONL
    videos/                      # Source long videos, ignored by Git
    audios/                      # BGM audio files, ignored by Git
  manifests/                     # Derived indexes for videos, audio, tasks, and summary
  schemas/                       # JSON Schema files for task/run/evaluation records
  scripts/                       # Validation and utility scripts
  runs/                          # System outputs, run_output.json files, and run manifests
  outputs/                       # Temporary exported artifacts that are not submitted runs
  eval/                          # Evaluation code
  eval_results/                  # Metric outputs and VLM-as-judge scores
  reports/                       # Aggregated tables, plots, and experiment notes
  docs/                          # Benchmark spec, metric protocol, and data card
```

## Expected System Output

For each task, a tested system should produce one complete edited short video. Baseline or system outputs should be placed at:

```text
runs/<run_id>/task_outputs/<task_id>/output.mp4
```

Per-task metadata must follow `schemas/run_output.schema.json`; whole-run metadata must follow `schemas/run_manifest.schema.json`. See `docs/run_submission_format.md` for the full submission format.

## Evaluation Dimensions

The full quality score uses 7 metrics:

```text
Quality = weighted_mean(IF, BCS, AEC, VQ, TC, NC, OQ)
```

Weighting policy:

- Local automatic metrics: `BCS = 0.20`, `AEC = 0.20`.
- VLM-as-judge metrics: `IF = 0.10`, `VQ = 0.10`, `TC = 0.10`, `NC = 0.10`.
- Human evaluation metric: `OQ = 0.20`.
- If human `OQ` is unavailable, the available 6 metrics are automatically renormalized: `BCS = 0.25`, `AEC = 0.25`, and `IF/VQ/TC/NC = 0.125`.

Metrics:

- IF: Instruction Following.
- BCS: Beat-Cut Synchronization.
- AEC: Audio-Visual Energy Correspondence.
- VQ: Visual Quality.
- TC: Transition Continuity.
- NC: Narrative Coherence.
- OQ: Overall Quality, optional human rating.

Efficiency is reported separately as API cost and end-to-end latency. See `eval/README.md` for the runnable evaluator.

## Validation And Evaluation

Validate the benchmark data structure:

```bash
python3 scripts/validate_benchmark.py
```

Validate a submitted run:

```bash
python3 scripts/validate_run.py runs/<run_id>
```

Evaluate a submitted run:

```bash
cp eval/config.example.yaml eval/config.yaml
python3 -m eval.run_evaluation --run runs/<run_id> --config eval/config.yaml
```

`eval/config.yaml` configures the VLM model name, API key, base URL, timeout, and metric weights. This file contains local credentials and is ignored by Git; do not commit it.

## Maintenance Policy

- `README.md` is the default Chinese entry point; `README_EN.md` is the mirrored English version.
- When editing the README, update both files and keep their meanings aligned.
- When changing data, schemas, evaluation code, or directory structure, update the README, relevant files under `docs/`, and examples accordingly.
- `data/videos/` and `data/audios/` store large media assets and are ignored by Git by default.
- `runs/` stores generated videos from different baselines or tested systems; formal results should include `run_manifest.json` and per-task `run_output.json` files.
