# Mashup-Benchmark

Mashup-Benchmark is a long-video automatic editing benchmark for evaluating short-form mashup/highlight generation systems.

## Dataset

- 10 hour-scale source videos: 3 sports broadcasts, 3 documentary episodes, 4 feature films.
- 40 video-prompt tasks: each source video has 4 task types: event, character, emotion, and narrative.
- 11 BGM tracks from Mixkit, assigned per task by mood and genre.
- Target output length: 60 seconds.
- Target shot length: 4 seconds.

The canonical task file is `data/tasks/mashup_benchmark.jsonl`. Each line is one video-prompt-audio task.

## Directory Layout

```text
Mashup-Benchmark/
  data/
    tasks/mashup_benchmark.jsonl # Canonical 40-task JSONL
    videos/                      # Source long videos
    audios/                      # BGM tracks
  manifests/                    # Derived indexes for videos, audio, tasks, summary
  schemas/                      # JSON schema for task/run/evaluation records
  scripts/                      # Validation and utility scripts
  runs/                         # Generated videos, per-task run.json files, and run manifests
  outputs/                      # Reserved for exported artifacts that are not submitted runs
  evaluations/                  # Metric outputs and VLM-as-judge scores
  reports/                      # Aggregated tables, plots, and experiment notes
  docs/                         # Benchmark spec, metric protocol, and data card
```

## Expected System Output

For each task, a system should produce one complete edited short video. Baseline outputs belong under `runs/<run_id>/task_outputs/<task_id>/output.mp4`. Per-task metadata must follow `schemas/run_output.schema.json`; whole-run metadata must follow `schemas/run_manifest.schema.json`. See `docs/run_submission_format.md`.

## Evaluation Dimensions

Quality score:

```text
Quality = 0.18*IF + 0.16*BCS + 0.14*AEC + 0.14*VQ + 0.14*TC + 0.14*NC + 0.10*OQ
```

Metrics:

- IF: instruction following
- BCS: beat-cut synchronization
- AEC: audio-visual energy correspondence
- VQ: visual quality
- TC: transition continuity
- NC: narrative coherence
- OQ: overall quality

Efficiency is reported separately as API cost and end-to-end latency.

## Validate

```bash
python3 scripts/validate_benchmark.py
```

Validate a submitted baseline run:

```bash
python3 scripts/validate_run.py runs/<run_id>
```
