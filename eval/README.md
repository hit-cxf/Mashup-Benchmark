# Evaluation Code

This package evaluates submitted runs under `runs/<run_id>/`.

## Metrics Implemented

Cross-modal alignment:

- `IF`: instruction following, scored by VLM-as-judge.
- `BCS`: beat-cut synchronization, computed from detected visual cuts and audio beat peaks.
- `AEC`: audio-visual energy correspondence, computed from visual motion and audio RMS correlation.

Single-modal quality:

- `VQ`: visual quality, scored by VLM-as-judge.
- `TC`: transition continuity, scored by VLM-as-judge.
- `NC`: narrative coherence, scored by VLM-as-judge.

Human preference:

- `OQ`: optional overall quality rating from human evaluation.

Default seven-metric weights are `BCS=0.20`, `AEC=0.20`, `OQ=0.20`, and `IF/VQ/TC/NC=0.10` each. If `OQ` or any other metric is missing, the evaluator renormalizes over available metrics.

## Configure VLM Judge

Copy the example config and fill in credentials:

```bash
cp eval/config.example.yaml eval/config.yaml
```

`eval/config.yaml` is ignored by git.

## Run

```bash
python3 -m eval.run_evaluation --run runs/<run_id> --config eval/config.yaml
```

Smoke-test automatic metrics only:

```bash
python3 -m eval.run_evaluation --run runs/<run_id> --skip-vlm --limit 1
```

Outputs:

```text
eval_results/<eval_id>/evaluation_scores.jsonl
eval_results/<eval_id>/summary.json
```
