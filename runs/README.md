# Runs

This directory stores generated videos and metadata from each baseline or ablation.

Expected layout:

```text
runs/<run_id>/
  run_manifest.json
  run_outputs.jsonl
  task_outputs/<task_id>/output.mp4
  task_outputs/<task_id>/run_output.json
```

See `../docs/run_submission_format.md` and the schemas in `../schemas/`.
