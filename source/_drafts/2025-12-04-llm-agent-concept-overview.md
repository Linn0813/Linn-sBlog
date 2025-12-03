---
title: 🧠 5/15｜Agent 概念全景：Agent 是如何从 LLM 进化而来的？
date: 2025-12-04 18:00:00
series: 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
categories:
  - 技术学习与行业趋势
  - AI与研究
tags:
  - LLM
  - Agent
  - 智能体
  - Agentic Loop
  - Planner
  - Tools
  - Memory
keywords: LLM, Agent, 智能体, Agentic Loop, Planner, Tools, Memory, 自主循环, 工具调用, 智能体架构
description: '系统理解 Agent 的本质：从 LLM 到智能体的进化路径，深入解析 Agent 的核心构成、生命周期和关键模块，构建完整的 Agent 系统架构'
top_img: /img/llm-agent-concept-overview.png
cover: /img/llm-agent-concept-overview.png
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

> **这是《LLM/Agent 核心知识体系》系列第 5 篇**

> 上一篇我们深入解析了 RAG 机制，构建了抗幻觉的知识增强系统。

> 本篇，我们将系统理解 Agent 的本质，揭秘 LLM 如何进化为具有"行动能力"的智能体，以及如何构建一个完整的 Agent 系统。

---

## 🚀 导言 — 从"大模型"到"智能体"

在之前几篇里，我们已经赋予 LLM 语言理解能力（Token、Transformer）、Prompt 控制能力、以及通过 RAG 获取知识的能力。

但纯粹的 LLM 是 **被动的** —— 它只能在你问它时才回应。

要让 LLM 真正变成一个 **有"行动能力 (Agency)"的智能体 (Agent)**，它需要能够 **自主分解任务 → 调用工具/接口 → 在环境中执行 → 根据反馈调整**。

本篇带你系统理解什么是 Agent，Agent 的核心构成、它与传统 LLM 的区别，以及如何构建一个 Agent 系统。

---

## 一、Agent 的本质 — 执行 + 决策 + 反馈 的闭环系统

### 1.1 什么是 Agent？

一个真正的 Agent，是一个能在 **环境 (Environment)** 中：

* **感知 (Perception)** —— 接收用户输入 + 工具／环境反馈 (Observation)

* **规划 (Planning)** —— 使用 LLM 分解问题，决定下一步行动

* **行动 (Action)** —— 调用外部工具 / API / 脚本 / 系统接口

* **记忆 (Memory)** —— 保存历史信息 / 结果，以利长期任务或上下文连贯

可以把它抽象成：

```
Agent = LLM (大脑) + Tools (手脚) + Memory (记忆) + Loop (自主循环)
```

| 组成              | 核心功能                  | 对应 LLM 概念                        |
| --------------- | --------------------- | -------------------------------- |
| Perception (感知) | 接收输入／反馈               | Prompt + Observation             |
| Planning (规划)   | 分析任务／选择工具／生成执行方案      | CoT / ReAct / Prompt Engineering |
| Action (行动)     | 执行具体操作（API／脚本／文件／数据库） | Function Calling / Tool Call     |
| Memory (记忆)     | 存储历史状态／结果／知识／用户偏好     | Context 管理 + 外部数据库/RAG           |

### 1.2 LLM vs Agent — 本质上的区别

| 维度          | 传统 LLM          | Agent (智能体)                   |
| ----------- | --------------- | ----------------------------- |
| **主动性**     | 被动 (只回应 Prompt) | 主动 (可以自主决定下一步)                |
| **目标 & 任务** | 单次生成 / 回答       | 多步、复杂任务 + 行动 + 环境交互           |
| **与外界交互能力** | 仅限文本输入/输出       | 可以调用工具、API、修改状态、操作系统等         |
| **机制**      | 自回归文本生成         | 决策–执行–观察–反馈的循环 (Agentic Loop) |

> 一个 Agent，不只是"会说话"的模型，而是"会做事、有记忆、能反馈、能修正"的系统。

---

## 二、♻️ Agent 的生命周期：Agentic Loop（自主循环）

Agent 的核心机制是一个 **循环 (Loop)**，它不是一次性，而是不断 "感知 → 规划 → 行动 → 反馈 → 继续"。

### 2.1 Agentic Loop 流程

1. **Observe (感知)**：接收用户指令或新的输入 + 上一步工具／系统的返回结果 (Observation)

2. **Plan (规划)**：LLM 根据当前上下文 + 记忆，决定下一步要做什么 (Thought)

3. **Act (执行)**：调用工具 / API / 脚本 / 系统命令 (Action)

4. **Feedback (反馈)**：获取工具或系统执行结果 (Observation)，更新记忆 / 状态

5. **Loop Continue**，直至满足最终目标或触发终止条件

### 2.2 为什么要循环 (Loop)

* 很多任务不是一次性可以完成，而是需要多个步骤（例如：数据查询 → 数据处理 → 输出报告 → 发送邮件）

* 环境是动态的，需要根据中间结果不断调整决策

* Agent 的闭环机制使它不仅能推理，还能"做事情 + 检查结果 + 再做"

### 2.3 循环终止条件 (Termination Criteria)

为了防止无限循环或失控，必须设定合理终止条件：

* **目标达成判断**：Agent 自己判断任务已完成 (e.g. "报告已发送")

* **资源限制**：最大步数、最大时间、最大 API 调用次数等

* **错误阈值**：连续失败次数达到上限 → 终止并返回错误日志

* **人工干预 / 审批**：对于高风险操作 (如删除数据、修改系统配置) 需要用户确认

---

## 三、Agent 的关键模块：构建一个完整 Agent 系统

为了实现上述功能，Agent 通常由以下模块组成：

### 3.1 🧠 Planner (LLM + Prompt 控制)

* **职责**

  * 将当前任务 + 环境状态 + 记忆 / 历史信息 编成 Prompt

  * 使用 Prompt 指导 LLM 输出 **结构化 Thought + Action**

* **关键能力**

  * Prompt engineering (包括角色定义、格式约束)

  * 支持 Function Calling（或 Tool Call）输出

### 3.2 🛠️ Tools & Executor (工具与执行器)

* **工具 (Tool)**：任何外部函数 / API / 模块 / 脚本 / RAG 查询 / 系统接口 —— 让 Agent 能做真实有用的事情

* **工具规范 (Tool Schema)**：必须为每个工具定义清晰输入 / 输出格式 (最好使用 JSON Schema)，让 Planner 输出可被正确解析

* **执行器 (Executor)**：负责实际执行工具调用，并捕获返回结果 (Observation)，包括成功输出或错误信息

> **实战提示**：建议尽可能将工具设计得简单、接口清晰、失败可控；这样 Agent 运行更稳定、易调试。

### 3.3 💾 Memory / Context Manager

Agent 需要同时处理 **短期记忆** 与 **长期记忆**：

* **短期记忆 (Short-term)**：当前 Loop 的历史 (Thoughts, Actions, Observations)，用于保持上下文连贯

* **长期记忆 (Long-term)**：通用知识库、用户偏好、历史任务结果、RAG 存储

* **压缩与管理**：因为 Context Window / Token 限制，需要对过长历史做 **摘要 / 压缩** 或外部存储

### 3.4 Agentic Loop 的伪代码示例

```python

def run_agent(task, initial_memory):

    memory = initial_memory

    steps = 0

    while steps < MAX_STEPS:

        prompt = build_prompt(memory, task)

        thought, action = llm.generate(prompt)

        if is_goal_reached(thought):

            return thought

        tool_name, args = parse(action)

        observation = executor.call(tool_name, args)

        memory.update(thought, action, observation)

        steps += 1

    return {"error": "max steps exceeded"}

```

---

## 🔍 为什么构建 Agent 很重要 — 它真正将 LLM 推向现实

* **自动化复杂任务**：不仅是"问答/生成文本"，而是"查资料 + 处理 + 输出 + 执行"，适合自动化流程

* **可追踪 & 可审计**：每一步都有工具调用、Observation、Memory 记录，便于审计与调试

* **持续能力 & 演化**：通过 Memory 和工具库，Agent 可以重复利用已有能力，也能扩展新能力

* **从辅助到主动**：不只是被动回应用户，而是主动完成任务 (e.g. 自动报告生成、日常流程自动化)

简而言之：Agent 是 LLM 从"会说话"到"能做事 + 会思考 + 会改"的演化，是构建真正智能自动化系统的基础。

---

## 📚 延伸阅读与关键资源（带链接）

| 主题 / 资源                           | 链接                                                                                                                                       |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| ReAct: Reasoning + Acting in LLMs | [ArXiv 原文 (2210.03629)](https://arxiv.org/abs/2210.03629) / [项目主页 + 示例 Prompt 模板](https://react-lm.github.io/) ([react-lm.github.io][1]) |
| Agentic AI 系统最新综述                 | [Adaptive and Resource‑efficient Agentic AI Systems (2025 survey)](https://arxiv.org/abs/2510.00078) ([arXiv][2])                        |
| 多模态 Agent 综述                      | [A Survey on Agentic Multimodal Large Language Models (2025)](https://arxiv.org/abs/2510.10991) ([arXiv][3])                             |
| Agent 架构 & 工具调用设计参考               | 各大框架文档 (如 LangChain / LlamaIndex 等) 与工具调用最佳实践指南（可通过搜索 "LLM Tool Calling best practices" 获取）                                              |

> 🔎 如果未来你想为这个系列添加"实践回顾 + Demo 代码 + 工具链推荐"，我也可以帮你整理一份。

---

## 🔔 下一篇预告

在理解了 Agent 的整体架构与构成后，下篇我们将深入 Agent 的"决策引擎"：分析 **ReAct / Self-Ask / Tree-of-Thought** 等高级策略，讨论它们的优缺点、适用场景与 Prompt 设计方法。

**标题（暂定）：**

### 《6/15｜Agent 决策引擎深度解析：ReAct / Self‑Ask / Tree‑of‑Thought 全景对比》

