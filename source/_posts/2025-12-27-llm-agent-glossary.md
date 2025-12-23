---
title: 📚 工具篇｜LLM/Agent 系列术语速查手册
date: 2025-12-27 20:00:00
updated: 2025-12-27 20:00:00
series: 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
categories:
  - 技术学习与行业趋势
  - AI与研究
tags:
  - LLM
  - Agent
  - 术语表
  - 词汇表
  - 速查手册
keywords: LLM, Agent, 术语表, 词汇表, 速查手册, 技术术语, 概念检索
description: 'LLM/Agent 系列完整术语速查手册，按主题分类整理所有核心概念，提供简洁定义和文章链接，方便快速检索和理解'
top_img: /img/llm-agent-glossary.png
cover: /img/llm-agent-glossary.png
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

> **这是[《🧠 LLM/Agent 从入门到精通：告别浅尝辄止》](/series/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/)系列的工具篇**

> 本文档是本系列的**术语速查手册**，按主题分类整理了所有核心概念，提供简洁定义和文章链接，方便你快速检索和理解。

---

## 🎯 使用说明

本文档按以下方式组织：

1. **按主题分类**：将术语分为 LLM 基础、Prompt 工程、RAG、Agent 架构等类别
2. **简洁定义**：每个术语提供一句话核心定义
3. **文章链接**：标注详细讲解的文章位置
4. **快速检索**：使用 `Ctrl+F` 或 `Cmd+F` 快速查找

---

## 📖 一、LLM 基础概念

### **LLM (Large Language Model)**
**定义**：大语言模型，基于 Transformer 架构的深度学习模型，能够理解和生成自然语言。

**详细讲解**：[主题1｜LLM 工作原理深度解析](/技术学习与行业趋势/AI与研究/2025-12-02-llm-working-principle-token-embedding-transformer/)

---

### **Token**
**定义**：LLM 处理文本的最小单位，可以是单词、词根、汉字或符号。

**详细讲解**：[主题1｜LLM 工作原理深度解析](/技术学习与行业趋势/AI与研究/2025-12-02-llm-working-principle-token-embedding-transformer/)

---

### **Embedding (向量嵌入)**
**定义**：将文本转换为数值向量的过程，让计算机能够"理解"文字的含义。

**详细讲解**：[主题1｜LLM 工作原理深度解析](/技术学习与行业趋势/AI与研究/2025-12-02-llm-working-principle-token-embedding-transformer/)

---

### **Transformer**
**定义**：LLM 的核心架构，通过 Self-Attention 机制让模型理解上下文关系。

**详细讲解**：[主题1｜LLM 工作原理深度解析](/技术学习与行业趋势/AI与研究/2025-12-02-llm-working-principle-token-embedding-transformer/)

---

### **Self-Attention (自注意力机制)**
**定义**：Transformer 的核心机制，让模型能够关注输入序列中不同位置的关系。

**详细讲解**：[主题1｜LLM 工作原理深度解析](/技术学习与行业趋势/AI与研究/2025-12-02-llm-working-principle-token-embedding-transformer/)

---

### **Context Window (上下文窗口)**
**定义**：LLM 能够处理的输入文本长度限制，超过此长度的信息会被"遗忘"。

**详细讲解**：[主题2｜理解 LLM 的"语言"](/技术学习与行业趋势/AI与研究/2025-12-03-llm-prompt-context-in-context-learning/)

---

### **In-Context Learning (ICL)**
**定义**：LLM 通过上下文中的示例学习任务模式，无需微调即可执行新任务。

**详细讲解**：[主题2｜理解 LLM 的"语言"](/技术学习与行业趋势/AI与研究/2025-12-03-llm-prompt-context-in-context-learning/)

---

### **Few-Shot Learning (少样本学习)**
**定义**：在 Prompt 中提供少量示例，让模型学习任务模式。

**详细讲解**：[主题2｜理解 LLM 的"语言"](/技术学习与行业趋势/AI与研究/2025-12-03-llm-prompt-context-in-context-learning/)

---

## 🎨 二、Prompt 工程

### **Prompt (提示词)**
**定义**：输入给 LLM 的指令或问题，是人与模型交互的接口。

**详细讲解**：[主题2｜理解 LLM 的"语言"](/技术学习与行业趋势/AI与研究/2025-12-03-llm-prompt-context-in-context-learning/)、[主题3｜Prompt 工程实战](/技术学习与行业趋势/AI与研究/2025-12-04-llm-prompt-engineering-practices/)

---

### **Prompt Engineering (提示工程)**
**定义**：设计和优化 Prompt 的技巧，让 LLM 更准确地理解和执行任务。

**详细讲解**：[主题3｜Prompt 工程实战](/技术学习与行业趋势/AI与研究/2025-12-04-llm-prompt-engineering-practices/)

---

### **Chain-of-Thought (CoT)**
**定义**：思维链提示，让模型逐步推理，展示思考过程。

**详细讲解**：[主题3｜Prompt 工程实战](/技术学习与行业趋势/AI与研究/2025-12-04-llm-prompt-engineering-practices/)

---

### **ReAct (Reasoning + Acting)**
**定义**：结合推理和行动的提示范式，让模型先思考再行动。

**详细讲解**：[主题3｜Prompt 工程实战](/技术学习与行业趋势/AI与研究/2025-12-04-llm-prompt-engineering-practices/)、[主题7｜决策引擎 ReAct](/技术学习与行业趋势/AI与研究/2025-12-16-llm-agent-decision-engine/)

---

### **Schema (模式/规范)**
**定义**：定义输出格式的结构化规范，如 JSON Schema、Pydantic 模型。

**详细讲解**：[主题3｜Prompt 工程实战](/技术学习与行业趋势/AI与研究/2025-12-04-llm-prompt-engineering-practices/)、[主题12｜Spec 设计](/技术学习与行业趋势/AI与研究/2025-12-21-llm-agent-spec-design/)

---

### **结构化输出 (Structured Output)**
**定义**：让 LLM 按照预定义的格式（JSON、YAML、Markdown）输出内容。

**详细讲解**：[主题3｜Prompt 工程实战](/技术学习与行业趋势/AI与研究/2025-12-04-llm-prompt-engineering-practices/)

---

### **Self-Correction (自我纠正)**
**定义**：让模型检查并修正自己的输出，提高准确性。

**详细讲解**：[主题3｜Prompt 工程实战](/技术学习与行业趋势/AI与研究/2025-12-04-llm-prompt-engineering-practices/)

---

## 🔍 三、RAG 机制

### **RAG (Retrieval-Augmented Generation)**
**定义**：检索增强生成，通过检索外部知识库来增强 LLM 的生成能力，解决幻觉问题。

**详细讲解**：[主题4｜RAG 机制](/技术学习与行业趋势/AI与研究/2025-12-08-llm-rag-deep-integration/)

---

### **Vector Database (向量数据库)**
**定义**：存储 Embedding 向量的数据库，用于快速检索相似文本。

**详细讲解**：[主题4｜RAG 机制](/技术学习与行业趋势/AI与研究/2025-12-08-llm-rag-deep-integration/)

---

### **Chunking (分块)**
**定义**：将长文档切分成小块，便于向量化和检索。

**详细讲解**：[主题4｜RAG 机制](/技术学习与行业趋势/AI与研究/2025-12-08-llm-rag-deep-integration/)

---

### **Re-ranking (重排序)**
**定义**：对检索到的文档按相关性重新排序，提高检索质量。

**详细讲解**：[主题4｜RAG 机制](/技术学习与行业趋势/AI与研究/2025-12-08-llm-rag-deep-integration/)

---

### **Query Transformation (查询转换)**
**定义**：将用户查询转换为更适合检索的形式，如关键词提取、查询扩展。

**详细讲解**：[主题4｜RAG 机制](/技术学习与行业趋势/AI与研究/2025-12-08-llm-rag-deep-integration/)

---

## 🤖 四、Agent 核心架构

### **Agent (智能体)**
**定义**：能够在环境中自主感知、规划、行动、反馈的智能系统。

**详细讲解**：[主题6｜Agent 从 LLM 进化而来](/技术学习与行业趋势/AI与研究/2025-12-10-llm-agent-concept-overview/)

---

### **Agentic Loop (智能体循环)**
**定义**：Agent 的自主循环：感知 → 规划 → 行动 → 反馈 → 感知...

**详细讲解**：[主题6｜Agent 从 LLM 进化而来](/技术学习与行业趋势/AI与研究/2025-12-10-llm-agent-concept-overview/)

---

### **Perception (感知)**
**定义**：Agent 接收用户输入和环境反馈的能力。

**详细讲解**：[主题6｜Agent 从 LLM 进化而来](/技术学习与行业趋势/AI与研究/2025-12-10-llm-agent-concept-overview/)

---

### **Planning (规划)**
**定义**：Agent 分解任务、制定执行计划的能力。

**详细讲解**：[主题6｜Agent 从 LLM 进化而来](/技术学习与行业趋势/AI与研究/2025-12-10-llm-agent-concept-overview/)、[主题9｜任务规划](/技术学习与行业趋势/AI与研究/2025-12-19-llm-agent-task-planning/)

---

### **Action (行动)**
**定义**：Agent 调用工具执行具体操作的能力。

**详细讲解**：[主题6｜Agent 从 LLM 进化而来](/技术学习与行业趋势/AI与研究/2025-12-10-llm-agent-concept-overview/)、[主题13｜工具封装](/技术学习与行业趋势/AI与研究/2025-12-18-llm-agent-tool-system/)

---

### **Memory (记忆)**
**定义**：Agent 保存和检索历史信息的能力，包括短期记忆和长期记忆。

**详细讲解**：[主题8｜记忆管理](/技术学习与行业趋势/AI与研究/2025-12-17-llm-agent-memory-management/)

---

### **STM (Short-Term Memory)**
**定义**：短期记忆，保存在 Context Window 中的当前对话信息。

**详细讲解**：[主题8｜记忆管理](/技术学习与行业趋势/AI与研究/2025-12-17-llm-agent-memory-management/)

---

### **LTM (Long-Term Memory)**
**定义**：长期记忆，保存在外部存储（如向量数据库）中的重要信息。

**详细讲解**：[主题8｜记忆管理](/技术学习与行业趋势/AI与研究/2025-12-17-llm-agent-memory-management/)

---

### **ExM (External Memory)**
**定义**：外部记忆，从知识库检索的外部知识。

**详细讲解**：[主题8｜记忆管理](/技术学习与行业趋势/AI与研究/2025-12-17-llm-agent-memory-management/)

---

## 🛠️ 五、Agent 决策与工具

### **Decision Engine (决策引擎)**
**定义**：Agent 的核心决策模块，决定下一步行动。

**详细讲解**：[主题7｜决策引擎 ReAct](/技术学习与行业趋势/AI与研究/2025-12-16-llm-agent-decision-engine/)

---

### **Tool (工具)**
**定义**：Agent 可以调用的外部功能，如 API、数据库、文件系统等。

**详细讲解**：[主题13｜工具封装](/技术学习与行业趋势/AI与研究/2025-12-18-llm-agent-tool-system/)

---

### **Tool Calling (工具调用)**
**定义**：Agent 调用外部工具执行操作的过程。

**详细讲解**：[主题13｜工具封装](/技术学习与行业趋势/AI与研究/2025-12-18-llm-agent-tool-system/)

---

### **Function Calling**
**定义**：LLM 调用预定义函数的能力，是工具调用的基础。

**详细讲解**：[主题13｜工具封装](/技术学习与行业趋势/AI与研究/2025-12-18-llm-agent-tool-system/)

---

### **Tool Description (工具描述)**
**定义**：描述工具功能、参数、返回值的文档，帮助 Agent 选择合适的工具。

**详细讲解**：[主题13｜工具封装](/技术学习与行业趋势/AI与研究/2025-12-18-llm-agent-tool-system/)

---

### **Human-in-the-Loop (HITL)**
**定义**：人类在循环中，关键操作需要人工审批或确认。

**详细讲解**：[主题13｜工具封装](/技术学习与行业趋势/AI与研究/2025-12-18-llm-agent-tool-system/)

---

### **Idempotency (幂等性)**
**定义**：同一个操作执行一次和执行多次的效果是一样的。

**详细讲解**：[主题13｜工具封装](/技术学习与行业趋势/AI与研究/2025-12-18-llm-agent-tool-system/)

---

## 📐 六、Spec 设计与输出规范

### **Spec (规范)**
**定义**：定义 Agent 输入输出格式的结构化规范。

**详细讲解**：[主题12｜Spec 设计](/技术学习与行业趋势/AI与研究/2025-12-21-llm-agent-spec-design/)

---

### **JSON Schema**
**定义**：用于定义 JSON 数据结构的规范格式。

**详细讲解**：[主题12｜Spec 设计](/技术学习与行业趋势/AI与研究/2025-12-21-llm-agent-spec-design/)

---

### **Pydantic**
**定义**：Python 的数据验证库，常用于定义 Agent 的输出规范。

**详细讲解**：[主题12｜Spec 设计](/技术学习与行业趋势/AI与研究/2025-12-21-llm-agent-spec-design/)

---

## 🏗️ 七、框架与工具

### **LangChain**
**定义**：流行的 Agent 开发框架，提供 Agent、工具、记忆等组件。

**详细讲解**：[主题11｜Agent 框架对比](/技术学习与行业趋势/AI与研究/2025-12-20-llm-agent-framework-comparison/)、[LangChain 框架详解](/技术学习与行业趋势/AI与研究/2025-10-27-langchain-framework/)

---

### **LangSmith**
**定义**：LangChain 的可观测性平台，用于调试、追踪和监控 Agent 执行。

**详细讲解**：[LangChain 框架详解](/技术学习与行业趋势/AI与研究/2025-10-27-langchain-framework/)

---

### **LCEL (LangChain Expression Language)**
**定义**：LangChain 的表达式语言，用于构建复杂的 Agent 工作流。

**详细说明**：LCEL 是 LangChain 提供的声明式语法，让你可以用简洁的代码组合 Prompt、LLM、工具等组件。它支持链式调用、条件分支、并行执行等复杂逻辑，是构建 Agent 工作流的核心方式。

**示例**：
```python
chain = prompt | llm | output_parser
```

**参考资源**：
- [LangChain LCEL 官方文档](https://python.langchain.com/docs/expression_language/)
- [LangChain 表达式语言入门](https://python.langchain.com/docs/expression_language/get_started)

**相关概念**：Chain、Pipeline

---

### **Chain (链)**
**定义**：将多个组件（Prompt、LLM、工具）串联起来的工作流。

**详细讲解**：[LangChain 框架详解](/技术学习与行业趋势/AI与研究/2025-10-27-langchain-framework/)

---

### **LlamaIndex**
**定义**：专注于 RAG 和知识管理的框架。

**详细讲解**：[主题11｜Agent 框架对比](/技术学习与行业趋势/AI与研究/2025-12-20-llm-agent-framework-comparison/)

---

### **AutoGPT**
**定义**：自动化的 Agent 系统，能够自主完成复杂任务。

**详细讲解**：[主题11｜Agent 框架对比](/技术学习与行业趋势/AI与研究/2025-12-20-llm-agent-framework-comparison/)

---

### **Ollama**
**定义**：本地运行开源 LLM 模型的工具。

**详细说明**：Ollama 是一个简单易用的工具，让你可以在本地运行 Llama、Mistral、CodeLlama 等开源模型，无需 GPU 或复杂的配置。它提供了命令行和 API 接口，支持模型下载、管理和推理，非常适合本地开发和测试。

**主要特点**：
- 一键安装和运行
- 支持多种开源模型
- 提供 REST API
- 支持模型量化，降低内存需求

**参考资源**：
- [Ollama 官网](https://ollama.ai/)
- [Ollama GitHub](https://github.com/ollama/ollama)

**相关概念**：本地模型、开源模型

---

### **DeepSeek**
**定义**：国产大语言模型，包括 DeepSeek-Coder（代码专用模型）。

**详细说明**：DeepSeek 是深度求索（DeepSeek AI）开发的大语言模型系列，包括通用模型和代码专用模型。DeepSeek-Coder 在代码生成、代码补全、代码解释等任务上表现优异，支持多种编程语言，是代码相关 Agent 的理想选择。

**主要特点**：
- 强大的代码理解和生成能力
- 支持多种编程语言
- 提供 API 接口
- 部分模型开源

**参考资源**：
- [DeepSeek 官网](https://www.deepseek.com/)
- [DeepSeek GitHub](https://github.com/deepseek-ai)

**相关概念**：开源模型、代码生成

---

### **Llama3**
**定义**：Meta 开发的开源大语言模型。

**详细说明**：Llama3 是 Meta（Facebook）开发的第三代开源大语言模型，在性能、安全性和可控性方面都有显著提升。它提供了多种规模的版本（8B、70B 等），支持商业使用，是构建 Agent 系统的热门选择。

**主要特点**：
- 完全开源，支持商业使用
- 多种规模版本可选
- 性能接近闭源模型
- 活跃的社区支持

**参考资源**：
- [Llama3 官方博客](https://ai.meta.com/blog/meta-llama-3/)
- [Llama3 GitHub](https://github.com/meta-llama/llama3)

**相关概念**：开源模型、模型选型

---

## 🔐 八、安全与治理

### **Security Governance (安全治理)**
**定义**：Agent 的安全管理机制，包括权限控制、审计、监控。

**详细讲解**：[主题14｜Agent 安全治理](/技术学习与行业趋势/AI与研究/2025-12-22-llm-agent-security-governance/)

---

### **Audit (审计)**
**定义**：记录 Agent 的所有操作，便于追溯和复盘。

**详细讲解**：[主题14｜Agent 安全治理](/技术学习与行业趋势/AI与研究/2025-12-22-llm-agent-security-governance/)

---

### **Observability (可观测性)**
**定义**：监控 Agent 的执行状态、性能指标和异常情况。

**详细讲解**：[主题14｜Agent 安全治理](/技术学习与行业趋势/AI与研究/2025-12-22-llm-agent-security-governance/)

---

### **Replay (回放)**
**定义**：重现 Agent 的历史执行过程，用于调试和分析。

**详细讲解**：[主题14｜Agent 安全治理](/技术学习与行业趋势/AI与研究/2025-12-22-llm-agent-security-governance/)

---

## 👥 九、多 Agent 协作

### **Multi-Agent Collaboration (多 Agent 协作)**
**定义**：多个 Agent 像团队一样协作完成复杂任务。

**详细讲解**：[主题14｜多 Agent 协作](/技术学习与行业趋势/AI与研究/2025-12-23-llm-agent-multi-agent-collaboration/)

---

### **Role (角色)**
**定义**：为 Agent 设定的身份和职责，如"测试工程师"、"产品经理"。

**详细讲解**：[主题14｜多 Agent 协作](/技术学习与行业趋势/AI与研究/2025-12-23-llm-agent-multi-agent-collaboration/)

---

### **Message Flow (消息流)**
**定义**：多个 Agent 之间传递信息和协作的流程。

**详细讲解**：[主题14｜多 Agent 协作](/技术学习与行业趋势/AI与研究/2025-12-23-llm-agent-multi-agent-collaboration/)

---

## 📊 十、评估与优化

### **Evaluation (评估)**
**定义**：评估 Agent 的性能，包括准确性、效率、成本等指标。

**详细讲解**：[主题15｜Agent 评估](/技术学习与行业趋势/AI与研究/2025-12-24-llm-agent-evaluation/)

---

### **Metrics (指标)**
**定义**：衡量 Agent 性能的量化指标，如成功率、响应时间、Token 消耗。

**详细讲解**：[主题15｜Agent 评估](/技术学习与行业趋势/AI与研究/2025-12-24-llm-agent-evaluation/)

---

### **Model Evaluation (模型评估)**
**定义**：评估和选择适合的 LLM 模型。

**详细讲解**：[主题5｜评估与选型](/技术学习与行业趋势/AI与研究/2025-12-09-llm-model-evaluation-selection/)

---

### **Parameters (参数量)**
**定义**：LLM 模型中的参数数量，通常反映模型的复杂度。

**详细讲解**：[主题5｜评估与选型](/技术学习与行业趋势/AI与研究/2025-12-09-llm-model-evaluation-selection/)

---

### **Inference Speed (推理速度)**
**定义**：LLM 生成文本的速度，通常用 Token/秒衡量。

**详细讲解**：[主题5｜评估与选型](/技术学习与行业趋势/AI与研究/2025-12-09-llm-model-evaluation-selection/)

---

## 🎯 十一、应用场景

### **平台集成 (Platform Integration)**
**定义**：将 Agent 集成到现有平台或系统中。

**详细说明**：平台集成是指将 Agent 能力嵌入到现有的业务系统、测试平台、开发工具等平台中。通常通过 API 接口、Webhook、插件等方式实现，让 Agent 能够访问平台的数据和功能，实现自动化工作流。

**常见场景**：
- 测试平台集成：Agent 自动生成测试用例、执行测试
- 开发工具集成：IDE 插件、代码审查助手
- 业务系统集成：客服机器人、数据分析助手
- CI/CD 集成：自动化部署、代码质量检查

**实现方式**：
- REST API 接口
- Webhook 回调
- SDK/插件开发
- 消息队列集成

**相关概念**：API 集成、系统集成

---

### **自动写用例 (Automated Test Case Generation)**
**定义**：使用 Agent 自动生成测试用例。

**详细说明**：自动写用例是指利用 Agent 的能力，根据需求文档、接口文档、代码等输入，自动生成测试用例。Agent 可以理解业务逻辑、识别测试场景、生成测试数据和断言，大幅提升测试效率。

**工作流程**：
1. **输入分析**：解析需求文档、接口文档、代码注释
2. **场景识别**：识别正常流程、异常流程、边界条件
3. **用例生成**：生成测试步骤、测试数据、预期结果
4. **格式输出**：输出为测试框架格式（如 pytest、JUnit）

**优势**：
- 快速生成大量用例
- 覆盖更多测试场景
- 减少重复性工作
- 保持用例格式统一

**注意事项**：
- 需要人工审核和调整
- 复杂业务逻辑可能需要补充
- 需要结合测试框架和工具

**相关概念**：测试自动化、用例生成、Human-in-the-Loop

---

### **人工调整 (Human Adjustment)**
**定义**：在自动生成的基础上，人工审核和调整结果。

**详细说明**：人工调整是 Human-in-the-Loop（人类在循环中）模式的重要组成部分。由于 Agent 自动生成的内容可能不完全符合业务需求或存在错误，需要人工进行审核、修正和优化，确保最终输出的质量。

**调整内容**：
- **内容修正**：修正错误、补充遗漏
- **格式优化**：调整格式、统一风格
- **业务适配**：根据实际业务场景调整
- **质量把关**：确保符合质量标准

**最佳实践**：
- 建立审核流程和标准
- 记录调整原因，用于模型优化
- 逐步减少人工干预比例
- 建立反馈机制，持续改进

**相关概念**：Human-in-the-Loop、质量控制、人工审核

---

### **产品文档规范化 (Product Documentation Standardization)**
**定义**：使用 Agent 规范化产品文档的格式和内容。

**详细说明**：产品文档规范化是指利用 Agent 的能力，将分散、格式不统一的产品文档（如需求文档、API 文档、用户手册）转换为统一格式、结构清晰的标准化文档。Agent 可以提取关键信息、补充缺失内容、统一术语和格式。

**应用场景**：
- **需求文档规范化**：统一需求文档模板和格式
- **API 文档生成**：从代码注释自动生成 API 文档
- **用户手册整理**：将零散文档整理成结构化手册
- **文档质量检查**：检查文档完整性、一致性

**实现方式**：
- 使用 RAG 检索现有文档
- 定义文档模板和规范（Spec）
- 使用 LLM 生成和格式化内容
- 人工审核和发布

**参考资源**：
- [文档生成最佳实践](https://www.writethedocs.org/)
- [API 文档规范](https://swagger.io/specification/)

**相关概念**：文档生成、内容管理、Spec 设计

---

### **意图理解 (Intent Understanding)**
**定义**：理解用户输入的真实意图，是 Agent 决策的基础。

**详细说明**：意图理解是 NLP（自然语言处理）的核心任务之一，指从用户的自然语言输入中识别出用户的真实意图和目标。对于 Agent 来说，准确的意图理解是正确决策和执行任务的前提。

**技术实现**：
- **分类方法**：将用户输入分类到预定义的意图类别
- **语义理解**：使用 Embedding 和相似度匹配
- **上下文分析**：结合对话历史理解当前意图
- **多轮对话**：通过多轮交互澄清模糊意图

**应用场景**：
- **对话系统**：理解用户问题，选择合适的回答
- **任务执行**：理解用户指令，执行相应操作
- **信息检索**：理解查询意图，检索相关内容
- **工具选择**：根据意图选择合适的工具

**挑战**：
- 同义表达：不同说法表达同一意图
- 歧义消除：一个输入可能有多种理解
- 上下文依赖：需要结合历史对话理解
- 领域适应：不同领域的意图差异大

**参考资源**：
- [意图识别技术综述](https://arxiv.org/abs/1909.10477)
- [对话系统意图理解](https://www.aclweb.org/anthology/P19-1026/)

**相关概念**：NLP、语义理解、对话系统

---

## 🌐 十二、其他概念

### **AGI (Artificial General Intelligence)**
**定义**：通用人工智能，具备人类水平的通用智能。

**详细说明**：AGI（通用人工智能）是指具备人类水平的通用智能的 AI 系统，能够在各种任务和领域中都表现出色，而不仅仅是单一任务。与当前的专用 AI（如 LLM、图像识别）不同，AGI 应该能够像人类一样学习、推理、适应和创新。

**关键特征**：
- **通用性**：能够处理各种不同类型的任务
- **学习能力**：能够快速学习新知识和技能
- **推理能力**：能够进行逻辑推理和问题解决
- **适应性**：能够适应新环境和场景
- **创造性**：能够产生新的想法和解决方案

**当前状态**：
- LLM（如 GPT-4）展现了部分通用能力
- 但仍局限于文本处理，缺乏多模态理解
- 距离真正的 AGI 还有很大差距

**参考资源**：
- [AGI 研究现状](https://www.deepmind.com/research/areas-of-research)
- [通用人工智能的定义](https://en.wikipedia.org/wiki/Artificial_general_intelligence)

**相关概念**：强 AI、通用智能、LLM

---

### **MCP (Model Context Protocol)**
**定义**：模型上下文协议，用于标准化模型与外部系统的交互。

**详细说明**：MCP（Model Context Protocol）是由 Anthropic 提出的开放协议，旨在标准化 LLM 与外部工具、数据源、服务的交互方式。它提供了一套统一的接口规范，让不同的模型和系统能够无缝集成。

**核心功能**：
- **工具调用**：标准化的工具调用接口
- **资源访问**：访问外部数据源和资源
- **提示模板**：可复用的提示模板管理
- **采样控制**：控制模型输出的采样参数

**优势**：
- **标准化**：统一的接口规范，降低集成成本
- **可扩展**：支持自定义工具和资源
- **可组合**：不同组件可以灵活组合
- **可观测**：提供执行追踪和调试能力

**参考资源**：
- [MCP 官方文档](https://modelcontextprotocol.io/)
- [MCP GitHub](https://github.com/modelcontextprotocol)
- [MCP 规范](https://spec.modelcontextprotocol.io/)

**相关概念**：协议、标准化、工具调用、Function Calling

---

### **Tavily**
**定义**：搜索 API 工具，用于 Agent 获取实时信息。

**详细说明**：Tavily 是一个专为 AI Agent 设计的搜索 API，提供高质量的实时信息检索能力。与传统的搜索引擎不同，Tavily 针对 Agent 的使用场景进行了优化，返回结构化的、经过筛选的搜索结果，更适合 LLM 处理和 Agent 决策。

**主要特点**：
- **实时搜索**：获取最新的网络信息
- **结构化输出**：返回格式化的搜索结果
- **高质量结果**：经过筛选和排序的相关内容
- **API 友好**：易于集成到 Agent 系统中

**应用场景**：
- **信息检索 Agent**：回答需要实时信息的问题
- **新闻监控**：监控特定主题的最新动态
- **市场研究**：收集和分析市场信息
- **知识更新**：补充 RAG 系统的实时知识

**参考资源**：
- [Tavily 官网](https://tavily.com/)
- [Tavily API 文档](https://docs.tavily.com/)
- [Tavily GitHub](https://github.com/tavily)

**相关概念**：搜索工具、实时信息、RAG、工具调用

---

### **spec-kit**
**定义**：Spec 规范工具包，用于定义和管理 Agent 的输入输出规范。

**详细说明**：spec-kit 是一个用于定义和管理 Agent Spec（规范）的工具包，帮助开发者更方便地创建、验证和管理 Agent 的输入输出格式。它通常提供 Schema 定义、验证、转换等功能，确保 Agent 的输入输出符合预期格式。

**主要功能**：
- **Schema 定义**：使用 JSON Schema、Pydantic 等定义规范
- **格式验证**：验证输入输出是否符合规范
- **格式转换**：在不同格式之间转换
- **文档生成**：自动生成规范文档

**使用场景**：
- 定义 Agent 的输入输出格式
- 验证工具调用的参数
- 确保结构化输出的正确性
- 生成 API 文档

**参考资源**：
- [JSON Schema 规范](https://json-schema.org/)
- [Pydantic 文档](https://docs.pydantic.dev/)

**相关概念**：Spec、工具包、JSON Schema、Pydantic

---

### **stitch**
**定义**：数据集成工具，用于连接不同数据源。

**详细说明**：Stitch 是一个数据集成平台（现已被 Talend 收购），用于从各种数据源（数据库、API、文件等）提取数据，并将其加载到数据仓库或数据湖中。在 Agent 场景中，Stitch 可以帮助 Agent 访问和整合来自不同系统的数据。

**主要功能**：
- **数据提取**：从多种数据源提取数据
- **数据转换**：清洗和转换数据格式
- **数据加载**：将数据加载到目标系统
- **自动化**：定时自动执行数据同步

**应用场景**：
- **数据仓库构建**：整合多个数据源
- **实时数据同步**：保持数据一致性
- **数据分析准备**：为分析准备数据
- **Agent 数据访问**：为 Agent 提供统一的数据接口

**参考资源**：
- [Stitch 官网](https://www.stitchdata.com/)
- [数据集成最佳实践](https://www.talend.com/resources/what-is-data-integration/)

**相关概念**：数据集成、ETL、数据仓库、数据湖

---

### **PyMySQL**
**定义**：Python 的 MySQL 数据库连接库。

**详细说明**：PyMySQL 是一个纯 Python 实现的 MySQL 客户端库，用于在 Python 程序中连接和操作 MySQL 数据库。在 Agent 开发中，PyMySQL 常用于构建数据库访问工具，让 Agent 能够查询和操作数据库。

**主要特点**：
- **纯 Python 实现**：无需编译，跨平台
- **简单易用**：API 简洁直观
- **兼容性好**：兼容 MySQL 5.5+
- **轻量级**：依赖少，体积小

**使用示例**：
```python
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='test'
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()
```

**在 Agent 中的应用**：
- 构建数据库查询工具
- 实现数据检索和更新功能
- 支持 RAG 系统的数据源接入

**参考资源**：
- [PyMySQL GitHub](https://github.com/PyMySQL/PyMySQL)
- [PyMySQL 文档](https://pymysql.readthedocs.io/)

**相关概念**：数据库、Python 库、工具调用、数据库工具

---

## 📝 使用建议

1. **快速查找**：使用浏览器的 `Ctrl+F` (Windows) 或 `Cmd+F` (Mac) 搜索关键词
2. **深入学习**：点击"详细讲解"链接，阅读对应的系列文章
3. **概念关联**：查看"相关概念"，了解相关术语
4. **持续更新**：本文档会随着系列更新而持续完善

---

## 🔗 相关资源

- [系列开篇：告别浅尝辄止](/技术学习与行业趋势/AI与研究/2025-11-29-llm-agent-core-concepts-guide/)
- [系列目录](/series/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/)
- [基础知识回顾：LLM 与智能体知识记录](/技术学习与行业趋势/AI与研究/2025-10-21-llm-agent-guide/)

---

**如果你发现本文档中有遗漏的术语或需要补充的内容，欢迎在评论区留言！**

