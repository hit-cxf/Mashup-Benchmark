# Run Submission Format

This document defines where baseline outputs go and which metadata each method must provide.

## Directory Convention

Each baseline or ablation should write one run directory:

```text
runs/<run_id>/
  run_manifest.json
  run_outputs.jsonl
  task_outputs/
    <task_id>/
      output.mp4
      run.json
      logs/
        backend.log
      artifacts/
        shot_plan.json
```

`run_id` should identify the method and experiment setting, for example:

```text
cutclaw_original
cutmaster_embedding_v4
cutmaster_local_embedding
baseline_random
```

Use stable names for comparison runs. Add a date only when the same method/config is intentionally rerun and both results need to be kept.

## Per-Task `run.json`

`task_outputs/<task_id>/run.json` is the canonical per-task record and must follow `schemas/run_output.schema.json`.

Required fields:

- `run_id`: run directory name.
- `method`: system or baseline name.
- `method_version`: optional method variant, model setting, or ablation name.
- `task_id`: benchmark task id from `data/tasks/mashup_benchmark.jsonl`.
- `video_id`, `audio_id`, `prompt_type`: copied from the task for easier joins.
- `status`: `success`, `failed`, or `skipped`.
- `output_video`: path to the generated video relative to benchmark root.
- `target_output_length_sec`, `target_shot_length_sec`: target values used by the method.
- `actual_output_length_sec`: measured final video duration.
- `wall_clock_sec`: end-to-end generation time for this task.
- `created_at`: ISO-8601 timestamp.

Recommended optional fields:

- `api_cost_usd`: total API cost for the task.
- `code_commit`: source code commit used for the method.
- `config`: key model and algorithm settings.
- `artifacts`: paths to logs, shot plans, intermediate plans, or traces.
- `error`: structured failure information when `status != success`.

Example:

```json
{
  "run_id": "cutmaster_embedding_v4",
  "method": "CutMaster",
  "method_version": "embedding_v4",
  "task_id": "mb_fifa_world_cup_group_a_mexico_vs_south_africa_event",
  "video_id": "video_001",
  "audio_id": "bgm_sports_highlights",
  "prompt_type": "event",
  "status": "success",
  "output_video": "runs/cutmaster_embedding_v4/task_outputs/mb_fifa_world_cup_group_a_mexico_vs_south_africa_event/output.mp4",
  "target_output_length_sec": 60,
  "target_shot_length_sec": 4.0,
  "actual_output_length_sec": 58.7,
  "wall_clock_sec": 1234.5,
  "api_cost_usd": 0.42,
  "created_at": "2026-06-29T12:00:00+08:00",
  "code_commit": "git_sha",
  "config": {
    "embedding_model": "text-embedding-v4",
    "vlm_model": "qwen-vl-plus",
    "llm_model": "qwen-max"
  },
  "artifacts": {
    "shot_plan": "runs/cutmaster_embedding_v4/task_outputs/mb_fifa_world_cup_group_a_mexico_vs_south_africa_event/artifacts/shot_plan.json",
    "backend_log": "runs/cutmaster_embedding_v4/task_outputs/mb_fifa_world_cup_group_a_mexico_vs_south_africa_event/logs/backend.log"
  },
  "error": null
}
```

## `run_outputs.jsonl`

`run_outputs.jsonl` duplicates the per-task `run.json` records as JSONL so evaluation scripts can stream a whole run without walking directories.

Every successful task should have both:

```text
task_outputs/<task_id>/run.json
one matching line in run_outputs.jsonl
```

## `run_manifest.json`

`run_manifest.json` stores global metadata for the whole baseline execution and must follow `schemas/run_manifest.schema.json`.

Example:

```json
{
  "run_id": "cutmaster_embedding_v4",
  "method": "CutMaster",
  "method_version": "embedding_v4",
  "benchmark": "Mashup-Benchmark",
  "task_file": "data/tasks/mashup_benchmark.jsonl",
  "created_at": "2026-06-29T12:00:00+08:00",
  "status": "success",
  "num_tasks": 40,
  "num_success": 40,
  "num_failed": 0,
  "run_outputs": "runs/cutmaster_embedding_v4/run_outputs.jsonl",
  "code": {
    "repo": "CutClaw",
    "branch": "CutMaster",
    "commit": "git_sha",
    "dirty": false
  },
  "config": {
    "embedding_model": "text-embedding-v4",
    "target_output_length_sec": 60,
    "target_shot_length_sec": 4.0
  },
  "aggregate": {
    "total_wall_clock_sec": 49320.1,
    "total_api_cost_usd": 16.8
  }
}
```

## Evaluation Outputs

Evaluation outputs are separate from generated videos:

```text
evaluations/<eval_id>/
  scores.jsonl
  summary.json
```

A score record should reference `run_id` and `task_id`, not copy the generated video.
