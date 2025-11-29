---
title: 🧠 2/15｜理解 LLM 的"语言"：Prompt、上下文与 In‑Context Learning
date: 2025-12-01 18:00:00
series: LLM/Agent系列教程
categories:
  - 技术学习与行业趋势
  - AI与研究
tags:
  - LLM
  - Prompt
  - In-Context Learning
  - Context Window
  - Chain-of-Thought
  - 大语言模型
keywords: LLM, Prompt, In-Context Learning, Context Window, Chain-of-Thought, CoT, 提示工程, 上下文学习, 大语言模型
description: '深入理解 LLM 的"语言"：从 Prompt 工程、上下文窗口管理到 In-Context Learning，掌握与 LLM 有效对话的核心技巧'
top_img: /img/llm-prompt-context-in-context-learning.png
cover: /img/llm-prompt-context-in-context-learning.png
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

> **这是《LLM/Agent 核心知识体系》系列第 2 篇**

> 上一篇我们讲了 LLM 的"物理基础"：Token、Embedding、Transformer。

> 本篇，我们从"人机对话"的角度，理解如何让 LLM 从"会说话"变成"按指令办事"。

---

## 🚀 导言 — 与 LLM 沟通的艺术

LLM 是一台**强大的概率预测机器**：它根据已有的 Token 预测下一个最可能出现的 Token。

* **但问题是**：预测本身 ≠ 执行任务

* **解决办法**：我们需要学会"对 LLM 说它能听懂的话"。这就是 **Prompt Engineering（提示工程）** 的意义

本篇我们聚焦三大关键概念：

1. **Prompt（提示 / 指令）** — 你给模型的"剧本"

2. **Context Window（上下文窗口）** — 模型的短期记忆

3. **In‑Context Learning（上下文学习）** — LLM 的"即学即用"魔法

---

## 📜 一、Prompt —— 给 LLM 的"剧本"

Prompt 就像导演给演员的剧本，告诉 LLM **做什么、怎样做、输出什么格式**。

### 1.1 两种核心 Prompt 类型

| 类型                   | 定义              | 示例                                  | 作用                  |
| -------------------- | --------------- | ----------------------------------- | ------------------- |
| **Zero‑Shot Prompt** | 不提供示例，仅给指令      | "请总结以下段落的核心观点。"                     | 模型依赖预训练知识直接推理       |
| **Few‑Shot Prompt**  | 提供 1–5 个输入‑输出示例 | 输入: `A -> 1`, `B -> 2`，然后问 `C -> ?` | 通过示例引导模型学习任务模式与输出风格 |

> **比喻理解**：

> Zero‑Shot 就像演员即兴表演；Few‑Shot 就像给演员提前排练几次，告诉他们节奏和风格。

### 1.2 System Prompt（系统指令）

System Prompt 是 LLM 的"身份设定"，它常具有比用户 Prompt 更高的优先级：

* **用途**：定义模型角色、风格、全局行为规则

* **示例**：

  ```
  你是一个严谨、专业的测试专家。  

  你只输出 Markdown 表格，不写解释文字。  

  ```

> ✅ **建议**：合理设置 System Prompt，有助于模型行为一致、稳定

---

## 🪟 二、Context Window —— 模型的"短期记忆"

LLM 不可能"无限记忆"，它有一个长度限制 —— **Context Window**

### 2.1 什么是 Context Window

* **定义**：模型在一次推理中"看到"的最大 Token 数

* **组成部分**：System Prompt + 历史对话 + 当前输入 + 模型的中间输出

* **物理限制**：由于 Transformer 中 Self‑Attention 的计算复杂度与 Token 数量平方相关，

  当 Token 数量过多时，代价将迅速上涨

* **结果**：当超过限制，最早的 Token 会被"遗忘" —— 即"上下文溢出 (overflow)"

> **比喻**：Context Window 就像办公桌，一张桌子放太多纸，旧纸就被挤下桌面

### 2.2 应对 Context Window 限制的策略

| 策略                                       | 方法                   | 效果              |
| ---------------------------------------- | -------------------- | --------------- |
| **摘要 (Summarization)**                   | 将旧对话 / 内容整理为简短摘要     | 节省 Token，保留关键信息 |
| **记忆模块 (Memory)**                        | 抽取关键信息存入外部数据库，当需要时检索 | 关键信息不丢失         |
| **RAG (Retrieval‑Augmented Generation)** | 只把与当前任务相关的片段放入窗口     | 支持超长文档处理        |

> 💡 用摘要 / Memory / RAG 结合起来，是处理长对话 / 文档时的常见实践

---

## ✨ 三、In‑Context Learning (ICL) —— LLM 的"魔法"

ICL 允许 LLM **无需微调**，仅通过 Prompt（尤其 Few‑Shot + 示例）学习新任务 / 模式

### 3.1 ICL 的本质

* **不是**改变模型参数

* **而是**在 Context Window 内识别输入‑输出示例之间的"模式 / 结构"，并应用到新输入上

* **效果**：快速上手新任务、无需大量数据

> 比喻：就像老师黑板上写几个例子，学生看懂规则，就能回答新问题

### 3.2 成功应用 — 思维链 (Chain‑of‑Thought, CoT)

CoT 是 ICL 的经典用法，在复杂推理、逻辑题、数学题中尤其有用

* **做法**：Prompt 要求模型"先写思考过程 (step by step)，再给答案"

* **好处**：

  1. 激活模型内部"逻辑推理链"

  2. 提供更多 Token "空间"给中间推理

  3. 输出可读、可复查、方便调试

| CoT 类型            | 使用方式                 | 示例 (prompt)              |
| ----------------- | -------------------- | ------------------------ |
| **Zero‑Shot CoT** | 在问题后加一句 "请一步步思考"     | `… + 请一步步思考。`            |
| **Few‑Shot CoT**  | Few‑Shot 示例中包含完整思考过程 | `[输入] → [详细思考过程] → [输出]` |

> ⚠️ 注意：ICL / CoT 与 **Fine‑Tuning（微调）** 是不同的 — 前者不改模型参数

---

## 🔍 总结 — 与 LLM 有效对话的三把"钥匙"

* **Prompt = 剧本**，Clear / Proper 的 Prompt 是控制 LLM 的基础

* **Context Window = 桌面**，合理管理上下文，防止"记忆溢出"

* **ICL / CoT = 魔法**，通过示例 + 思考链，让模型迅速适应新任务

掌握它们，就可以设计结构化、高稳定性的 Prompt，实现复杂任务处理

---

## 📚 延伸阅读（可点击链接直接访问）

| 主题                                       | 资源 / 链接                                                                                                                                                         |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Few‑Shot / In‑Context Learning           | **"Language Models are Few‑Shot Learners" (GPT‑3 原始论文)** — [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165) ([OpenAI][1])                   |
| Chain‑of‑Thought (CoT) Prompting         | **"Chain‑of‑Thought Prompting Elicits Reasoning in Large Language Models"** — [https://arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903) ([arXiv][2]) |
| Context Window 与 长文本处理                   | 推荐阅读 Transformer / LLM 的上下文处理文章（如 "Transformer Complexity & Context Management"）／相关博客                                                                           |
| Prompt Engineering 实践 / System Prompt 方法 | 官方 API 文档 + 各大技术博客 (如 OpenAI 教程、Hugging Face Blog)                                                                                                              |

> ✅ **建议**：你可以把这些链接加入文章结尾，方便读者点击、深入学习

---

## 🔔 下一篇预告

**第 3 篇将进入实战技巧**：

> 如何设计结构化、高稳定性的 Prompt？

> 如何结合 RAG 突破 Context Window 的限制？

**标题（暂定）：**

### 《3/15｜Prompt 工程基础：三大核心技巧与结构化输出》

