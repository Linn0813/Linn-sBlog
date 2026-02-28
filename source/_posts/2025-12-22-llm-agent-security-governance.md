---
title: Agent 失控了怎么办？日志、审计与可观测性
date: 2025-12-22 18:00:00
updated: {{current_date_time}}
categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - AI与研究
tags:
  - LLM
  - Agent
  - Security
  - Governance
  - Logging
  - Observability
keywords: LLM, Agent, Security, Governance, Logging, Observability, 安全治理, 日志, 审计
description: '深入解析 Agent 安全治理：从日志记录、审计追踪到可观测性，掌握如何监控和管理 Agent 的行为，确保安全可控'
top_img: /img/llm-agent-security-governance.png
cover: /img/llm-agent-security-governance.png
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

Agent 调用了不该调用的接口、泄露了敏感信息、陷入无限循环——**出事了怎么查、怎么拦？**

安全治理通过日志、审计、可观测性，让 Agent 行为可追溯、可复盘、可拦截。本篇解析如何设计日志体系、审计追踪、监控告警，确保 Agent 安全可控。

**安全治理** = 日志（记操作）+ 审计（追行为）+ 可观测性（指标、日志、追踪）。Agent 行为难控、出问题难排查、有安全风险——三者结合让行为可追溯、可复盘、可拦截。

---

## 📝 一、日志记录（Logging）

金融 Agent 误调了转账接口——**没有日志，根本查不到是谁、何时、传了什么参数**。记录 Agent 的每一步：用户输入、Thought、工具调用、执行结果、错误。记录内容：
- **用户输入**：用户给 Agent 的指令
- **Agent 思考**：Agent 的思考过程（Thought）
- **工具调用**：Agent 调用了哪些工具
- **执行结果**：工具执行的结果
- **错误信息**：遇到的错误和异常

**代码示例**：

```python
# 日志记录（伪代码）

import logging
from datetime import datetime

class AgentLogger:
    def __init__(self, log_file="agent.log"):
        self.logger = logging.getLogger("Agent")
        self.logger.setLevel(logging.INFO)
        
        # 文件处理器
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        self.logger.addHandler(file_handler)
    
    def log_user_input(self, user_input, user_id):
        """记录用户输入"""
        self.logger.info(f"[USER_INPUT] User: {user_id}, Input: {user_input}")
    
    def log_thought(self, thought, agent_id):
        """记录 Agent 思考"""
        self.logger.info(f"[THOUGHT] Agent: {agent_id}, Thought: {thought}")
    
    def log_tool_call(self, tool_name, args, agent_id):
        """记录工具调用"""
        self.logger.info(
            f"[TOOL_CALL] Agent: {agent_id}, Tool: {tool_name}, Args: {args}"
        )
    
    def log_result(self, result, agent_id):
        """记录执行结果"""
        self.logger.info(f"[RESULT] Agent: {agent_id}, Result: {result}")
    
    def log_error(self, error, agent_id):
        """记录错误"""
        self.logger.error(f"[ERROR] Agent: {agent_id}, Error: {error}")

# 使用示例
logger = AgentLogger()

logger.log_user_input("查询用户数据", user_id="user_123")
logger.log_thought("我需要查询数据库", agent_id="agent_001")
logger.log_tool_call("query_database", {"sql": "SELECT * FROM users"}, "agent_001")
logger.log_result({"success": True, "count": 1000}, "agent_001")
```

### 1.2 结构化日志

用 JSON 等结构化格式记录，便于后续分析和检索。代码示例：

```python
# 结构化日志（伪代码）

import json
from datetime import datetime

class StructuredLogger:
    def log(self, event_type, data, agent_id=None, user_id=None):
        """记录结构化日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "agent_id": agent_id,
            "user_id": user_id,
            "data": data
        }
        
        # 输出 JSON 格式日志
        print(json.dumps(log_entry))

# 使用示例
logger = StructuredLogger()

logger.log(
    event_type="tool_call",
    data={"tool": "query_database", "args": {"sql": "SELECT * FROM users"}},
    agent_id="agent_001",
    user_id="user_123"
)
```

---

## 🔍 二、审计追踪（Audit Trail）

审计追踪记录 Agent 的完整行为历史，用于安全审计和问题排查。

### 2.1 审计追踪实现

记录 Agent 的完整行为链——谁、何时、做了什么、结果如何。代码示例：

```python
# 审计追踪（伪代码）

class AuditTrail:
    def __init__(self, db):
        self.db = db  # 数据库连接
    
    def record_action(self, agent_id, action_type, details, user_id=None):
        """记录操作"""
        audit_entry = {
            "agent_id": agent_id,
            "user_id": user_id,
            "action_type": action_type,
            "details": details,
            "timestamp": datetime.now(),
            "ip_address": self.get_client_ip(),
            "user_agent": self.get_user_agent()
        }
        
        # 保存到数据库
        self.db.audit_logs.insert(audit_entry)
    
    def query_audit_log(self, agent_id=None, start_time=None, end_time=None):
        """查询审计日志"""
        query = {}
        if agent_id:
            query["agent_id"] = agent_id
        if start_time:
            query["timestamp"] = {"$gte": start_time}
        if end_time:
            query["timestamp"]["$lte"] = end_time
        
        return self.db.audit_logs.find(query)
```

---

## 📊 三、可观测性（Observability）

可观测性包括指标、日志和追踪，帮助理解 Agent 的运行状态。

### 3.1 指标监控（Metrics）

监控成功率、响应时间、工具调用次数等——像健康检查。代码示例：

```python
# 指标监控（伪代码）

class MetricsCollector:
    def __init__(self):
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "tool_call_count": {}
        }
    
    def record_request(self, success, response_time):
        """记录请求"""
        self.metrics["total_requests"] += 1
        if success:
            self.metrics["successful_requests"] += 1
        else:
            self.metrics["failed_requests"] += 1
        
        # 更新平均响应时间
        total = self.metrics["total_requests"]
        current_avg = self.metrics["average_response_time"]
        self.metrics["average_response_time"] = (
            (current_avg * (total - 1) + response_time) / total
        )
    
    def record_tool_call(self, tool_name):
        """记录工具调用"""
        if tool_name not in self.metrics["tool_call_count"]:
            self.metrics["tool_call_count"][tool_name] = 0
        self.metrics["tool_call_count"][tool_name] += 1
    
    def get_metrics(self):
        """获取指标"""
        return self.metrics
```

---

## 🔒 四、安全审计（Security Audit）

安全审计检查 Agent 的安全合规性，识别潜在的安全风险。

### 4.1 安全审计检查

**代码示例**：

```python
# 安全审计（伪代码）

class SecurityAuditor:
    def audit(self, agent_id, time_range):
        """安全审计"""
        # 1. 获取审计日志
        logs = self.get_audit_logs(agent_id, time_range)
        
        # 2. 检查安全风险
        risks = []
        
        # 检查：是否有异常操作
        risks.extend(self.check_anomalous_operations(logs))
        
        # 检查：是否有权限滥用
        risks.extend(self.check_permission_abuse(logs))
        
        # 检查：是否有敏感操作
        risks.extend(self.check_sensitive_operations(logs))
        
        return {
            "agent_id": agent_id,
            "time_range": time_range,
            "risks": risks,
            "risk_level": self.calculate_risk_level(risks)
        }
```

---

## 🔍 总结：安全治理确保 Agent 可控可观测

### 💡 快速回顾：你学到了什么？

1. **日志记录**：记录 Agent 的所有操作
2. **审计追踪**：追踪 Agent 的行为历史
3. **可观测性**：监控 Agent 的运行状态
4. **安全审计**：检查 Agent 的安全合规性

### 安全治理的核心组件

| 组件 | 作用 | 简单理解 |
|------|------|---------|
| **日志记录** | 记录所有操作 | 就像"操作记录本" |
| **审计追踪** | 追踪行为历史 | 就像"行为档案" |
| **可观测性** | 监控运行状态 | 就像"健康检查" |
| **安全审计** | 检查安全合规性 | 就像"安全检查" |

**生活化理解**：
> 就像公司管理：
> - **日志记录**：记录员工的所有操作（如：谁在什么时候做了什么）
> - **审计追踪**：追踪员工的行为历史（如：查看某个员工的操作记录）
> - **可观测性**：监控系统运行状态（如：系统是否正常，性能如何）
> - **安全审计**：检查安全合规性（如：是否有异常操作，是否符合安全规范）

### 设计原则总结

| 原则 | 说明 | 示例 |
|------|------|------|
| **完整性** | 记录所有重要操作 | ✅ 记录所有工具调用<br>❌ 只记录部分操作 |
| **可追溯性** | 能够追溯操作历史 | ✅ 记录时间、用户、操作<br>❌ 只记录操作内容 |
| **实时性** | 实时监控和告警 | ✅ 实时监控，及时告警<br>❌ 事后分析 |
| **安全性** | 保护日志和审计数据 | ✅ 加密存储，权限控制<br>❌ 明文存储 |

### 实战建议与检查清单

1. **从基础开始**：先实现基本的日志记录，再逐步完善
2. **重视安全**：日志和审计数据要加密存储，权限控制
3. **实时监控**：实时监控 Agent 运行状态，及时发现问题
4. **定期审计**：定期进行安全审计，检查合规性

**上线前检查**：工具调用是否全量记录？敏感信息是否脱敏？是否有异常行为告警阈值？

> 💡 **核心理解**：
> 安全治理是 Agent 系统的重要组成部分，通过日志、审计、可观测性和安全审计，确保 Agent 的行为可控、可观测、可审计。
> 
> 就像企业治理一样，好的安全治理能让 Agent 系统更安全、更可靠，便于管理和维护。

---

## 📚 延伸阅读

* [**Agent Security Best Practices**](https://www.langchain.com/docs/security/)：Agent 安全最佳实践
* [**Observability for LLM Applications**](https://www.langchain.com/docs/observability/)：LLM 应用的可观测性

---

## 🔔 系列说明

> 本文是[《🧠 LLM/Agent 从入门到精通：告别浅尝辄止》](/categories/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/)系列第 13 篇。上一篇：[Agent 怎么查数据库、调 API？Function Calling 与工具封装](/2025-12-18-llm-agent-tool-system/)。下一篇：[一个 Agent 不够用？多 Agent 协作像团队一样干活](/2025-12-23-llm-agent-multi-agent-collaboration/)。

