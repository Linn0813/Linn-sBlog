---
title: Agent 能力怎么提升？微调与 Prompt 工程进阶
date: 2026-01-02 18:00:00
updated: {{current_date_time}}

categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - AI与研究
tags:
  - LLM
  - Agent
  - Fine-Tuning
  - Prompt工程
  - LoRA
  - 能力调优
keywords: LLM, Agent, Fine-Tuning, 微调, Prompt工程, LoRA, PEFT, Structured CoT, RLHF-A, 能力调优
description: '深入解析 Agent 能力调优：从 Prompt 工程进阶到模型微调，掌握思维链优化、工具 Schema 优化和持续学习反馈闭环，实现专业化 Agent'
top_img: /img/llm-agent-capability-tuning.png
cover: /img/llm-agent-capability-tuning.png
comments: true
toc: true
toc_number: true
toc_style_simple: false
copyright: true
copyright_author: yuxiaoling
copyright_info: 版权所有，转载请注明出处。
mathjax: false
katex: false
aplayer: false
highlight_shrink: false
aside: true
noticeOutdate: false
---

Agent 在 70% 的场景表现不错，但一到复杂边界就崩——**怎么提升到专业级可靠？**

能力调优有两条路径：**Prompt 工程进阶**（不碰模型参数，优化思维链和工具 Schema）和**模型微调**（LoRA/PEFT，让 Agent 在特定领域稳定表现）。本篇解析两者策略选择与工程实践。

---

## 一、Prompt Engineering 进阶：思维链优化

即便不微调模型，也能通过优化 Prompt 显著提升 Agent **规划和推理能力**。

### 1.1 思维链结构优化（Structured CoT）

金融风控 Agent 判断是否放贷——Thought 跳跃或模糊会导致误判。ReAct 思维链在实际工程中可能产生跳跃或模糊的 Thought。通过**强制结构化**：

```text

Thought:

1. Previous Observation Analysis: [分析上一步结果]

2. Missing Information: [确认缺失信息]

3. Next Action Plan: [明确下一步目标]

4. Action Call: [生成工具调用]

```

* **价值**：确保逻辑严密、自省完整，降低规划错误率。

* **工程实践**：在生产 Agent 中统一 Thought 模板，便于日志分析和失败模式追踪。

### 1.2 拒绝机制与安全强化

通过 Prompt 指令增强安全性和权限遵守：

```text

System: 你是安全主管。首要任务是保障系统安全。

Rule: 严禁执行涉及删除数据的操作。如果用户要求，你必须回复:

"权限不足，操作被拒绝。"

```

* **Few-Shot 示例**：提供拒绝操作案例，教会模型标准回应。

* **效果**：降低越权或敏感操作风险。

### 1.3 工具 Schema 优化

Agent 误用工具通常源于描述不清：

| 错误示例                                  | 优化示例                                                                 |
| :------------------------------------ | :------------------------------------------------------------------- |
| `Search(query): Search the database.` | `SearchFinancialRecords(query): 访问最新 Q3 财报和股权变动数据，参数必须包含公司名和查询日期范围。` |

* **价值**：提高工具选择正确率，减少重复试错。

---

## 二、模型微调（Fine-Tuning）：定制化 Agent

Prompt Engineering 有其极限，当 Agent 需要**稳定掌握特定行为模式或专业术语**时，微调必不可少。

### 2.1 选择微调的场景

| 调优目标    | 推荐策略      | 深度解析                    |
| :------ | :-------- | :---------------------- |
| 通用推理    | Prompt 调优 | LLM 基础能力够强，无需修改参数       |
| 工具使用稳定性 | 微调        | 教会模型在特定场景下选择正确工具和参数     |
| 特定格式生成  | 微调        | 确保输出 XML、YAML 或企业内部格式稳定 |
| 领域术语掌握  | 微调        | 保证专业术语、缩写和行话使用准确        |

### 2.2 微调数据集构建

微调需要完整的 **Thought-Action-Observation** 序列：

1. **收集失败案例**：从评估日志中获取错误 Thought 和 Action。

2. **专家修正**：人类专家修正 Thought 链和 Action，生成正确序列。

3. **构建训练序列**：

```text

Input: System Prompt + User Query + Tools Schema + (History)

Output: Correct Thought + Correct Action Call + Expected Observation

```

### 2.3 微调技术：LoRA（Low-Rank Adaptation）

* **机制**：冻结预训练权重，在 Transformer 模块中注入可训练低秩矩阵。

* **优势**：大幅降低计算和存储成本，可在消费级硬件上进行专业化训练。

* **实践**：可结合 Prompt 工程，在微调后使用 Structured CoT 提高推理可靠性。

---

## 三、持续学习与反馈闭环

Agent 调优是持续过程，构建类似 **RLHF-A** 的反馈闭环尤为重要：

1. **部署（Deploy）**：生产环境运行 Agent

2. **监控（Monitor）**：收集结构化日志、成功/失败案例

3. **评估（Evaluate）**：Judge LLM 或专家评分失败案例

4. **数据生成（Data Generation）**：将失败案例修正成高质量 Thought-Action 序列

5. **调优（Tune）**：Prompt 优化或模型微调

6. **迭代（Iterate）**：部署新版本，循环监控与优化

> **名词卡片**

>

> * **PEFT**：参数高效微调技术，如 LoRA

> * **Structured CoT**：强制逻辑步骤的 Thought 结构

> * **RLHF-A**：面向 Agent 的强化学习反馈机制，关注完整行动序列

---

## 🔍 总结：工程与科学结合

Agent 调优体现 LLM 工程的最高价值。通过：

* 系统化优化 Thought 结构（Prompt Engineering）

* 精准微调工具使用与专业术语（Fine-Tuning）

可以将 Agent 性能从"可用"提升到 **专业级可靠**。

---

## 📚 知识来源与进阶阅读

| 主题                | 搜索关键词                                      | 来源                         |
| :---------------- | :----------------------------------------- | :------------------------- |
| Agent Fine-Tuning | Fine-Tuning LLMs for Tool Use              | Hugging Face 教程、Agent 框架博客 |
| LoRA 技术           | Low-Rank Adaptation of LLMs                | 微软论文 (2021)                |
| RLHF for Agents   | Reinforcement Learning for Agentic Systems | 学术研究与强化学习论文                |
| Structured CoT    | Advanced Prompt Engineering for Reasoning  | 行业指南、技术博客                  |

---

> 本文是[《🧠 LLM/Agent 从入门到精通：告别浅尝辄止》](/categories/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/)系列第 16 篇。上一篇：[Agent 好不好怎么衡量？评估指标体系与避坑指南](/2025-12-24-llm-agent-evaluation/)。下一篇：[Agent 怎么落地企业？RPA、流程自动化与实践](/2026-01-03-llm-agent-enterprise-applications/)。

