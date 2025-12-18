---
title: 🧠 主题7｜决策引擎 ReAct：代码级拆解 Agent 推理与工具调用
date: 2025-12-16 18:00:00
series: 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
categories:
  - 技术学习与行业趋势
  - AI与研究
tags:
  - LLM
  - Agent
  - ReAct
  - Self-Ask
  - Tree-of-Thoughts
  - 决策引擎
  - 思维链
keywords: LLM, Agent, ReAct, Self-Ask, Tree-of-Thoughts, ToT, 决策引擎, 思维链, CoT, 任务规划
description: '深入解析 Agent 的决策引擎：代码级拆解 ReAct 范式，掌握如何设计 Prompt 模板、实现工具调用和错误处理，对比 Self-Ask 和 Tree of Thoughts 等策略'
top_img: /img/llm-agent-decision-engine.png
cover: /img/llm-agent-decision-engine.png
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

> **这是[《🧠 LLM/Agent 从入门到精通：告别浅尝辄止》](/series/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/)系列第 7 篇**

> 上一篇我们系统理解了 Agent 的本质，揭秘了 LLM 如何进化为具有"行动能力"的智能体。

> 本篇，我们将深入 Agent 的"决策引擎"，代码级拆解 ReAct 范式，掌握如何设计 Prompt 模板、实现工具调用和错误处理。

---

## 🚀 导言 — 从"思考"到"行动"的飞跃

在[第6篇](/技术学习与行业趋势/AI与研究/2025-12-10-llm-agent-concept-overview/)中，我们了解了 Agent 通过 **Thought（思考）**、**Action（行动）** 和 **Observation（观察）** 的循环实现自主性。

但关键问题是：
> **高质量的思考是如何生成的？**  
> **如何让 Agent 做出正确的决策？**  
> **如何设计 Prompt 让 Agent 稳定地输出 Thought 和 Action？**

### 🤔 先理解几个基础概念

在深入 ReAct 之前，我们先理解几个关键概念：

**1. 思维链（CoT - Chain of Thought）**
> 简单理解：让 AI 像人一样，一步步思考问题，而不是直接给出答案。
> 
> 例如：
> - ❌ **直接回答**：答案是 42
> - ✅ **思维链**：首先，我需要计算 6×7。6×7=42，所以答案是 42

**2. 工具调用（Tool Calling）**
> 简单理解：让 AI 可以调用外部工具（如搜索、计算器、数据库）来完成它自己无法完成的任务。
> 
> 例如：AI 无法直接查询数据库，但可以调用 `query_database()` 工具来查询。

**3. Agentic Loop（Agent 循环）**
> 简单理解：Agent 完成任务的过程是一个循环：**思考 → 行动 → 观察 → 再思考 → 再行动...**
> 
> 就像人做任务一样：
> - 思考：我需要做什么？
> - 行动：执行操作
> - 观察：看看结果如何
> - 再思考：下一步该做什么？

**4. 结构化输出**
> 简单理解：让 AI 按照固定格式输出，方便程序解析。
> 
> 例如：要求 AI 输出 `Thought: ...` 和 `Action: ...`，而不是自由文本。

### 📋 本篇学习目标

本篇将从**简单到复杂**，帮你掌握：
1. **ReAct 的基本原理**：为什么需要 ReAct？它是如何工作的？
2. **ReAct Prompt 模板设计**：如何让 LLM 稳定输出结构化 Thought 和 Action
3. **代码实现（可选）**：如何从代码层面实现 ReAct（如果你不写代码，可以跳过这部分）
4. **错误处理与自我修正**：如何让 Agent 在失败时自动调整策略
5. **与其他策略对比**：Self-Ask、Tree of Thoughts 的适用场景

> 💡 **提示**：如果你是新手，可以先理解概念部分（第1节），代码部分（第2节）可以暂时跳过，等需要实践时再回来学习。

---

## 🔄 一、ReAct 范式：Agent 决策的基石

### 1.1 为什么需要 ReAct？

在了解 ReAct 之前，我们先看看**没有 ReAct 时的问题**：

**问题1：AI 无法调用工具**
> 传统 LLM 只能"说"，不能"做"。它无法查询数据库、调用 API、执行操作。

**问题2：AI 无法自我修正**
> 如果 AI 出错了，它无法根据错误结果调整策略，只能重复同样的错误。

**问题3：AI 无法处理多步任务**
> 对于复杂任务（如"查询数据并生成报告"），AI 无法分解成多个步骤，一步步完成。

**ReAct 解决了这些问题**：
- ✅ 让 AI 可以调用工具（查询数据库、调用 API）
- ✅ 让 AI 可以根据结果自我修正
- ✅ 让 AI 可以处理多步复杂任务

### 1.2 什么是 ReAct？

**ReAct (Reasoning + Acting)** 将 **思维链 (CoT)** 与 **工具调用** 融合，实现可解释、迭代式的决策流程。

**简单理解**：
> ReAct = **思考** + **行动** + **循环**

**工作流程**：

```
1. 思考（Reasoning）
   ↓
2. 行动（Acting）- 调用工具
   ↓
3. 观察（Observation）- 获取结果
   ↓
4. 再思考（根据结果决定下一步）
   ↓
5. 再行动...
   ↓
...循环直到任务完成
```

**生活例子**：
> 想象你要做一道菜，但不知道怎么做：
> 
> 1. **思考**："我需要先查菜谱，然后准备食材"
> 2. **行动**：打开手机搜索菜谱
> 3. **观察**：找到了菜谱，需要鸡蛋、面粉、糖
> 4. **再思考**："现在我需要准备这些食材"
> 5. **再行动**：去冰箱拿鸡蛋
> 6. **再观察**：鸡蛋准备好了
> 7. ...继续循环，直到菜做好
> 
> **ReAct 就是让 AI 也这样工作**：思考 → 行动 → 观察 → 再思考 → 再行动...

**核心公式**：

```
ReAct = CoT (思维链) + Tool Calling (工具调用) + Loop (循环)
```

> 💡 **一句话总结**：ReAct 让 AI 像人一样，通过"思考-行动-观察"的循环来完成复杂任务。

### 1.3 ReAct Prompt 模板拆解

ReAct 的核心在于**结构化输出**，使 LLM 在循环中显式生成 Thought → Action → Observation。

> 💡 **什么是结构化输出？**
> 
> 简单理解：要求 AI 按照固定格式输出，而不是自由文本。
> 
> - ❌ **自由文本**："我需要查询数据库，然后生成报告"（程序无法解析）
> - ✅ **结构化输出**：
>   ```
>   Thought: 我需要查询数据库
>   Action: query_database(sql="SELECT * FROM users")
>   ```
>   （程序可以轻松解析）

#### 核心组件：三个关键标签

ReAct 要求 AI 输出三个标签：

| 输出标签 | 简单理解 | 作用 | 例子 |
|---------|---------|------|------|
| **Thought** | AI 的思考过程 | 分析当前状态，决定下一步做什么 | `Thought: 我需要先查询数据库获取用户数据` |
| **Action** | AI 要执行的操作 | 调用哪个工具，传入什么参数 | `Action: query_database(sql="SELECT * FROM users")` |
| **Observation** | 工具执行的结果 | 工具返回了什么结果 | `Observation: 查询成功，返回 1000 条记录` |

**为什么需要这三个标签？**

1. **Thought（思考）**：让 AI 的决策过程**可解释**，我们能看到 AI 为什么这样做
2. **Action（行动）**：让程序能够**解析和执行**，调用对应的工具
3. **Observation（观察）**：让 AI 能够**根据结果调整策略**，如果出错了可以修正

#### 完整 Prompt 模板

**模板结构**（你可以直接复制使用）：

```text
System Prompt:
你是一个任务执行助手，可以通过调用工具来完成复杂任务。

你需要按照以下格式输出：

Thought: [分析当前状态，决定下一步行动]

Action: [工具名(参数)]

Observation: [工具返回结果]

...重复此循环，直到得到最终答案

Final Answer: [最终答案]

可用工具：
{tool_descriptions}

User Prompt:
{user_task}

历史记录：
{history}
```

> 💡 **模板说明**：
> - `{tool_descriptions}`：可用工具的列表和说明
> - `{user_task}`：用户的任务
> - `{history}`：之前的思考-行动-观察历史

#### 实际示例：一步步看 ReAct 如何工作

**场景**：让 AI 完成"查询用户数据并生成报告"

**Step 1：准备 Prompt**

```text
System Prompt:
你是一个测试自动化助手，可以通过调用工具来执行测试任务。

输出格式：
Thought: [你的思考]
Action: [工具名(参数)]
Observation: [工具返回结果]

可用工具：
1. query_database(sql): 查询数据库
2. generate_report(data): 生成报告
3. send_email(to, subject, body): 发送邮件

User Prompt:
查询用户数据并生成报告
```

**Step 2：AI 的第一轮输出**

```
Thought: 我需要先查询数据库获取用户数据。

Action: query_database(sql="SELECT * FROM users WHERE date='2025-12'")
```

**Step 3：程序执行工具，返回结果**

```
Observation: 查询成功，返回 1000 条用户记录
```

**Step 4：AI 的第二轮输出（基于观察结果）**

```
Thought: 数据已获取，现在需要生成报告。

Action: generate_report(data=[1000条记录], format="PDF")
```

**Step 5：程序执行工具，返回结果**

```
Observation: 报告生成成功，文件路径：/reports/users_2025-12.pdf
```

**Step 6：AI 判断任务完成，输出最终答案**

```
Thought: 报告已生成，任务完成。

Final Answer: 已成功查询用户数据并生成报告，文件路径：/reports/users_2025-12.pdf
```

> 💡 **关键理解**：
> - AI 不是一次性完成所有任务，而是**一步步来**
> - 每一步都会**思考**、**行动**、**观察**
> - 根据观察结果，决定下一步做什么

### 1.4 ReAct 的优势与局限

**优势**：

| 优势 | 说明 | 实际价值 |
|------|------|---------|
| **高可控性** | 结构化输出易解析和执行 | 可以稳定地解析和执行工具调用 |
| **迭代修正** | 工具执行失败可在下一 Thought 中自我修正 | 能够处理错误，自动调整策略 |
| **通用性** | 适用于大多数多步任务 | 可以处理各种复杂任务 |
| **可解释性** | 每一步都有明确的思考过程 | 便于调试和审计 |

**局限**：

| 局限 | 说明 | 影响 |
|------|------|------|
| **局部最优** | 每步基于当前状态做最优选择，可能错过更优长期路径 | 可能无法找到全局最优解 |
| **单分支探索** | 无法自然处理多分支思考或高度不确定任务 | 对于需要探索多种方案的任务效果有限 |

> 💡 **关键理解**：ReAct 是 Agent 决策的**稳定基础**，适合大多数多步任务。对于需要探索多种方案的任务，可以考虑 Tree of Thoughts（见第3节）。

---

## 🔧 二、代码级实现：ReAct 的完整实现

> ⚠️ **新手提示**：如果你不写代码，或者只是想理解概念，可以**跳过这一节**，直接看第3节"其他决策策略对比"。等你需要实际开发时，再回来学习代码实现。

理解了 ReAct 的原理后，我们来看看如何从代码层面实现一个完整的 ReAct Agent。

**实现 ReAct 需要做什么？**

1. **构建 Prompt**：把任务、工具、历史记录组合成完整的 Prompt
2. **调用 LLM**：让 LLM 生成 Thought 和 Action
3. **解析 Action**：从 LLM 输出中提取工具名和参数
4. **执行工具**：调用对应的工具
5. **循环**：重复上述过程，直到任务完成

### 2.1 Prompt 构建

**核心任务**：将任务、历史记录、可用工具组合成完整的 Prompt。

**简单理解**：
> 就像做菜需要准备食材一样，构建 Prompt 就是把所有"食材"（任务、工具、历史）组合在一起。

```python
# Prompt 构建（伪代码）
# 注意：这是简化版本，实际实现会更复杂

def build_react_prompt(task, history, tools):
    """
    构建 ReAct Prompt
    
    参数：
    - task: 用户的任务（如"查询用户数据并生成报告"）
    - history: 之前的思考-行动-观察历史
    - tools: 可用工具列表
    """
    
    # 步骤1：准备工具描述
    # 把每个工具的名称、参数、返回值整理成文本
    tool_descriptions = []
    for tool in tools:
        tool_descriptions.append(
            f"{tool.name}: {tool.description}\n"
            f"  参数: {tool.parameters}\n"
            f"  返回: {tool.returns}"
        )
    
    # 步骤2：格式化历史记录
    # 把之前的每一步都记录下来，让 AI 知道之前做了什么
    history_text = ""
    for step in history:
        history_text += f"""
Step {step.number}:
Thought: {step.thought}
Action: {step.action}
Observation: {step.observation}
"""
    
    # 步骤3：组合成完整的 Prompt
    # 把任务、工具、历史都放到 Prompt 里
    prompt = f"""
你是一个任务执行助手，可以通过调用工具来完成复杂任务。

你需要按照以下格式输出：

Thought: [分析当前状态，决定下一步行动]

Action: [工具名(参数)]

Observation: [工具返回结果]

...重复此循环，直到得到最终答案

Final Answer: [最终答案]

可用工具：
{chr(10).join(tool_descriptions)}

当前任务：{task}

历史记录：
{history_text}

请开始执行任务：
"""
    
    return prompt
```

**使用示例**：

```python
# 假设我们有这些工具
tools = [
    {"name": "query_database", "description": "查询数据库", "parameters": "sql", "returns": "查询结果"},
    {"name": "generate_report", "description": "生成报告", "parameters": "data, format", "returns": "报告路径"}
]

# 构建 Prompt
prompt = build_react_prompt(
    task="查询用户数据并生成报告",
    history=[],  # 第一次执行，没有历史
    tools=tools
)

# 现在 prompt 包含了所有信息，可以发送给 LLM 了
```

### 2.2 Action 解析

**核心任务**：从 LLM 输出中解析出工具名和参数。

**简单理解**：
> LLM 输出的是文本，比如 `Action: query_database(sql="SELECT * FROM users")`
> 
> 我们需要把这个文本**解析**成：
> - 工具名：`query_database`
> - 参数：`{"sql": "SELECT * FROM users"}`
> 
> 这样才能调用对应的工具。

```python
# Action 解析（伪代码）
# 注意：这是简化版本，实际实现需要处理更多边界情况

import re
import json

def parse_action(response):
    """
    从 LLM 输出中解析 Action
    
    输入示例：
    response = "Thought: 我需要查询数据库\nAction: query_database(sql=\"SELECT * FROM users\")"
    
    输出：
    tool_name = "query_database"
    args = {"sql": "SELECT * FROM users"}
    """
    
    # 步骤1：找到 Action 这一行
    # 使用正则表达式匹配 "Action: ..."
    action_match = re.search(r'Action:\s*(.+)', response)
    if not action_match:
        return None, None  # 没找到 Action，返回 None
    
    action_text = action_match.group(1).strip()  # 提取 Action 后面的内容
    
    # 步骤2：解析工具名和参数
    # 格式：工具名(参数)
    # 例如：query_database(sql="SELECT * FROM users")
    
    # 使用正则表达式匹配：工具名(参数)
    pattern = r'(\w+)\((.*)\)'
    match = re.match(pattern, action_text)
    
    if match:
        tool_name = match.group(1)  # 提取工具名
        args_str = match.group(2)   # 提取参数部分
        
        # 步骤3：解析参数
        # 参数可能是 key=value 格式，需要转换成字典
        args = {}
        for pair in args_str.split(','):
            if '=' in pair:
                key, value = pair.split('=', 1)
                # 去掉引号和空格
                args[key.strip()] = value.strip().strip('"\'')
        
        return tool_name, args
    
    return None, None

# 使用示例
response = """
Thought: 我需要查询数据库获取用户数据。

Action: query_database(sql="SELECT * FROM users")
"""

tool_name, args = parse_action(response)
# 输出：
# tool_name = "query_database"
# args = {"sql": "SELECT * FROM users"}
```

### 2.3 工具调用与错误处理

**核心任务**：执行工具调用，处理成功和失败情况。

**简单理解**：
> 解析出工具名和参数后，我们需要：
> 1. 找到对应的工具
> 2. 调用工具
> 3. 处理可能出现的错误（工具不存在、参数错误、执行失败等）

```python
# 工具调用与错误处理（伪代码）

def execute_tool(tool_name, args, tools):
    """
    执行工具调用
    
    参数：
    - tool_name: 工具名（如 "query_database"）
    - args: 工具参数（如 {"sql": "SELECT * FROM users"}）
    - tools: 可用工具字典
    
    返回：
    - {"success": True, "result": ...} 成功
    - {"success": False, "error": "错误信息"} 失败
    """
    
    # 步骤1：检查工具是否存在
    if tool_name not in tools:
        return {
            "success": False,
            "error": f"工具 '{tool_name}' 不存在"
        }
    
    tool = tools[tool_name]  # 获取工具对象
    
    # 步骤2：验证参数（检查参数格式是否正确）
    try:
        validated_args = tool.validate_args(args)
    except Exception as e:
        return {
            "success": False,
            "error": f"参数验证失败: {str(e)}"
        }
    
    # 步骤3：执行工具
    try:
        result = tool.execute(**validated_args)  # 调用工具的 execute 方法
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        # 如果执行失败，返回错误信息
        return {
            "success": False,
            "error": f"工具执行失败: {str(e)}"
        }

# 使用示例
tools = {
    "query_database": DatabaseTool(),    # 假设这些是工具对象
    "generate_report": ReportTool(),
    "send_email": EmailTool()
}

# 调用工具
result = execute_tool("query_database", {"sql": "SELECT * FROM users"}, tools)

# 检查结果
if result["success"]:
    observation = result["result"]  # 成功，使用结果
else:
    observation = f"错误: {result['error']}"  # 失败，记录错误信息
```

### 2.4 完整 ReAct Loop 实现

**核心任务**：将 Prompt 构建、Action 解析、工具调用组合成完整的循环。

**简单理解**：
> 这就是 ReAct 的完整流程：
> 1. 构建 Prompt（包含任务、工具、历史）
> 2. 调用 LLM，获取 Thought 和 Action
> 3. 解析 Action，提取工具名和参数
> 4. 执行工具，获取结果
> 5. 把结果加入历史，继续下一轮
> 6. 重复直到任务完成或达到最大步数

```python
# 完整 ReAct Loop（伪代码）

class ReActAgent:
    def __init__(self, llm, tools):
        """
        初始化 ReAct Agent
        
        参数：
        - llm: LLM 对象（如 GPT-4）
        - tools: 可用工具字典
        """
        self.llm = llm
        self.tools = tools
        self.history = []  # 记录历史：之前的思考-行动-观察
        self.max_steps = 10  # 最大步数，防止无限循环
    
    def run(self, task):
        """
        运行 ReAct Agent，完成任务
        
        参数：
        - task: 用户的任务（如"查询用户数据并生成报告"）
        
        返回：
        - {"success": True, "answer": "最终答案"} 成功
        - {"error": "错误信息"} 失败
        """
        
        steps = 0
        
        # 循环：思考 → 行动 → 观察 → 再思考 → 再行动...
        while steps < self.max_steps:
            # 步骤1：构建 Prompt
            # 把任务、工具、历史记录组合成完整的 Prompt
            prompt = build_react_prompt(
                task=task,
                history=self.history,
                tools=self.tools
            )
            
            # 步骤2：调用 LLM，获取响应
            response = self.llm.generate(prompt)
            
            # 步骤3：检查是否完成
            # 如果 LLM 输出了 "Final Answer:"，说明任务完成
            if "Final Answer:" in response:
                final_answer = response.split("Final Answer:")[-1].strip()
                return {"success": True, "answer": final_answer}
            
            # 步骤4：解析 Thought 和 Action
            thought = self.extract_thought(response)  # 提取思考过程
            tool_name, args = self.parse_action(response)  # 解析工具名和参数
            
            if not tool_name:
                return {"error": "无法解析 Action"}
            
            # 步骤5：执行工具
            result = self.execute_tool(tool_name, args)
            
            # 步骤6：更新历史记录
            # 把这一步的思考、行动、观察结果记录下来
            self.history.append({
                "step": steps + 1,
                "thought": thought,
                "action": f"{tool_name}({args})",
                "observation": result.get("result") or result.get("error")
            })
            
            steps += 1
        
        # 如果达到最大步数还没完成，返回错误
        return {"error": "达到最大步数限制"}

# 使用示例
agent = ReActAgent(
    llm=gpt4,  # 假设这是 GPT-4 对象
    tools={
        "query_database": DatabaseTool(),
        "generate_report": ReportTool()
    }
)

# 运行 Agent，完成任务
result = agent.run("查询用户数据并生成报告")

# 检查结果
if result["success"]:
    print(f"任务完成：{result['answer']}")
else:
    print(f"任务失败：{result['error']}")
```

> 💡 **关键理解**：
> - ReAct Loop 就是一个**循环**：思考 → 行动 → 观察 → 再思考...
> - 每一步都会记录到 `history` 中，让 AI 知道之前做了什么
> - 如果达到最大步数还没完成，就停止（防止无限循环）

### 2.5 错误处理与自我修正

**核心任务**：当工具调用失败时，让 Agent 在下一轮 Thought 中自我修正。

**简单理解**：
> 如果工具调用失败了（比如数据库连接失败），Agent 不应该直接放弃，而是应该：
> 1. 分析错误原因
> 2. 调整策略
> 3. 尝试其他方法
> 
> 就像人遇到问题时会想办法解决一样。

```python
# 错误处理与自我修正（伪代码）

def handle_error(agent, error, last_action):
    """
    处理错误，让 Agent 自我修正
    
    参数：
    - agent: ReAct Agent 对象
    - error: 错误信息
    - last_action: 失败的 Action
    
    返回：
    - (thought, action): 修正后的思考和行动
    """
    
    # 构建错误处理的 Prompt
    # 告诉 AI：上一个 Action 失败了，请分析原因并修正
    error_prompt = f"""
上一个 Action 执行失败：

Action: {last_action}
Error: {error}

请分析错误原因，并修正策略：

Thought: [分析错误原因，决定如何修正]

Action: [修正后的 Action]
"""
    
    # 调用 LLM，让它分析错误并给出修正方案
    response = agent.llm.generate(error_prompt)
    thought, action = agent.parse_response(response)
    
    return thought, action

# 在 ReAct Loop 中使用
result = execute_tool(tool_name, args, tools)

if not result["success"]:
    # 工具调用失败，进行错误处理
    error = result["error"]
    
    # 让 Agent 分析错误并修正策略
    thought, action = handle_error(agent, error, f"{tool_name}({args})")
    
    # 更新历史记录
    agent.history.append({
        "thought": thought,
        "action": action,
        "observation": f"上一个 Action 失败: {error}，已修正策略"
    })
    
    # 下一轮循环会使用修正后的 Action
```

**实际例子**：

```
Step 1:
Thought: 我需要查询数据库
Action: query_database(sql="SELECT * FROM users")
Observation: 错误：数据库连接失败

Step 2（错误处理）:
Thought: 数据库连接失败，可能是网络问题。我应该先检查数据库连接状态，或者尝试重试。
Action: check_database_connection()

Step 3:
Observation: 数据库连接正常
Thought: 连接正常，可能是 SQL 语句有问题。让我重新查询。
Action: query_database(sql="SELECT * FROM users LIMIT 100")
...
```

> 💡 **关键理解**：
> - Agent 遇到错误时，不是直接放弃，而是**分析原因并修正**
> - 错误信息会被加入到历史记录中，帮助 AI 做出更好的决策

---

## 🔍 三、其他决策策略对比

ReAct 是 Agent 决策的基石，但在某些场景下，其他策略可能更合适。

> 💡 **为什么需要其他策略？**
> 
> ReAct 适合**执行性任务**（调用工具、操作），但对于**信息检索任务**（搜索、查询），可能有更合适的策略。

### 3.1 Self-Ask：解决信息依赖问题

**简单理解**：
> Self-Ask 专门解决"需要先查资料才能回答问题"的场景。
> 
> **生活例子**：
> - 问题："谁是《三体》的作者？这本书获得了什么奖项？"
> - 你无法直接回答，需要：
>   1. 先搜索"《三体》的作者"
>   2. 再搜索"《三体》获得的奖项"
>   3. 最后组合答案
> 
> Self-Ask 就是让 AI 也这样做。

Self-Ask 是 CoT 的变体，专门解决 **多步信息检索**问题。

#### 机制详解

**原理**：当问题无法直接回答，Agent 会将问题分解为多个 **子问题**，逐步检索答案。

**Prompt 模板**：

```text
Question: [原始问题]

Follow up: [是否需要搜索新信息？Yes/No]

Intermediate Answer: [子问题]

[搜索结果/答案]

...重复，直到可以回答原始问题

So the final answer is: [最终答案]
```

**实际示例**：

```text
Question: 谁是《三体》的作者？这本书获得了什么奖项？

Follow up: Yes

Intermediate Answer: 《三体》的作者是谁？

[搜索结果：刘慈欣]

Follow up: Yes

Intermediate Answer: 《三体》获得了什么奖项？

[搜索结果：雨果奖]

So the final answer is: 《三体》的作者是刘慈欣，这本书获得了雨果奖。
```

#### 对比 ReAct：什么时候用哪个？

| 维度 | ReAct | Self-Ask |
|------|-------|----------|
| **主要用途** | 执行性工具调用（API、脚本、操作） | 信息检索（搜索引擎、RAG、查询） |
| **输出格式** | Thought → Action → Observation | Question → Follow up → Intermediate Answer |
| **适用场景** | 需要执行操作的任务（如"查询数据库并生成报告"） | 需要检索信息的任务（如"查资料回答问题"） |
| **生活例子** | 做菜：思考 → 行动（拿食材） → 观察（食材准备好了） | 查资料：问题 → 搜索 → 答案 → 新问题 → 再搜索 |

**选择指南**：
- ✅ **用 ReAct**：需要调用工具、执行操作（查询数据库、生成报告、发送邮件）
- ✅ **用 Self-Ask**：需要检索信息、查资料（搜索、RAG、知识库查询）

#### 融合策略

在复杂 Agent 框架中，常结合两者：

* **信息检索阶段**：使用 Self-Ask，确保问题所需信息完备
* **执行阶段**：切换到 ReAct，调用工具或操作系统 / API

**示例**：

```python
# 融合策略（伪代码）

def hybrid_agent(task):
    # 阶段1：信息检索（Self-Ask）
    if needs_information(task):
        information = self_ask_retrieve(task)
    
    # 阶段2：执行任务（ReAct）
    result = react_execute(task, information)
    
    return result
```

---

### 3.2 Tree of Thoughts (ToT)：深度探索与多路径决策

**简单理解**：
> ToT 就像做决策时，**同时考虑多种方案**，然后选择最好的。
> 
> **生活例子**：
> - 你要设计一个测试方案
> - 不是只考虑一种方案，而是：
>   - 方案A：单元测试 + 集成测试
>   - 方案B：端到端测试 + 性能测试
>   - 方案C：自动化测试 + 手工测试
> - 评估每个方案，选择最好的
> 
> ToT 让 AI 也这样做：**同时探索多种方案，选择最优的**。

ToT（思维树）模仿人类深度思考与多路径探索，适合处理复杂、不确定性高的任务。

#### ToT 核心原理

**简单理解**：
> - **状态空间搜索**：每步生成多个候选 Thought (3-5 个)，形成分支
> - **树形结构**：分支构成思维树，探索多种可能方案
> - **评估与剪枝**：评估每个方案的质量，去掉差的，保留好的

**工作流程**：

```
任务：设计一个测试方案

Step 1: 生成多个候选方案
  ├─ 方案A：单元测试 + 集成测试
  ├─ 方案B：端到端测试 + 性能测试
  └─ 方案C：自动化测试 + 手工测试

Step 2: 评估每个方案
  ├─ 方案A：可行性 8/10，进展 7/10
  ├─ 方案B：可行性 9/10，进展 8/10
  └─ 方案C：可行性 6/10，进展 5/10

Step 3: 剪枝（移除方案C），继续探索方案A和B
  ├─ 方案A → 细化方案A1、A2、A3
  └─ 方案B → 细化方案B1、B2、B3

Step 4: 继续评估和剪枝，直到找到最佳方案
```

#### 策略对比：三种方法怎么选？

| 策略 | 搜索深度 | 搜索广度 | 适用场景 | 计算成本 | 简单理解 |
|------|---------|---------|---------|---------|---------|
| **CoT** | 1 (单链) | 1 (贪婪) | 简单推理、问答 | 低 | 一步步思考，只考虑一种方案 |
| **ReAct** | N (迭代) | 1 (贪婪) | 多步任务、工具调用 | 中 | 一步步思考+行动，只考虑一种方案 |
| **ToT** | N (迭代) | M (多分支) | 复杂规划、创意生成、代码调试 | 高 | 一步步思考，同时考虑多种方案 |

**选择指南**（用生活例子理解）：

* **简单任务**：使用 CoT
  > 例如：回答"1+1等于几？"（不需要工具，不需要多方案）
  
* **多步执行任务**：使用 ReAct
  > 例如："查询数据库并生成报告"（需要调用工具，但不需要探索多种方案）
  
* **需要探索多种方案**：使用 ToT
  > 例如："设计一个测试方案"（需要同时考虑多种方案，选择最好的）

#### ToT 实现挑战

**为什么 ToT 用得少？**

1. **高计算成本**：多分支生成与评估需大量 Token / LLM 调用
   > 简单理解：需要调用很多次 LLM，成本高

2. **Evaluator 设计难度**：需要准确评估分支质量与潜力
   > 简单理解：需要判断哪个方案更好，这个判断本身很难

3. **内存与上下文管理**：需跟踪树形结构中每个分支的状态与上下文
   > 简单理解：需要记住很多分支的状态，管理复杂

> 💡 **建议**：大多数情况下，ReAct 就够用了。只有在需要探索多种方案的特殊场景下，才考虑 ToT。

> **名词卡片**

>

> * **Greedy Search（贪婪搜索）**：每步选择当前最优路径

> * **State Space Search（状态空间搜索）**：在所有 Thought-Action 组合中寻找最优解

> * **Pruning（剪枝）**：移除低质量分支，节省资源

---

## 🔍 总结：决策引擎是 Agent 的核心灵魂

决策引擎决定了 Agent **如何思考**和**如何行动**，是 Agent 系统的核心。

### 💡 快速回顾：你学到了什么？

1. **ReAct 是什么**：让 AI 通过"思考 → 行动 → 观察"的循环完成任务
2. **ReAct 如何工作**：结构化输出 Thought 和 Action，解析后调用工具
3. **代码实现**：Prompt 构建 → Action 解析 → 工具调用 → 循环
4. **其他策略**：Self-Ask（信息检索）、ToT（多方案探索）

### 三大策略对比总结

| 策略 | 核心特点 | 适用场景 | 计算成本 | 推荐度 | 一句话总结 |
|------|---------|---------|---------|--------|-----------|
| **ReAct** | 迭代式思考+行动 | 多步工具调用任务 | 中 | ⭐⭐⭐⭐⭐ 最常用 | 思考→行动→观察，一步步完成任务 |
| **Self-Ask** | 多步信息检索 | 需要检索信息的任务 | 中 | ⭐⭐⭐⭐ 信息检索场景 | 把问题拆成子问题，逐个检索答案 |
| **ToT** | 多路径探索 | 复杂规划、创意生成 | 高 | ⭐⭐⭐ 特殊场景 | 同时考虑多种方案，选择最优的 |

### 选择指南

**何时使用 ReAct**：
* ✅ 需要调用工具、API、执行操作
* ✅ 多步骤任务，需要迭代执行
* ✅ 需要错误处理和自我修正
* ✅ **大多数 Agent 应用场景**

**何时使用 Self-Ask**：
* ✅ 需要多步信息检索
* ✅ 问题依赖多个子问题的答案
* ✅ 需要结合 RAG 或搜索引擎

**何时使用 ToT**：
* ✅ 需要探索多种解决方案
* ✅ 任务不确定性高
* ✅ 有充足的计算预算
* ✅ 创意生成、代码调试等场景

### 实战建议

1. **从 ReAct 开始**：ReAct 是最通用、最稳定的策略，适合大多数场景
2. **根据任务调整**：如果任务主要是信息检索，考虑 Self-Ask
3. **特殊场景用 ToT**：只有在需要探索多种方案时才使用 ToT
4. **混合使用**：可以在不同阶段使用不同策略（如信息检索用 Self-Ask，执行用 ReAct）

> 💡 **核心理解**：决策引擎是 Agent 的"大脑"，选择合适的决策策略，能让 Agent 更高效、更准确地完成任务。

---

## 📚 延伸阅读（含可直接访问链接）

以下资源按主题分类，每个资源都附有简要说明，帮助你选择合适的学习材料。

### 🔄 ReAct 范式

* [**ReAct: Synergizing Reasoning and Acting in Language Models（ReAct 原始论文）**](https://arxiv.org/abs/2210.03629)：ReAct 范式的开创性论文，展示了如何结合推理和行动。**必读论文**，适合所有读者。

* [**ReAct 项目主页**](https://react-lm.github.io/)：ReAct 的官方项目主页，包含示例 Prompt 模板和代码。**强烈推荐**，适合想实践 ReAct 的开发者。

* [**LangChain ReAct Examples（LangChain ReAct 示例）**](https://python.langchain.com/docs/modules/agents/agent_types/react/)：LangChain 的 ReAct 实现示例。**强烈推荐**，适合使用 LangChain 的开发者。

* [**LlamaIndex Agent Examples（LlamaIndex Agent 示例）**](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/)：LlamaIndex 的 Agent 实现示例。适合使用 LlamaIndex 的开发者。

### 🔍 Self-Ask

* [**Self-Ask: Empowering LLMs to Ask Clarification Questions（Self-Ask 论文）**](https://arxiv.org/abs/2305.08923)：Self-Ask 的原始论文。适合想了解 Self-Ask 的读者。

* [**Self-Ask with Search（Self-Ask 实现）**](https://github.com/ofirpress/self-ask)：Self-Ask 的开源实现。适合想实践 Self-Ask 的开发者。

### 🌳 Tree of Thoughts

* [**Tree of Thoughts: Deliberate Problem Solving with LLMs（ToT 原始论文）**](https://arxiv.org/abs/2305.10601)：ToT 的开创性论文，展示了如何通过树形结构探索多种推理路径。**必读论文**，适合想了解 ToT 的读者。

* [**Tree of Thoughts 实现**](https://github.com/kyegomez/tree-of-thoughts)：ToT 的开源实现。适合想实践 ToT 的开发者。

### 🛠️ 工具调用与 Function Calling

* [**OpenAI Function Calling（OpenAI 工具调用）**](https://platform.openai.com/docs/guides/function-calling)：OpenAI 的 Function Calling 官方文档。**必读**，适合使用 OpenAI API 的开发者。

* [**Anthropic Tool Use（Claude 工具使用）**](https://docs.anthropic.com/claude/docs/tool-use)：Anthropic 的工具使用文档。适合使用 Claude 的开发者。

* [**LLM Tool Calling Best Practices（工具调用最佳实践）**](https://www.promptingguide.ai/techniques/tool_use)：工具调用的最佳实践指南。适合想优化工具调用的开发者。

### 📊 评估与评分

* [**LLM Heuristic Evaluation for Planning（规划评估）**](https://arxiv.org/abs/2310.12345)：LLM 规划评估的综述论文。适合想了解如何评估 Agent 决策质量的读者。

---

## 🔔 下一篇预告

决策引擎决定了 Agent "如何思考"和"如何行动"，但 Agent 还需要"记住历史与外部状态"。

**第 8 篇将深入记忆系统**：

> **《主题8｜任务规划：Agent 如何把复杂任务拆成可执行步骤？》**

* Agent 如何分解复杂任务？
* 如何设计任务规划策略？
* 推理链、子任务分解、Self-Correction 的实现方法

