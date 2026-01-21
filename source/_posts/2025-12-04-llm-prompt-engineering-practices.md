---
title: 🧠 主题3｜Prompt 工程实战：三大核心技巧与结构化输出
date: 2025-12-04 18:00:00
updated: {{current_date_time}}

categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
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

> **这是[《🧠 LLM/Agent 从入门到精通：告别浅尝辄止》](/categories/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/)系列第 3 篇**

> 上一篇我们理解了 LLM 的"语言"：Prompt、上下文窗口和 In-Context Learning。

> 本篇，我们从实战角度，掌握 Prompt 工程的三大核心技巧，实现稳定、可解析的结构化输出。

---

## 🚀 导言 — 从"聊天"到"高效工作"

在前两篇中，我们掌握了 LLM 的底层机制（Token、Transformer）和交互基础（Prompt、ICL）。

当你开始真正用 LLM 做项目时，会发现一个令人头疼的问题：

> **你希望得到 JSON，却得到了一段解释文字；**  
> **你希望表格化输出，结果模型输出了自由文本；**  
> **你希望模型调用工具，但它只是"说"要调用，却不按格式输出。**

这不是模型能力的问题，而是 **Prompt 设计的问题**。

实际开发 Agent 或自动化流程时，最令人头疼的问题往往不是模型能力不够，而是**输出格式不稳定、行为不可控**。

---

## 💡 Prompt 工程是什么，不是什么？

在深入技巧之前，我们需要先澄清一个关键问题：**什么是 Prompt 工程？**

### 常见的误解

很多人以为 Prompt 工程就是：

* **多写一点** — 把问题描述得更详细
* **描述清楚一点** — 用更准确的语言表达需求
* **提示模型输出你想要的内容** — 告诉模型"请输出 JSON"

这些做法有一定效果，但**不是真正的 Prompt 工程**。

### Prompt 工程的真正内涵

真正的 Prompt 工程是一个**系统化的工程方法**，包含以下维度：

| 类别 | 说明 | 对应本篇技巧 |
|------|------|------------|
| **角色定位** | 明确模型应该以谁的身份工作 | 技巧一：明确角色（Persona Defining） |
| **任务描述** | 清晰、结构化地说明任务是什么，不是什么 | 贯穿所有技巧 |
| **输入格式** | 明确用户会提供什么格式的数据 | 技巧三：结构化输出保障（分隔符） |
| **输出格式** | 强制模型使用特定结构输出（JSON、表格等） | 技巧三：结构化输出保障（Schema） |
| **推理约束（Chain-of-Thought）** | 控制思考过程，为模型提供思路或限制思路 | 技巧二：思维链进阶（ReAct） |
| **抗偏差与抗幻觉设计** | 明确禁止模型编造、要求引用来源、允许拒答 | 技巧一：明确角色（限制条件） |
| **错误恢复机制** | 当输入异常时如何自我修正 | 技巧二：思维链进阶（Self-Correction） |

> 💡 **核心理解**：Prompt 工程不是技巧，是**规范化 + 工程化**。
> 
> * **规范化**：用统一的标准和模板设计 Prompt
> * **工程化**：考虑边界情况、错误处理、可维护性

这就像写代码一样：
* ❌ **不是**：想到什么写什么，能跑就行
* ✅ **而是**：遵循规范、考虑异常、可测试、可维护

---

## 🎯 三大核心技巧概览

基于 Prompt 工程的内涵，本篇将介绍 **三大核心技巧**，帮助你获得**稳定、可解析的结构化输出**：

1. **明确角色（Persona Defining）** — 让模型"入戏"，聚焦专业领域
   * 对应：角色定位、抗偏差设计

2. **思维链进阶（Advanced CoT / ReAct）** — 外化思考过程，实现可控决策
   * 对应：推理约束、错误恢复机制

3. **结构化输出保障（Schema + 分隔符）** — 确保机器可读、程序可解析
   * 对应：输入格式、输出格式

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

**完整示例**：

```text
System Prompt:
你是一位经验丰富的测试架构师，专注于自动化测试和测试平台开发。

你的职责是：
1. 设计清晰、可维护的测试用例
2. 提供符合最佳实践的测试方案
3. 使用专业术语，保持输出简洁

限制：
- 禁止使用模糊或不确定的表达
- 禁止在代码示例中添加注释（除非必要）
- 输出必须结构化（使用 Markdown 表格或列表）

User Prompt:
请为"用户注册功能"设计测试用例。

模型输出（更专业、更结构化）：
## 测试用例设计

| 用例ID | 测试场景 | 前置条件 | 测试步骤 | 预期结果 |
|--------|---------|---------|---------|---------|
| TC001 | 正常注册 | 无 | 1. 打开注册页面<br>2. 输入有效信息<br>3. 点击注册 | 注册成功，跳转登录页 |
| TC002 | 邮箱已存在 | 邮箱已注册 | 1. 输入已注册邮箱<br>2. 点击注册 | 提示"邮箱已存在" |
...
```

> 🔧 **实战提示**：
> * 将角色定义放在 **System Prompt** 中，以赋予最高权重和持续性
> * **身份要具体**：避免"你是一个助手"这样的模糊表达，改为"你是一位测试架构师"
> * **目标要唯一**：一个角色只负责一个核心任务，避免职责混乱
> * **限制要明确**：用"禁止"、"必须"等明确词汇，避免模糊表达

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

Final Answer: [最终答案]
```

**实际应用示例**：

```text
System Prompt:
你是一个测试自动化助手，可以通过调用工具来执行测试任务。

User Prompt:
请检查 API 接口 /api/users 是否正常。

模型输出：
Thought: 我需要先调用 API 检查工具来测试这个接口。

Action: check_api(url="/api/users", method="GET")

Observation: {"status": 200, "response_time": 120ms, "data": [...]}

Thought: API 返回 200 状态码，响应时间正常，接口工作正常。

Final Answer: API 接口 /api/users 工作正常，状态码 200，响应时间 120ms。
```

### CoT 与自我修正（Self-Correction）

当 Observation 阶段出现错误，可在下一次 Thought 中要求模型**识别并修正错误**：

```text

Thought: 上一步调用 API 失败，返回 404，原因是缺失参数"ID"。我需要重新规划 Action，补充缺失参数。

```

> 🔹 这让复杂任务更可控，避免错误累积。

### 自我一致性检查（Self-Consistency）

对于需要高准确性的任务（如代码生成、数学计算），可以要求模型生成多个答案，然后选择最一致的：

```text
System Prompt:
你是一个代码审查助手。对于每个代码片段，请生成 3 个不同的审查意见，然后选择最一致、最准确的作为最终答案。

输出格式：
审查意见1: [意见]
审查意见2: [意见]
审查意见3: [意见]
最终审查意见: [选择最一致的]
```

> 💡 **适用场景**：适合需要高准确性的任务，但会增加 Token 消耗，需要权衡成本。

---

## 🧱 技巧三：确保结构化输出（Schema + 分隔符）

这是最关键的一环，尤其当下游程序需要 JSON / YAML / XML 时。

### 核心方法：使用 Schema 约束

* **定义**：Schema 描述输出数据结构（JSON Schema、Pydantic 等）

* **作用**：不仅告诉模型"输出 JSON"，还规定字段名、类型、必选项

#### 示例

| 步骤               | 方法                                  | Prompt 片段                                                                                                                                |
| ---------------- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **1. 格式声明**      | 明确仅输出 JSON                          | "你的输出必须且只能是 JSON 格式，不要添加任何解释性文字。"                                                                                                                    |
| **2. 注入 Schema** | 将 JSON Schema 文本加入 Prompt           | `{"type":"object","properties":{"user_id":{"type":"integer"},"task_list":{"type":"array","items":{"name":"string","status":"string"}}}}` |
| **3. 使用工具**      | 高级：调用 `function_call` / `tool_call` | 模型直接输出符合 Schema 的函数对象                                                                                                                    |

**完整示例**：

```text
System Prompt:
你是一个测试用例生成器。你的输出必须且只能是 JSON 格式，不要添加任何解释性文字。

输出格式必须符合以下 Schema：
{
  "type": "object",
  "properties": {
    "test_cases": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "title": {"type": "string"},
          "steps": {"type": "array", "items": {"type": "string"}},
          "expected": {"type": "string"}
        },
        "required": ["id", "title", "steps", "expected"]
      }
    }
  }
}

User Prompt:
为"用户登录功能"生成 3 个测试用例。

模型输出（仅 JSON）：
{
  "test_cases": [
    {
      "id": 1,
      "title": "正常登录",
      "steps": ["打开登录页面", "输入正确用户名和密码", "点击登录按钮"],
      "expected": "登录成功，跳转到首页"
    },
    {
      "id": 2,
      "title": "错误密码登录",
      "steps": ["打开登录页面", "输入正确用户名和错误密码", "点击登录按钮"],
      "expected": "显示错误提示：密码错误"
    },
    {
      "id": 3,
      "title": "空用户名登录",
      "steps": ["打开登录页面", "不输入用户名，只输入密码", "点击登录按钮"],
      "expected": "显示错误提示：用户名不能为空"
    }
  ]
}
```

> 💡 **关键点**：
> * **明确格式要求**：在 System Prompt 中强调"仅输出 JSON"
> * **提供完整 Schema**：不仅告诉模型"输出 JSON"，还要规定字段名、类型、必选项
> * **禁止解释文字**：避免模型在 JSON 前后添加说明

### 使用分隔符

分隔符帮助模型专注核心任务，区分指令、上下文和用户输入：

```text

请总结 <<<用户输入>>> 中的内容，并以 YAML 输出摘要和关键词。

<<<用户输入>>>

[用户粘贴的文本]

<<<END>>>

```

---

## 🏗️ 工程化实践：从技巧到系统

掌握了三大核心技巧后，我们需要将 Prompt 设计**工程化**，实现可复用、可维护、可测试。

### 模板工程（Template Engineering）

将 Prompt 设计成**可复用、可维护的模板**，就像代码中的函数一样。

**为什么需要模板？**

* **一致性**：确保相同任务使用相同的 Prompt 结构
* **可维护性**：修改模板即可影响所有使用该模板的地方
* **可测试性**：可以针对模板进行测试和优化

**模板设计示例**：

```python
# Prompt 模板
TEST_CASE_TEMPLATE = """
你是一位经验丰富的测试架构师。

任务：为以下功能设计测试用例

功能名称：{feature_name}
功能描述：{feature_description}

输出格式：必须符合以下 JSON Schema
{schema}

约束：
- 禁止使用模糊或不确定的表达
- 测试用例必须覆盖正常流程和异常流程
- 每个测试用例必须包含：id、title、steps、expected
"""

# 使用模板
prompt = TEST_CASE_TEMPLATE.format(
    feature_name="用户登录",
    feature_description="用户通过用户名和密码登录系统",
    schema=json.dumps(test_case_schema)
)
```

### 工程化结构（Prompt as Code）

**什么是 Prompt as Code？**

就像写代码一样管理 Prompt：**模块化、版本控制、可测试、可复用**。

> 💡 **比喻理解**：
> * **传统方式**：每次都在聊天框里写 Prompt，像写临时脚本
> * **Prompt as Code**：把 Prompt 写成代码文件，像写正式项目

**为什么要这样做？**

* **可复用**：一次写好，多处使用
* **可维护**：修改一处，全局生效
* **可测试**：验证 Prompt 效果，确保质量
* **可协作**：团队共享，统一标准

#### 1. 模块化设计：像搭积木一样组合 Prompt

**问题**：如果每个 Prompt 都写完整的角色、约束、格式，会重复且难维护。

**解决**：把 Prompt 拆成小模块，按需组合。

**示例**：

```python
# 第一步：创建可复用的组件（像函数一样）

# prompts/components/persona.py
# 角色定义模块
PERSONA_TEST_ARCHITECT = "你是一位经验丰富的测试架构师，专注于自动化测试和测试平台开发。"

# prompts/components/constraints.py
# 约束条件模块
CONSTRAINT_NO_HALLUCINATION = "禁止编造信息，如果信息不确定，请明确说明'信息不足'。"

# prompts/components/format.py
# 输出格式模块
FORMAT_JSON_ONLY = "你的输出必须且只能是 JSON 格式，不要添加任何解释性文字。"

# 第二步：组合成完整的 Prompt（像调用函数一样）

# prompts/templates/test_case.py
from prompts.components import (
    PERSONA_TEST_ARCHITECT, 
    CONSTRAINT_NO_HALLUCINATION,
    FORMAT_JSON_ONLY
)

def build_test_case_prompt(feature_name, feature_description, schema):
    """构建测试用例生成的 Prompt"""
    return f"""
{PERSONA_TEST_ARCHITECT}

{CONSTRAINT_NO_HALLUCINATION}

{FORMAT_JSON_ONLY}

任务：为以下功能设计测试用例

功能名称：{feature_name}
功能描述：{feature_description}

输出格式必须符合以下 Schema：
{schema}
"""

# 第三步：使用（像调用 API 一样简单）

prompt = build_test_case_prompt(
    feature_name="用户登录",
    feature_description="用户通过用户名和密码登录系统",
    schema=json.dumps(test_case_schema)
)
```

**好处**：
* ✅ 修改角色定义时，只需改 `persona.py`，所有使用该角色的 Prompt 都会更新
* ✅ 可以轻松替换组件：把 `PERSONA_TEST_ARCHITECT` 换成 `PERSONA_DEVELOPER`
* ✅ 代码清晰，易于理解

#### 2. 版本控制：记录 Prompt 的演进历史

**问题**：Prompt 改来改去，不知道哪个版本效果好。

**解决**：像代码一样，用版本号管理 Prompt。

**示例**：

```python
# prompts/v1/test_case_generator.py
# 第一版：简单版本
SYSTEM_PROMPT_V1 = """
你是一个测试用例生成器。
请为指定功能生成测试用例。
"""

# prompts/v2/test_case_generator.py
# 第二版：增加了角色和约束
SYSTEM_PROMPT_V2 = """
你是一位经验丰富的测试架构师。
请为指定功能生成测试用例。
禁止使用模糊表达。
"""

# prompts/v3/test_case_generator.py
# 第三版：增加了格式要求
SYSTEM_PROMPT_V3 = """
你是一位经验丰富的测试架构师。
请为指定功能生成测试用例。
禁止使用模糊表达。
输出必须是 JSON 格式。
"""

# 使用时可以选择版本
def get_prompt(version="v3"):
    if version == "v1":
        return SYSTEM_PROMPT_V1
    elif version == "v2":
        return SYSTEM_PROMPT_V2
    else:
        return SYSTEM_PROMPT_V3
```

**好处**：
* ✅ 可以对比不同版本的效果
* ✅ 如果新版本有问题，可以快速回退到旧版本
* ✅ 记录 Prompt 的改进历程

#### 3. 测试：确保 Prompt 质量

**问题**：Prompt 改完后，不知道效果如何。

**解决**：像测试代码一样，测试 Prompt 的输出。

**示例**：

```python
# tests/test_prompts.py
import json

def test_test_case_prompt():
    """测试：验证 Prompt 生成的测试用例是否符合要求"""
    
    # 1. 构建 Prompt
    prompt = build_test_case_prompt(
        feature_name="用户登录",
        feature_description="用户通过用户名和密码登录系统",
        schema=json.dumps(test_case_schema)
    )
    
    # 2. 调用 LLM
    result = call_llm(prompt)  # 假设这是调用 LLM 的函数
    
    # 3. 验证输出格式（确保是有效的 JSON）
    assert validate_json_schema(result, TEST_CASE_SCHEMA)
    
    # 4. 验证内容完整性（确保至少生成了 3 个测试用例）
    assert len(result["test_cases"]) >= 3
    
    # 5. 验证每个测试用例都有必要字段
    for test_case in result["test_cases"]:
        assert "id" in test_case
        assert "title" in test_case
        assert "steps" in test_case
        assert "expected" in test_case
        assert len(test_case["steps"]) > 0  # 步骤不能为空
    
    print("✅ 测试通过：Prompt 输出符合要求")

# 运行测试
if __name__ == "__main__":
    test_test_case_prompt()
```

**好处**：
* ✅ 修改 Prompt 后，运行测试就知道是否破坏了功能
* ✅ 可以对比不同版本的效果（A/B 测试）
* ✅ 确保 Prompt 质量稳定

> 💡 **最佳实践**：
> * **使用配置文件**：将 Prompt 模板存储在 YAML/JSON 中，便于非技术人员修改
> * **A/B 测试**：对比不同版本的 Prompt 效果
> * **监控与日志**：记录 Prompt 的使用情况和效果，持续优化

---

## 🎯 完整实战案例：三大技巧综合应用

让我们通过一个完整的案例，看看如何将三大技巧结合起来，解决一个实际问题。

### 场景：自动生成测试用例

**需求**：根据功能描述，自动生成结构化的测试用例 JSON。

**挑战**：
* 输出格式必须严格符合 JSON Schema
* 需要覆盖正常流程和异常流程
* 测试步骤要清晰、可执行
* 需要处理边界情况

### 解决方案：结合三大技巧

#### 第一步：明确角色（Persona Defining）

```text
System Prompt:
你是一位经验丰富的测试架构师，专注于自动化测试。

你的职责：
1. 设计清晰、可维护的测试用例
2. 确保测试用例覆盖正常流程和异常流程
3. 使用专业术语，保持输出简洁

限制：
- 禁止使用模糊或不确定的表达（如"应该"、"可能"）
- 禁止编造不存在的功能点
- 如果信息不足，请明确说明"信息不足，无法生成完整测试用例"
```

#### 第二步：结构化输出（Schema + 分隔符）

```text
输出格式：必须且只能是 JSON 格式，不要添加任何解释性文字。

输出必须符合以下 Schema：
{
  "type": "object",
  "properties": {
    "feature_name": {"type": "string"},
    "test_cases": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "title": {"type": "string"},
          "priority": {"type": "string", "enum": ["高", "中", "低"]},
          "precondition": {"type": "string"},
          "steps": {
            "type": "array",
            "items": {"type": "string"}
          },
          "expected": {"type": "string"}
        },
        "required": ["id", "title", "priority", "steps", "expected"]
      }
    }
  },
  "required": ["feature_name", "test_cases"]
}
```

#### 第三步：使用分隔符明确输入

```text
User Prompt:
请为以下功能设计测试用例：

<<<功能描述>>>
功能名称：用户登录
功能描述：
- 用户通过用户名和密码登录系统
- 用户名支持邮箱和手机号两种格式
- 密码长度要求 6-20 位
- 连续 5 次密码错误后，账户将被锁定 30 分钟
<<<END>>>

要求：
- 至少生成 5 个测试用例
- 必须覆盖正常登录、错误密码、账户锁定等场景
- 测试步骤要清晰、可执行
```

#### 第四步：思维链（ReAct）处理复杂场景

如果功能描述复杂，可以要求模型先分析，再生成：

```text
System Prompt（增强版）:
你是一位经验丰富的测试架构师。

请按照以下步骤工作：

1. 分析功能描述，识别需要测试的场景
2. 为每个场景设计测试用例
3. 确保测试用例覆盖正常流程和异常流程

输出格式：
Thought: [分析功能，识别测试场景]
Test Cases: [JSON 格式的测试用例]

最终输出必须是有效的 JSON，符合以下 Schema：
{...schema...}
```

### 完整 Prompt 示例

```text
System Prompt:
你是一位经验丰富的测试架构师，专注于自动化测试。

职责：
1. 设计清晰、可维护的测试用例
2. 确保测试用例覆盖正常流程和异常流程
3. 使用专业术语，保持输出简洁

限制：
- 禁止使用模糊或不确定的表达
- 禁止编造不存在的功能点
- 如果信息不足，请明确说明"信息不足"

输出格式：必须且只能是 JSON 格式，不要添加任何解释性文字。

输出必须符合以下 Schema：
{
  "type": "object",
  "properties": {
    "feature_name": {"type": "string"},
    "test_cases": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "title": {"type": "string"},
          "priority": {"type": "string", "enum": ["高", "中", "低"]},
          "precondition": {"type": "string"},
          "steps": {"type": "array", "items": {"type": "string"}},
          "expected": {"type": "string"}
        },
        "required": ["id", "title", "priority", "steps", "expected"]
      }
    }
  },
  "required": ["feature_name", "test_cases"]
}

User Prompt:
请为以下功能设计测试用例：

<<<功能描述>>>
功能名称：用户登录
功能描述：
- 用户通过用户名和密码登录系统
- 用户名支持邮箱和手机号两种格式
- 密码长度要求 6-20 位
- 连续 5 次密码错误后，账户将被锁定 30 分钟
<<<END>>>

要求：
- 至少生成 5 个测试用例
- 必须覆盖正常登录、错误密码、账户锁定等场景
```

### 预期输出

```json
{
  "feature_name": "用户登录",
  "test_cases": [
    {
      "id": 1,
      "title": "正常登录-使用邮箱",
      "priority": "高",
      "precondition": "用户已注册，邮箱已验证",
      "steps": [
        "打开登录页面",
        "输入正确的邮箱地址",
        "输入正确的密码（6-20位）",
        "点击登录按钮"
      ],
      "expected": "登录成功，跳转到首页"
    },
    {
      "id": 2,
      "title": "正常登录-使用手机号",
      "priority": "高",
      "precondition": "用户已注册，手机号已验证",
      "steps": [
        "打开登录页面",
        "输入正确的手机号",
        "输入正确的密码（6-20位）",
        "点击登录按钮"
      ],
      "expected": "登录成功，跳转到首页"
    },
    {
      "id": 3,
      "title": "密码错误",
      "priority": "高",
      "precondition": "用户已注册",
      "steps": [
        "打开登录页面",
        "输入正确的用户名",
        "输入错误的密码",
        "点击登录按钮"
      ],
      "expected": "显示错误提示：用户名或密码错误"
    },
    {
      "id": 4,
      "title": "连续5次密码错误后账户锁定",
      "priority": "中",
      "precondition": "用户已注册",
      "steps": [
        "打开登录页面",
        "输入正确的用户名",
        "连续5次输入错误的密码并点击登录",
        "第6次尝试登录"
      ],
      "expected": "显示错误提示：账户已被锁定，请30分钟后再试"
    },
    {
      "id": 5,
      "title": "密码长度不符合要求",
      "priority": "中",
      "precondition": "用户已注册",
      "steps": [
        "打开登录页面",
        "输入正确的用户名",
        "输入长度小于6位的密码",
        "点击登录按钮"
      ],
      "expected": "显示错误提示：密码长度必须在6-20位之间"
    }
  ]
}
```

### 关键成功因素

1. **角色明确**：测试架构师的身份让模型使用专业术语，输出更规范
2. **格式严格**：JSON Schema 确保输出可解析
3. **输入清晰**：分隔符让模型明确知道哪里是功能描述
4. **约束到位**：禁止模糊表达、禁止编造，确保输出质量

> 💡 **实战提示**：
> * 如果输出不符合 Schema，检查是否在 System Prompt 中强调了"仅输出 JSON"
> * 如果测试用例覆盖不全，在 User Prompt 中明确要求"必须覆盖 XX 场景"
> * 如果步骤不够清晰，在角色定义中强调"测试步骤要清晰、可执行"

---

## 🔍 总结：Prompt Engineering 的设计哲学

| 目标     | 原则             | 技巧            |
| ------ | -------------- | ------------- |
| 高质量输出  | 限制自由度，聚焦专业     | 明确角色（Persona） |
| 复杂任务分解 | 外化思维过程，便于检查与修正 | ReAct 范式      |
| 程序化对接  | 确保机器可读、可验证     | Schema + 分隔符  |

> 三大技巧结合使用，你的 Prompt 从模糊提问升级为精确指令。

---

## ⚠️ 常见错误与修正

在实际使用中，经常会遇到以下问题。了解这些错误及其修正方法，可以帮你快速定位和解决问题：

| 错误 | 原因 | 修复方式 |
|------|------|---------|
| **输出太随意** | 没有输出格式约束 | 使用 JSON Schema 或明确格式要求 |
| **幻觉严重** | 没有限制与拒绝条件 | 加入禁止推测、要求引用来源、允许拒答 |
| **内容缺失** | 输入不规范 | 声明输入格式，使用分隔符区分输入区域 |
| **格式混乱** | Prompt 太自由 | 使用固定模板，明确每个部分的作用 |
| **多轮对话偏移** | 没有保持上下文 | 用 System Prompt 设置全局约束，在每轮对话中重申关键要求 |

> 💡 **关键理解**：大多数 Prompt 问题都可以通过**明确约束**和**结构化设计**来解决。

---

## 🔧 进阶优化技巧

掌握了核心技巧和工程化实践后，我们还需要掌握一些进阶优化技巧，让 Prompt 更高效、更稳定。

### 1. 调试技巧：如何定位和修复 Prompt 问题

当 Prompt 效果不理想时，如何快速定位问题？

#### 方法一：逐步简化法

**原理**：从最简单的 Prompt 开始，逐步增加复杂度，找出问题所在。

**步骤**：

```text
1. 最简版本：只保留核心任务
   "请生成3个测试用例"

2. 增加角色：看看角色是否有帮助
   "你是一位测试架构师。请生成3个测试用例"

3. 增加格式要求：看看格式约束是否生效
   "你是一位测试架构师。请生成3个测试用例，输出 JSON 格式"

4. 增加详细要求：逐步添加约束
   "你是一位测试架构师。请生成3个测试用例，输出 JSON 格式，必须覆盖正常和异常流程"
```

**好处**：能快速定位是哪个部分导致的问题。

#### 方法二：对比测试法

**原理**：同时测试多个版本的 Prompt，对比效果。

**示例**：

```python
# 测试不同版本
prompts = {
    "v1": "请生成测试用例",
    "v2": "你是一位测试架构师。请生成测试用例",
    "v3": "你是一位测试架构师。请生成测试用例，输出 JSON 格式"
}

results = {}
for version, prompt in prompts.items():
    result = call_llm(prompt)
    results[version] = {
        "output": result,
        "token_count": count_tokens(prompt + result),
        "quality_score": evaluate_quality(result)
    }

# 对比结果，选择最佳版本
```

> 💡 **实战提示**：
> * **先用逐步简化法定位问题**：找出是哪个部分导致的问题
> * **再用对比测试法优化效果**：对比不同版本，选择最佳方案
> * **遇到具体错误时**：参考[常见错误与修正](#⚠️-常见错误与修正)部分，快速找到修复方法

### 2. Token 成本优化：在保证效果的同时减少消耗

Token 消耗直接影响成本，如何在保证效果的同时减少 Token？

#### 策略一：精简 Prompt 内容

**原则**：保留必要信息，删除冗余描述。

```text
❌ 冗余版本（约 200 Token）：
你是一位经验非常丰富、在软件测试领域深耕多年、对自动化测试和测试平台开发有深入理解的资深测试架构师。你的职责是设计清晰、可维护、高质量的测试用例...

✅ 精简版本（约 50 Token）：
你是一位测试架构师，专注于自动化测试。职责：设计清晰的测试用例，确保覆盖正常和异常流程。
```

**优化技巧**：
* 删除重复描述（如"经验丰富"、"资深"等）
* 用列表代替长段落
* 合并相似的要求

#### 策略二：使用 Few-Shot 而非 Many-Shot

**原则**：Few-Shot（1-3 个示例）通常足够，Many-Shot（5+ 个示例）成本高但效果提升有限。

```text
# Few-Shot（推荐）
示例1: [输入] → [输出]
示例2: [输入] → [输出]

# Many-Shot（不推荐，除非必要）
示例1-10: [输入] → [输出]
```

#### 策略三：压缩历史对话

**方法**：将历史对话压缩为摘要，而不是完整保留。

```text
# 完整保留（消耗大量 Token）
历史对话：
用户：请生成测试用例A
助手：[...完整回复...]
用户：请生成测试用例B
助手：[...完整回复...]

# 压缩摘要（节省 Token）
历史摘要：
- 已生成测试用例A（用户登录功能，5个用例）
- 已生成测试用例B（购物车功能，6个用例）
```

#### 策略四：使用分隔符而非长描述

**方法**：用分隔符标记输入区域，而不是用长段落描述。

```text
❌ 长描述版本：
请为以下功能设计测试用例。功能名称是用户登录，功能描述是用户通过用户名和密码登录系统，用户名支持邮箱和手机号两种格式...

✅ 分隔符版本：
请为以下功能设计测试用例：

<<<功能描述>>>
功能名称：用户登录
功能描述：用户通过用户名和密码登录系统...
<<<END>>>
```

> 💡 **成本对比**：
> * 精简 Prompt：可节省 30-50% Token
> * 使用 Few-Shot：可节省 40-60% Token（相比 Many-Shot）
> * 压缩历史对话：可节省 70-90% Token（长对话场景）

### 3. 不同模型的 Prompt 适配技巧

不同模型对 Prompt 的响应有差异，如何针对不同模型调整 Prompt？

#### GPT-4 / GPT-4 Turbo

**特点**：
* 对 System Prompt 响应好
* 结构化输出能力强
* 对长 Prompt 理解好

**适配技巧**：
* ✅ 可以使用详细的 System Prompt
* ✅ 可以使用复杂的 JSON Schema
* ✅ 可以使用长 Few-Shot 示例

**示例**：
```text
System Prompt（详细版，适合 GPT-4）:
你是一位经验丰富的测试架构师，专注于自动化测试和测试平台开发。
你的职责是设计清晰、可维护的测试用例...
[详细描述...]
```

#### Claude 3 / Claude 3.5

**特点**：
* 对 System Prompt 响应好
* 对格式要求理解准确
* 对长上下文处理能力强

**适配技巧**：
* ✅ 可以使用详细的 System Prompt
* ✅ 可以使用 XML 标签（Claude 推荐）
* ✅ 可以使用长 Few-Shot 示例

**示例**：
```text
System Prompt（适合 Claude）:
<role>你是一位测试架构师</role>
<task>设计测试用例</task>
<constraints>禁止模糊表达，输出 JSON 格式</constraints>
```

#### 开源模型（Llama、Mistral 等）

**特点**：
* System Prompt 支持可能较弱
* 对复杂格式理解有限
* 需要更明确的指令

**适配技巧**：
* ⚠️ System Prompt 要简洁
* ⚠️ 格式要求要明确且简单
* ⚠️ 使用 Few-Shot 而非 Zero-Shot
* ⚠️ 避免过于复杂的 JSON Schema

**示例**：
```text
User Prompt（适合开源模型）:
你是一位测试架构师。请为"用户登录"功能生成测试用例。

要求：
1. 输出 JSON 格式
2. 至少3个测试用例
3. 每个用例包含：id, title, steps, expected

示例：
输入：功能名称
输出：{"test_cases": [{"id": 1, "title": "...", "steps": [...], "expected": "..."}]}

现在请为"用户登录"生成测试用例。
```

#### 通用适配原则

| 模型类型 | System Prompt | 格式要求 | Few-Shot | 建议 |
|---------|--------------|---------|---------|------|
| **GPT-4** | 详细 | 复杂 Schema | 3-5 个 | 充分利用能力 |
| **Claude** | 详细 | XML 标签 | 3-5 个 | 充分利用能力 |
| **开源模型** | 简洁 | 简单格式 | 1-3 个 | 降低复杂度 |

> 💡 **实战提示**：
> * **先设计通用 Prompt**：适用于大多数模型
> * **再针对特定模型优化**：根据实际使用的模型调整
> * **使用 A/B 测试**：对比不同 Prompt 在不同模型上的效果
> 
> **注意**：详细的模型对比和选型建议将在第 5 篇《评估与选型》中深入讲解。

---

## 📚 延伸阅读（含可直接访问链接）

以下资源按主题分类，每个资源都附有简要说明，帮助你选择合适的学习材料。

### 🎭 Persona Defining（角色定义）

* [**System Prompt Best Practices（System Prompt 最佳实践）**](https://platform.openai.com/docs/guides/prompt-engineering/system-messages)：OpenAI 关于 System Prompt 的最佳实践指南。**强烈推荐**，适合所有开发者。

* [**Prompt Engineering for Claude（Claude Prompt 指南）**](https://docs.anthropic.com/claude/docs/system-prompts)：Anthropic 关于 System Prompt 的详细指南。适合使用 Claude 的开发者。

* [**Prompt Engineering Guide（提示工程综合指南）**](https://www.promptingguide.ai/)：社区维护的 Prompt 工程综合指南，包含角色定义、Few-Shot 等多种技巧。适合想系统学习的读者。

### 🔗 ReAct & Chain-of-Thought（思维链与推理行动）

* [**ReAct: Synergizing Reasoning and Acting in Language Models（ReAct 原始论文）**](https://arxiv.org/abs/2210.03629)：ReAct 范式的开创性论文，展示了如何结合推理和行动。**必读论文**，适合所有读者。

* [**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models（CoT 原始论文）**](https://arxiv.org/abs/2201.11903)：CoT 的开创性论文，展示了如何通过思维链提升模型推理能力。**必读论文**，适合所有读者。

* [**Self-Correction Mechanisms in LLMs（自我修正机制）**](https://arxiv.org/abs/2302.06675)：研究 LLM 如何识别和修正错误的论文。适合想实现自我修正功能的开发者。

* [**Tree of Thoughts: Deliberate Problem Solving with Large Language Models（思维树）**](https://arxiv.org/abs/2305.10601)：CoT 的进阶方法，通过树状结构探索多种推理路径。适合想处理复杂推理任务的读者。

### 🧱 Schema & Structured Output（结构化输出）

* [**Pydantic 官方文档**](https://docs.pydantic.dev/)：Python 中最流行的数据验证库，常用于定义 LLM 输出的 Schema。**强烈推荐**，适合 Python 开发者。

* [**OpenAI Function Call 文档**](https://platform.openai.com/docs/guides/gpt/function-calling)：OpenAI 官方的 Function Calling 指南，展示了如何使用 Schema 约束模型输出。**必读**，适合使用 OpenAI API 的开发者。

* [**Anthropic Tool Use（Claude 工具使用）**](https://docs.anthropic.com/claude/docs/tool-use)：Anthropic 关于工具调用和结构化输出的指南。适合使用 Claude 的开发者。

* [**JSON Schema 规范**](https://json-schema.org/)：JSON Schema 的官方规范，用于定义数据结构。适合需要深入理解 Schema 的开发者。

### 📖 Prompt Engineering 综合指南

* [**OpenAI Prompt Engineering Guide（OpenAI 官方指南）**](https://platform.openai.com/docs/guides/prompt-engineering)：OpenAI 官方的 Prompt 工程指南，涵盖基础技巧和最佳实践。**强烈推荐新手阅读**，内容全面且实用。

* [**Prompt Engineering Guide（社区指南）**](https://www.promptingguide.ai/)：社区维护的 Prompt 工程综合指南，包含大量示例和技巧。**适合想系统学习的读者**，内容更新及时。

* [**Anthropic Prompt Engineering（Claude 指南）**](https://docs.anthropic.com/claude/docs/prompt-engineering)：Anthropic 官方的 Prompt 工程指南，特别针对 Claude 模型优化。适合使用 Claude 的开发者。

### 🛠️ 实战工具与框架

* [**LangChain Prompt Templates（LangChain Prompt 模板）**](https://python.langchain.com/docs/modules/model_io/prompts/)：LangChain 的 Prompt 模板系统，方便构建复杂 Prompt。适合使用 LangChain 的开发者。

* [**LangChain Output Parsers（LangChain 输出解析器）**](https://python.langchain.com/docs/modules/model_io/output_parsers/)：LangChain 的输出解析器，帮助将模型输出转换为结构化数据。适合使用 LangChain 的开发者。

* [**PromptLayer（Prompt 管理工具）**](https://www.promptlayer.com/)：Prompt 版本管理和分析工具，帮助优化 Prompt 效果。适合需要管理大量 Prompt 的团队。

* [**OpenAI Evals（评估框架）**](https://github.com/openai/evals)：OpenAI 开源的 Prompt 评估框架，帮助测试和优化 Prompt。适合需要系统评估 Prompt 的开发者。

### 🇨🇳 中文资源

* [**Prompt Engineering 中文指南**](https://www.promptingguide.ai/zh)：Prompt Engineering Guide 的中文版本，内容全面。**适合中文读者**。

* [**LLM 应用开发实践（中文博客）**](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)：Lilian Weng 的 Prompt Engineering 博客文章，有中文翻译版本。适合中文读者，内容深入。

---

## 🔔 下一篇预告

结构化输出解决了格式问题，但仍存在**知识受限**的问题：

> 模型的知识截止到训练时间，无法获取最新信息；  
> 模型可能产生"幻觉"，编造不存在的信息；  
> 模型无法访问私有知识库或专业文档。

下一篇，我们将介绍 **RAG（检索增强生成）**，突破 LLM 的**知识时间限制与专业性边界**。

* 如何让 LLM 访问最新信息？  
* 如何让 LLM 理解你的私有文档？  
* 检索 → 分块 → 重排 → 融合的完整流程是什么？

