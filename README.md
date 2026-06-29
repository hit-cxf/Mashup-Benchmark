# Mashup-Benchmark

[English](README_EN.md)

Mashup-Benchmark 是一个面向长视频自动剪辑的 benchmark，用于评估短视频混剪、精彩集锦和音乐驱动剪辑系统的生成质量与效率。

本仓库默认以中文 README 作为主入口。以后修改 benchmark 结构、数据协议、评测指标或运行方式时，需要同步更新 `README.md` 和 `README_EN.md`，保证中英文内容一致，并与项目当前实现保持同步。示意图、图表和论文风格插图可以统一使用英文标注。

![Mashup-Benchmark Overview](docs/assets/mashup_benchmark_overview.png)

## 数据集

- 10 个小时级长视频源：3 场体育赛事、3 集纪录片、4 部电影。
- 40 个视频-提示词任务：每个长视频对应 4 类任务，分别是事件型、人物型、情绪型和叙事型。
- 11 首 Mixkit BGM，根据任务情绪和风格进行分配。
- 默认目标成片时长：60 秒。
- 默认目标 shot 时长：4 秒。

标准任务文件是 `data/tasks/mashup_benchmark.jsonl`，其中每一行对应一个视频-提示词-音频任务。

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
- BCS：Beat-Cut Synchronization，节拍-切点同步。
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

## 维护约定

- `README.md` 是默认中文入口，`README_EN.md` 是英文镜像版本。
- 修改 README 时，两份文件需要同步更新，内容含义保持一致。
- 修改数据、schema、评测代码或目录结构后，需要同步更新 README、`docs/` 中对应规范和相关示例。
- `data/videos/` 和 `data/audios/` 存放大体积媒体文件，默认不纳入 Git。
- `runs/` 存放不同 baseline 或待测系统生成的视频结果；正式结果应附带 `run_manifest.json` 和每个任务的 `run_output.json`。
