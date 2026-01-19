---
title: 🚀 服务器性能问题排查完全指南：从 OOM、CPU 高到压测配合，测试工程师必知必会
date: 2026-01-06 20:00:00
updated: 2026-01-06 20:00:00
categories:
  - 技术学习与行业趋势
  - 开发与技术栈
tags:
  - 服务器性能
  - OOM
  - CPU
  - 压测
  - 异步处理
  - 资源管理
keywords: 服务器性能, OOM, CPU高, 内存泄漏, 压测, 异步处理, 队列, 锁, 资源管理, 性能排查
description: 系统解析服务器性能问题：从资源本质到问题排查，涵盖 OOM、CPU 高、异步处理、队列、锁等核心概念，帮助测试工程师理解性能问题的本质和排查思路。
top_img: /img/server-performance-guide.png
cover: /img/server-performance-guide.png
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

> **背景**：最近遇到一个线上问题，运维反馈服务器出现 OOM、CPU 高的情况，需要压测配合排查。作为测试工程师，我发现自己对服务器性能问题缺乏系统认知，于是整理了这篇文档，希望能一次性讲清楚所有相关概念和排查思路。

---

## 📋 目录概览

1. [理解服务器资源的本质](#1️⃣-理解服务器资源的本质)
2. [性能问题的根源：资源竞争与瓶颈](#2️⃣-性能问题的根源资源竞争与瓶颈)
3. [内存问题：OOM 与内存泄漏](#3️⃣-内存问题oom-与内存泄漏)
4. [CPU 问题：高负载与死循环](#4️⃣-cpu-问题高负载与死循环)
5. [并发处理机制：异步、队列与锁](#5️⃣-并发处理机制异步队列与锁)
6. [IO 阻塞与资源等待](#6️⃣-io-阻塞与资源等待)
7. [压测配合排查：如何定位问题](#7️⃣-压测配合排查如何定位问题)
8. [常见性能问题模式与解决方案](#8️⃣-常见性能问题模式与解决方案)
9. [性能优化最佳实践](#9️⃣-性能优化最佳实践)

---

## 1️⃣ 理解服务器资源的本质

在深入性能问题之前，我们需要理解服务器的三大核心资源：**CPU、内存、IO**。

### 1.1 三大资源的本质

| 资源 | 本质 | 特点 | 限制因素 |
|------|------|------|---------|
| **CPU** | 计算能力 | 有限的核心数，串行执行 | 核心数、主频 |
| **内存** | 临时存储空间 | 速度快但容量有限 | 容量大小 |
| **IO** | 数据输入输出 | 磁盘、网络读写 | 带宽、延迟 |

### 1.2 资源之间的关系

**资源竞争的本质**：
- 多个任务同时需要同一资源
- 资源有限，无法同时满足所有需求
- 导致任务排队等待，性能下降

**资源依赖关系**：
```
CPU 处理数据 → 需要从内存读取数据
内存数据不足 → 需要从磁盘（IO）加载
IO 操作慢 → CPU 等待，资源浪费
```

**形象理解**：
> 想象一个餐厅：
> - **CPU** = 厨师（处理能力有限）
> - **内存** = 工作台（空间有限）
> - **IO** = 食材仓库（取食材需要时间）
> 
> 如果工作台（内存）满了，厨师（CPU）无法继续工作；如果仓库（IO）太远，厨师需要等待食材，效率下降。

---

## 2️⃣ 性能问题的根源：资源竞争与瓶颈

### 2.1 什么是性能问题？

**性能问题的本质**：系统无法在预期时间内完成预期任务。

**表现形式**：
- 响应时间变慢
- 吞吐量下降
- 错误率上升
- 资源耗尽（OOM、CPU 100%）

### 2.2 资源瓶颈的类型

#### 2.2.1 CPU 瓶颈

**现象**：
- CPU 使用率接近 100%
- 请求响应变慢
- 系统卡顿

**常见原因**：
- 死循环或无限递归
- 大量计算密集型任务
- 线程过多，上下文切换开销大
- 锁竞争激烈

**排查思路**：
```bash
# 查看 CPU 使用率
top
htop

# 查看 CPU 占用最高的进程
ps aux --sort=-%cpu | head -10

# 查看线程状态
ps -eLf | grep <进程名>
```

#### 2.2.2 内存瓶颈

**现象**：
- 内存使用率持续上升
- OOM（Out of Memory）错误
- 系统开始使用 Swap（交换空间），性能急剧下降

**常见原因**：
- 内存泄漏（对象未释放）
- 缓存过大
- 大对象频繁创建
- 连接池未释放

**排查思路**：
```bash
# 查看内存使用情况
free -h
top (按 M 键按内存排序)

# 查看进程内存占用
ps aux --sort=-%mem | head -10

# 查看内存泄漏（Java）
jmap -histo <pid>
jstat -gc <pid> 1000

# 查看内存泄漏（Python）
memory_profiler
py-spy
```

#### 2.2.3 IO 瓶颈

**现象**：
- 磁盘 IO 等待时间长
- 网络 IO 延迟高
- 数据库查询慢

**常见原因**：
- 磁盘读写频繁
- 网络带宽不足
- 数据库连接池耗尽
- 慢查询

**排查思路**：
```bash
# 查看磁盘 IO
iostat -x 1
iotop

# 查看网络 IO
iftop
netstat -an | grep ESTABLISHED | wc -l

# 查看数据库连接
SHOW PROCESSLIST;
SHOW STATUS LIKE 'Threads_connected';
```

### 2.3 资源瓶颈的连锁反应

**典型场景**：内存不足 → 触发 OOM → 进程被杀死 → 请求失败 → CPU 处理错误 → 系统负载上升

**资源相互影响**：
- **内存不足**：系统使用 Swap，磁盘 IO 增加，CPU 等待 IO，整体性能下降
- **CPU 高**：处理变慢，请求堆积，内存占用增加（请求数据堆积）
- **IO 慢**：CPU 等待 IO，线程阻塞，内存中等待的请求增加

---

## 3️⃣ 内存问题：OOM 与内存泄漏

### 3.1 什么是 OOM？

**OOM（Out of Memory）**：内存溢出，系统无法分配足够的内存给进程。

**触发条件**：
- 进程申请的内存超过系统可用内存
- 系统内存不足，无法满足新请求

**OOM Killer**：
- Linux 系统在内存不足时会触发 OOM Killer
- 自动杀死占用内存最多的进程
- 保证系统核心功能正常运行

### 3.2 OOM 的常见场景

#### 场景 1：内存泄漏

**问题**：对象创建后未释放，内存持续增长

**示例（Python）**：
```python
# ❌ 错误：全局列表不断增长，永不释放
cache = []

def process_request(data):
    cache.append(data)  # 内存泄漏！
    return process(data)

# ✅ 正确：使用 LRU 缓存，限制大小
from functools import lru_cache

@lru_cache(maxsize=1000)
def process_request(data):
    return process(data)
```

**示例（Java）**：
```java
// ❌ 错误：静态集合不断增长
private static List<Object> cache = new ArrayList<>();

public void processRequest(Object data) {
    cache.add(data);  // 内存泄漏！
}

// ✅ 正确：使用有界集合
private static final int MAX_SIZE = 1000;
private static List<Object> cache = new ArrayList<>(MAX_SIZE);

public void processRequest(Object data) {
    if (cache.size() >= MAX_SIZE) {
        cache.remove(0);  // 移除最老的
    }
    cache.add(data);
}
```

#### 场景 2：大对象频繁创建

**问题**：每次请求都创建大对象，GC 来不及回收

**示例**：
```python
# ❌ 错误：每次请求都创建大对象
def handle_request():
    large_data = load_large_file()  # 100MB
    return process(large_data)

# ✅ 正确：对象池或缓存
from functools import lru_cache

@lru_cache(maxsize=1)
def get_large_data():
    return load_large_file()

def handle_request():
    large_data = get_large_data()  # 复用
    return process(large_data)
```

#### 场景 3：连接池未释放

**问题**：数据库连接、HTTP 连接未关闭，连接数持续增长

**示例**：
```python
# ❌ 错误：连接未关闭
def query_database():
    conn = pymysql.connect(...)
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM users")
    # 忘记关闭连接！
    return result

# ✅ 正确：使用上下文管理器
def query_database():
    with pymysql.connect(...) as conn:
        with conn.cursor() as cursor:
            result = cursor.execute("SELECT * FROM users")
            return result
    # 自动关闭连接
```

### 3.3 内存泄漏的排查方法

#### 方法 1：监控内存趋势

```bash
# 持续监控内存使用
watch -n 1 'free -h'

# 查看进程内存增长趋势
while true; do
    ps aux | grep <进程名> | awk '{print $6}'
    sleep 1
done
```

#### 方法 2：使用内存分析工具

**Java**：
```bash
# 生成堆转储
jmap -dump:format=b,file=heap.hprof <pid>

# 使用 Eclipse MAT 或 VisualVM 分析
```

**Python**：
```python
# 使用 memory_profiler
from memory_profiler import profile

@profile
def my_function():
    # 代码
    pass
```

#### 方法 3：压测配合排查

**步骤**：
1. **基线测试**：记录正常情况下的内存使用
2. **逐步加压**：逐步增加并发数，观察内存变化
3. **稳定压力**：保持稳定压力，观察内存是否持续增长
4. **停止压测**：停止压测后，观察内存是否回落

**判断标准**：
- ✅ **正常**：压测停止后，内存回落
- ❌ **内存泄漏**：压测停止后，内存不回落或持续增长

---

## 4️⃣ CPU 问题：高负载与死循环

### 4.1 CPU 高负载的原因

#### 原因 1：死循环或无限递归

**问题**：代码逻辑错误，导致 CPU 持续 100% 占用

**示例**：
```python
# ❌ 错误：死循环
def process_data():
    while True:  # 缺少退出条件！
        data = get_data()
        if not data:
            break  # 如果 get_data() 总是返回数据，永远不会退出
        process(data)

# ✅ 正确：添加超时或限制
def process_data():
    max_iterations = 1000
    count = 0
    while count < max_iterations:
        data = get_data()
        if not data:
            break
        process(data)
        count += 1
```

#### 原因 2：大量计算密集型任务

**问题**：CPU 密集型任务占用过多 CPU 资源

**解决方案**：
- **异步处理**：将计算任务放到后台线程
- **限流**：限制并发计算任务数
- **缓存**：避免重复计算

#### 原因 3：线程过多

**问题**：线程数超过 CPU 核心数，上下文切换开销大

**计算线程数的经验公式**：
```
最佳线程数 = CPU 核心数 × (1 + IO 等待时间 / CPU 计算时间)
```

**示例**：
- CPU 核心数：8
- IO 等待时间：50ms
- CPU 计算时间：10ms
- **最佳线程数** = 8 × (1 + 50/10) = 48

**如果线程数过多**：
- 上下文切换开销增加
- CPU 缓存命中率下降
- 整体性能下降

### 4.2 CPU 问题的排查方法

#### 方法 1：定位 CPU 占用最高的线程

```bash
# 查看 CPU 占用最高的进程
top -H -p <pid>

# 查看线程详细信息
ps -eLf | grep <进程名>

# Java 应用：查看线程栈
jstack <pid> | grep -A 10 "cpu"
```

#### 方法 2：分析线程栈

**Java**：
```bash
# 生成线程转储
jstack <pid> > thread_dump.txt

# 查找 CPU 占用高的线程
top -H -p <pid>  # 获取线程 ID（十进制）
printf "%x\n" <线程ID>  # 转换为十六进制
jstack <pid> | grep -A 10 <十六进制线程ID>
```

**Python**：
```bash
# 使用 py-spy 分析
py-spy top --pid <pid>
py-spy record -o profile.svg --pid <pid>
```

#### 方法 3：压测配合排查

**步骤**：
1. **基线测试**：记录正常情况下的 CPU 使用率
2. **逐步加压**：逐步增加并发数，观察 CPU 变化
3. **定位热点**：使用性能分析工具定位 CPU 热点代码
4. **优化验证**：优化后再次压测验证

---

## 5️⃣ 并发处理机制：异步、队列与锁

### 5.1 为什么需要并发处理？

**问题场景**：
- 单线程处理：一个请求处理完才能处理下一个，效率低
- 多线程处理：可以同时处理多个请求，但资源竞争问题

**并发处理的本质**：在有限的资源下，最大化资源利用率。

### 5.2 异步处理（Async）

#### 5.2.1 什么是异步？

**同步 vs 异步**：

| 方式 | 特点 | 示例 |
|------|------|------|
| **同步** | 等待操作完成才继续 | 调用 API，等待响应 |
| **异步** | 不等待操作完成，继续执行 | 调用 API，立即返回，回调处理结果 |

**形象理解**：
> **同步**：你去餐厅点餐，站在柜台前等待，直到拿到餐才离开
> **异步**：你去餐厅点餐，拿到号码牌后去座位等待，餐好了服务员通知你

#### 5.2.2 异步的优势

**优势**：
- **提高吞吐量**：不阻塞等待，可以处理更多请求
- **资源利用率高**：IO 等待时，CPU 可以处理其他任务
- **响应更快**：不需要等待慢操作完成

**适用场景**：
- IO 密集型操作（数据库查询、API 调用、文件读写）
- 不需要立即返回结果的操作

**不适用场景**：
- CPU 密集型操作（会阻塞事件循环）
- 需要立即返回结果的操作

#### 5.2.3 异步的实现方式

**Python（asyncio）**：
```python
import asyncio
import aiohttp

# ✅ 异步处理多个请求
async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = ['http://example.com'] * 100
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# 运行
asyncio.run(main())
```

**Java（CompletableFuture）**：
```java
// ✅ 异步处理
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return fetchData();  // 异步执行
});

future.thenAccept(result -> {
    // 处理结果
    processResult(result);
});
```

### 5.3 队列（Queue）

#### 5.3.1 什么是队列？

**队列的本质**：缓冲和调度机制，解决生产者和消费者速度不匹配的问题。

**队列的作用**：
- **缓冲**：临时存储待处理的任务
- **削峰**：高峰期请求先入队，后台慢慢处理
- **解耦**：生产者和消费者不需要直接交互

**形象理解**：
> 队列就像餐厅的排队系统：
> - 客人（生产者）到达后排队
> - 服务员（消费者）按顺序处理
> - 如果处理不过来，客人排队等待

#### 5.3.2 队列的类型

**1. 同步队列（Blocking Queue）**

**特点**：队列满时，生产者阻塞；队列空时，消费者阻塞

**示例（Python）**：
```python
from queue import Queue

# 创建队列
task_queue = Queue(maxsize=100)

# 生产者：添加任务
def producer():
    for i in range(1000):
        task_queue.put(i)  # 队列满时会阻塞

# 消费者：处理任务
def consumer():
    while True:
        task = task_queue.get()  # 队列空时会阻塞
        process_task(task)
        task_queue.task_done()
```

**2. 异步队列（Async Queue）**

**特点**：非阻塞，使用协程处理

**示例（Python）**：
```python
import asyncio

async def producer(queue):
    for i in range(1000):
        await queue.put(i)  # 非阻塞

async def consumer(queue):
    while True:
        task = await queue.get()  # 非阻塞
        await process_task(task)
        queue.task_done()

# 运行
queue = asyncio.Queue(maxsize=100)
await asyncio.gather(
    producer(queue),
    consumer(queue)
)
```

**3. 消息队列（Message Queue）**

**特点**：分布式、持久化、支持多消费者

**常见实现**：
- **Redis**：简单快速，适合小规模
- **RabbitMQ**：功能完整，适合复杂场景
- **Kafka**：高吞吐，适合大数据场景

**示例（Redis）**：
```python
import redis

# 连接 Redis
r = redis.Redis(host='localhost', port=6379)

# 生产者：推送任务
def producer():
    for i in range(1000):
        r.lpush('task_queue', i)

# 消费者：处理任务
def consumer():
    while True:
        task = r.brpop('task_queue', timeout=1)  # 阻塞等待
        if task:
            process_task(task[1])
```

#### 5.3.3 队列的使用场景

**场景 1：削峰填谷**

**问题**：高峰期请求量大，直接处理会导致系统崩溃

**解决方案**：
```
请求 → 队列 → 后台处理
高峰期：请求入队，不立即处理
低峰期：队列中的任务慢慢处理
```

**场景 2：异步任务处理**

**问题**：某些任务不需要立即返回结果（如发送邮件、生成报表）

**解决方案**：
```
用户请求 → 立即返回 → 任务入队 → 后台处理
```

**场景 3：解耦系统**

**问题**：系统 A 需要通知系统 B，但不想直接耦合

**解决方案**：
```
系统 A → 消息队列 → 系统 B
```

### 5.4 锁（Lock）

#### 5.4.1 为什么需要锁？

**问题场景**：多个线程同时访问共享资源，可能导致数据不一致

**示例**：
```python
# ❌ 问题：多线程同时修改共享变量
counter = 0

def increment():
    global counter
    for i in range(100000):
        counter += 1  # 不是原子操作！

# 两个线程同时执行 increment()
# 预期结果：counter = 200000
# 实际结果：counter < 200000（数据竞争）
```

**锁的作用**：保证同一时间只有一个线程访问共享资源

#### 5.4.2 锁的类型

**1. 互斥锁（Mutex Lock）**

**特点**：同一时间只有一个线程可以获取锁

**示例（Python）**：
```python
import threading

lock = threading.Lock()
counter = 0

def increment():
    global counter
    for i in range(100000):
        with lock:  # 获取锁
            counter += 1
        # 自动释放锁
```

**2. 读写锁（Read-Write Lock）**

**特点**：多个读操作可以并发，写操作独占

**适用场景**：读多写少的场景

**示例**：
```python
import threading

class ReadWriteLock:
    def __init__(self):
        self._read_lock = threading.Lock()
        self._write_lock = threading.Lock()
        self._readers = 0
    
    def acquire_read(self):
        with self._read_lock:
            self._readers += 1
            if self._readers == 1:
                self._write_lock.acquire()
    
    def release_read(self):
        with self._read_lock:
            self._readers -= 1
            if self._readers == 0:
                self._write_lock.release()
```

**3. 分布式锁**

**特点**：跨进程、跨服务器的锁

**实现方式**：
- **Redis**：使用 SETNX 命令
- **Zookeeper**：使用临时节点
- **数据库**：使用唯一索引

**示例（Redis）**：
```python
import redis
import time

def acquire_lock(conn, lock_name, timeout=10):
    identifier = str(time.time())
    end = time.time() + timeout
    
    while time.time() < end:
        if conn.setnx(f'lock:{lock_name}', identifier):
            conn.expire(f'lock:{lock_name}', timeout)
            return identifier
        time.sleep(0.001)
    return False

def release_lock(conn, lock_name, identifier):
    pipe = conn.pipeline(True)
    while True:
        try:
            pipe.watch(f'lock:{lock_name}')
            if pipe.get(f'lock:{lock_name}') == identifier:
                pipe.multi()
                pipe.delete(f'lock:{lock_name}')
                pipe.execute()
                return True
            pipe.unwatch()
            break
        except redis.WatchError:
            pass
    return False
```

#### 5.4.3 锁的常见问题

**问题 1：死锁**

**场景**：两个线程互相等待对方释放锁

**示例**：
```python
# ❌ 死锁示例
lock1 = threading.Lock()
lock2 = threading.Lock()

def thread1():
    lock1.acquire()
    lock2.acquire()  # 等待 lock2
    # ...
    lock2.release()
    lock1.release()

def thread2():
    lock2.acquire()
    lock1.acquire()  # 等待 lock1（死锁！）
    # ...
    lock1.release()
    lock2.release()
```

**解决方案**：
- 按固定顺序获取锁
- 使用超时机制
- 避免嵌套锁

**问题 2：锁竞争激烈**

**问题**：太多线程竞争同一把锁，导致性能下降

**解决方案**：
- **减少锁的粒度**：只锁必要的代码段
- **使用无锁数据结构**：如原子操作
- **使用读写锁**：读操作不互斥

---

## 6️⃣ IO 阻塞与资源等待

### 6.1 IO 阻塞的本质

**IO 阻塞**：线程等待 IO 操作完成，期间无法处理其他任务

**阻塞时间**：
- **磁盘 IO**：毫秒级（1-10ms）
- **网络 IO**：毫秒到秒级（10ms-10s）
- **数据库查询**：毫秒到秒级（10ms-10s）

**问题**：阻塞期间，线程无法处理其他请求，资源浪费

### 6.2 IO 阻塞的解决方案

#### 方案 1：异步 IO

**原理**：IO 操作不阻塞线程，使用回调或协程处理结果

**示例（Python）**：
```python
import asyncio
import aiohttp

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()  # 非阻塞

# 可以同时处理多个 IO 操作
async def main():
    urls = ['http://example.com'] * 100
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results
```

#### 方案 2：连接池

**原理**：复用连接，减少连接建立和关闭的开销

**示例（Python）**：
```python
import pymysql
from contextlib import contextmanager

# 创建连接池
pool = pymysql.ConnectionPool(
    host='localhost',
    user='root',
    password='password',
    database='test',
    maxconnections=10  # 最大连接数
)

@contextmanager
def get_connection():
    conn = pool.get_connection()
    try:
        yield conn
    finally:
        pool.release_connection(conn)

# 使用连接池
def query_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
```

#### 方案 3：批量处理

**原理**：减少 IO 次数，提高效率

**示例**：
```python
# ❌ 错误：逐个查询
def process_users(user_ids):
    results = []
    for user_id in user_ids:
        user = query_user(user_id)  # 100 次数据库查询
        results.append(user)
    return results

# ✅ 正确：批量查询
def process_users(user_ids):
    users = batch_query_users(user_ids)  # 1 次数据库查询
    return users
```

### 6.3 资源等待的优化

#### 优化 1：超时机制

**问题**：资源等待时间过长，影响用户体验

**解决方案**：设置超时时间

**示例**：
```python
import requests

# 设置超时
response = requests.get('http://example.com', timeout=5)  # 5 秒超时

# 数据库查询超时
cursor.execute("SELECT * FROM users", timeout=10)  # 10 秒超时
```

#### 优化 2：重试机制

**问题**：临时故障导致请求失败

**解决方案**：失败后重试

**示例**：
```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1)
def fetch_data(url):
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
```

#### 优化 3：缓存

**问题**：重复查询相同数据

**解决方案**：缓存查询结果

**示例**：
```python
from functools import lru_cache
import redis

# 内存缓存
@lru_cache(maxsize=1000)
def get_user(user_id):
    return query_user(user_id)

# Redis 缓存
def get_user_cached(user_id):
    cache_key = f'user:{user_id}'
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    user = query_user(user_id)
    redis_client.setex(cache_key, 3600, json.dumps(user))  # 缓存 1 小时
    return user
```

---

## 7️⃣ 压测配合排查：如何定位问题

### 7.1 压测的目的

**压测的作用**：
1. **验证系统容量**：系统能承受多少并发
2. **发现性能瓶颈**：定位性能问题
3. **验证优化效果**：优化后再次压测验证

### 7.2 压测的步骤

#### 步骤 1：建立基线

**目的**：了解系统正常情况下的性能指标

**需要记录的数据**：
- CPU 使用率
- 内存使用率
- 响应时间
- 错误率
- QPS/TPS

**工具**：
```bash
# 监控系统资源
top
htop
iostat -x 1
vmstat 1

# 监控应用指标
# 使用 APM 工具（如 Prometheus、Grafana）
```

#### 步骤 2：逐步加压

**目的**：找到系统的临界点

**方法**：
1. 从低并发开始（如 10 并发）
2. 逐步增加（10 → 50 → 100 → 200）
3. 每个阶段稳定运行一段时间（如 5 分钟）
4. 观察指标变化

**观察指标**：
- **响应时间**：是否开始变慢
- **错误率**：是否开始出现错误
- **资源使用**：CPU、内存是否接近上限
- **吞吐量**：QPS 是否不再增长

#### 步骤 3：稳定压力测试

**目的**：验证系统在稳定压力下的表现

**方法**：
1. 保持稳定的并发数（略低于临界点）
2. 持续运行较长时间（如 30 分钟）
3. 观察是否有内存泄漏、连接泄漏等问题

**观察指标**：
- **内存趋势**：是否持续增长（内存泄漏）
- **连接数**：是否持续增长（连接泄漏）
- **错误率**：是否稳定

#### 步骤 4：峰值压力测试

**目的**：测试系统在峰值压力下的表现

**方法**：
1. 快速增加到峰值并发
2. 观察系统如何应对
3. 观察恢复能力

### 7.3 压测配合排查 OOM

**场景**：运维反馈 OOM，需要压测配合排查

**排查步骤**：

**1. 基线测试**
```bash
# 记录正常情况下的内存使用
free -h
ps aux --sort=-%mem | head -10
```

**2. 逐步加压**
```bash
# 使用 JMeter 或 Locust 逐步增加并发
# 同时监控内存使用
watch -n 1 'free -h'
```

**3. 观察内存趋势**
- **正常**：内存使用稳定，压测停止后回落
- **内存泄漏**：内存持续增长，压测停止后不回落

**4. 定位泄漏点**
```bash
# Java 应用
jmap -histo <pid> | head -20  # 查看对象数量
jmap -dump:format=b,file=heap.hprof <pid>  # 生成堆转储

# Python 应用
py-spy record -o profile.svg --pid <pid>
```

**5. 分析结果**
- 查看哪些对象占用内存最多
- 查看对象是否应该被释放
- 定位代码中的问题

### 7.4 压测配合排查 CPU 高

**场景**：运维反馈 CPU 高，需要压测配合排查

**排查步骤**：

**1. 基线测试**
```bash
# 记录正常情况下的 CPU 使用
top
```

**2. 逐步加压**
```bash
# 使用压测工具逐步增加并发
# 同时监控 CPU 使用
top -H -p <pid>
```

**3. 定位 CPU 占用高的线程**
```bash
# 查看线程 CPU 占用
top -H -p <pid>

# Java 应用：查看线程栈
jstack <pid> | grep -A 10 "cpu"

# Python 应用：使用 py-spy
py-spy top --pid <pid>
```

**4. 分析代码**
- 查看线程栈，定位热点代码
- 分析是否有死循环、无限递归
- 分析是否有大量计算

**5. 优化验证**
- 优化代码后再次压测
- 验证 CPU 使用率是否下降

### 7.5 压测工具选择

**JMeter**：
- **优点**：功能强大，支持多种协议
- **缺点**：资源消耗大，学习曲线陡
- **适用场景**：HTTP API 压测

**Locust**：
- **优点**：Python 编写，易于扩展
- **缺点**：功能相对简单
- **适用场景**：HTTP API 压测，需要自定义逻辑

**wrk**：
- **优点**：性能好，资源消耗低
- **缺点**：功能简单，需要写 Lua 脚本
- **适用场景**：简单 HTTP 压测

**Apache Bench (ab)**：
- **优点**：简单易用
- **缺点**：功能有限
- **适用场景**：快速验证

---

## 8️⃣ 常见性能问题模式与解决方案

### 8.1 问题模式 1：内存泄漏

**症状**：
- 内存使用持续增长
- 压测停止后内存不回落
- 最终导致 OOM

**常见原因**：
- 全局变量不断增长
- 缓存未设置上限
- 连接未关闭
- 监听器未移除

**解决方案**：
- 使用有界集合
- 设置缓存过期时间
- 使用连接池
- 及时移除监听器

### 8.2 问题模式 2：CPU 高

**症状**：
- CPU 使用率接近 100%
- 响应时间变慢
- 系统卡顿

**常见原因**：
- 死循环或无限递归
- 大量计算密集型任务
- 线程过多
- 锁竞争激烈

**解决方案**：
- 修复死循环
- 异步处理计算任务
- 优化线程数
- 减少锁竞争

### 8.3 问题模式 3：连接泄漏

**症状**：
- 数据库连接数持续增长
- HTTP 连接数持续增长
- 最终导致连接耗尽

**常见原因**：
- 连接未关闭
- 异常未处理，连接未释放
- 连接池配置不当

**解决方案**：
- 使用 try-finally 确保连接关闭
- 使用上下文管理器
- 配置连接池最大连接数
- 设置连接超时时间

### 8.4 问题模式 4：慢查询

**症状**：
- 数据库查询慢
- IO 等待时间长
- 响应时间变慢

**常见原因**：
- 缺少索引
- 查询语句不当
- 数据量过大
- 锁等待

**解决方案**：
- 添加索引
- 优化查询语句
- 分页查询
- 使用缓存

### 8.5 问题模式 5：线程池耗尽

**症状**：
- 请求排队等待
- 响应时间变慢
- 线程数达到上限

**常见原因**：
- 线程池大小配置不当
- 任务执行时间过长
- 线程阻塞

**解决方案**：
- 调整线程池大小
- 优化任务执行时间
- 使用异步处理
- 设置任务超时

---

## 9️⃣ 性能优化最佳实践

### 9.1 代码层面

#### 实践 1：避免内存泄漏

```python
# ✅ 使用上下文管理器
with open('file.txt') as f:
    data = f.read()

# ✅ 使用连接池
with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")

# ✅ 使用有界缓存
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_function(x):
    return compute(x)
```

#### 实践 2：优化 IO 操作

```python
# ✅ 批量操作
def batch_insert(records):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO users VALUES (?, ?)", records)

# ✅ 使用连接池
pool = ConnectionPool(max_connections=10)

# ✅ 异步 IO
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

#### 实践 3：减少锁竞争

```python
# ✅ 减少锁的粒度
def process_data(data):
    # 不需要锁的操作
    processed = preprocess(data)
    
    # 只在必要时加锁
    with lock:
        shared_resource.update(processed)
    
    # 不需要锁的操作
    return postprocess(processed)

# ✅ 使用无锁数据结构
from collections import deque
queue = deque()  # 线程安全的操作
```

### 9.2 架构层面

#### 实践 1：使用缓存

**缓存策略**：
- **本地缓存**：快速但容量有限
- **分布式缓存**：容量大但需要网络
- **多级缓存**：结合两者优势

**缓存更新策略**：
- **Cache-Aside**：应用负责缓存更新
- **Write-Through**：写入时同时更新缓存
- **Write-Behind**：异步更新缓存

#### 实践 2：使用队列削峰

**场景**：高峰期请求量大

**方案**：
```
请求 → 队列 → 后台处理
```

**优势**：
- 削峰填谷
- 系统更稳定
- 用户体验更好

#### 实践 3：异步处理

**场景**：不需要立即返回结果的操作

**方案**：
```
用户请求 → 立即返回 → 任务入队 → 后台处理
```

**优势**：
- 响应更快
- 系统吞吐量更高
- 资源利用率更高

### 9.3 监控与告警

#### 监控指标

**系统指标**：
- CPU 使用率
- 内存使用率
- 磁盘 IO
- 网络 IO

**应用指标**：
- 响应时间
- 错误率
- QPS/TPS
- 连接数

**业务指标**：
- 订单量
- 用户数
- 交易量

#### 告警规则

**告警条件**：
- CPU 使用率 > 80% 持续 5 分钟
- 内存使用率 > 90%
- 错误率 > 1%
- 响应时间 > 1 秒

**告警处理**：
- 自动扩容
- 降级处理
- 通知相关人员

### 9.4 压测实践

#### 压测前准备

1. **环境准备**：独立的压测环境
2. **数据准备**：足够的测试数据
3. **监控准备**：监控系统就绪
4. **预案准备**：应急预案准备

#### 压测执行

1. **逐步加压**：从低到高逐步增加
2. **稳定测试**：每个阶段稳定运行
3. **记录数据**：详细记录各项指标
4. **分析问题**：及时分析发现的问题

#### 压测后分析

1. **数据分析**：分析各项指标
2. **问题定位**：定位性能瓶颈
3. **优化方案**：制定优化方案
4. **验证效果**：优化后再次压测验证

---

## 📝 总结

### 核心要点

1. **资源本质**：CPU、内存、IO 是服务器的三大核心资源
2. **问题根源**：资源竞争和瓶颈导致性能问题
3. **常见问题**：OOM、CPU 高、连接泄漏、慢查询
4. **解决方案**：异步处理、队列、缓存、连接池
5. **排查方法**：监控、压测、分析工具

### 排查思路

**遇到性能问题时**：
1. **观察现象**：CPU 高？内存高？响应慢？
2. **定位资源**：哪个资源是瓶颈？
3. **分析原因**：为什么会出现这个问题？
4. **制定方案**：如何解决？
5. **验证效果**：优化后是否改善？

### 最佳实践

1. **预防为主**：代码层面避免常见问题
2. **监控告警**：及时发现问题
3. **压测验证**：定期压测验证系统性能
4. **持续优化**：根据监控和压测结果持续优化

---

## 📚 延伸阅读

### 工具推荐

**监控工具**：
- **Prometheus + Grafana**：系统监控
- **APM 工具**：应用性能监控（如 New Relic、Datadog）
- **日志分析**：ELK Stack（Elasticsearch、Logstash、Kibana）

**压测工具**：
- **JMeter**：功能强大的压测工具
- **Locust**：Python 编写的压测工具
- **wrk**：高性能 HTTP 压测工具

**分析工具**：
- **Java**：jstack、jmap、VisualVM
- **Python**：py-spy、memory_profiler
- **系统**：top、htop、iostat、vmstat

### 相关文章

- [流式接口压测实践](/2025/06/30/2025-06-30-streaming-api-performance-test/)
- [数据库连接泄漏排查](/2025/06/30/2025-06-30-mysql-connection-leak-fix/)
- [QPS vs RPS 的区别](/2025/08/06/2025-08-06-qps-vs-rps/)


