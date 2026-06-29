from __future__ import annotations

import base64
import json
import re
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from eval.media import extract_evenly_spaced_frames

SYSTEM_PROMPT = """You are a strict evaluator for short-form video editing benchmarks. Score only what is visible in the sampled frames and described task metadata. Return JSON only."""

USER_PROMPT_TEMPLATE = """
Evaluate this generated short video for Mashup-Benchmark.

Task prompt:
{prompt}

Task type: {task_type}
Source video title: {video_title}
BGM title: {audio_title}
Target output length: {target_output_length_sec}s
Target shot length: {target_shot_length_sec}s
Actual output length: {actual_output_length_sec}s

Score the following metrics from 0 to 100:
- IF: Instruction Following. Does the edit follow the requested subject, event, style, emotion, or narrative?
- VQ: Visual Quality. Are sampled frames clear, well-composed, subject-focused, and free of obvious technical defects?
- TC: Transition Continuity. Based on the frame sequence, do adjacent segments feel coherent in visual semantics, motion, and composition?
- NC: Narrative Coherence. Does the edit appear to have a clear structure, progression, or story arc matching the prompt?

Return a JSON object exactly like:
{{
  "scores": {{"IF": 0, "VQ": 0, "TC": 0, "NC": 0}},
  "rationale": {{
    "IF": "short reason",
    "VQ": "short reason",
    "TC": "short reason",
    "NC": "short reason"
  }}
}}
""".strip()


def _image_content(path: Path) -> dict[str, Any]:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}}


def _extract_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.S)
        if not match:
            raise
        return json.loads(match.group(0))


class VLMJudge:
    def __init__(self, config: dict[str, Any]):
        vlm = config.get("vlm") or {}
        self.model = str(vlm.get("model") or "")
        self.api_key = str(vlm.get("api_key") or "")
        self.base_url = str(vlm.get("base_url") or "").rstrip("/")
        self.timeout_sec = int(vlm.get("timeout_sec") or 120)
        self.temperature = float(vlm.get("temperature") or 0)
        self.max_frames = int(vlm.get("max_frames") or 8)
        if not self.model or not self.api_key or not self.base_url:
            raise ValueError("vlm.model, vlm.api_key, and vlm.base_url are required in eval/config.yaml")

    def score(self, output_video: Path, task: dict[str, Any], run_record: dict[str, Any]) -> dict[str, Any]:
        with tempfile.TemporaryDirectory(prefix="mashup_vlm_frames_") as tmp:
            frames = extract_evenly_spaced_frames(output_video, Path(tmp), max_frames=self.max_frames)
            user_text = USER_PROMPT_TEMPLATE.format(
                prompt=task["task"]["prompt"],
                task_type=task["task"]["type"],
                video_title=task["video"].get("title_en") or task["video"].get("title_zh") or task["video"].get("id"),
                audio_title=task["audio"].get("title") or task["audio"].get("id"),
                target_output_length_sec=task["task"]["target_output_length_sec"],
                target_shot_length_sec=task["task"]["target_shot_length_sec"],
                actual_output_length_sec=run_record.get("actual_output_length_sec"),
            )
            content: list[dict[str, Any]] = [{"type": "text", "text": user_text}]
            content.extend(_image_content(frame) for frame in frames)
            payload = {
                "model": self.model,
                "temperature": self.temperature,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": content},
                ],
            }
            request = urllib.request.Request(
                f"{self.base_url}/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_sec) as response:
                    raw = json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")[-2000:]
                raise RuntimeError(f"VLM request failed: HTTP {exc.code}: {body}") from exc

        content_text = raw["choices"][0]["message"]["content"]
        parsed = _extract_json(content_text)
        scores = parsed.get("scores") or {}
        normalized_scores = {}
        for key in ["IF", "VQ", "TC", "NC"]:
            value = float(scores.get(key, 0.0))
            normalized_scores[key] = max(0.0, min(100.0, value))
        return {
            "scores": normalized_scores,
            "rationale": parsed.get("rationale") or {},
            "usage": raw.get("usage"),
            "model": self.model,
            "num_frames": len(frames) if 'frames' in locals() else None,
        }
