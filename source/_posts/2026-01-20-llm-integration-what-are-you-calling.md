---
title: "🤖 项目里调用大模型，其实在调用什么？"
date: 2026-01-20 10:00:00
updated: {{current_date_time}}
categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - AI与研究
tags:
  - LLM
  - 大模型
  - 模型选型
  - 推理服务
  - Ollama
  - OpenAI API
  - Azure OpenAI
  - 术语对照
keywords: 大模型接入, LLM, 推理服务, 模型层, API, SDK, Ollama, ChatGPT API, Azure OpenAI, Bedrock, Vertex AI, 责任边界
description: '当你说“项目里接入大模型”时，究竟在接入什么？用四层结构（模型层/推理服务层/接入方式层/责任边界层）把 Ollama、ChatGPT API、Azure OpenAI 等名词放回正确位置。'
top_img: /img/llm-integration-what-are-you-calling.png
cover: /img/llm-integration-what-are-you-calling.png
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

> **这是[《🧠 LLM/Agent 从入门到精通：告别浅尝辄止》](/categories/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/)系列的工具篇**

当我们说“在项目里接入大模型”时，往往并不是在讨论一件单独的事情，而是在同时讨论**多层不同的技术选择**。

混乱通常来自于：

* 模型能力
* 模型运行方式
* 接入方式
* 责任与边界

这些本来不在同一层的问题，经常被放在一起比较，导致 **Ollama、ChatGPT API、Azure OpenAI 被当成同一类东西来选**。

这篇文章只做一件事：

> **用一套清晰的分层结构，把常见的大模型相关名词放回它们各自的位置。**

---

## 1. 模型层：能力从哪里来

这一层只关心一件事：**模型本身是谁训练的，能力大概在什么水平。**

### 常见模型

* GPT-4 / GPT-4o（OpenAI）
* Claude（Anthropic）
* Gemini（Google）
* Qwen / LLaMA / DeepSeek（开源模型）

### 这一层决定什么

* 语言理解与生成能力
* 推理、代码、多模态等能力上限

### 关键认知

> **模型只决定能力上限，不决定使用方式。**

同一个 GPT-4：

* 可以被做成 ChatGPT 产品
* 可以通过 API 给程序调用
* 也可以被云厂商托管后提供给企业

仅仅知道“用了什么模型”，**并不能说明你的项目是如何接入大模型的**。

---

## 2. 推理服务层：模型在哪里跑

模型是“能力描述”，
**推理服务才是真正让模型跑起来的系统。**

这一层，是理解 Ollama 与云 API 差异的关键。

---

### 2.1 自管推理服务（自己跑模型）

#### 典型工具

* Ollama
* LM Studio
* vLLM（偏生产）

#### 在做什么

* 将模型部署在本地或自有服务器
* 负责模型加载、推理和资源占用
* 对外提供一个 HTTP 接口

#### 一句话理解 Ollama

> **Ollama 是一个把开源模型跑起来，并对外提供 API 的工具。**

#### 适合场景

* 内部工具
* 测试平台
* 数据不出网
* 并发要求不高

#### 📚 扩展阅读

* [Ollama 官方文档](https://ollama.com/docs) - 了解如何安装、配置和使用 Ollama

---

### 2.2 云端推理服务（模型即服务）

#### 典型服务

* OpenAI API（ChatGPT API）
* Claude API
* Gemini API

#### 在做什么

* 模型运行在厂商云端
* 你通过 HTTP API 调用模型能力
* 不需要关心硬件、部署和扩容

#### 常见误区

* **ChatGPT ≠ ChatGPT API**

  * ChatGPT 是面向人的产品
  * ChatGPT API 是面向程序的接口

#### 适合场景

* 产品原型
* 快速验证
* 对效果要求高
* 不想维护模型

---

### 2.3 企业级托管推理服务

#### 典型平台

* Azure OpenAI
* AWS Bedrock
* GCP Vertex AI

#### 在做什么

* 使用的仍然是 GPT / Claude 等模型
* 运行在云厂商的企业级体系中
* 提供账号、权限、审计、网络隔离等能力

#### 一句话理解 Azure OpenAI

> **Azure OpenAI = OpenAI 模型 + Azure 的企业级治理能力。**

#### 适合场景

* 企业内部系统
* ToB 产品
* 对合规和数据边界要求高

---

## 3. 接入方式层：你是怎么用模型的

这一层经常被忽略，但却是概念混乱的重要来源。

### 常见说法

* Chat / 对话
* API
* SDK
* Function Calling / 工具调用

### 它们的关系

* **API**：模型能力的访问入口
* **SDK**：对 API 的代码封装
* **Chat**：一种交互形式，不是技术本质

同一个模型能力，可以：

* 被包装成聊天界面
* 被后端服务调用
* 被嵌入业务流程中

> **看起来像聊天，不代表只能聊天。**

---

## 4. 责任与边界层：出问题谁负责

这是技术选型之外，最现实的一层。

### 三种典型责任模式

#### 4.1 全部自己负责

* 自建模型 / 自管推理（如 Ollama）
* 数据、安全、稳定性都由你承担

#### 4.2 能力由厂商负责

* OpenAI API / Claude API
* 你负责业务逻辑
* 厂商负责模型服务

#### 4.3 能力与合规由平台负责

* Azure OpenAI / Bedrock
* 平台提供企业级治理能力

同一个 GPT-4，
在不同责任边界下，
**会变成完全不同的技术方案。**

---

## 5. 常见名词的正确位置

现在可以重新理解这些常见名词：

* **Ollama**：自管推理服务层
* **ChatGPT API**：云端推理服务层
* **Azure OpenAI**：企业级托管推理服务层

它们并不在竞争同一件事，
而是在解决**不同层级的问题**。

---

## 6. 名词会变，但结构不会

今天你看到的是：

* Ollama
* vLLM
* Bedrock

明天一定还会出现新的名字。

但只要记住这四层结构：

1. 模型层
2. 推理服务层
3. 接入方式层
4. 责任与边界层

任何新名词，都可以被快速归类。

---

## 7. 总结

好的技术科普，不是让你记住更多工具名，
而是：

> **让你看到任何新名词，都知道它在解决哪一层的问题。**

当你建立了这套结构：

* 不需要死记结论
* 不容易被营销话术带偏
* 技术选型会自然清晰

