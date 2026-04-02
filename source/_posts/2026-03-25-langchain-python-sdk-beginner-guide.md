---
title: LangChain Python SDK 入门实战：从 0 到常见能力全覆盖
date: 2026-03-25 22:40:00
updated: 2026-03-25 22:40:00
categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - AI与研究
tags:
  - LangChain
  - Python
  - SDK
  - Agent
  - Chain
  - Memory
  - Tool
  - PromptTemplate
keywords: LangChain Python SDK, langchain 库, Agent, Chain, Memory, Tool, PromptTemplate, 新手教程
description: '一篇给新手的 LangChain Python SDK 实战文章：环境配置、常见调用模板、Agent 实践、Memory 应用、错误排查与延伸阅读。'
top_img: /img/langchain-python-sdk-beginner-guide.png
cover: /img/langchain-python-sdk-beginner-guide.png
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

## 1. 先建立正确认知：LangChain 是什么

当你写下这行代码：

```python
from langchain_openai import ChatOpenAI
from langchain import PromptTemplate
```

本质是在做三件事：

- 通过 LangChain 提供的统一接口调用底层 LLM 服务
- 利用 LangChain 的模块化组件构建复杂 AI 工作流
- 连接外部工具与数据源，让 LLM 真正“动起来”

也就是说，LangChain 是你与 LLM 之间的“智能编排层”，它让你不用手写底层流程细节，而是通过组合模块来构建强大的 AI 应用。

---

## 2. 环境准备（最小可用）

### 2.1 安装依赖

```bash
pip install langchain langchain-openai
```

### 2.2 配置 API Key（推荐环境变量）

```bash
export OPENAI_API_KEY="sk-xxxx"
```

可选：

```bash
export OPENAI_MODEL="gpt-4o-mini"
export OPENAI_BASE_URL="https://your-compatible-endpoint/v1"
```

> `OPENAI_BASE_URL` 只在代理或兼容端点场景下使用，标准接入可以不设置。

---

## 3. LangChain Python 库核心组件速查表

基于 **`langchain>=0.2`** 官方库整理：常用组件、作用与主要参数。

| 组件及作用 | 参数及参数含义 |
| --- | --- |
| **`PromptTemplate`**<br>提示模板：标准化、参数化指令 | ① **template**：必选，模板字符串<br>② **input_variables**：可选，变量列表<br>③ **partial_variables**：可选，部分变量预填充 |
| **`ChatOpenAI`**<br>OpenAI 聊天模型接口 | ① **model**：必选，模型名称（如 `gpt-4o-mini`）<br>② **temperature**：可选，随机性（约 0～2；越低越稳，越高越发散）<br>③ **max_tokens**：可选，生成长度上限（token）<br>④ **base_url**：可选，兼容端点 / 代理根 URL |
| **`ConversationBufferMemory`**<br>对话记忆：缓存对话历史 | ① **memory_key**：可选，记忆在链中的键名<br>② **return_messages**：可选，是否返回消息对象列表 |
| **`LLMChain`**<br>基础链式调用：连接 Prompt 与 LLM | ① **llm**：必选，语言模型实例<br>② **prompt**：必选，提示模板<br>③ **memory**：可选，记忆实例<br>④ **output_key**：可选，输出键名 |
| **`Tool`**<br>工具定义：供 Agent 调用的外部能力 | ① **name**：必选，工具名称<br>② **func**：必选，工具函数<br>③ **description**：必选，工具描述（Agent 依赖此描述决定是否调用） |
| **`initialize_agent`**<br>初始化智能体：组合 LLM 与工具 | ① **tools**：必选，工具列表<br>② **llm**：必选，语言模型实例<br>③ **agent_type**：必选，智能体类型（如 `zero-shot-react-description`）<br>④ **verbose**：可选，是否打印详细日志 |

---

## 4. LangChain Python SDK 方法知识字典（按组件分类）

### 4.1 `PromptTemplate`：提示模板

- 作用：标准化、参数化提示，避免硬编码
- 常用参数：`template`、`input_variables`
- 推荐：使用 `from_template` 快速创建

```python
from langchain import PromptTemplate

# 方式 A：快速创建
template = PromptTemplate.from_template(
    "你是一名软件测试专家，请分析以下测试报告并给出{n}条改进建议：{report}"
)

# 方式 B：显式指定变量
template = PromptTemplate(
    template="你是{role}，请{task}",
    input_variables=["role", "task"]
)

# 使用模板
prompt = template.format(role="测试工程师", task="分析测试报告")
```

### 4.2 `ChatOpenAI`：模型接口

- 作用：统一调用 OpenAI 模型
- 常用参数：`model`、`temperature`、`base_url`
- 推荐：优先用环境变量 `OPENAI_API_KEY`

```python
import os
from langchain_openai import ChatOpenAI

# 方式 A：推荐。只要环境变量里有 OPENAI_API_KEY 即可
# export OPENAI_API_KEY="sk-xxxx"
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# 方式 B：显式传 API Key（测试脚本常用，生产不建议明文写死）
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini"
)

# 方式 C：兼容端点 / 代理（比如企业网关）
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://your-proxy-or-compatible-endpoint/v1",
    model="gpt-4o-mini"
)
```

### 4.3 `LLMChain`：基础链式调用

- 作用：连接 Prompt 与 LLM，执行基本推理
- 常用参数：`llm`、`prompt`、`memory`
- 常见读取：直接调用 `run()` 或 `predict()`

```python
from langchain import LLMChain

chain = LLMChain(
    llm=llm,
    prompt=template
)

# 方式 A：run 方法
response = chain.run(report="系统测试结果显示性能下降20%", n=3)
print(response)

# 方式 B：predict 方法（更灵活的参数传递）
response = chain.predict(report="系统测试结果显示性能下降20%", n=3)
print(response)
```

### 4.4 `Memory`：对话记忆

- 作用：维护对话状态，支持多轮交互
- 常用类型：`ConversationBufferMemory`、`ConversationSummaryMemory`
- 注意：需要在 Chain 中指定 `memory_key`

```python
from langchain.memory import ConversationBufferMemory

# 创建记忆实例
memory = ConversationBufferMemory(memory_key="chat_history")

# 在 Chain 中使用
chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(
        "{chat_history}\n用户：{input}\n助手："
    ),
    memory=memory
)

# 多轮对话
response1 = chain.run(input="你好，我是测试工程师")
print(response1)

response2 = chain.run(input="如何分析性能测试报告？")
print(response2)

# 查看记忆内容
print(memory.load_memory_variables({}))
```

### 4.5 `Tool` + `initialize_agent`：智能体与工具

- 作用：让 LLM 调用外部工具，执行复杂任务
- 核心流程：定义工具 → 初始化 Agent → 执行任务

```python
from langchain.agents import initialize_agent, Tool
from langchain.tools import DuckDuckGoSearchRun

# 1) 定义工具
search_tool = Tool(
    name="Search",
    func=DuckDuckGoSearchRun().run,
    description="用来搜索最新测试框架资讯"
)

# 2) 初始化 Agent
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent_type="zero-shot-react-description",
    verbose=True
)

# 3) 执行任务
response = agent.run("帮我查一下2026年流行的AI测试框架")
print(response)
```

### 4.6 `SequentialChain`：顺序链式调用

- 作用：组合多个 Chain，按顺序执行
- 适用：复杂工作流，多步骤处理

```python
from langchain.chains import SequentialChain

# 创建第一个 Chain（分析报告）
template1 = PromptTemplate.from_template(
    "分析以下测试报告，提取关键问题：{report}"
)
chain1 = LLMChain(
    llm=llm,
    prompt=template1,
    output_key="issues"
)

# 创建第二个 Chain（生成建议）
template2 = PromptTemplate.from_template(
    "针对以下问题，生成改进建议：{issues}"
)
chain2 = LLMChain(
    llm=llm,
    prompt=template2,
    output_key="suggestions"
)

# 组合为顺序链
overall_chain = SequentialChain(
    chains=[chain1, chain2],
    input_variables=["report"],
    output_variables=["issues", "suggestions"]
)

# 执行
result = overall_chain("系统测试结果显示性能下降20%，内存占用过高")
print("问题：", result["issues"])
print("建议：", result["suggestions"])
```

### 4.7 常见参数速查

- `temperature`：控制输出随机性/发散度（低=更稳定，高=更多样）
- `memory_key`：记忆在链中的键名，需与 Prompt 中的变量名对应
- `agent_type`：智能体类型，决定其推理和调用工具的方式
- `verbose`：是否打印详细执行日志，调试时建议开启

`temperature` 实战建议：

- `0~0.3`：问答、抽取、格式化输出（优先稳定）
- `0.4~0.7`：通用助手、改写润色（平衡稳定和表达）
- `0.8~1.0`：创意写作、头脑风暴（更发散，需防跑偏）

---

## 5. 除了 LangChain ，还有哪些选择？

这篇主线仍是 `langchain` 库。为了避免“学了一个框架就被技术栈锁死”，你可以了解常见的替代框架与工具：

- **LangChain**：`langchain`（Python 包）
- **LlamaIndex**：`llama-index`（专注于 RAG 场景）
- **Haystack**：`farm-haystack`（企业级 NLP 框架）
- **Transformers Agent**：`transformers` 库内置的智能体功能
- **自定义实现**：基于原生 SDK 自行封装工作流

各家都提供了官方文档，建议至少收藏这些入口：

- LangChain Docs: [https://python.langchain.com/docs/introduction](https://python.langchain.com/docs/introduction)
- LlamaIndex Docs: [https://docs.llamaindex.ai/en/stable/](https://docs.llamaindex.ai/en/stable/)
- Haystack Docs: [https://docs.haystack.deepset.ai/](https://docs.haystack.deepset.ai/)
- Transformers Docs: [https://huggingface.co/docs/transformers/](https://huggingface.co/docs/transformers/)

它们的功能是不是差不多？**大方向是相似的，细节并不完全一样。**

共同能力（大多数框架都有）：

- 提示模板管理
- 模型接口统一
- 记忆机制
- 工具调用
- 链式工作流

常见差异（建议单独关注）：

- **生态集成**：与外部工具、数据源的集成深度不同
- **性能优化**：对大规模 RAG、长上下文的处理能力不同
- **企业特性**：部署选项、安全控制、监控能力不同
- **学习曲线**：API 设计复杂度和文档完善度不同

实践建议：主教程先用 `langchain` 跑通，再根据具体场景评估其他框架。

---

## 6. 相关阅读（建议收藏）

### 官方文档（首选）

- [LangChain Python Docs](https://python.langchain.com/docs/introduction)
- [LangChain API Reference](https://api.python.langchain.com/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [LangSmith Docs](https://docs.smith.langchain.com/)
- [LangServe Docs](https://docs.langchain.com/serve/)

### 进阶学习（与工程化更相关）

- [LangChain Cookbook](https://github.com/langchain-ai/langchain/tree/master/cookbook)
- [Agent 最佳实践](https://python.langchain.com/docs/modules/agents/best_practices/)
- [RAG 深度指南](https://python.langchain.com/docs/use_cases/question_answering/)
- [LangGraph 文档](https://docs.langchain.com/langgraph/)
- [LlamaIndex 文档](https://docs.llamaindex.ai/en/stable/)
- [Haystack 文档](https://docs.haystack.deepset.ai/)

---

## 7. 小结

如果你是新手，建议按这个顺序练习：

1. `PromptTemplate` + `ChatOpenAI`（先把基本提示跑通）
2. `LLMChain`（构建简单工作流）
3. `Memory`（支持多轮对话）
4. `Tool` + `Agent`（让模型调用外部能力）
5. `SequentialChain`（构建复杂工作流）

当你把这 5 块串起来时，就已经具备了搭建一个可用 AI 应用的核心能力。LangChain 不只是一个框架，而是一种新的工程范式——让语言模型“理解、推理、行动、协作”。