---
title: 一个 Agent 不够用？多 Agent 协作像团队一样干活
date: 2025-12-23 18:00:00
updated: {{current_date_time}}
categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - AI与研究
tags:
  - LLM
  - Agent
  - Multi-Agent
  - Collaboration
  - 多 Agent
  - 协作
keywords: LLM, Agent, Multi-Agent, Collaboration, 多 Agent, 协作, 角色设定, 消息流
description: '深入解析多 Agent 协作：从角色设定、协作协议到消息流，掌握如何让多个 Agent 像团队一样协作完成复杂任务'
top_img: /img/llm-agent-multi-agent-collaboration.png
cover: /img/llm-agent-multi-agent-collaboration.png
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

查数据的、做分析的、写报告的——**一个 Agent 干不完，多个 Agent 怎么配合？**

多 Agent 协作通过角色设定、协作协议、消息流，让多个 Agent 像团队一样分工协作。本篇解析如何设计角色、话术、通信协议，构建可扩展的多 Agent 系统。

**多 Agent 协作** = 角色分工（各司其职）+ 协作协议（怎么配合）+ 消息流（怎么通信）。单 Agent 能力有限、复杂任务需专业分工、并行可提效——像团队一样干活。

---

## 👥 一、角色设定（Role Assignment）

订单处理流水线：查库存的、算优惠的、发通知的——**一个 Agent 全包会乱，拆成多个各司其职**。为每个 Agent 分配明确角色：专业化（专注一域）、互补性（覆盖所需技能）、清晰性（避免职责重叠）。

### 1.1 角色设计原则

**原则1：专业化**
> 每个 Agent 专注于一个领域，成为该领域的专家。

**原则2：互补性**
> Agent 之间要互补，覆盖所有需要的技能。

**原则3：清晰性**
> 角色定义要清晰，避免职责重叠。

**代码示例**：

```python
# 角色设定（伪代码）

class AgentRole:
    def __init__(self, name, description, capabilities, tools):
        self.name = name
        self.description = description
        self.capabilities = capabilities
        self.tools = tools

# 定义角色
roles = {
    "data_analyst": AgentRole(
        name="数据分析师",
        description="负责数据查询和分析",
        capabilities=["数据查询", "数据分析", "数据可视化"],
        tools=["query_database", "analyze_data", "visualize_data"]
    ),
    "report_writer": AgentRole(
        name="报告撰写员",
        description="负责报告撰写和格式化",
        capabilities=["报告撰写", "格式美化", "内容审核"],
        tools=["generate_report", "format_report", "review_report"]
    ),
    "project_manager": AgentRole(
        name="项目经理",
        description="负责任务规划和协调",
        capabilities=["任务规划", "进度管理", "团队协调"],
        tools=["plan_tasks", "track_progress", "coordinate_team"]
    )
}
```

### 1.2 角色协作模式

**模式1：流水线模式**
> Agent 按顺序工作，前一个 Agent 的输出是后一个 Agent 的输入。

**模式2：并行模式**
> 多个 Agent 并行工作，最后汇总结果。

**模式3：层次模式**
> 有主 Agent 和子 Agent，主 Agent 协调子 Agent。

---

## 💬 二、消息流（Message Flow）

消息流管理 Agent 之间的通信，确保信息正确传递。

### 2.1 消息格式

**代码示例**：

```python
# 消息格式（伪代码）

class Message:
    def __init__(self, sender, receiver, content, message_type):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.message_type = message_type
        self.timestamp = datetime.now()

# 消息类型
MESSAGE_TYPES = {
    "REQUEST": "请求",
    "RESPONSE": "响应",
    "NOTIFICATION": "通知",
    "ERROR": "错误"
}
```

### 2.2 消息路由

**代码示例**：

```python
# 消息路由（伪代码）

class MessageRouter:
    def __init__(self):
        self.agents = {}
        self.message_queue = []
    
    def register_agent(self, agent_id, agent):
        """注册 Agent"""
        self.agents[agent_id] = agent
    
    def send_message(self, message):
        """发送消息"""
        if message.receiver in self.agents:
            self.agents[message.receiver].receive_message(message)
        else:
            # 消息路由失败
            self.handle_routing_error(message)
```

---

## 🔄 三、协作协议（Collaboration Protocol）

协作协议定义 Agent 之间的协作规则，确保协作有序进行。

### 3.1 协议设计

**代码示例**：

```python
# 协作协议（伪代码）

class CollaborationProtocol:
    def __init__(self):
        self.rules = []
    
    def add_rule(self, condition, action):
        """添加规则"""
        self.rules.append({
            "condition": condition,
            "action": action
        })
    
    def execute(self, context):
        """执行协议"""
        for rule in self.rules:
            if rule["condition"](context):
                rule["action"](context)
```

---

## 🔍 总结：多 Agent 协作提升任务处理能力

### 💡 快速回顾：你学到了什么？

1. **角色设定**：为每个 Agent 分配明确的角色和职责
2. **消息流**：管理 Agent 之间的通信
3. **协作协议**：定义 Agent 之间的协作规则
4. **工程实践**：如何实现多 Agent 协作系统

### 多 Agent 协作的核心组件

| 组件 | 作用 | 简单理解 |
|------|------|---------|
| **角色设定** | 分配角色和职责 | 就像团队分工 |
| **消息流** | 管理通信 | 就像团队开会 |
| **协作协议** | 定义协作规则 | 就像团队规范 |

**生活化理解**：
> 就像团队协作：
> - **角色设定**：项目经理、开发工程师、测试工程师，各司其职
> - **消息流**：通过会议、邮件、即时消息沟通
> - **协作协议**：定义工作流程、沟通规范、决策机制

### 协作模式总结

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **流水线模式** | Agent 按顺序工作 | 任务有明确顺序 |
| **并行模式** | 多个 Agent 并行工作 | 任务可以并行 |
| **层次模式** | 主 Agent 协调子 Agent | 复杂任务需要协调 |

### 实战建议与检查清单

1. **从简单开始**：先实现两个 Agent 的协作，再逐步扩展
2. **明确角色**：每个 Agent 的角色要明确，避免职责重叠
3. **设计协议**：定义清晰的协作协议，确保协作有序
4. **监控协作**：监控 Agent 之间的通信，及时发现问题

**上线前检查**：消息格式是否统一？是否有死锁/循环依赖检测？主 Agent 是否有超时与降级策略？

> 💡 **核心理解**：
> 多 Agent 协作让多个 Agent 能够像团队一样工作，通过分工协作完成复杂任务，提升任务处理能力和效率。
> 
> 就像团队协作一样，好的多 Agent 协作能让 Agent 系统更强大、更高效，能够处理单个 Agent 无法完成的复杂任务。

---

## 📚 延伸阅读

* [**Multi-Agent Systems（多 Agent 系统）**](https://en.wikipedia.org/wiki/Multi-agent_system)：多 Agent 系统的维基百科
* [**CrewAI（多 Agent 框架）**](https://www.crewai.com/)：CrewAI 多 Agent 协作框架

---

## 🔔 系列说明

> 本文是[《🧠 LLM/Agent 从入门到精通：告别浅尝辄止》](/categories/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/)系列第 14 篇。上一篇：[Agent 失控了怎么办？日志、审计与可观测性](/2025-12-22-llm-agent-security-governance/)。下一篇：[Agent 好不好怎么衡量？评估指标体系与避坑指南](/2025-12-24-llm-agent-evaluation/)。

