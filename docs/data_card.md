# Data Card

## Scope

Mashup-Benchmark focuses on evaluating automatic editing systems on long-form source videos. The benchmark is intended for research comparison of retrieval, planning, alignment, and editing quality.

## Composition

- Sports: 3 FIFA World Cup match broadcasts.
- Documentary: Planet Earth Season 1 Episodes 1-3.
- Film: The Godfather, Spirited Away, La La Land, Interstellar.
- Task types per video: event, character, emotion, narrative.

## Assets

The benchmark stores local paths only. Users are responsible for ensuring they have lawful access to source videos. BGM tracks are from Mixkit and include license URLs in the task JSONL.

## Labels

There are no human temporal annotations in the current benchmark. Evaluation is designed around automatic metrics and VLM-as-judge rubrics, plus optional human preference studies later.

## Known Limitations

- No ground-truth edit decision list is provided.
- VLM-as-judge scoring can be sensitive to judge model choice and prompt wording.
- Source videos vary in genre, aspect ratio, codec, and visual style.
