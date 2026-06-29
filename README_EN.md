# Mashup-Benchmark

[中文](README.md)

Mashup-Benchmark is a long-video automatic editing benchmark for evaluating short-form mashup, highlight, and music-driven video editing systems.

![Mashup-Benchmark Overview](docs/assets/mashup_benchmark_overview.png)

## Dataset

- 10 hour-scale source videos: 3 sports broadcasts, 3 documentary episodes, and 4 feature films.
- 40 video-prompt tasks: each source video has 4 task types: event, character, emotion, and narrative.
- 11 BGM tracks from Mixkit, assigned by task mood and genre.
- Default target output length: 60 seconds.
- Default target shot length: 4 seconds.

The canonical task file is `data/tasks/mashup_benchmark.jsonl`. Each line is one video-prompt-audio task. Task ids follow `task_<index>`, from `task_001` to `task_040`.

### Videos

| ID | Category | Title | Duration | Resolution |
|---|---|---|---:|---|
| `video_001` | sports | FIFA World Cup Group A: Mexico vs South Africa<br>美加墨世界杯A组第1轮：墨西哥VS南非 | 01:38:53 | 480x270 |
| `video_002` | sports | FIFA World Cup Group H: Spain vs Cape Verde<br>美加墨世界杯H组第1轮：西班牙VS佛得角 | 02:03:58 | 1920x1080 |
| `video_003` | sports | FIFA World Cup Group E: Germany vs Curacao<br>美加墨世界杯E组第1轮：德国VS库拉索 | 02:09:00 | 1920x1080 |
| `video_004` | documentary | Planet Earth S01E01: From Pole to Pole<br>地球脉动 第一季第一集：From Pole to Pole | 49:02 | 1920x1080 |
| `video_005` | documentary | Planet Earth S01E02: Mountains<br>地球脉动 第一季第二集：Mountains | 47:52 | 1920x1080 |
| `video_006` | documentary | Planet Earth S01E03: Fresh Water<br>地球脉动 第一季第三集：Fresh Water | 49:11 | 1920x1080 |
| `video_007` | film | The Godfather (1972)<br>教父1 | 02:57:09 | 1920x1080 |
| `video_008` | film | Spirited Away (2001)<br>千与千寻 | 02:04:32 | 1920x1038 |
| `video_009` | film | La La Land (2016)<br>爱乐之城 | 02:07:48 | 1920x754 |
| `video_010` | film | Interstellar (2014)<br>星际穿越 | 02:49:04 | 1920x1080 |

### Audios

| ID | Title | Artist | Duration | Mood Tags |
|---|---|---|---:|---|
| `audio_001` | Sports Highlights | Ahjay Stelino | 01:36 | sports, rock, aggressive, propulsive |
| `audio_002` | Dirty Thinkin' | Michael Ramir C. | 01:29 | funk, energetic, groove, playful |
| `audio_003` | Techno Fest Vibes | Alejandro Magana (A. M.) | 01:09 | edm, high_energy, driving, celebratory |
| `audio_004` | Fright Night | Michael Ramir C. | 01:41 | cinematic, tension, dark, suspense |
| `audio_005` | Sun and His Daughter | Eugenio Mininni | 02:48 | nature, poetic, world, expansive |
| `audio_006` | Discover | Eugenio Mininni | 02:24 | documentary, hopeful, orchestral, wonder |
| `audio_007` | Relax Beat | Arulo | 01:48 | ambient, calm, observational, soft |
| `audio_008` | Silent Descent | Eugenio Mininni | 02:40 | film_score, melancholic, reflective, dramatic |
| `audio_009` | Epical Drums 01 | Grigoriy Nuzhny | 01:46 | cinematic, drums, epic, action |
| `audio_010` | Romantic Getaway | Ahjay Stelino | 01:44 | romantic, warm, emotional, classical |
| `audio_011` | Romantic Vacation | Ahjay Stelino | 01:52 | jazz, romantic, lounge, stylish |

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
- BCS: Beat-Cut Synchronization; based on full-frame visual cut detection on the final rendered video, without reading the edit timeline.
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
