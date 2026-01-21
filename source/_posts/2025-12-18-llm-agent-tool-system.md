---
title: 🛠️ 主题9｜Agent 工具系统：Function Calling 与外部世界连接
date: 2025-12-18 18:00:00
updated: {{current_date_time}}

categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - AI与研究
tags:
  - LLM
  - Agent
  - Function Calling
  - Tools
  - 工具系统
  - Executor
keywords: LLM, Agent, Function Calling, Tools, 工具系统, Tool Schema, Executor, 工具封装, 权限治理
description: '深入解析 Agent 工具系统：从 Function Calling 机制、工具封装规范化设计到安全权限治理，让 Agent 拥有连接外部世界的能力'
top_img: /img/llm-agent-tool-system.png
cover: /img/llm-agent-tool-system.png
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

> **这是[《🧠 LLM/Agent 从入门到精通：告别浅尝辄止》](/categories/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/)系列第 9 篇**

> 上一篇我们深入解析了 Agent 的记忆管理，探讨了如何突破 Context Window 限制，实现长期且连贯的记忆系统。

> 本篇，我们将聚焦 Agent 的工具系统，解析 Function Calling 机制与工具标准化设计，让 Agent 拥有连接外部世界的能力。

---

## 🚀 导言 — 让 Agent 拥有"手脚"

在[第8篇](/技术学习与行业趋势/AI与研究/2025-12-17-llm-agent-memory-management/)中，我们掌握了 Agent 如何记住历史信息。在[第7篇](/技术学习与行业趋势/AI与研究/2025-12-16-llm-agent-decision-engine/)中，我们了解了 Agent 如何思考和决策。

但 Agent 还有一个关键问题：
> **Agent 如何执行实际操作？**  
> **如何让 Agent 调用外部工具？**  
> **如何安全地让 Agent 连接外部世界？**

Agent 的核心是 **ReAct 循环**，其中 **Action（行动）**环节必须依赖外部工具才能执行。工具是 Agent 与现实世界的唯一通道，赋予它搜索、计算、操作数据库、发送邮件等实际能力。

### 🤔 先理解几个基础概念

**1. Function Calling（函数调用）**
> 简单理解：让 LLM 能够调用外部函数（工具），就像人使用工具一样。
> 
> 例如：
> - LLM 想查询数据库，不能直接查
> - 但可以调用 `query_database()` 函数
> - Function Calling 就是让 LLM 能够"告诉程序"调用哪个函数

**2. Tool Schema（工具模式）**
> 简单理解：工具的"说明书"，告诉 LLM 有哪些工具可用，每个工具做什么，需要什么参数。
> 
> 例如：
> - 工具名：`query_database`
> - 功能：查询数据库
> - 参数：`sql`（SQL 查询语句）

**3. Executor（执行器）**
> 简单理解：实际执行工具调用的"工人"，负责解析 LLM 的输出，调用真实的函数。
> 
> 例如：
> - LLM 输出：`{"function": "query_database", "arguments": {"sql": "SELECT * FROM users"}}`
> - Executor 解析后，调用真实的 `query_database()` 函数

### 💡 为什么需要工具系统？

**问题1：LLM 无法直接操作外部系统**
> LLM 只能"说"，不能"做"。它无法查询数据库、调用 API、发送邮件。

**问题2：LLM 输出不稳定**
> LLM 输出的是文本，程序难以解析和执行。

**问题3：安全性问题**
> 如果让 LLM 直接执行代码，会有安全风险。

**解决方案：Function Calling**
> - LLM 输出结构化的 JSON（函数调用指令）
> - Executor 解析 JSON，调用真实函数
> - 安全可控，易于管理

### 📋 本篇学习目标

本篇将从**简单到复杂**，帮你掌握：
1. **Function Calling 机制**：LLM 如何调用外部工具？
2. **工具封装设计**：如何设计好的工具？
3. **工具系统安全**：如何确保工具调用的安全性？
4. **工程实践**：如何实现完整的工具系统？

> 💡 **提示**：工具系统是 Agent 连接外部世界的桥梁，理解它有助于设计更强大的 Agent。

---

## 一、Function Calling 的机制本质

Function Calling 是 LLM 提供的一种高级能力，将自由文本输出转化为 **结构化函数调用对象**，使 LLM 能够安全、可控地调用外部工具。

### 1.1 核心流程：Schema → JSON → 执行

1. **Tool Schema 注入（定义）**

   * 开发者将可用工具规范描述注入 LLM（通常为 JSON Schema）

   * 包含工具名、功能描述、参数及类型

2. **LLM 推理（决策）**

   * LLM 接收到用户指令和工具 Schema

   * 在 ReAct 循环中判断是否调用工具

   * 生成符合 Schema 的 **Action Call JSON 对象**

3. **Executor 执行（行动）**

   * 解析 JSON，调用真实函数

   * 执行结果返回给 LLM 作为 **Observation**

### 1.2 Function Calling 的优势

* **高稳定性：** 模型底层优化输出 JSON，解析成功率高

* **减少歧义：** LLM 仅可选择预定义工具，参数明确

* **安全性：** LLM 输出的是 JSON，而非直接代码，确保执行环境受控

> **💡 名词卡片**
> * **Tool Schema：** 使用 JSON Schema 定义的工具蓝图
> * **Function Calling：** 结构化 JSON 输出，指示函数调用
> * **Executor：** 解析 JSON 并实际执行工具的模块

---

## 🛠️ 二、工具封装与规范化设计

并非所有代码都适合作为 Agent 工具。优质工具必须遵循 **原子性（Atomicity）** 与 **可理解性（Descriptiveness）** 原则。

**简单理解**：
> 就像设计 API：
> - **原子性**：一个工具只做一件事（就像 RESTful API 的设计原则）
> - **可理解性**：工具的描述要清晰，让 LLM 知道什么时候用它

### 2.1 工具封装核心原则

#### 1. 原子性（Atomicity）

**简单理解**：
> 一个工具只做一件事，不要把所有功能都塞到一个工具里。

**生活例子**：
> - ❌ **错误**：一个工具既能"处理数据"又能"发送邮件"
> - ✅ **正确**：`AnalyzeData()` 和 `SendEmail()` 分开

**代码示例**：

```python
# ❌ 错误：违反原子性原则

def process_data_and_send_email(data, recipient):
    """处理数据并发送邮件"""
    # 处理数据
    processed_data = analyze_data(data)
    
    # 发送邮件
    send_email(recipient, processed_data)
    
    return "完成"

# ✅ 正确：拆分成两个原子工具

def analyze_data(data):
    """分析数据"""
    # 只做数据分析
    result = perform_analysis(data)
    return result

def send_email(recipient, content):
    """发送邮件"""
    # 只做发送邮件
    result = email_service.send(recipient, content)
    return result
```

**为什么需要原子性？**
> - **可复用性**：工具可以独立使用
> - **可组合性**：多个工具可以组合完成复杂任务
> - **可测试性**：每个工具可以独立测试
> - **可理解性**：LLM 更容易理解每个工具的用途

#### 2. 描述性（Descriptiveness）

**简单理解**：
> 工具的描述要清晰、详细，让 LLM 知道什么时候用它。

**生活例子**：
> - ❌ **错误**：`tool_1: Search DB`（太简单，不知道什么时候用）
> - ✅ **正确**：`tool_1: 专业数据库查询工具，用于检索公司最新销售数据，参数必须包含时间范围和产品名称`（清晰明确）

**代码示例**：

```python
# ❌ 错误：描述不够清晰

tool_schema = {
    "name": "search_db",
    "description": "Search database",  # 太简单
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        }
    }
}

# ✅ 正确：描述清晰详细

tool_schema = {
    "name": "query_sales_database",
    "description": """
    专业数据库查询工具，用于检索公司最新销售数据。
    
    使用场景：
    - 需要查询销售数据时
    - 需要分析销售趋势时
    
    参数要求：
    - date_range: 时间范围（必填），格式：YYYY-MM-DD 到 YYYY-MM-DD
    - product_name: 产品名称（可选），如果不提供则查询所有产品
    
    返回格式：
    - JSON 格式，包含销售数据列表
    """,
    "parameters": {
        "type": "object",
        "properties": {
            "date_range": {
                "type": "string",
                "description": "时间范围，格式：YYYY-MM-DD 到 YYYY-MM-DD"
            },
            "product_name": {
                "type": "string",
                "description": "产品名称（可选）"
            }
        },
        "required": ["date_range"]
    }
}
```

**描述性检查清单**：
> - ✅ 工具做什么？（功能）
> - ✅ 什么时候用？（使用场景）
> - ✅ 需要什么参数？（参数说明）
> - ✅ 返回什么？（返回格式）

#### 3. 明确的输入/输出

**简单理解**：
> 工具的输入和输出要明确，最好是结构化的数据。

**代码示例**：

```python
# ❌ 错误：输出不明确

def query_database(sql):
    """查询数据库"""
    # 返回冗长的日志
    return """
    [2025-12-18 10:00:00] 开始查询数据库
    [2025-12-18 10:00:01] 连接数据库成功
    [2025-12-18 10:00:02] 执行 SQL: SELECT * FROM users
    [2025-12-18 10:00:03] 查询成功，返回 1000 条记录
    [2025-12-18 10:00:04] 关闭数据库连接
    """

# ✅ 正确：输出结构化

def query_database(sql):
    """查询数据库"""
    # 执行查询
    results = db.execute(sql)
    
    # 返回结构化数据
    return {
        "success": True,
        "count": len(results),
        "data": results,
        "message": "查询成功"
    }
```

**输出格式建议**：
> - ✅ **JSON 格式**：结构化，易于解析
> - ✅ **简洁文本**：如果必须返回文本，要简洁明了
> - ❌ **冗长日志**：避免返回调试日志
> - ❌ **非结构化**：避免返回难以解析的数据

### 2.2 工具设计最佳实践

**设计检查清单**：

| 原则 | 检查项 | 示例 |
|------|--------|------|
| **原子性** | 一个工具只做一件事 | ✅ `query_database()` 只查询数据库<br>❌ `process_and_send()` 既处理又发送 |
| **描述性** | 描述清晰、详细 | ✅ "专业数据库查询工具，用于..."<br>❌ "Search DB" |
| **输入/输出** | 输入明确，输出结构化 | ✅ JSON 格式返回<br>❌ 返回冗长日志 |
| **错误处理** | 有明确的错误处理 | ✅ 返回 `{"success": False, "error": "..."}`<br>❌ 抛出异常但不处理 |
| **可测试性** | 工具可以独立测试 | ✅ 有单元测试<br>❌ 依赖外部状态 |

### 2.3 工具与 RAG 的集成

**简单理解**：
> RAG 也可以作为一个工具，让 Agent 在需要时检索知识。

**机制**：
> - **RAG 作为工具**：`RetrieveKnowledge(query)`
> - **功能**：调用向量数据库，返回最相关的 Top K 记忆片段
> - **Agent 使用场景**：当 LLM 缺乏事实信息时执行 Action，补充 Context

**代码示例**：

```python
# RAG 作为工具（伪代码）

def retrieve_knowledge(query, top_k=5):
    """
    RAG 检索工具：从知识库检索相关信息
    
    参数：
    - query: 查询文本
    - top_k: 返回最相关的 K 条结果
    
    返回：
    - 最相关的知识片段列表
    """
    # 1. 生成查询向量
    query_vector = embedding_model.embed(query)
    
    # 2. 从向量数据库检索
    results = vector_db.similarity_search(query_vector, top_k=top_k)
    
    # 3. 返回结构化结果
    return {
        "success": True,
        "count": len(results),
        "knowledge": [
            {
                "text": r["text"],
                "score": r["similarity_score"],
                "source": r["metadata"]["source"]
            }
            for r in results
        ]
    }

# 在 Agent 中使用
tools = {
    "query_database": query_database,
    "retrieve_knowledge": retrieve_knowledge,  # RAG 作为工具
    "send_email": send_email
}

# Agent 可以根据需要调用 RAG 工具检索知识
```

**使用场景**：
> - Agent 需要事实信息时，调用 `retrieve_knowledge()` 检索知识
> - 检索到的知识作为 Context 注入到 LLM Prompt 中
> - Agent 基于检索到的知识进行推理和决策

---

## 🔒 三、工具系统的安全与权限治理

Agent 可以执行数据库写入、文件操作等实际行为，安全治理是落地生产的最高优先级。

**简单理解**：
> 就像给员工分配权限：
> - **最小权限原则**：只给必要的权限
> - **权限隔离**：不同员工有不同的权限
> - **高风险操作审批**：重要操作需要审批

### 3.1 权限分级与最小权限原则

**简单理解**：
> **最小权限原则**：Agent 只拥有完成任务所需的最小权限，不要给太多权限。

**生活例子**：
> - ❌ **错误**：给所有 Agent 所有权限（包括删除数据库）
> - ✅ **正确**：查询 Agent 只能查询，不能删除；管理 Agent 才能删除

**权限分级示例**：

```python
# 权限分级（伪代码）

class PermissionLevel:
    READ_ONLY = "read_only"      # 只读权限
    READ_WRITE = "read_write"    # 读写权限
    ADMIN = "admin"              # 管理员权限

# Agent 权限配置
agent_permissions = {
    "query_agent": {
        "level": PermissionLevel.READ_ONLY,
        "allowed_tools": ["query_database", "retrieve_knowledge"]
    },
    "admin_agent": {
        "level": PermissionLevel.ADMIN,
        "allowed_tools": ["query_database", "delete_database", "send_email"]
    }
}
```

**最小权限原则**：
> - Agent 仅拥有完成任务所需权限
> - 不要给不必要的权限
> - 定期审查权限，及时回收不需要的权限

**权限隔离**：
> - 不同 Agent 实例使用不同 API Key
> - 工具集互相隔离
> - 避免权限泄露

### 3.2 沙箱机制与风险隔离

**简单理解**：
> **沙箱**：就像"隔离房间"，在隔离环境中运行代码，即使出错也不会影响主系统。

**生活例子**：
> - 就像在实验室做实验，即使爆炸也不会影响外面

**沙箱机制**：

```python
# 沙箱机制（伪代码）

class SandboxExecutor:
    def __init__(self):
        self.docker_client = DockerClient()  # Docker 客户端
    
    def execute_in_sandbox(self, tool_name, args, code):
        """在沙箱中执行代码"""
        # 1. 创建隔离容器
        container = self.docker_client.create_container(
            image="python:3.9",
            command=["python", "-c", code],
            network_disabled=True,  # 禁用网络
            read_only=True,         # 只读文件系统
            mem_limit="512m"        # 内存限制
        )
        
        # 2. 启动容器
        container.start()
        
        # 3. 等待执行完成
        container.wait()
        
        # 4. 获取结果
        logs = container.logs()
        
        # 5. 删除容器
        container.remove()
        
        return logs
```

**高风险操作审批**：
> 关键操作如数据库写入需 **Human-in-the-Loop** 审批

**代码示例**：

```python
# 高风险操作审批（伪代码）

class SecureExecutor:
    def __init__(self, approval_service):
        self.approval_service = approval_service
        self.high_risk_tools = ["delete_database", "drop_table", "send_email"]
    
    def execute(self, tool_name, args, agent_id):
        """执行工具，高风险操作需要审批"""
        # 1. 检查是否是高风险操作
        if tool_name in self.high_risk_tools:
            # 2. 需要人工审批
            approval = self.approval_service.request_approval(
                agent_id=agent_id,
                tool_name=tool_name,
                args=args
            )
            
            if not approval.approved:
                return {
                    "success": False,
                    "error": "操作未获得审批"
                }
        
        # 3. 执行工具
        return self._execute_tool(tool_name, args)
```

### 3.3 完整的安全校验流程

**代码示例**：

```python
# 完整的安全校验（伪代码）

class SecureExecutor:
    def __init__(self, permission_manager, sandbox, approval_service):
        self.permission_manager = permission_manager
        self.sandbox = sandbox
        self.approval_service = approval_service
    
    def execute_tool(self, tool_name, args, agent_id):
        """执行工具，包含完整的安全校验"""
        
        # 1. 权限检查
        if not self.permission_manager.has_permission(agent_id, tool_name):
            raise PermissionError(f"Agent {agent_id} 没有权限调用 {tool_name}")
        
        # 2. 参数清理（防止注入攻击）
        sanitized_args = self.sanitize_args(args)
        
        # 3. 高风险操作审批
        if self.is_high_risk_tool(tool_name):
            approval = self.approval_service.request_approval(
                agent_id=agent_id,
                tool_name=tool_name,
                args=sanitized_args
            )
            if not approval.approved:
                return {
                    "success": False,
                    "error": "操作未获得审批"
                }
        
        # 4. 在沙箱中执行（如果是代码执行工具）
        if self.is_code_execution_tool(tool_name):
            result = self.sandbox.execute(tool_name, sanitized_args)
        else:
            # 5. 直接执行（如果是 API 调用）
            result = self._execute_tool(tool_name, sanitized_args)
        
        # 6. 记录日志
        self.log_execution(agent_id, tool_name, sanitized_args, result)
        
        return result
    
    def sanitize_args(self, args):
        """清理参数，防止注入攻击"""
        sanitized = {}
        for key, value in args.items():
            # 移除危险字符
            if isinstance(value, str):
                sanitized[key] = value.replace(";", "").replace("--", "")
            else:
                sanitized[key] = value
        return sanitized
    
    def is_high_risk_tool(self, tool_name):
        """判断是否是高风险工具"""
        high_risk_tools = ["delete_database", "drop_table", "send_email", "execute_code"]
        return tool_name in high_risk_tools
    
    def is_code_execution_tool(self, tool_name):
        """判断是否是代码执行工具"""
        code_tools = ["execute_python", "execute_sql", "execute_shell"]
        return tool_name in code_tools

# 使用示例
executor = SecureExecutor(
    permission_manager=PermissionManager(),
    sandbox=SandboxExecutor(),
    approval_service=ApprovalService()
)

result = executor.execute_tool(
    tool_name="query_database",
    args={"sql": "SELECT * FROM users"},
    agent_id="agent_123"
)
```

### 3.4 安全最佳实践

**安全检查清单**：

| 安全措施 | 说明 | 简单理解 |
|---------|------|---------|
| **权限分级** | 不同 Agent 有不同的权限 | 只给必要的权限 |
| **权限隔离** | 不同 Agent 使用不同的 API Key | 避免权限泄露 |
| **参数清理** | 清理用户输入，防止注入攻击 | 过滤危险字符 |
| **沙箱机制** | 在隔离环境中执行代码 | 即使出错也不影响主系统 |
| **高风险审批** | 重要操作需要人工审批 | 防止误操作 |
| **日志记录** | 记录所有操作日志 | 便于审计和追踪 |

> 💡 **关键理解**：
> - **最小权限原则**：只给必要的权限
> - **权限隔离**：不同 Agent 有不同的权限
> - **沙箱机制**：在隔离环境中执行代码
> - **高风险审批**：重要操作需要人工审批

---

## 🔍 总结：工具决定 Agent 的能力边界

### 💡 快速回顾：你学到了什么？

1. **Function Calling 机制**：LLM 如何调用外部工具（Schema → JSON → 执行）
2. **工具封装设计**：原子性、描述性、明确的输入/输出
3. **工具系统安全**：权限分级、沙箱机制、高风险审批
4. **工程实践**：如何实现完整的工具系统

### 工具系统的核心作用

| 组件 | 作用 | 简单理解 |
|------|------|---------|
| **Planner（大脑）** | 决定智能上限 | Agent 的思考能力 |
| **工具集（手脚）** | 决定能力边界与实用价值 | Agent 的执行能力 |

**关键理解**：
> - **Planner（大脑）** 决定智能上限
> - **工具集（手脚）** 决定能力边界与实用价值
> 
> 高效、安全的 Agent 系统依赖于 **Function Calling 机制 + 原子化工具 + 权限治理**，是 Agent 从"思考"到"改变世界"的关键一步。

### 设计原则总结

| 原则 | 说明 | 示例 |
|------|------|------|
| **原子性** | 一个工具只做一件事 | ✅ `query_database()`<br>❌ `process_and_send()` |
| **描述性** | 描述清晰、详细 | ✅ "专业数据库查询工具，用于..."<br>❌ "Search DB" |
| **安全性** | 权限控制、沙箱隔离 | ✅ 最小权限原则<br>❌ 给所有权限 |
| **可测试性** | 工具可以独立测试 | ✅ 有单元测试<br>❌ 依赖外部状态 |

### 实战建议

1. **从简单开始**：先实现基本的 Function Calling，再逐步优化
2. **遵循原子性**：一个工具只做一件事，不要把所有功能都塞到一个工具里
3. **重视安全性**：权限控制、参数清理、沙箱隔离，一个都不能少
4. **完善文档**：工具的描述要清晰详细，让 LLM 知道什么时候用它

> 💡 **核心理解**：
> 工具系统是 Agent 连接外部世界的桥梁，设计好的工具系统能让 Agent 更强大、更安全、更可靠。

---

## 📚 延伸阅读（含可直接访问链接）

以下资源按主题分类，每个资源都附有简要说明，帮助你选择合适的学习材料。

### 🔧 Function Calling

* [**OpenAI Function Calling 文档（OpenAI 函数调用官方文档）**](https://platform.openai.com/docs/guides/function-calling)：OpenAI Function Calling 的官方文档，包含详细的 API 说明和示例。**必读**，适合使用 OpenAI API 的开发者。

* [**Anthropic Tool Use（Claude 工具使用）**](https://docs.anthropic.com/claude/docs/tool-use)：Anthropic 的工具使用文档。适合使用 Claude 的开发者。

* [**LangChain Tools（LangChain 工具）**](https://python.langchain.com/docs/modules/tools/)：LangChain 的工具实现，包含丰富的工具示例。**强烈推荐**，适合使用 LangChain 的开发者。

### 🛠️ 工具设计原则

* [**Agent Tool Design Principles（Agent 工具设计原则）**](https://www.langchain.com/docs/modules/agents/toolkits/)：LangChain 的工具设计原则和最佳实践。适合想设计好工具的开发者。

* [**Tool Calling Best Practices（工具调用最佳实践）**](https://www.promptingguide.ai/techniques/tool_use)：工具调用的最佳实践指南。适合想优化工具调用的开发者。

### 🔒 Agent 安全

* [**LLM Agent Security & Sandboxing（LLM Agent 安全与沙箱）**](https://arxiv.org/abs/2305.17592)：LLM Agent 安全性的研究论文。适合想了解 Agent 安全性的读者。

* [**Agent Security Best Practices（Agent 安全最佳实践）**](https://www.langchain.com/docs/security/)：LangChain 的安全最佳实践。适合想确保 Agent 安全的开发者。

### 🔨 Executor 实现

* [**LangChain Executor 源码分析（LangChain 执行器源码）**](https://github.com/langchain-ai/langchain/tree/main/libs/langchain/langchain/agents)：LangChain Executor 的源码实现。适合想深入了解 Executor 实现的开发者。

* [**LlamaIndex Agent Executor（LlamaIndex Agent 执行器）**](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/)：LlamaIndex 的 Agent Executor 实现。适合使用 LlamaIndex 的开发者。

---

## 🔔 下一篇预告

工具系统让 Agent 能够连接外部世界，但 Agent 的行为需要监控和管理。

**第 10 篇将深入监控与治理**：

> **《主题10｜Agent 监控与治理：日志、可观测性与安全审计》**

* 如何监控 Agent 的行为？
* 如何记录和分析 Agent 的执行日志？
* 如何实现 Agent 的可观测性？
* Agent 安全审计的最佳实践

