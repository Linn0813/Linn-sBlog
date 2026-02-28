---
title: 学了那么多术语，为什么还是不理解？LLM/Agent 学习路线图
date: 2025-11-29 18:00:00
updated: {{current_date_time}}

categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - AI与研究
tags:
  - LLM
  - Agent
  - 大语言模型
  - 智能体
  - Prompt工程
  - RAG
  - 学习指南
keywords: LLM, Agent, 大语言模型, 智能体, Prompt工程, RAG, 学习指南, Transformer, ReAct
description: 'Prompt、Token、RAG、ReAct…学了一堆术语却还是不理解？这份路线图帮你从「会用」走到「真懂」，系统掌握 LLM 与 Agent。'
top_img: /img/llm-agent-core-concepts-guide.png
cover: /img/llm-agent-core-concepts-guide.png 
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

> "我知道它能用，但我真的不理解它为什么能做到。"

学了 Prompt、Token、Embedding、RAG、ReAct、Agentic Loop……术语一堆，做项目时却还是"一知半解"。如果你也有这种感觉，这个系列就是为你写的。

过去一年，LLM 和 Agent 从写代码、自动化测试到知识问答、流程自动化，各种 Demo 层出不穷。但很多教程只讲"怎么用"，不讲"为什么能这样用"——底层机制拆得不够，实践心法也给得不够。

所以我做了这个**面向新手到进阶开发者**的系列：**《🧠 LLM/Agent 从入门到精通：告别浅尝辄止》**。每篇聚焦两个问题：

* **Why？** —— 这些机制为什么重要？解决了什么问题？
* **How？** —— 实际开发中该怎么正确使用？

目标是帮你从"会用"走到"理解原理"，从"能跑 Demo"走到"能做项目"。

---

## 📘 系列起点

想快速过一遍概念？可以先看[《LLM 与智能体（Agent）知识记录》](/2025-10-21-llm-agent-guide/)，当作本系列的知识地基。想直接开啃原理？从下面 Part I 第 1 篇开始即可。

---

## 🚀 系列展望：核心主题规划

下面是本系列计划覆盖的核心主题，它们构成了 LLM / Agent 理解体系的完整地图。

> **说明**：以下主题为初步规划，在实际写作过程中可能会根据内容需要、读者反馈进行调整（如拆分、合并、新增主题）。但核心知识体系会保持完整，确保你能系统掌握 LLM 和 Agent 的关键概念。

我会通过图示、例子、类比、真实项目经验，将这些看似"玄学"的内容拆得足够简单和清晰。

---

## **Part I: LLM 基础认知与 Prompt 工程（模型是大脑）**

> 新手建议从第 1 篇开始，按顺序读效果更好。

| #     | **主题**                                           | **核心拆解方向**                                | 
| :---- | :----------------------------------------------- | :---------------------------------------- |
| **1** | <a href="/2025-12-02-llm-working-principle-token-embedding-transformer/">ChatGPT 几秒出千字？背后只做了一件事</a>           | Token、Embedding、Transformer —— LLM 底层三件事。              |
| **2** | <a href="/2025-12-03-llm-prompt-context-in-context-learning/">模型答非所问？理解 Prompt、上下文与 In-Context Learning</a> | 大模型记忆的本质是什么？上下文限制怎么影响效果？                  |
| **3** | <a href="/2025-12-04-llm-prompt-engineering-practices/">想要 JSON 却得到废话？Prompt 工程的三大核心技巧</a>                   | 如何让模型稳定产生 JSON/YAML/Markdown。             |
| **4** | <a href="/2025-12-08-llm-rag-deep-integration/">模型一本正经地胡说八道？RAG 如何让 LLM 有据可查</a>                          | 检索 → 分块 → 重排 → 融合的完整流程。                   |
| **5** | <a href="/2025-12-09-llm-model-evaluation-selection/">GPT-4、Claude、Llama 怎么选？模型选型避坑指南</a>                     | 参数量、推理速度、成本如何权衡？ |

---

## **Part II: Agent 核心架构与决策机制（模型是大脑，Agent 是身体）**

| #      | **主题**                                         | **核心拆解方向**                    |
| :----- | :--------------------------------------------- | :---------------------------- |
| **6**  | <a href="/2025-12-10-llm-agent-concept-overview/">只会聊天不够用？Agent 如何让 LLM 能做事、会思考、能修正</a>              | 感知、规划、行动 → Agentic Loop 的全流程。 |
| **7**  | <a href="/2025-12-16-llm-agent-decision-engine/">Agent 怎么"想"和"做"？ReAct 决策引擎代码级拆解</a>             | ReAct Prompt 模板与真实调用示例。       |
| **8**  | <a href="/2025-12-19-llm-agent-task-planning/">复杂任务 Agent 怎么拆？任务规划与 Self-Correction</a>                 | 推理链、子任务分解、Self-Correction。   |
| **9**  | <a href="/2025-12-17-llm-agent-memory-management/">Agent 聊着聊着就忘了？记忆管理如何突破 Context Window</a>                  | 为什么 Agent 需要"记忆"？怎么设计高质量记忆？   |
| **10** | <a href="/2025-12-20-llm-agent-framework-comparison/">LangChain、LlamaIndex、AutoGPT 怎么选？Agent 框架对比</a> | 如何快速搭建一个可靠的 Agentic System。   |

---

## **Part III: 实践、治理与进阶应用（落地、可控、可观测）**

| #      | **主题**                                 | **深度聚焦**                         |
| :----- | :------------------------------------- | :------------------------------- |
| **11** | <a href="/2025-12-21-llm-agent-spec-design/">Agent 输出飘忽不定？用 Schema 锁死格式</a> | 如何设计结构化规范（JSON Schema、Pydantic）。 |
| **12** | <a href="/2025-12-18-llm-agent-tool-system/">Agent 怎么查数据库、调 API？Function Calling 与工具封装</a>          | 安全、幂等、工具自描述（Tool Description）。   |
| **13** | <a href="/2025-12-22-llm-agent-security-governance/">Agent 失控了怎么办？日志、审计与可观测性</a>           | 如何避免 Agent"失控"？如何复盘 Agent 行为？    |
| **14** | <a href="/2025-12-23-llm-agent-multi-agent-collaboration/">一个 Agent 不够用？多 Agent 协作像团队一样干活</a>           | 角色设定、话术设计、协作协议、消息流。              |
| **15** | <a href="/2025-12-24-llm-agent-evaluation/">Agent 好不好怎么衡量？评估指标体系与避坑指南</a>                 | 减少工具滥用、避免无限循环、提高成功率。             |

---

## 🎯 这个系列适合谁？

* **希望从零入门 LLM/Agent 的新手**
* **已经做过 Demo，希望系统提升的人**
* **做知识库问答、自动化测试、业务流自动化的开发者**
* **AI 产品经理 / QA / 技术 Leader**
* 想把"碎片化知识 → 体系化理解"的任何人

如果你在工作中想：

* 构建自己的 Agent
* 为公司做 AI 赋能
* 做 LLM 测试或知识库问答
* 更深入理解大模型机制
* 不再只是"调调 Prompt"

那么，这个系列会非常适合你。

---

## 🔔 从这里开始

> **[ChatGPT 几秒出千字？背后只做了一件事](/2025-12-02-llm-working-principle-token-embedding-transformer/)** —— 搞懂 Token、Embedding、Transformer 三件事，你就搞懂了 LLM 的底层逻辑。
