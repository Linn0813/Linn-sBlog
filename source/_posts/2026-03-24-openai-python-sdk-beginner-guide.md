---
title: OpenAI Python SDK 入门实战：从 0 到常见能力全覆盖
date: 2026-03-24 22:40:00
updated: 2026-03-24 22:40:00
categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - AI与研究
tags:
  - OpenAI API
  - Python
  - SDK
  - Function Calling
  - Embeddings
  - 流式输出
keywords: OpenAI Python SDK, openai 库, Chat Completions, 流式输出, JSON 输出, Function Calling, Embeddings, 新手教程
description: '一篇给新手的 OpenAI Python SDK 实战文章：环境配置、常见调用模板、函数调用、向量实践、错误排查与延伸阅读。'
top_img: /img/openai-python-sdk-beginner-guide.png
cover: /img/openai-python-sdk-beginner-guide.png
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

## 1. 先建立正确认知：你在调用什么

当你写下这行代码：

```python
from openai import OpenAI
client = OpenAI(api_key="...")
```

本质是在做三件事：

- 通过 SDK 生成标准 HTTP 请求
- 带上身份凭证（`OPENAI_API_KEY`）
- 请求云端模型服务并获取结果

也就是说，`openai` 库是你与模型服务之间的“客户端封装层”，它让你不用手写底层 HTTP 细节。

---

## 2. 环境准备（最小可用）

### 2.1 安装依赖

```bash
pip install openai
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

## 3. OpenAI Python 库核心方法速查表

基于 **`openai>=1.0`** 官方库（`from openai import OpenAI` → `client = OpenAI()`）整理：常用入口、作用与主要参数。下列调用均挂在 **`client`** 上；与 0.x 时代的 `ChatCompletion.create()` 等**类方法**写法不同，请勿混淆。

| 方法及作用 | 参数及参数含义 |
| --- | --- |
| **`client.chat.completions.create()`**<br>核心对话接口：多轮对话、问答、文本创作（GPT-3.5/4/4o 等） | ① **model**：必选，模型名称（如 `gpt-4o-mini`）<br>② **messages**：必选，消息列表，如 `[{"role":"user","content":"..."}]`<br>③ **temperature**：可选，随机性（约 0～2；越低越稳，越高越发散）<br>④ **max_tokens**：可选，生成长度上限（token）<br>⑤ **top_p**：可选，核采样（0～1；常与 temperature 二选一调优）<br>⑥ **stream**：可选，是否流式输出<br>⑦ **stop**：可选，停止生成的标记序列<br>⑧ **frequency_penalty**：可选，重复惩罚（约 -2～2） |
| **`client.embeddings.create()`**<br>文本向量化：语义检索、聚类、相似度 | ① **model**：必选，嵌入模型（如 `text-embedding-3-small`）<br>② **input**：必选，单条字符串或多条列表<br>③ **encoding_format**：可选，向量编码（如默认浮点 / `base64`）<br>④ **dimensions**：可选，输出维度（部分新嵌入模型支持） |
| **`client.completions.create()`**<br>文本**补全**（单段 prompt 续写）；多用于 **Instruct** 旧式模型 | ① **model**：必选（如 `gpt-3.5-turbo-instruct`）<br>② **prompt**：必选，输入提示<br>③ **temperature** / **max_tokens** / **stop** 等与 Chat 类似，含义相近 |
| **`client.images.generate()`**<br>文生图 | ① **prompt**：必选，画面描述<br>② **n**：可选，张数（依模型限制，如 1～10）<br>③ **size**：可选，如 `1024x1024` 等<br>④ **response_format**：可选，如 `url`、`b64_json`<br>⑤ **model**：可选，如 `dall-e-3`、`dall-e-2` |
| **`client.audio.transcriptions.create()`**<br>语音转文字 | ① **file**：必选，音频文件对象（如 mp3/wav/m4a）<br>② **model**：必选，识别模型（常用 `whisper-1`）<br>③ **language**：可选，语言提示（如 `zh`）<br>④ **prompt**：可选，风格/词汇提示以提升准确率<br>⑤ **response_format**：可选，如 `json`、`text` |
| **`client.files.create()`**<br>上传文件：微调、Batch、Assistants 等 | ① **file**：必选，待上传文件（二进制可读对象或路径按 SDK 用法传入）<br>② **purpose**：必选，用途（如 `fine-tune`、`assistants`、`batch` 等，以文档为准） |
| **`client.fine_tuning.jobs.create()`**<br>创建微调任务（openai≥1.0 中为 **jobs** 资源；非旧名 `FineTunes.create`） | ① **training_file**：必选，已上传文件的 file id<br>② **model**：可选，基底模型<br>③ **hyperparameters**：可选，如 `n_epochs` 等（以当前 API 为准） |
| **`OpenAI(...)`**<br>初始化客户端：密钥、代理、超时等 | ① **api_key**：API 密钥（可省略，读环境变量 `OPENAI_API_KEY`）<br>② **base_url**：可选，兼容端点 / 代理根 URL<br>③ **timeout**：可选，请求超时<br>④ **max_retries**：可选，失败重试次数 |

---

## 4. OpenAI Python SDK 方法知识字典（按方法分类）

### 4.1 `OpenAI(...)`：创建客户端

- 作用：初始化 SDK 客户端
- 常用参数：`api_key`、`base_url`
- 推荐：优先用环境变量 `OPENAI_API_KEY`

常见传参方式（按场景选一个）：

```python
import os
from openai import OpenAI

# 方式 A：推荐。只要环境变量里有 OPENAI_API_KEY 即可
# export OPENAI_API_KEY="sk-xxxx"
client = OpenAI()

# 方式 B：显式传 API Key（测试脚本常用，生产不建议明文写死）
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 方式 C：兼容端点 / 代理（比如企业网关）
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://your-proxy-or-compatible-endpoint/v1",
)

# 方式 D：集中 kwargs，方便按环境切换
kwargs = {"api_key": os.getenv("OPENAI_API_KEY")}
base_url = os.getenv("OPENAI_BASE_URL", "").strip()
if base_url:
    kwargs["base_url"] = base_url
client = OpenAI(**kwargs)
```

### 4.2 `client.chat.completions.create(...)`：对话生成

- 作用：最常用文本生成入口
- 常用参数：`model`、`messages`、`temperature`、`max_tokens`
- 常见读取（取模型回复正文）：`resp.choices[0].message.content`

为什么这样读：

- `resp` 是完整响应对象
- `choices` 是候选答案列表（通常至少 1 个）
- `choices[0]` 表示第一个候选答案
- `message.content` 才是最终文本内容

```python
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "你是一个简洁的助手"},
        {"role": "user", "content": "用一句话解释 API Key"},
    ],
    temperature=0.3,
)
text = resp.choices[0].message.content or ""
print(text)
```

### 4.3 `client.chat.completions.create(..., stream=True)`：流式输出

- 作用：边生成边返回，适合聊天 UI
- 读取方式：遍历 `chunk`，读取 `chunk.choices[0].delta.content`

```python
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "给我 3 条学习 API 的建议"}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content if chunk.choices else None
    if delta:
        print(delta, end="", flush=True)
```

### 4.4 `response_format={"type":"json_object"}`：JSON 结构化输出

- 作用：让模型按 JSON 返回，便于程序处理
- 常用搭配：`json.loads(...)`
- 注意：仍要做 JSON 解析异常兜底

```python
import json

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "你是学习规划助手，只输出 JSON"},
        {"role": "user", "content": "给我 3 天 Python+OpenAI 学习计划"},
    ],
    response_format={"type": "json_object"},
    temperature=0.2,
)
data = json.loads(resp.choices[0].message.content or "{}")
print(data)
```

### 4.5 `tools` / `tool_choice`：Function Calling

- 作用：让模型决定是否调用你定义的函数
- 核心流程：模型返回 `tool_calls` -> 代码执行函数 -> 把工具结果回传模型

```python
import json

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询城市天气",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        },
    }
]

# 1) 入参（给模型）
messages = [
    {"role": "system", "content": "你是天气助理，需要时调用工具。"},
    {"role": "user", "content": "北京今天天气如何？顺便给穿衣建议。"},
]

first = client.chat.completions.create(
    model="gpt-4o-mini",   # 模型入参
    messages=messages,     # 对话入参
    tools=tools,           # 工具定义入参
    tool_choice="auto",    # 让模型自己决定是否调用
)

# 2) 出参（模型先返回 tool_calls）
msg = first.choices[0].message
tool_calls = msg.tool_calls or []

# 3) 你的代码执行工具，并把结果回传给模型
messages.append(msg.model_dump(exclude_none=True))
for tc in tool_calls:
    args = json.loads(tc.function.arguments or "{}")
    city = args.get("city", "beijing")

    # 这里模拟真实函数返回
    tool_result = {"city": city, "temp_c": 21, "condition": "sunny"}

    messages.append(
        {
            "role": "tool",
            "tool_call_id": tc.id,
            "content": json.dumps(tool_result, ensure_ascii=False),
        }
    )

second = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,   # 回传了 tool 结果的消息数组
)

# 4) 最终出参（可直接展示给用户）
final_text = second.choices[0].message.content or ""
print(final_text)
```

关键入参/出参对应关系：

- 入参：`model`、`messages`、`tools`、`tool_choice`
- 第一轮出参：`first.choices[0].message.tool_calls`
- 工具回传消息：`{"role":"tool","tool_call_id":"...","content":"..."}`
- 最终出参：`second.choices[0].message.content`

### 4.6 `client.embeddings.create(...)`：向量生成

- 作用：把文本转向量
- 适用：RAG、检索、相似度、去重
- 读取：`resp.data[0].embedding`

```python
emb = client.embeddings.create(
    model="text-embedding-3-small",
    input="OpenAI Python SDK 基本用法",
)
vec = emb.data[0].embedding
print(len(vec), vec[:8])
```

### 4.7 `client.files.*`：文件管理

- `client.files.create(file=..., purpose="...")`：上传文件
- `client.files.list()`：列文件
- `client.files.retrieve(file_id)`：查文件信息
- `client.files.delete(file_id)`：删文件

> `purpose` 取值按具体能力文档要求设置。

### 4.8 `client.models.*`：模型管理

- `client.models.list()`：查看账号可用模型
- `client.models.retrieve(model_id)`：查看单模型详情

### 4.9 Chat 常见参数速查

- `model`：模型名称
- `messages`：消息数组（system/user/assistant）
- `temperature`：控制输出随机性/发散度（低=更稳定，高=更多样）
- `max_tokens`：最大输出长度
- `stream`：是否流式
- `tools`：工具定义
- `tool_choice`：工具调用策略
- `timeout`：请求超时时间

`temperature` 实战建议：

- `0~0.3`：问答、抽取、JSON 输出（优先稳定）
- `0.4~0.7`：通用助手、改写润色（平衡稳定和表达）
- `0.8~1.0`：创意写作、头脑风暴（更发散，需防跑偏）

一句记忆：要“准”就低一点，要“新”就高一点。  
补充：`temperature` 不增加模型知识量，主要影响输出风格和稳定性。

### 4.10 常见返回字段速查

- `choices`：候选结果
- `message.content`：文本内容
- `message.tool_calls`：工具调用建议
- `usage`：token 统计
- `id`：请求 ID

---

## 5. 除了 OpenAI ，还有哪些选择？

这篇主线仍是 `openai` 库。为了避免“学了一个 SDK 就被平台锁死”，你可以了解常见的替代供应商与对应 SDK：

- **OpenAI**：`openai`（Python 包）
- **Azure OpenAI**：常见仍用 `openai`（配 Azure 端点与部署名）；也可走 Azure 自家 SDK 生态
- **Anthropic**：`anthropic`
- **Google Gemini**：`google-genai`（新）/ `google-generativeai`（旧）
- **阿里云通义千问（DashScope）**：`dashscope`（或 OpenAI 兼容方式接入）
- **本地自托管（Ollama）**：`ollama`（也可通过 OpenAI 兼容网关）

各家都提供了官方文档，建议至少收藏这些入口：

- OpenAI Docs: [https://platform.openai.com/docs](https://platform.openai.com/docs)
- Azure OpenAI 文档: [https://learn.microsoft.com/azure/ai-services/openai/](https://learn.microsoft.com/azure/ai-services/openai/)
- Anthropic Docs: [https://docs.anthropic.com/](https://docs.anthropic.com/)
- Gemini Docs: [https://ai.google.dev/](https://ai.google.dev/)
- DashScope 文档: [https://help.aliyun.com/zh/model-studio/](https://help.aliyun.com/zh/model-studio/)
- Ollama Docs: [https://ollama.com/docs](https://ollama.com/docs)

它们的功能是不是差不多？**大方向是相似的，细节并不完全一样。**

共同能力（大多数平台都有）：

- 文本对话（chat）
- 流式输出（streaming）
- 工具调用（function/tool calling）
- 向量（embeddings）

常见差异（建议单独关注）：

- **接口协议差异**：同名能力的请求参数可能不同（如 tool schema 字段、响应字段）
- **模型能力差异**：同样是“多模态/工具调用”，稳定性和效果会有差别
- **企业能力差异**：鉴权方式、私网部署、审计合规、区域可用性不同
- **计费与限流差异**：价格模型、QPS/TPM 配额和超限策略不同

实践建议：主教程先用 `openai` 跑通，再做一层“供应商适配层”（Provider Adapter），把差异封装在一处。

---

## 6. 相关阅读（建议收藏）

### 官方文档（首选）

- [OpenAI Developer Docs](https://platform.openai.com/docs/overview)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [OpenAI Python SDK（GitHub）](https://github.com/openai/openai-python)
- [Model Overview](https://platform.openai.com/docs/models)
- [Rate limits 指南](https://platform.openai.com/docs/guides/rate-limits)
- [Prompt Engineering 指南](https://platform.openai.com/docs/guides/prompt-engineering)

### 进阶学习（与工程化更相关）

- [Cookbook（官方示例集合）](https://cookbook.openai.com/)
- [Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Safety Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Azure OpenAI 文档](https://learn.microsoft.com/azure/ai-services/openai/)
- [Anthropic Docs](https://docs.anthropic.com/)
- [Google AI for Developers（Gemini）](https://ai.google.dev/)
- [DashScope 文档（通义千问）](https://help.aliyun.com/zh/model-studio/)
- [Ollama 官方文档](https://ollama.com/docs)

---

## 7. 小结

如果你是新手，建议按这个顺序练习：

1. `chat.completions.create`（先把单轮对话跑通）
2. `stream=True`（做出更好的交互体验）
3. `response_format=json_object`（让结果可编程）
4. `tools/function calling`（让模型调用真实能力）
5. `embeddings`（为 RAG 和检索做准备）

当你把这 5 块串起来时，就已经具备了搭建一个可用 AI 功能模块的核心能力。

