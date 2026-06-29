# VLM Judge Rubric Draft

Use this rubric when scoring a generated video against one benchmark task.

Inputs:

- User prompt
- Source video title/category metadata
- BGM metadata
- Generated short video

Score each metric from 0 to 100:

- IF: Does the video follow the prompt subject, event, style, and constraints?
- VQ: Is the visual quality clear, stable, well-composed, and free of obvious defects?
- TC: Are transitions between clips natural in content, motion, and rhythm?
- NC: Does the video have coherent progression rather than random clips?
- OQ: Would a viewer consider the result good, natural, and publishable?

Return JSON only:

```json
{
  "IF": 0,
  "VQ": 0,
  "TC": 0,
  "NC": 0,
  "OQ": 0,
  "rationale": "short explanation"
}
```
