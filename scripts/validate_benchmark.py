#!/usr/bin/env python3
import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASK_FILE = ROOT / "data" / "tasks" / "mashup_benchmark.jsonl"

REQUIRED_TOP = {"id", "benchmark", "video", "task", "audio", "expected_output", "evaluation_focus"}
TASK_TYPES = {"event", "character", "emotion", "narrative"}
VIDEO_CATEGORIES = {"sports", "documentary", "film"}


def ffprobe_audio_codec(path: Path) -> str:
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=codec_name,channels,channel_layout",
        "-of", "json", str(path),
    ]
    info = json.loads(subprocess.check_output(cmd, text=True))
    streams = info.get("streams", [])
    if not streams:
        return "missing_audio_stream"
    stream = streams[0]
    return f"{stream.get('codec_name')}:{stream.get('channels')}:{stream.get('channel_layout')}"


def main() -> int:
    errors = []
    rows = []
    with TASK_FILE.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid json: {exc}")
                continue
            rows.append(row)

    ids = set()
    video_ids = set()
    video_paths = []
    audio_paths = []
    task_type_counts = Counter()
    category_counts = Counter()

    for i, row in enumerate(rows, 1):
        missing = REQUIRED_TOP - set(row)
        if missing:
            errors.append(f"row {i}: missing top-level keys {sorted(missing)}")
            continue
        if row["id"] in ids:
            errors.append(f"row {i}: duplicate id {row['id']}")
        ids.add(row["id"])
        if row["benchmark"] != "Mashup-Benchmark":
            errors.append(f"row {i}: benchmark must be Mashup-Benchmark")

        video = row["video"]
        task = row["task"]
        audio = row["audio"]
        if video.get("category") not in VIDEO_CATEGORIES:
            errors.append(f"row {i}: invalid video category {video.get('category')}")
        if task.get("type") not in TASK_TYPES:
            errors.append(f"row {i}: invalid task type {task.get('type')}")
        if task.get("target_shot_length_sec") != 4.0:
            errors.append(f"row {i}: target_shot_length_sec should be 4.0")
        if task.get("target_output_length_sec") != 60:
            errors.append(f"row {i}: target_output_length_sec should be 60")

        video_path = ROOT / video.get("local_path", "")
        audio_path = ROOT / audio.get("local_path", "")
        if not video_path.exists():
            errors.append(f"row {i}: missing video {video_path}")
        if not audio_path.exists():
            errors.append(f"row {i}: missing audio {audio_path}")
        video_ids.add(video.get("id"))
        if video.get("local_path") not in video_paths:
            video_paths.append(video.get("local_path"))
        if audio.get("local_path") not in audio_paths:
            audio_paths.append(audio.get("local_path"))
        task_type_counts[task.get("type")] += 1
        category_counts[video.get("category")] += 1

    for rel in video_paths:
        if not rel:
            continue
        path = ROOT / rel
        if path.exists():
            codec = ffprobe_audio_codec(path)
            if not codec.startswith("aac:"):
                errors.append(f"video audio is not AAC: {rel} -> {codec}")

    print(f"rows: {len(rows)}")
    print(f"unique tasks: {len(ids)}")
    print(f"videos: {len(video_paths)}")
    print(f"audios: {len(audio_paths)}")
    print(f"task types: {dict(task_type_counts)}")
    print(f"video categories across task rows: {dict(category_counts)}")

    if errors:
        print("\nERRORS:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("\nOK: benchmark structure and assets validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
