---
title: 复杂任务 Agent 怎么拆？任务规划与 Self-Correction
date: 2025-12-19 18:00:00
updated: {{current_date_time}}
categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - AI与研究
tags:
  - LLM
  - Agent
  - Task Planning
  - 任务规划
  - 任务分解
  - Self-Correction
keywords: LLM, Agent, Task Planning, 任务规划, 任务分解, 子任务, Self-Correction, 推理链
description: '深入解析 Agent 任务规划：从任务分解、子任务生成到 Self-Correction，掌握如何让 Agent 把复杂任务拆成可执行步骤'
top_img: /img/llm-agent-task-planning.png
cover: /img/llm-agent-task-planning.png
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

"开发一个测试平台"——Agent 怎么拆？先设计数据库还是先写 API？某一步失败了怎么自动调整？

**任务规划**让 Agent 把大任务分解为可执行子任务，按序执行，出错时 Self-Correction。本篇解析任务分解、子任务生成、推理链与自我修正，掌握如何让 Agent 稳定完成复杂任务。

**任务规划** = 把大任务拆成可执行子任务 + 确定顺序 + 出错时 Self-Correction。就像做项目：先需求分析，再数据库设计，再开发——顺序错了会白干，某步失败要能重试或换策略。

---

## 🎯 一、任务分解策略

接到"自动处理电商退单"——先拆成查订单、验库存、退款项、发通知。拆到哪一层？**拆到每个子任务都能直接调用工具执行为止**。

### 1.1 基于目标的分解（Goal-Based Decomposition）

根据任务目标递归分解，直到每个子目标都可直接执行。方法：
> 1. 分析任务目标
> 2. 识别关键步骤
> 3. 对每个步骤继续分解（如果需要）
> 4. 直到所有步骤都可以直接执行

**代码示例**：

```python
# 基于目标的分解（伪代码）

def decompose_task(task_description):
    """分解任务"""
    # 1. 分析任务目标
    goal = analyze_goal(task_description)
    
    # 2. 识别关键步骤
    steps = identify_steps(goal)
    
    # 3. 递归分解（如果步骤太复杂）
    subtasks = []
    for step in steps:
        if is_complex(step):
            # 继续分解
            subtasks.extend(decompose_task(step))
        else:
            # 可以直接执行
            subtasks.append(step)
    
    return subtasks

# 使用示例
task = "开发一个测试平台"
subtasks = decompose_task(task)
# 输出：
# [
#   "需求分析：确定功能需求",
#   "数据库设计：设计用户表、测试用例表",
#   "后端开发：开发用户API、测试用例API",
#   "前端开发：开发登录页面、测试用例管理页面",
#   "测试：编写单元测试、集成测试"
# ]
```

### 1.2 基于工作流的分解（Workflow-Based Decomposition）

任务有固定流程时（如"查数据→分析→生成报告"），按流程拆。方法：
> 1. 识别工作流程
> 2. 确定流程步骤
> 3. 按流程顺序分解

**代码示例**：

```python
# 基于工作流的分解（伪代码）

def decompose_by_workflow(task_description):
    """基于工作流分解任务"""
    # 1. 识别工作流程类型
    workflow_type = identify_workflow(task_description)
    
    # 2. 获取标准工作流
    workflow = get_standard_workflow(workflow_type)
    
    # 3. 根据工作流分解任务
    subtasks = []
    for step in workflow:
        subtask = adapt_step_to_task(step, task_description)
        subtasks.append(subtask)
    
    return subtasks

# 标准工作流示例
standard_workflows = {
    "数据查询": ["连接数据库", "执行查询", "处理结果", "返回数据"],
    "报告生成": ["收集数据", "分析数据", "生成报告", "保存报告"],
    "测试执行": ["准备环境", "执行测试", "收集结果", "生成报告"]
}

# 使用示例
task = "查询用户数据并生成报告"
subtasks = decompose_by_workflow(task)
# 输出：
# [
#   "连接数据库：建立数据库连接",
#   "执行查询：查询用户数据",
#   "处理结果：处理查询结果",
#   "收集数据：收集处理后的数据",
#   "分析数据：分析数据趋势",
#   "生成报告：生成PDF报告",
#   "保存报告：保存到指定路径"
# ]
```

### 1.3 基于工具的分解（Tool-Based Decomposition）

根据可用工具把任务拆成工具调用序列。方法：
> 1. 分析任务需求
> 2. 匹配可用工具
> 3. 确定工具调用顺序

**代码示例**：

```python
# 基于工具的分解（伪代码）

def decompose_by_tools(task_description, available_tools):
    """基于工具分解任务"""
    # 1. 分析任务需求
    requirements = analyze_requirements(task_description)
    
    # 2. 匹配可用工具
    tool_sequence = []
    for requirement in requirements:
        # 找到匹配的工具
        tool = find_matching_tool(requirement, available_tools)
        if tool:
            tool_sequence.append({
                "tool": tool,
                "requirement": requirement
            })
    
    # 3. 确定工具调用顺序（考虑依赖关系）
    ordered_sequence = order_tools_by_dependency(tool_sequence)
    
    return ordered_sequence

# 使用示例
task = "查询用户数据并生成报告"
available_tools = ["query_database", "process_data", "generate_report"]

subtasks = decompose_by_tools(task, available_tools)
# 输出：
# [
#   {"tool": "query_database", "requirement": "查询用户数据"},
#   {"tool": "process_data", "requirement": "处理数据"},
#   {"tool": "generate_report", "requirement": "生成报告"}
# ]
```

### 1.4 三种分解策略对比

| 策略 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **基于目标** | 灵活，适应性强 | 需要智能分析 | 复杂、不确定的任务 |
| **基于工作流** | 标准化，可复用 | 不够灵活 | 有标准流程的任务 |
| **基于工具** | 直接可执行 | 受限于工具集 | 工具明确的任务 |

**选择指南**：
- ✅ **复杂任务**：使用基于目标的分解
- ✅ **标准流程**：使用基于工作流的分解
- ✅ **工具明确**：使用基于工具的分解
- ✅ **最佳实践**：结合使用（如：先基于目标分解，再基于工具细化）

---

## 🔄 二、任务规划方法

分解后要确定执行顺序——像做菜：先备料、再切、再炒、再装盘，顺序错了会乱。

### 2.1 顺序规划（Sequential Planning）

按顺序执行，前一个完成再执行下一个。方法：
> 1. 确定任务顺序
> 2. 按顺序执行
> 3. 等待前一个任务完成再执行下一个

**代码示例**：

```python
# 顺序规划（伪代码）

class SequentialPlanner:
    def plan(self, subtasks):
        """顺序规划"""
        # 1. 确定执行顺序（可以根据依赖关系排序）
        ordered_tasks = self.order_tasks(subtasks)
        
        # 2. 按顺序执行
        results = []
        for task in ordered_tasks:
            result = self.execute_task(task)
            results.append(result)
            
            # 如果任务失败，停止执行
            if not result["success"]:
                break
        
        return results
    
    def order_tasks(self, subtasks):
        """确定任务顺序"""
        # 简单的按依赖关系排序（实际应该用拓扑排序）
        return sorted(subtasks, key=lambda x: x.get("order", 0))

# 使用示例
planner = SequentialPlanner()
subtasks = [
    {"name": "查询数据库", "order": 1},
    {"name": "处理数据", "order": 2, "depends_on": ["查询数据库"]},
    {"name": "生成报告", "order": 3, "depends_on": ["处理数据"]}
]

results = planner.plan(subtasks)
```

### 2.2 并行规划（Parallel Planning）

无依赖的任务可并行执行。方法：
> 1. 识别可以并行的任务
> 2. 并行执行
> 3. 等待所有任务完成

**代码示例**：

```python
# 并行规划（伪代码）

import asyncio

class ParallelPlanner:
    async def plan(self, subtasks):
        """并行规划"""
        # 1. 识别可以并行的任务组
        task_groups = self.group_parallel_tasks(subtasks)
        
        # 2. 按组顺序执行，组内并行
        results = []
        for group in task_groups:
            # 并行执行组内任务
            group_results = await asyncio.gather(*[
                self.execute_task_async(task) for task in group
            ])
            results.extend(group_results)
        
        return results
    
    def group_parallel_tasks(self, subtasks):
        """分组：可以并行的任务放在一组"""
        # 简单的分组逻辑（实际应该分析依赖关系）
        groups = []
        current_group = []
        
        for task in subtasks:
            if not task.get("depends_on"):
                # 没有依赖，可以并行
                current_group.append(task)
            else:
                # 有依赖，开始新组
                if current_group:
                    groups.append(current_group)
                groups.append([task])
                current_group = []
        
        if current_group:
            groups.append(current_group)
        
        return groups

# 使用示例
planner = ParallelPlanner()
subtasks = [
    {"name": "查询用户数据", "depends_on": []},
    {"name": "查询产品数据", "depends_on": []},  # 可以并行
    {"name": "生成报告", "depends_on": ["查询用户数据", "查询产品数据"]}
]

results = await planner.plan(subtasks)
```

### 2.3 条件规划（Conditional Planning）

根据执行结果动态调整后续任务。

**方法**：
> 1. 执行任务
> 2. 根据结果决定下一步
> 3. 动态调整计划

**代码示例**：

```python
# 条件规划（伪代码）

class ConditionalPlanner:
    def plan(self, subtasks, context=None):
        """条件规划"""
        results = []
        current_context = context or {}
        
        for task in subtasks:
            # 1. 检查条件
            if self.should_execute(task, current_context):
                # 2. 执行任务
                result = self.execute_task(task, current_context)
                results.append(result)
                
                # 3. 更新上下文
                current_context.update(result.get("context", {}))
                
                # 4. 根据结果调整后续任务
                if result.get("should_skip_remaining"):
                    break
            else:
                # 跳过任务
                results.append({"skipped": True, "task": task})
        
        return results
    
    def should_execute(self, task, context):
        """判断是否应该执行任务"""
        # 检查条件（如：如果数据为空，跳过生成报告）
        condition = task.get("condition")
        if condition:
            return evaluate_condition(condition, context)
        return True

# 使用示例
planner = ConditionalPlanner()
subtasks = [
    {"name": "查询数据", "condition": None},
    {"name": "生成报告", "condition": "data_count > 0"}  # 只有数据不为空才生成报告
]

results = planner.plan(subtasks, context={})
```

---

## 🔧 三、Self-Correction（自我修正）

执行出错时分析原因并修正——如数据库查询失败，检查连接后重试。

### 3.1 错误检测（Error Detection）

检测执行是否出错。方法：
> 1. 检查执行结果
> 2. 识别错误类型
> 3. 记录错误信息

**代码示例**：

```python
# 错误检测（伪代码）

class ErrorDetector:
    def detect_error(self, result):
        """检测错误"""
        errors = []
        
        # 1. 检查执行结果
        if not result.get("success"):
            errors.append({
                "type": "execution_error",
                "message": result.get("error"),
                "severity": "high"
            })
        
        # 2. 检查结果质量
        if result.get("quality_score", 1.0) < 0.5:
            errors.append({
                "type": "quality_error",
                "message": "结果质量不达标",
                "severity": "medium"
            })
        
        # 3. 检查超时
        if result.get("timeout"):
            errors.append({
                "type": "timeout_error",
                "message": "任务执行超时",
                "severity": "high"
            })
        
        return errors
```

### 3.2 错误分析（Error Analysis）

分析错误原因，定位问题。方法：
> 1. 分析错误类型
> 2. 识别根本原因
> 3. 评估影响范围

**代码示例**：

```python
# 错误分析（伪代码）

class ErrorAnalyzer:
    def analyze(self, error, context):
        """分析错误"""
        # 1. 分析错误类型
        error_type = error["type"]
        
        # 2. 识别根本原因
        root_cause = self.identify_root_cause(error, context)
        
        # 3. 评估影响
        impact = self.assess_impact(error, context)
        
        return {
            "error_type": error_type,
            "root_cause": root_cause,
            "impact": impact,
            "suggested_fix": self.suggest_fix(error, root_cause)
        }
    
    def identify_root_cause(self, error, context):
        """识别根本原因"""
        # 使用 LLM 分析错误原因
        prompt = f"""
        分析以下错误的原因：
        
        错误：{error["message"]}
        上下文：{context}
        
        请分析根本原因。
        """
        
        analysis = llm.analyze(prompt)
        return analysis
```

### 3.3 策略修正（Strategy Correction）

根据错误分析更新计划并重试。方法：
> 1. 根据错误分析生成修正方案
> 2. 更新任务计划
> 3. 重新执行

**代码示例**：

```python
# 策略修正（伪代码）

class StrategyCorrector:
    def correct(self, error_analysis, current_plan):
        """修正策略"""
        # 1. 生成修正方案
        correction = self.generate_correction(error_analysis)
        
        # 2. 更新任务计划
        updated_plan = self.update_plan(current_plan, correction)
        
        return updated_plan
    
    def generate_correction(self, error_analysis):
        """生成修正方案"""
        root_cause = error_analysis["root_cause"]
        
        # 根据根本原因生成修正方案
        corrections = {
            "connection_error": {
                "action": "retry",
                "max_retries": 3,
                "backoff": "exponential"
            },
            "data_error": {
                "action": "validate_input",
                "validate_before_execute": True
            },
            "timeout_error": {
                "action": "increase_timeout",
                "timeout_multiplier": 2.0
            }
        }
        
        return corrections.get(root_cause, {"action": "skip"})
```

### 3.4 完整的 Self-Correction 流程

**代码示例**：

```python
# 完整的 Self-Correction 流程（伪代码）

class SelfCorrectingPlanner:
    def __init__(self):
        self.error_detector = ErrorDetector()
        self.error_analyzer = ErrorAnalyzer()
        self.strategy_corrector = StrategyCorrector()
    
    def execute_with_correction(self, plan):
        """执行计划，带自我修正"""
        max_corrections = 3
        correction_count = 0
        
        while correction_count < max_corrections:
            # 1. 执行计划
            results = self.execute_plan(plan)
            
            # 2. 检测错误
            errors = []
            for result in results:
                detected_errors = self.error_detector.detect_error(result)
                errors.extend(detected_errors)
            
            # 3. 如果没有错误，返回结果
            if not errors:
                return {"success": True, "results": results}
            
            # 4. 分析错误
            error_analysis = self.error_analyzer.analyze(errors[0], {"results": results})
            
            # 5. 修正策略
            plan = self.strategy_corrector.correct(error_analysis, plan)
            
            correction_count += 1
        
        # 如果修正次数超过限制，返回失败
        return {"success": False, "error": "无法修正错误"}
```

---

## 🔍 总结：任务规划是 Agent 处理复杂任务的关键

### 💡 快速回顾：你学到了什么？

1. **任务分解策略**：基于目标、基于工作流、基于工具
2. **任务规划方法**：顺序规划、并行规划、条件规划
3. **Self-Correction**：错误检测、错误分析、策略修正
4. **工程实践**：如何实现完整的任务规划系统

### 任务规划的核心作用

| 组件 | 作用 | 简单理解 |
|------|------|---------|
| **任务分解** | 把大任务拆成小步骤 | 化整为零 |
| **任务规划** | 确定执行顺序 | 有序执行 |
| **Self-Correction** | 检测错误并修正 | 自我修正 |

**生活化理解**：
> 就像做项目：
> - **任务分解**：把"开发测试平台"拆成"需求分析 → 数据库设计 → 后端开发 → 前端开发 → 测试"
> - **任务规划**：确定先做什么，后做什么（必须先设计数据库，才能开发后端）
> - **Self-Correction**：如果某个步骤失败，分析原因并修正（如数据库连接失败，检查连接后重试）

### 设计原则总结

| 原则 | 说明 | 示例 |
|------|------|------|
| **可分解性** | 任务可以分解成子任务 | ✅ "开发平台" → "设计数据库" + "开发API"<br>❌ "思考"（无法分解） |
| **可执行性** | 每个子任务都可以直接执行 | ✅ "查询数据库"<br>❌ "做得好"（太模糊） |
| **可修正性** | 出错时可以修正 | ✅ 检测错误并重试<br>❌ 直接放弃 |

### 实战建议

1. **从简单开始**：先实现顺序规划，再逐步优化
2. **重视错误处理**：错误检测、分析、修正，一个都不能少
3. **优化执行效率**：识别可以并行的任务，提高效率
4. **完善日志记录**：记录任务执行过程，便于调试和优化

> 💡 **核心理解**：
> 任务规划是 Agent 处理复杂任务的关键能力，好的任务规划能让 Agent 更高效、更可靠地完成任务。
> 
> 就像项目管理一样，好的任务规划能让 Agent 像项目经理一样，把复杂任务拆解、规划、执行、修正，最终完成任务。

---

## 📚 延伸阅读（含可直接访问链接）

以下资源按主题分类，每个资源都附有简要说明，帮助你选择合适的学习材料。

### 🎯 任务规划

* [**Task Planning for LLM Agents（LLM Agent 任务规划）**](https://arxiv.org/abs/2305.15000)：任务规划的研究论文。适合想了解任务规划理论的读者。

* [**LangChain Planning（LangChain 规划）**](https://python.langchain.com/docs/modules/agents/agent_types/plan-and-execute/)：LangChain 的任务规划实现。适合使用 LangChain 的开发者。

### 🔄 Self-Correction

* [**Self-Correction in LLM Agents（LLM Agent 自我修正）**](https://arxiv.org/abs/2303.08896)：Self-Correction 的研究论文。适合想了解自我修正机制的读者。

* [**Reflexion: Language Agents with Verbal Reinforcement Learning（Reflexion 论文）**](https://arxiv.org/abs/2303.11366)：Reflexion 框架，展示了如何实现自我修正。**强烈推荐**，适合想实现 Self-Correction 的开发者。

### 🔧 任务分解

* [**Task Decomposition Strategies（任务分解策略）**](https://www.promptingguide.ai/techniques/task_decomposition)：任务分解的最佳实践。适合想优化任务分解的开发者。

---

## 🔔 系列说明

> 本文是[《🧠 LLM/Agent 从入门到精通：告别浅尝辄止》](/categories/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/)系列第 8 篇。上一篇：[Agent 怎么"想"和"做"？ReAct 决策引擎代码级拆解](/2025-12-16-llm-agent-decision-engine/)。下一篇：[Agent 聊着聊着就忘了？记忆管理如何突破 Context Window](/2025-12-17-llm-agent-memory-management/)。

