# Evaluation Metrics

## Quality Score

```text
Quality = 0.18*IF + 0.16*BCS + 0.14*AEC + 0.14*VQ + 0.14*TC + 0.14*NC + 0.10*OQ
```

All component scores should be normalized to `[0, 100]` before aggregation.

## Metrics

### IF: Instruction Following

Checks whether the output follows the prompt's requested subject, event, emotion, style, and narrative intent. Recommended implementation: VLM-as-judge with the prompt and generated video.

### BCS: Beat-Cut Synchronization

Measures whether visual cuts align with beats, downbeats, or music structure points. Compute distance from each cut to the nearest beat/downbeat and average with exponential decay.

### AEC: Audio-Visual Energy Correspondence

Measures whether visual motion intensity follows audio energy. Compute shot-level or window-level visual motion, compare to RMS/energy curve, and report correlation.

### VQ: Visual Quality

Scores clarity, composition, subject prominence, and absence of obvious technical defects. Recommended implementation: VLM-as-judge or human Likert scoring.

### TC: Transition Continuity

Scores whether neighboring clips connect naturally in semantics, movement, and composition.

### NC: Narrative Coherence

Scores whether the complete edit has a coherent structure, emotional progression, or story arc.

### OQ: Overall Quality

Human-facing holistic quality: whether the video feels watchable, natural, professional, and publishable.

## Efficiency

Efficiency is reported separately:

- API cost per task
- end-to-end latency per task
- optional module-level latency breakdown
