# VLM Judge Rubric Draft

Use this rubric when scoring a generated video against one benchmark task.

Inputs:

- User prompt
- Source video title/category metadata
- BGM metadata
- Generated short video

The VLM judge scores only four metrics from 0 to 100:

- IF: Does the video follow the prompt subject, event, style, and constraints?
- VQ: Is the visual quality clear, stable, well-composed, and free of obvious defects?
- TC: Are transitions between clips natural in content, motion, and rhythm?
- NC: Does the video have coherent progression rather than random clips?

`OQ` is not scored by the VLM judge. It is reserved for optional human overall-quality evaluation and can be supplied as `human_scores.OQ` or `scores.OQ` in a run record.

Return JSON only:

```json
{
  "scores": {
    "IF": 0,
    "VQ": 0,
    "TC": 0,
    "NC": 0
  },
  "rationale": {
    "IF": "short reason",
    "VQ": "short reason",
    "TC": "short reason",
    "NC": "short reason"
  }
}
```
