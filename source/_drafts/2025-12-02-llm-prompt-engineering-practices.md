---
title: 🧠 3/15｜Prompt 工程实战：三大核心技巧与结构化输出
date: 2025-12-02 18:00:00
series: LLM/Agent 核心概念与新手快速上手指南
categories:
  - 技术学习与行业趋势
  - AI与研究
tags:
  - LLM
  - Prompt工程
  - ReAct
  - Schema
  - 结构化输出
  - Chain-of-Thought
keywords: LLM, Prompt工程, ReAct, Schema, 结构化输出, Chain-of-Thought, CoT, Self-Correction, 提示工程实战
description: 'Prompt 工程实战指南：掌握明确角色、思维链进阶和结构化输出三大核心技巧，实现稳定、可解析的高质量输出'
top_img: /img/llm-prompt-engineering-practices.png
cover: /img/llm-prompt-engineering-practices.png
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

> **这是《LLM/Agent 核心知识体系》系列第 3 篇**

> 上一篇我们理解了 LLM 的"语言"：Prompt、上下文窗口和 In-Context Learning。

> 本篇，我们从实战角度，掌握 Prompt 工程的三大核心技巧，实现稳定、可解析的结构化输出。

---

## 🚀 导言 — 从"聊天"到"高效工作"

在前两篇中，我们掌握了 LLM 的底层机制（Token、Transformer）和交互基础（Prompt、ICL）。

实际开发 Agent 或自动化流程时，最令人头疼的问题往往不是模型能力不够，而是**输出格式不稳定**：

> 你希望得到 JSON，却得到了一段解释文字；

> 你希望表格化输出，结果模型输出了自由文本。

本篇，我们将介绍 **Prompt Engineering 的三大核心技巧**，帮助你获得**稳定、可解析的结构化输出**：

1. **明确角色（Persona Defining）**

2. **思维链进阶（Advanced CoT / ReAct）**

3. **结构化输出保障（Schema + 分隔符）**

---

## 👑 技巧一：明确角色（Persona Defining）

定义一个清晰、专业的角色，是高质量输出的第一步。

### 为什么定义角色很重要？

* **聚焦领域**：让模型扮演"资深测试架构师"，它会使用更专业的术语和逻辑。

* **约束语气**：确保输出专业、简洁、不冗长。

* **减少幻觉**：专业角色能减少随意编造信息的可能。

### 角色定义要点

| 要点     | 描述           | 示例                        |
| ------ | ------------ | ------------------------- |
| **身份** | 具体且权威        | "你是一位经验丰富的 Python 后端工程师。" |
| **目标** | 唯一任务目标，消除歧义  | "你的目标是生成符合 PEP 8 的代码。"    |
| **限制** | 明确禁止或必须遵守的行为 | "禁止在代码块之外添加任何解释性文字。"      |

> 🔧 **实战提示**：将角色定义放在 **System Prompt** 中，以赋予最高权重和持续性。

---

## 🔗 技巧二：思维链进阶（Advanced CoT / ReAct）

在复杂任务中，单纯的 Prompt 可能不够。

**ReAct（Reasoning + Acting）** 能让 LLM 在行动前先思考，再执行工具调用，实现闭环决策。

### ReAct 步骤

| 步骤              | 内容          | 作用                       |
| --------------- | ----------- | ------------------------ |
| **Thought**     | 分析任务，决定下一步  | 激活内部逻辑，将复杂任务拆解           |
| **Action**      | 决定调用工具或执行函数 | 明确执行路径，如 `Search(Query)` |
| **Observation** | 接收工具结果      | 为下一次 Thought 提供输入，形成反馈闭环 |

### Prompt 模板示例

```text

你需要按照以下格式输出：

Thought: [你的思考]

Action: [调用的工具名(参数)]

Observation: [工具返回结果]

...重复此循环，直到得到最终答案

```

### CoT 与自我修正（Self-Correction）

当 Observation 阶段出现错误，可在下一次 Thought 中要求模型**识别并修正错误**：

```text

Thought: 上一步调用 API 失败，返回 404，原因是缺失参数"ID"。我需要重新规划 Action，补充缺失参数。

```

> 🔹 这让复杂任务更可控，避免错误累积。

---

## 🧱 技巧三：确保结构化输出（Schema + 分隔符）

这是最关键的一环，尤其当下游程序需要 JSON / YAML / XML 时。

### 核心方法：使用 Schema 约束

* **定义**：Schema 描述输出数据结构（JSON Schema、Pydantic 等）

* **作用**：不仅告诉模型"输出 JSON"，还规定字段名、类型、必选项

#### 示例

| 步骤               | 方法                                  | Prompt 片段                                                                                                                                |
| ---------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **1. 格式声明**      | 明确仅输出 JSON                          | "你的输出必须且只能是 JSON 格式。"                                                                                                                    |
| **2. 注入 Schema** | 将 JSON Schema 文本加入 Prompt           | `{"type":"object","properties":{"user_id":{"type":"integer"},"task_list":{"type":"array","items":{"name":"string","status":"string"}}}}` |
| **3. 使用工具**      | 高级：调用 `function_call` / `tool_call` | 模型直接输出符合 Schema 的函数对象                                                                                                                    |

### 使用分隔符

分隔符帮助模型专注核心任务，区分指令、上下文和用户输入：

```text

请总结 <<<用户输入>>> 中的内容，并以 YAML 输出摘要和关键词。

<<<用户输入>>>

[用户粘贴的文本]

<<<END>>>

```

---

## 🔍 总结：Prompt Engineering 的设计哲学

| 目标     | 原则             | 技巧            |
| ------ | -------------- | ------------- |
| 高质量输出  | 限制自由度，聚焦专业     | 明确角色（Persona） |
| 复杂任务分解 | 外化思维过程，便于检查与修正 | ReAct 范式      |
| 程序化对接  | 确保机器可读、可验证     | Schema + 分隔符  |

> 三大技巧结合使用，你的 Prompt 从模糊提问升级为精确指令。

---

## 📚 延伸阅读（带链接）

| 主题                    | 链接                                                                                                                                    |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| ReAct 范式              | [ReAct: Synergizing Reasoning and Acting in Language Models (arXiv 2022)](https://arxiv.org/abs/2210.03629)                           |
| Schema 约束             | [Pydantic 官方文档](https://docs.pydantic.dev/) & [OpenAI Function Call 文档](https://platform.openai.com/docs/guides/gpt/function-calling) |
| Prompt Engineering 指南 | [OpenAI Prompting Guide](https://platform.openai.com/docs/guides/prompting)                                                           |
| Self-Correction       | [Self-Correction Mechanisms in LLMs (论文)](https://arxiv.org/abs/2302.06675)                                                           |

---

## 🔔 下一篇预告

结构化输出解决了格式问题，但仍存在**知识受限**的问题。下一篇，我们将介绍 **RAG（检索增强生成）**，突破 LLM 的**知识时间限制与专业性边界**。

**标题：**

### 《4/15｜解决"幻觉"：RAG机制与外部知识融合》

