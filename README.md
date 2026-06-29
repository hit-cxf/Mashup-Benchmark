# Mashup-Benchmark

[English](README_EN.md)

Mashup-Benchmark 是一个面向长视频自动剪辑的 benchmark，用于评估短视频混剪、精彩集锦和音乐驱动剪辑系统的生成质量与效率。

![Mashup-Benchmark Overview](docs/assets/mashup_benchmark_overview.png)

## 数据集

- 10 个小时级长视频源：3 场体育赛事、3 集纪录片、4 部电影。
- 40 个视频-提示词任务：每个长视频对应 4 类任务，分别是事件型、人物型、情绪型和叙事型。
- 11 首 Mixkit BGM，根据任务情绪和风格进行分配。
- 默认目标成片时长：60 秒。
- 默认目标 shot 时长：4 秒。

标准任务文件是 `data/tasks/mashup_benchmark.jsonl`，其中每一行对应一个视频-提示词-音频任务。任务 id 命名为 `task_<index>`，范围为 `task_001` 到 `task_040`。

### 视频

| 编号          | 类型     | 名称                                                                             |     时长 | 分辨率    |
| ------------- | -------- | -------------------------------------------------------------------------------- | -------: | --------- |
| `video_001` | 体育赛事 | 美加墨世界杯A组第1轮：墨西哥VS南非FIFA World Cup Group A: Mexico vs South Africa | 01:38:53 | 480x270   |
| `video_002` | 体育赛事 | 美加墨世界杯H组第1轮：西班牙VS佛得角FIFA World Cup Group H: Spain vs Cape Verde  | 02:03:58 | 1920x1080 |
| `video_003` | 体育赛事 | 美加墨世界杯E组第1轮：德国VS库拉索FIFA World Cup Group E: Germany vs Curacao     | 02:09:00 | 1920x1080 |
| `video_004` | 纪录片   | 地球脉动 第一季第一集：From Pole to PolePlanet Earth S01E01: From Pole to Pole   |    49:02 | 1920x1080 |
| `video_005` | 纪录片   | 地球脉动 第一季第二集：MountainsPlanet Earth S01E02: Mountains                   |    47:52 | 1920x1080 |
| `video_006` | 纪录片   | 地球脉动 第一季第三集：Fresh WaterPlanet Earth S01E03: Fresh Water               |    49:11 | 1920x1080 |
| `video_007` | 电影     | 教父1The Godfather (1972)                                                        | 02:57:09 | 1920x1080 |
| `video_008` | 电影     | 千与千寻Spirited Away (2001)                                                     | 02:04:32 | 1920x1038 |
| `video_009` | 电影     | 爱乐之城La La Land (2016)                                                        | 02:07:48 | 1920x754  |
| `video_010` | 电影     | 星际穿越Interstellar (2014)                                                      | 02:49:04 | 1920x1080 |

### 音频

| 编号          | 曲名                 | 作者                     |  时长 | 风格标签                                      |
| ------------- | -------------------- | ------------------------ | ----: | --------------------------------------------- |
| `audio_001` | Sports Highlights    | Ahjay Stelino            | 01:36 | sports, rock, aggressive, propulsive          |
| `audio_002` | Dirty Thinkin'       | Michael Ramir C.         | 01:29 | funk, energetic, groove, playful              |
| `audio_003` | Techno Fest Vibes    | Alejandro Magana (A. M.) | 01:09 | edm, high_energy, driving, celebratory        |
| `audio_004` | Fright Night         | Michael Ramir C.         | 01:41 | cinematic, tension, dark, suspense            |
| `audio_005` | Sun and His Daughter | Eugenio Mininni          | 02:48 | nature, poetic, world, expansive              |
| `audio_006` | Discover             | Eugenio Mininni          | 02:24 | documentary, hopeful, orchestral, wonder      |
| `audio_007` | Relax Beat           | Arulo                    | 01:48 | ambient, calm, observational, soft            |
| `audio_008` | Silent Descent       | Eugenio Mininni          | 02:40 | film_score, melancholic, reflective, dramatic |
| `audio_009` | Epical Drums 01      | Grigoriy Nuzhny          | 01:46 | cinematic, drums, epic, action                |
| `audio_010` | Romantic Getaway     | Ahjay Stelino            | 01:44 | romantic, warm, emotional, classical          |
| `audio_011` | Romantic Vacation    | Ahjay Stelino            | 01:52 | jazz, romantic, lounge, stylish               |

## 目录结构

```text
Mashup-Benchmark/
  data/
    tasks/mashup_benchmark.jsonl # 标准 40 任务 JSONL
    videos/                      # 长视频源文件，Git 忽略
    audios/                      # BGM 音频文件，Git 忽略
  manifests/                     # 视频、音频、任务和统计摘要索引
  schemas/                       # task/run/evaluation 记录的 JSON Schema
  scripts/                       # 校验脚本和工具脚本
  runs/                          # 待测系统输出、run_output.json 和 run_manifest.json
  outputs/                       # 非正式提交 run 的临时导出结果
  eval/                          # 评测代码
  eval_results/                  # 指标结果和 VLM-as-judge 打分结果
  reports/                       # 汇总表格、图表和实验记录
  docs/                          # benchmark 规范、指标协议和数据说明
```

## 系统输出格式

对每个任务，待测系统需要生成一个完整的短视频成片。Baseline 或待测方法的输出应放在：

```text
runs/<run_id>/task_outputs/<task_id>/output.mp4
```

每个任务的元数据需要符合 `schemas/run_output.schema.json`；整次运行的元数据需要符合 `schemas/run_manifest.schema.json`。详细提交格式见 `docs/run_submission_format.md`。

## 评测维度

完整质量分包含 7 个指标：

```text
Quality = weighted_mean(IF, BCS, AEC, VQ, TC, NC, OQ)
```

权重规则：

- 本地自动指标：`BCS = 0.20`，`AEC = 0.20`。
- VLM-as-judge 指标：`IF = 0.10`，`VQ = 0.10`，`TC = 0.10`，`NC = 0.10`。
- 人类评估指标：`OQ = 0.20`。
- 如果没有人类 `OQ` 分数，则对可用的 6 个指标自动归一化：`BCS = 0.25`，`AEC = 0.25`，`IF/VQ/TC/NC = 0.125`。

指标含义：

- IF：Instruction Following，指令遵循。
- BCS：Beat-Cut Synchronization，节拍-切点同步；基于最终成片的全帧视觉切换检测，不读取编辑 timeline。
- AEC：Audio-Visual Energy Correspondence，音画能量对应。
- VQ：Visual Quality，视觉质量。
- TC：Transition Continuity，片段和转场连续性。
- NC：Narrative Coherence，叙事连贯性。
- OQ：Overall Quality，人类整体质量评分，可选。

效率单独报告，包括 API 成本和端到端耗时。可运行评测器的说明见 `eval/README.md`。

## 校验与评测

校验 benchmark 数据结构：

```bash
python3 scripts/validate_benchmark.py
```

校验一个待测 run：

```bash
python3 scripts/validate_run.py runs/<run_id>
```

评测一个待测 run：

```bash
cp eval/config.example.yaml eval/config.yaml
python3 -m eval.run_evaluation --run runs/<run_id> --config eval/config.yaml
```

`eval/config.yaml` 用于配置 VLM 模型名、API key、base URL、超时时间和指标权重。该文件包含本地密钥配置，已被 Git 忽略；请不要提交。

## 许可证

- 代码使用 Apache License 2.0，见 `LICENSE`。
- benchmark 元数据、任务定义、prompt、schema、manifest 和文档使用 CC BY-NC 4.0，见 `LICENSE-DATA`。
- 本仓库不重新分发源视频或音频素材。用户需要自行从合法来源获取媒体文件，并遵守对应素材的原始版权、许可证和使用条款。
- 包含第三方版权媒体的生成视频不属于本仓库代码或数据许可证的授权范围。

第三方媒体和素材说明见 `NOTICE`。
