---
title: 深入理解「可序列化」：开发与测试都绕不开的隐形规则
date: 2025-10-14 01:00:00
categories:
- 自动化测试 & 工具开发（Test Automation & Tool Development）
  - 测试理论
  - 开发技巧
tags:
  - 序列化
  - JSON
  - Python
  - 测试开发
keywords: 序列化, JSON, 测试开发, Python, 接口测试
description: '深入探讨可序列化概念，分析开发与测试过程中遇到的序列化问题及解决方案'
top_img: /img/serialization-deep-dive.png
cover: /img/serialization-deep-dive.png
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

# 💡深入理解「可序列化」：开发与测试都绕不开的隐形规则

你可能在接口请求、缓存、日志、报告里见过" Object of type X is not JSON serializable "这样的报错。
这时候，系统并不是在"挑刺"，而是在提醒你一个几乎所有开发与测试都会遇到的基本问题—— 可序列化（Serializable） 。

## 🧠 一、什么是可序列化？

可序列化（Serializable） ，简单来说，就是：
一个对象可以被转换成 可存储或可传输的格式 （如字节流、JSON 字符串），之后还能再恢复为原始对象。

换句话说：
- 序列化（Serialization） ：对象 → 字节或文本
- 反序列化（Deserialization） ：字节或文本 → 对象

### 🌰 举个简单的例子（以 Python 为例）

```python
import json

user = {"name": "Alice", "age": 25}

# 序列化
json_str = json.dumps(user)  
print(json_str)  # {"name": "Alice", "age": 25}

# 反序列化
obj = json.loads(json_str)
print(obj["name"])  # Alice
```

你就完成了一次序列化与反序列化。
如果对象中有 datetime 、 Decimal 、 set 等类型，就可能出现 "not JSON serializable" 的错误。

## 🧩 二、开发者在什么场景会遇到可序列化

### 1️⃣ 接口返回与传输

当后端接口要返回自定义对象时：
```python
return jsonify(user)  # ❌ 会报错：not JSON serializable
```

必须转成字典：
```python
return jsonify(user.to_dict())
```

**要点：**
- JSON 只能序列化基础类型
- 日期、枚举、Decimal 需转字符串

### 2️⃣ 缓存与存储（Redis、数据库）

Redis 只接受字符串或字节流。
```python
redis.set("user:1", pickle.dumps(user))  # ✅
```

**建议：**
- JSON 跨语言兼容
- Pickle 性能高但有安全风险
- 不要序列化外部输入

### 3️⃣ Session、Token、状态保持

Session 中的数据必须是可序列化的。
不要往里面放数据库连接、文件句柄或线程对象。

### 4️⃣ 异步与分布式任务（Celery、消息队列）

Celery 会自动序列化任务参数：
```python
@celery.task
def send_email(user):  # ❌ 如果 user 是复杂对象
    ...
```

建议只传基础字段或对象 ID。

### 5️⃣ 多进程/多线程通信

Python 的 multiprocessing 在进程间通信时依赖 pickle。
如果测试对象中有线程锁、连接池，会报错：
```
TypeError: can't pickle _thread.lock objects
```

### 6️⃣ 配置与模型持久化

保存模型或配置文件时，也是在做序列化：
- ML 模型 → joblib.dump() / torch.save()
- 配置 → JSON 、 YAML

## 💾 三、测试人员在什么场景会遇到可序列化

### 1️⃣ 接口测试

请求体、响应体、断言结果都必须可序列化为 JSON。
比如：
```python
payload = {"created_at": datetime.now()}  # ❌ 无法序列化
```

应改为：
```python
payload = {"created_at": str(datetime.now())}
```

### 2️⃣ 自动化测试框架

框架会将测试结果写入报告（如 Allure、JSON、XML），
如果日志或断言结果中包含不可序列化对象，会导致报告生成失败。

**✅ 建议：**
- 测试上下文中仅保存基础类型
- 输出日志前统一调用 json.dumps(obj, default=str)

### 3️⃣ 测试数据与 Mock 管理

Mock 文件和接口回放都需要用 JSON/YAML 保存。
如果数据中包含 bytes、datetime 等类型，要转字符串或 Base64。

### 4️⃣ 分布式测试与多进程执行

pytest-xdist 或多节点压测时，测试结果要在进程间传递。
包含不可序列化对象时，会出现：
```
pickle.PicklingError: Can't pickle <class '...'>
```

### 5️⃣ 日志与报告输出

Allure 报告、日志文件、监控输出都依赖序列化。
对象没法被转成字符串时，会导致报告部分缺失或写入失败。

### 6️⃣ 性能与压测

Locust / JMeter 分布式执行时节点之间同步数据，也要依赖序列化。
如果测试数据太复杂或包含对象引用，会导致节点同步失败。

## ⚠️ 四、常见错误与解决方法

| 错误类型 | 常见报错 | 解决方案 |
|---------|---------|--------|
| 类型不支持 | Object of type datetime is not JSON serializable | 转字符串或自定义 encoder |
| Pickle 错误 | Can't pickle _thread.lock objects | 不传锁、连接、句柄等对象 |
| 报告生成失败 | TypeError: Object is not serializable | 转成基础类型或字符串 |
| Mock 文件加载异常 | JSONDecodeError | 检查 mock 文件格式是否有效 JSON |
| 安全问题 | 恶意 pickle 文件执行任意代码 | 不反序列化外部输入 |

## 🧠 五、最佳实践总结

| 目标 | 最佳做法 |
|-----|--------|
| 接口通信 | 统一 JSON 格式，复杂类型转字符串 |
| 缓存/存储 | 只存可序列化字段，必要时自定义 to_dict() |
| Session/Token | 仅存基础数据，避免运行时对象 |
| 自动化框架 | 报告与日志输出前执行序列化安全检查 |
| 多进程测试 | 进程间只传递基础类型 |
| Mock 数据 | 统一存为 JSON/YAML 格式，保存前验证可序列化性 |
| 安全 | 禁止反序列化外部 pickle 数据 |

## ✨ 六、核心总结

"可序列化"看似底层，但它是开发与测试的共同语言。
每当你要" 跨边界传输数据 "（从内存到文件、从本地到网络、从进程到进程），
底层都在做一件事： 对象序列化 。

对开发来说：
要确保接口、缓存、Session、RPC 的数据可安全序列化。

对测试来说：
要保证请求、响应、报告、日志、Mock 都能被安全持久化。

记住这条规则：
跨边界传输的数据，一定要能被序列化。

## 🧾 附录：一行可序列化安全工具（Python）

```python
import json

def safe_json(data):
    """安全序列化，自动处理特殊类型"""
    return json.dumps(data, ensure_ascii=False, default=str)
```

适用于接口响应、日志记录、报告输出等场景。

## 📚 推荐阅读

- 《Python 官方文档：json 模块》
- 《Java Serializable 接口详解》
- 《Google Protobuf 序列化机制》
- 《Celery 官方文档：序列化与安全性》

---

作者：yuxiaoling
测试工程师 · 专注测试自动化与质量体系建设
分享让测试更智能、更高效的实践经验 💪