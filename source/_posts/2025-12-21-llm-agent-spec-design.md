---
title: Agent 输出飘忽不定？用 Schema 锁死格式
date: 2025-12-21 18:00:00
updated: {{current_date_time}}
categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - AI与研究
tags:
  - LLM
  - Agent
  - Spec
  - Schema
  - JSON Schema
  - Pydantic
keywords: LLM, Agent, Spec, Schema, JSON Schema, Pydantic, 结构化输出, 输出规范
description: '深入解析 Agent Spec 设计：从 JSON Schema 到 Pydantic，掌握如何用 Schema 限制 Agent 输出，提升稳定性和可控性'
top_img: /img/llm-agent-spec-design.png
cover: /img/llm-agent-spec-design.png
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

Agent 有时输出 JSON，有时多几句解释，有时字段名拼错——**下游解析直接崩**。

Spec 设计用 JSON Schema、Pydantic 等约束输出格式，让 Agent 稳定产出可解析的结构。本篇解析如何设计 Spec、选择 Schema 工具、处理边界情况，提升 Agent 输出的可控性。

**Spec** = 用 Schema（JSON Schema、Pydantic）定义输出格式，强制验证，让 Agent 稳定产出可解析的 JSON。输出飘忽、字段缺失、类型错误——Schema 约束 + 验证能解决。

---

## 📐 一、JSON Schema：定义输出格式

下游要解析"用户信息"做入库——Agent 有时多输出 `remark` 字段，有时少 `phone`，**解析直接报错**。JSON Schema 定义 JSON 结构——哪些字段、什么类型、是否必填。基本语法：

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "用户姓名"
    },
    "age": {
      "type": "integer",
      "description": "用户年龄",
      "minimum": 0,
      "maximum": 150
    }
  },
  "required": ["name", "age"]
}
```

**代码示例**：

```python
# JSON Schema 示例（伪代码）

user_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "用户姓名"
        },
        "age": {
            "type": "integer",
            "description": "用户年龄",
            "minimum": 0,
            "maximum": 150
        },
        "email": {
            "type": "string",
            "format": "email",
            "description": "用户邮箱"
        }
    },
    "required": ["name", "age"]
}

# 在 Prompt 中使用
prompt = f"""
请输出用户信息，格式必须符合以下 JSON Schema：

{json.dumps(user_schema, indent=2)}

用户输入：{user_input}
"""

# LLM 输出会被 Schema 限制
response = llm.generate(prompt)
```

### 1.2 复杂 Schema 示例

**嵌套对象**：

```json
{
  "type": "object",
  "properties": {
    "user": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"}
      },
      "required": ["name", "age"]
    },
    "address": {
      "type": "object",
      "properties": {
        "city": {"type": "string"},
        "street": {"type": "string"}
      }
    }
  },
  "required": ["user"]
}
```

**数组**：

```json
{
  "type": "object",
  "properties": {
    "users": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "age": {"type": "integer"}
        },
        "required": ["name", "age"]
      }
    }
  },
  "required": ["users"]
}
```

---

## 🐍 二、Pydantic：Python 的数据验证

**Pydantic** 是 Python 的数据验证库，可以用来验证 Agent 的输出。

### 2.1 Pydantic 基础

Pydantic 做数据校验——定义模型后自动检查类型和约束。基本用法：

```python
# Pydantic 示例

from pydantic import BaseModel, Field, validator

class User(BaseModel):
    name: str = Field(..., description="用户姓名")
    age: int = Field(..., ge=0, le=150, description="用户年龄")
    email: str = Field(..., description="用户邮箱")
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('邮箱格式不正确')
        return v

# 使用 Pydantic 验证
try:
    user = User(name="张三", age=25, email="zhangsan@example.com")
    print(user.json())
except ValidationError as e:
    print(f"验证失败：{e}")
```

### 2.2 Pydantic 与 Agent 集成

**代码示例**：

```python
# Pydantic 与 Agent 集成（伪代码）

from pydantic import BaseModel, Field

class TaskResult(BaseModel):
    """任务结果模型"""
    success: bool = Field(..., description="是否成功")
    result: str = Field(..., description="结果内容")
    error: str = Field(None, description="错误信息")

def validate_agent_output(output: str, schema: BaseModel):
    """验证 Agent 输出"""
    try:
        # 解析 JSON
        data = json.loads(output)
        
        # 验证 Schema
        result = schema(**data)
        
        return {"success": True, "data": result}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON 解析失败：{e}"}
    except ValidationError as e:
        return {"success": False, "error": f"Schema 验证失败：{e}"}

# 使用示例
agent_output = '{"success": true, "result": "任务完成"}'
schema = TaskResult

validation_result = validate_agent_output(agent_output, schema)
```

---

## 🔧 三、Spec 设计最佳实践

### 3.1 设计原则

**原则1：明确性**
> Schema 定义要明确，不要有歧义。

**原则2：完整性**
> 定义所有必需的字段，不要遗漏。

**原则3：可扩展性**
> Schema 要易于扩展，支持未来需求。

**原则4：可验证性**
> Schema 要可以验证，确保输出符合要求。

### 3.2 常见模式

**模式1：结果包装**
> 用统一的格式包装结果。

```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "data": {"type": "object"},
    "error": {"type": "string"}
  },
  "required": ["success"]
}
```

**模式2：分页结果**
> 支持分页的结果格式。

```json
{
  "type": "object",
  "properties": {
    "items": {
      "type": "array",
      "items": {"type": "object"}
    },
    "total": {"type": "integer"},
    "page": {"type": "integer"},
    "page_size": {"type": "integer"}
  },
  "required": ["items", "total"]
}
```

---

## 🔍 总结：Spec 设计提升 Agent 输出稳定性

### 💡 快速回顾：你学到了什么？

1. **JSON Schema**：定义输出格式的标准
2. **Pydantic**：Python 的数据验证库
3. **最佳实践**：Spec 设计的原则和模式
4. **工程实践**：如何在实际项目中应用 Spec 设计

### Spec 设计的核心作用

| 组件 | 作用 | 简单理解 |
|------|------|---------|
| **JSON Schema** | 定义输出格式 | 告诉 Agent 输出应该是什么样子 |
| **Pydantic** | 验证输出数据 | 检查输出是否符合要求 |
| **错误处理** | 处理不符合 Schema 的输出 | 当输出不符合时如何处理 |

**生活化理解**：
> 就像填表格：
> - **JSON Schema**：表格模板，定义哪些字段必填，字段类型是什么
> - **Pydantic**：表格检查员，检查填写的内容是否符合要求
> - **错误处理**：如果填写错误，提示用户修正

### 设计原则总结

| 原则 | 说明 | 示例 |
|------|------|------|
| **明确性** | Schema 定义要明确 | ✅ 字段类型、必填项都明确<br>❌ 模糊的定义 |
| **完整性** | 定义所有必需字段 | ✅ 所有必需字段都定义<br>❌ 遗漏必需字段 |
| **可扩展性** | Schema 易于扩展 | ✅ 支持可选字段<br>❌ 固定结构 |
| **可验证性** | Schema 可以验证 | ✅ 可以用工具验证<br>❌ 无法验证 |

### 实战建议与检查清单

1. **从简单开始**：先定义简单的 Schema，再逐步完善
2. **重视验证**：使用 Pydantic 等工具验证输出
3. **错误处理**：处理不符合 Schema 的输出，不要直接失败
4. **持续优化**：根据实际使用情况优化 Schema

**上线前检查**：Schema 是否覆盖所有必需字段？是否有默认值处理？解析失败时是否有降级策略（如重试、提示用户）？

> 💡 **核心理解**：
> Spec 设计是提升 Agent 输出稳定性的关键，通过 Schema 限制输出格式，确保输出的可控性和可解析性。
> 
> 就像 API 设计一样，好的 Spec 设计能让 Agent 的输出更稳定、更可靠，便于后续处理和使用。

---

## 📚 延伸阅读

* [**JSON Schema 官方文档**](https://json-schema.org/)：JSON Schema 的官方文档
* [**Pydantic 官方文档**](https://docs.pydantic.dev/)：Pydantic 的官方文档

---

## 🔔 系列说明

> 本文是[《🧠 LLM/Agent 从入门到精通：告别浅尝辄止》](/categories/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/)系列第 11 篇。上一篇：[LangChain、LlamaIndex、AutoGPT 怎么选？Agent 框架对比](/2025-12-20-llm-agent-framework-comparison/)。下一篇：[Agent 怎么查数据库、调 API？Function Calling 与工具封装](/2025-12-18-llm-agent-tool-system/)。

