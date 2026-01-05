---
title: 📋 日志轮转完全指南：从原理到实践，让你的日志管理更专业
date: 2025-12-31 20:00:00
updated: 2025-12-31 20:00:00
categories:
  - 技术学习与行业趋势
  - 开发与技术栈
tags:
  - 日志管理
  - 日志轮转
  - logrotate
  - logback
  - log4j
  - 运维
keywords: 日志轮转, logrotate, logback, log4j, 日志管理, 日志切割, 日志归档, 日志清理, 运维实践
description: 系统讲解日志轮转的原理、工具和实践，从 logrotate 到 logback、log4j，帮你掌握专业的日志管理方法，避免日志文件无限增长导致的问题。
top_img: /img/log-rotation-guide.png
cover: /img/log-rotation-guide.png
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

你有没有遇到过这样的情况：

> **服务器磁盘空间告警，一查发现是日志文件占满了磁盘**  
> **应用运行几个月后，日志文件达到几十 GB，打开都困难**  
> **想删除旧日志，又担心误删正在使用的日志文件**

这些问题，都可以通过 **日志轮转（Log Rotation）** 来解决。

这篇文章将从**问题场景 → 核心原理 → 工具使用 → 最佳实践**，带你系统掌握日志轮转的完整知识体系。

---

## 一、问题场景：为什么需要日志轮转？

### **1️⃣ 典型问题**

#### **问题 1：磁盘空间被占满**

```bash
# 查看磁盘使用情况
df -h

# 输出
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   48G  500M  99% /

# 查找大文件
du -sh /var/log/* | sort -rh | head -5

# 输出
45G    /var/log/app.log
2G     /var/log/nginx/access.log
500M   /var/log/syslog
```

**结果：** 应用日志文件 `app.log` 已经达到 45GB，占满了磁盘空间。

#### **问题 2：日志文件过大，难以处理**

* 打开日志文件需要很长时间
* 搜索日志内容非常慢
* 传输日志文件困难
* 日志分析工具无法处理

#### **问题 3：历史日志丢失**

* 手动删除日志容易误删
* 没有归档机制，历史日志无法追溯
* 无法按时间、大小等规则管理日志

### **2️⃣ 日志轮转的价值**

**日志轮转（Log Rotation）** 是一种日志管理机制，通过以下方式解决上述问题：

* ✅ **自动切割**：按时间或大小自动切割日志文件
* ✅ **自动归档**：将旧日志压缩、归档，节省空间
* ✅ **自动清理**：删除过期的历史日志
* ✅ **无缝切换**：应用无需重启，自动切换到新日志文件

---

## 二、基础概念科普：理解日志和文件系统

在深入日志轮转之前，我们需要先理解一些基础概念。

### **1️⃣ 什么是日志文件**

**日志文件（Log File）** 是应用程序记录运行状态、错误信息、操作记录等信息的文本文件。

**日志的作用：**
* **问题排查**：当应用出错时，通过日志定位问题
* **行为追踪**：记录用户操作、系统事件
* **性能分析**：记录响应时间、资源使用情况
* **审计合规**：满足合规要求，保留操作记录

**日志的特点：**
* **只追加（Append Only）**：日志通常只往文件末尾追加内容，不修改已有内容
* **持续增长**：只要应用在运行，日志就会不断增长
* **文本格式**：通常是可读的文本格式，便于人工查看

### **2️⃣ 为什么日志文件会不断增长**

**日志文件增长的原因：**

1. **应用持续运行**：只要应用在运行，就会不断产生日志
2. **高频操作**：用户请求、数据库操作、API 调用都会产生日志
3. **详细记录**：为了排查问题，日志通常记录得很详细
4. **没有清理机制**：如果不主动清理，日志会一直累积

**举个例子：**
```
一个 Web 应用，每秒处理 100 个请求
每个请求产生 1KB 日志
一天产生的日志 = 100 请求/秒 × 1KB × 86400 秒 = 8.64GB
一个月 = 8.64GB × 30 = 259GB
```

### **3️⃣ 文件描述符（File Descriptor）的概念**

**文件描述符**是操作系统用来标识打开文件的数字。理解这个概念对理解日志轮转很重要。

**工作原理：**
```
应用启动时：
1. 打开日志文件 app.log
2. 操作系统分配文件描述符（比如 fd=3）
3. 应用通过 fd=3 写入日志

应用写入日志时：
write(fd=3, "log message")  →  写入到 app.log

如果直接删除或重命名 app.log：
- 文件描述符 fd=3 仍然指向原来的文件
- 应用继续通过 fd=3 写入
- 但文件已经不在文件系统中了（成为"孤儿文件"）
- 只有应用关闭文件或重启，文件才会真正删除
```

**为什么这很重要？**
* 日志轮转时，不能直接删除或重命名正在写入的文件
* 需要让应用重新打开文件，获取新的文件描述符
* 这就是为什么需要 `postrotate` 脚本发送信号让应用重新打开文件

### **4️⃣ 日志写入的机制**

**应用如何写入日志：**

```python
# Python 示例
import logging

# 打开日志文件（获取文件描述符）
logging.basicConfig(filename='app.log', level=logging.INFO)

# 写入日志（通过文件描述符）
logging.info('This is a log message')
```

**底层过程：**
1. 应用打开文件，获取文件描述符
2. 写入日志时，操作系统将数据写入文件
3. 数据可能先写入缓冲区，然后刷新到磁盘
4. 文件指针（文件末尾）不断后移

### **5️⃣ 文件重命名的原理**

**文件重命名（Rename）** 是日志轮转的核心操作。

**重命名的特点：**
* **原子操作**：重命名是原子性的，要么成功要么失败
* **不改变文件内容**：只改变文件名，文件内容不变
* **不改变文件描述符**：已打开的文件描述符仍然有效

**示例：**
```bash
# 初始状态
app.log (文件描述符 fd=3 指向它)

# 重命名操作
mv app.log app.log.1

# 结果
app.log.1 (文件描述符 fd=3 仍然指向它)
app.log (不存在)

# 应用继续通过 fd=3 写入，数据写入到 app.log.1
# 这就是为什么需要让应用重新打开文件
```

### **6️⃣ 什么是日志轮转**

**日志轮转（Log Rotation）** 是指**定期或按条件将当前日志文件重命名、归档，并创建新的日志文件继续写入**的过程。

**核心思想：**
* 不删除正在使用的日志文件
* 通过重命名"冻结"旧日志
* 创建新文件继续写入
* 对旧日志进行压缩、归档、清理

### **7️⃣ 轮转过程详细示意**

让我们详细看看轮转的每一步：

```
【初始状态】
app.log (100MB，正在写入，文件描述符 fd=3)

【触发轮转：文件达到 100MB】

步骤 1：重命名当前文件
app.log → app.log.1 (重命名，fd=3 仍然指向 app.log.1)

步骤 2：创建新文件
创建新的 app.log (空文件)

步骤 3：通知应用重新打开文件
发送信号（如 SIGHUP）给应用
应用关闭 fd=3，重新打开 app.log，获得新的 fd=4

步骤 4：压缩旧文件（可选）
app.log.1 → app.log.1.gz (压缩，节省空间)

【结果】
app.log (新文件，0MB，正在写入，fd=4)
app.log.1.gz (旧文件，压缩后 20MB，已归档)
```

### **8️⃣ 为什么需要重新打开文件**

**如果不重新打开文件会怎样？**

```
场景：轮转后不通知应用

1. app.log → app.log.1 (重命名)
2. 创建新的 app.log
3. 应用仍然通过 fd=3 写入

结果：
- 应用写入的数据进入 app.log.1（旧文件）
- 新的 app.log 是空的
- 日志写入到了错误的地方
```

**重新打开文件后：**
```
1. app.log → app.log.1 (重命名)
2. 创建新的 app.log
3. 发送信号给应用
4. 应用关闭旧文件，打开新文件
5. 应用通过新的文件描述符写入 app.log（正确）
```

### **9️⃣ 轮转触发条件详解**

日志轮转可以在以下条件下触发：

#### **按时间轮转**
* **daily（每天）**：每天午夜轮转
* **weekly（每周）**：每周轮转（通常是周日）
* **monthly（每月）**：每月第一天轮转
* **适合场景**：日志量相对稳定，需要按时间查找日志

#### **按大小轮转**
* **size 100M**：文件达到 100MB 时轮转
* **size 1G**：文件达到 1GB 时轮转
* **适合场景**：日志量不固定，可能突然增长

#### **按大小+时间轮转**
* **size 500M 或 daily**：满足任一条件就轮转
* **适合场景**：生产环境推荐，兼顾大小和时间

#### **手动触发**
* 通过命令手动触发轮转
* 用于测试或特殊情况

### **🔟 轮转后的处理操作**

#### **压缩（Compress）**
* **目的**：节省磁盘空间（通常可节省 70-90%）
* **工具**：gzip、bzip2、xz
* **时机**：立即压缩或延迟压缩（delaycompress）

**压缩效果示例：**
```
原始日志：100MB
压缩后：10-30MB（取决于日志内容）
节省空间：70-90%
```

#### **归档（Archive）**
* **目的**：将旧日志移动到指定目录保存
* **方式**：移动到 archive 目录，按日期组织
* **用途**：长期保存，便于查找

#### **删除（Delete）**
* **目的**：删除超过保留期的旧日志
* **策略**：按天数（maxHistory）或总大小（totalSizeCap）
* **注意**：确保重要日志已备份

#### **通知（Notification）**
* **目的**：轮转完成后通知管理员
* **方式**：邮件、告警、日志记录

---

## 三、核心概念：日志轮转的原理

### **1️⃣ 日志轮转的完整流程**

```
【监控阶段】
持续监控日志文件（大小、时间）

【触发阶段】
满足轮转条件（大小/时间）

【执行阶段】
1. 重命名当前日志文件
2. 创建新的日志文件
3. 通知应用重新打开文件
4. 压缩旧日志文件
5. 清理过期日志文件

【完成阶段】
记录轮转日志，发送通知
```

### **2️⃣ 轮转策略对比**

| 策略 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **按时间** | 便于按时间查找、日志量可控 | 可能单个文件过大 | 日志量稳定 |
| **按大小** | 防止文件过大、灵活 | 文件数量不可控 | 日志量波动大 |
| **按大小+时间** | 兼顾两者优点 | 配置复杂 | 生产环境推荐 |

### **3️⃣ 保留策略**

**保留策略决定保留多少历史日志：**

* **按数量（rotate）**：保留 N 个文件
  * 例如：`rotate 10` 保留 10 个文件
* **按天数（maxHistory）**：保留 N 天的日志
  * 例如：`maxHistory 30` 保留 30 天
* **按总大小（totalSizeCap）**：总大小不超过 N
  * 例如：`totalSizeCap 10GB` 总大小不超过 10GB

**推荐配置：**
```
保留天数：30 天（业务日志）
保留大小：10GB（总大小限制）
保留数量：10-30 个文件
```

---

## 四、Linux 系统工具：logrotate

### **1️⃣ logrotate 简介**

**logrotate** 是 Linux 系统自带的日志轮转工具，通过配置文件定义轮转规则。

**logrotate 的特点：**
* **系统自带**：大多数 Linux 发行版都预装了 logrotate
* **配置文件驱动**：通过配置文件定义轮转规则，无需编程
* **定时执行**：通过 cron 定时任务自动执行
* **灵活强大**：支持多种轮转策略和自定义脚本

### **2️⃣ 配置文件位置和结构**

#### **配置文件位置**

* **主配置文件**：`/etc/logrotate.conf`
  * 定义全局默认设置
  * 包含其他配置文件的引用
  
* **应用配置文件**：`/etc/logrotate.d/*`
  * 每个应用一个配置文件
  * 文件名通常与应用名相同

#### **配置文件结构**

```bash
# /etc/logrotate.conf（主配置）
# 全局默认设置
weekly          # 默认每周轮转
rotate 4        # 默认保留 4 个文件
create          # 默认创建新文件
compress        # 默认压缩

# 包含应用配置
include /etc/logrotate.d

# /etc/logrotate.d/myapp（应用配置）
/var/log/myapp/*.log {
    # 应用特定的配置
    # 会覆盖全局默认设置
}
```

#### **配置文件的优先级**

1. **应用配置** 覆盖 **全局配置**
2. **后面的配置** 覆盖 **前面的配置**
3. **具体配置** 覆盖 **通用配置**

### **3️⃣ 基本配置示例**

#### **示例 1：按大小轮转**

```bash
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    size 100M          # 文件达到 100MB 时轮转
    rotate 10         # 保留 10 个历史文件
    compress          # 压缩旧日志
    delaycompress     # 延迟压缩（压缩前一个文件）
    missingok         # 文件不存在时不报错
    notifempty        # 空文件不轮转
    create 0644 app app  # 创建新文件的权限和所有者
    postrotate        # 轮转后执行的命令
        /bin/kill -HUP `cat /var/run/myapp.pid 2> /dev/null` 2> /dev/null || true
    endscript
}
```

#### **示例 2：按时间轮转**

```bash
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily             # 每天轮转
    rotate 30         # 保留 30 天的日志
    compress          # 压缩
    dateext           # 使用日期作为后缀
    dateformat -%Y%m%d  # 日期格式
    missingok
    notifempty
    sharedscripts     # 所有文件轮转完再执行脚本
    postrotate
        systemctl reload myapp || true
    endscript
}
```

#### **示例 3：按大小和时间轮转**

```bash
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    size 500M         # 达到 500MB 或
    daily             # 每天轮转（满足任一条件）
    rotate 7          # 保留 7 个文件
    compress
    delaycompress
    missingok
    notifempty
    create 0644 app app
    sharedscripts
    postrotate
        /usr/bin/pkill -HUP -f myapp
    endscript
}
```

### **4️⃣ 常用配置参数详解**

| 参数 | 说明 | 示例 | 详细解释 |
|------|------|------|---------|
| `daily` | 每天轮转 | `daily` | 每天午夜（00:00）轮转一次 |
| `weekly` | 每周轮转 | `weekly` | 每周轮转一次（通常是周日） |
| `monthly` | 每月轮转 | `monthly` | 每月第一天轮转 |
| `size` | 按大小轮转 | `size 100M` | 文件达到指定大小时轮转，支持 K/M/G 单位 |
| `rotate` | 保留文件数 | `rotate 10` | 保留 N 个历史文件，超过的会被删除 |
| `compress` | 压缩旧日志 | `compress` | 使用 gzip 压缩旧日志文件 |
| `delaycompress` | 延迟压缩 | `delaycompress` | 延迟压缩，只压缩前一个文件（不压缩最新的旧文件） |
| `dateext` | 使用日期后缀 | `dateext` | 使用日期作为文件后缀，而不是数字 |
| `dateformat` | 日期格式 | `dateformat -%Y%m%d` | 日期格式，如 `-20251230` |
| `missingok` | 文件不存在不报错 | `missingok` | 如果日志文件不存在，不报错继续执行 |
| `notifempty` | 空文件不轮转 | `notifempty` | 如果日志文件为空，不进行轮转 |
| `create` | 创建新文件 | `create 0644 user group` | 创建新文件的权限、所有者、组 |
| `postrotate` | 轮转后执行脚本 | `postrotate ... endscript` | 轮转完成后执行的命令（通常用于通知应用） |
| `prerotate` | 轮转前执行脚本 | `prerotate ... endscript` | 轮转前执行的命令 |
| `sharedscripts` | 共享脚本 | `sharedscripts` | 所有文件轮转完再执行脚本（而不是每个文件都执行） |

### **5️⃣ 重要参数详解**

#### **compress vs delaycompress**

**compress（立即压缩）：**
```
轮转后：
app.log.1 → app.log.1.gz (立即压缩)
app.log.2 → app.log.2.gz (立即压缩)
```

**delaycompress（延迟压缩）：**
```
轮转后：
app.log.1 (不压缩，方便查看最新旧日志)
app.log.2 → app.log.2.gz (压缩)
app.log.3 → app.log.3.gz (压缩)
```

**为什么需要 delaycompress？**
* 最新的旧日志可能还需要查看
* 压缩后的文件需要解压才能查看
* 延迟压缩让最新旧日志保持可读

#### **create 参数详解**

```bash
create 0644 app app
```

**格式：** `create [权限] [所有者] [组]`

* **权限**：`0644` 表示 `rw-r--r--`（所有者可读写，其他人只读）
* **所有者**：新文件的所有者
* **组**：新文件的组

**为什么需要 create？**
* 轮转后创建的新文件需要正确的权限
* 确保应用可以写入新文件
* 避免权限问题导致日志写入失败

#### **postrotate 脚本的作用**

**为什么需要 postrotate？**

```
问题：轮转后应用还在写旧文件

原因：
1. 应用打开文件时获得文件描述符（fd=3）
2. 文件重命名后，fd=3 仍然指向旧文件
3. 应用继续通过 fd=3 写入旧文件

解决：
postrotate
    /bin/kill -HUP `cat /var/run/myapp.pid`
endscript

作用：
- 发送 SIGHUP 信号给应用
- 应用收到信号后重新打开日志文件
- 获得新的文件描述符，指向新文件
```

**常见的 postrotate 命令：**
```bash
# 方式 1：通过 PID 文件发送信号
/bin/kill -HUP `cat /var/run/myapp.pid`

# 方式 2：使用 systemd 重载
systemctl reload myapp

# 方式 3：使用 pkill
/usr/bin/pkill -HUP -f myapp

# 方式 4：重启服务（不推荐，会中断服务）
systemctl restart myapp
```

### **5️⃣ 测试和调试**

```bash
# 测试配置文件语法
sudo logrotate -d /etc/logrotate.d/myapp

# 强制执行轮转（测试）
sudo logrotate -f /etc/logrotate.d/myapp

# 查看执行日志
cat /var/lib/logrotate/status
```

### **6️⃣ logrotate 的工作原理**

#### **执行机制**

logrotate 通过 **cron** 定时任务执行：

```bash
# 查看 cron 任务
cat /etc/cron.daily/logrotate

# 内容
#!/bin/sh
/usr/sbin/logrotate /etc/logrotate.conf
EXITVALUE=$?
if [ $EXITVALUE != 0 ]; then
    /usr/bin/logger -t logrotate "ALERT exited abnormally with [$EXITVALUE]"
fi
exit 0
```

**执行流程：**
1. **cron 定时触发**：每天执行一次（默认）
2. **读取配置**：读取 `/etc/logrotate.conf` 和 `/etc/logrotate.d/*`
3. **检查条件**：检查每个日志文件是否满足轮转条件
4. **执行轮转**：满足条件的文件执行轮转
5. **记录状态**：将执行结果记录到 `/var/lib/logrotate/status`

#### **执行时机**

* **默认**：每天执行一次（通过 `/etc/cron.daily/logrotate`）
* **可调整**：可以修改 cron 任务调整执行频率
* **手动执行**：可以通过命令手动触发

#### **状态文件**

logrotate 会记录每个文件的最后轮转时间：

```bash
# 查看状态文件
cat /var/lib/logrotate/status

# 内容示例
logrotate state -- version 2
"/var/log/myapp/app.log" 2025-12-29-12:0:0
"/var/log/nginx/access.log" 2025-12-30-0:0:0
```

**作用：**
* 记录每个文件的最后轮转时间
* 判断是否满足时间轮转条件（如 daily）
* 避免重复轮转

#### **执行日志**

logrotate 的执行结果会记录到系统日志：

```bash
# 查看执行日志
grep logrotate /var/log/syslog

# 或
journalctl -u logrotate
```

---

## 五、Java 应用：Logback 日志轮转

### **1️⃣ Logback 简介**

**Logback** 是 Java 应用常用的日志框架，是 Log4j 的继任者，内置了强大的日志轮转功能。

**Logback 的特点：**
* **内置轮转**：不需要外部工具，框架自身支持轮转
* **配置灵活**：支持 XML 和 Groovy 配置
* **性能优秀**：异步写入、缓冲等优化
* **自动重载**：支持配置文件自动重载

**为什么 Java 应用需要框架级轮转？**
* **文件描述符管理**：框架自动处理文件重新打开
* **无缝切换**：轮转时应用无需重启
* **配置集中**：日志配置和应用配置在一起
* **跨平台**：不依赖操作系统工具

### **2️⃣ 配置文件示例**

#### **示例 1：按大小和时间轮转**

```xml
<!-- logback.xml -->
<configuration>
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <!-- 当前日志文件 -->
        <file>logs/app.log</file>
        
        <!-- 轮转策略 -->
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <!-- 历史日志文件命名模式 -->
            <fileNamePattern>logs/app.%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
            <!-- 单个文件最大大小 -->
            <maxFileSize>100MB</maxFileSize>
            <!-- 保留天数 -->
            <maxHistory>30</maxHistory>
            <!-- 总大小限制 -->
            <totalSizeCap>10GB</totalSizeCap>
        </rollingPolicy>
        
        <!-- 日志格式 -->
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <root level="INFO">
        <appender-ref ref="FILE" />
    </root>
</configuration>
```

#### **示例 2：按大小轮转**

```xml
<configuration>
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/app.log</file>
        
        <rollingPolicy class="ch.qos.logback.core.rolling.FixedWindowRollingPolicy">
            <fileNamePattern>logs/app.%i.log.gz</fileNamePattern>
            <minIndex>1</minIndex>
            <maxIndex>10</maxIndex>
        </rollingPolicy>
        
        <triggeringPolicy class="ch.qos.logback.core.rolling.SizeBasedTriggeringPolicy">
            <maxFileSize>100MB</maxFileSize>
        </triggeringPolicy>
        
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <root level="INFO">
        <appender-ref ref="FILE" />
    </root>
</configuration>
```

#### **示例 3：按时间轮转**

```xml
<configuration>
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/app.log</file>
        
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>logs/app.%d{yyyy-MM-dd}.log.gz</fileNamePattern>
            <maxHistory>30</maxHistory>
            <totalSizeCap>10GB</totalSizeCap>
        </rollingPolicy>
        
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <root level="INFO">
        <appender-ref ref="FILE" />
    </root>
</configuration>
```

### **3️⃣ 常用配置参数详解**

| 参数 | 说明 | 示例 | 详细解释 |
|------|------|------|---------|
| `fileNamePattern` | 历史文件命名模式 | `logs/app.%d{yyyy-MM-dd}.%i.log.gz` | 定义历史日志文件的命名规则，支持日期和索引 |
| `maxFileSize` | 单个文件最大大小 | `100MB` | 单个日志文件的最大大小，超过后轮转 |
| `maxHistory` | 保留天数 | `30` | 保留多少天的历史日志，超过的会被删除 |
| `totalSizeCap` | 总大小限制 | `10GB` | 所有日志文件的总大小限制，超过后删除最旧的 |
| `minIndex` | 最小索引 | `1` | 索引号的最小值（FixedWindowRollingPolicy） |
| `maxIndex` | 最大索引 | `10` | 索引号的最大值，超过后删除最旧的 |

### **4️⃣ 日期格式说明**

**fileNamePattern 中的格式符：**

| 格式 | 说明 | 示例 | 生成的文件名 |
|------|------|------|------------|
| `%d{yyyy-MM-dd}` | 日期 | `%d{yyyy-MM-dd}` | `app.2025-12-30.log` |
| `%d{yyyy-MM-dd HH}` | 日期+小时 | `%d{yyyy-MM-dd HH}` | `app.2025-12-30-14.log` |
| `%d{yyyy-MM-dd HH:mm}` | 日期+小时+分钟 | `%d{yyyy-MM-dd HH:mm}` | `app.2025-12-30-14-30.log` |
| `%i` | 索引号 | `%i` | `app.0.log`, `app.1.log` |
| `.gz` | 压缩后缀 | `.gz` | 自动压缩为 gzip 格式 |

**组合使用示例：**
```
logs/app.%d{yyyy-MM-dd}.%i.log.gz
生成：logs/app.2025-12-30.0.log.gz
     logs/app.2025-12-30.1.log.gz
     logs/app.2025-12-29.0.log.gz
```

### **5️⃣ 轮转策略详解**

#### **SizeAndTimeBasedRollingPolicy（大小+时间）**

**特点：**
* 同时支持按大小和时间轮转
* 满足任一条件就轮转
* 文件名包含日期和索引

**工作原理：**
```
初始：app.log (0MB)

写入到 100MB：
app.log → app.2025-12-30.0.log (重命名)
创建新的 app.log

同一天内再次达到 100MB：
app.log → app.2025-12-30.1.log (重命名)
创建新的 app.log

第二天（即使文件很小）：
app.log → app.2025-12-31.0.log (按时间轮转)
创建新的 app.log
```

#### **FixedWindowRollingPolicy（固定窗口）**

**特点：**
* 只按大小轮转
* 使用索引号（1, 2, 3...）
* 超过最大索引后，删除最旧的

**工作原理：**
```
maxIndex=3

app.log → app.1.log
app.1.log → app.2.log
app.2.log → app.3.log
app.3.log → 删除（超过 maxIndex）
```

#### **TimeBasedRollingPolicy（时间）**

**特点：**
* 只按时间轮转
* 文件名包含日期
* 适合日志量稳定的场景

**工作原理：**
```
每天午夜轮转：
app.log → app.2025-12-30.log
创建新的 app.log
```

---

## 五、Java 应用：Log4j2 日志轮转

### **1️⃣ Log4j2 简介**

**Log4j2** 是 Apache 的日志框架，也支持强大的日志轮转功能。

### **2️⃣ 配置文件示例**

#### **示例 1：按大小和时间轮转**

```xml
<!-- log4j2.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
    <Appenders>
        <RollingFile name="RollingFile" fileName="logs/app.log"
                     filePattern="logs/app-%d{yyyy-MM-dd}-%i.log.gz">
            <PatternLayout>
                <Pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n</Pattern>
            </PatternLayout>
            <Policies>
                <!-- 按时间轮转 -->
                <TimeBasedTriggeringPolicy />
                <!-- 按大小轮转 -->
                <SizeBasedTriggeringPolicy size="100MB" />
            </Policies>
            <!-- 保留文件数 -->
            <DefaultRolloverStrategy max="30" />
        </RollingFile>
    </Appenders>
    
    <Loggers>
        <Root level="INFO">
            <AppenderRef ref="RollingFile" />
        </Root>
    </Loggers>
</Configuration>
```

#### **示例 2：按大小轮转**

```xml
<Configuration status="WARN">
    <Appenders>
        <RollingFile name="RollingFile" fileName="logs/app.log"
                     filePattern="logs/app-%i.log.gz">
            <PatternLayout>
                <Pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n</Pattern>
            </PatternLayout>
            <Policies>
                <SizeBasedTriggeringPolicy size="100MB" />
            </Policies>
            <DefaultRolloverStrategy max="10" />
        </RollingFile>
    </Appenders>
    
    <Loggers>
        <Root level="INFO">
            <AppenderRef ref="RollingFile" />
        </Root>
    </Loggers>
</Configuration>
```

### **3️⃣ 常用配置参数**

| 参数 | 说明 | 示例 |
|------|------|------|
| `fileName` | 当前日志文件 | `logs/app.log` |
| `filePattern` | 历史文件命名模式 | `logs/app-%d{yyyy-MM-dd}-%i.log.gz` |
| `SizeBasedTriggeringPolicy` | 按大小触发 | `<SizeBasedTriggeringPolicy size="100MB" />` |
| `TimeBasedTriggeringPolicy` | 按时间触发 | `<TimeBasedTriggeringPolicy />` |
| `max` | 保留文件数 | `max="30"` |

---

## 六、Python 应用：日志轮转

### **1️⃣ 使用 logging.handlers**

Python 标准库提供了日志轮转功能。

#### **示例 1：按大小轮转**

```python
import logging
from logging.handlers import RotatingFileHandler

# 创建轮转处理器
handler = RotatingFileHandler(
    'app.log',
    maxBytes=100 * 1024 * 1024,  # 100MB
    backupCount=10  # 保留 10 个备份文件
)

# 设置格式
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

# 配置 logger
logger = logging.getLogger('myapp')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# 使用
logger.info('This is a log message')
```

#### **示例 2：按时间轮转**

```python
import logging
from logging.handlers import TimedRotatingFileHandler

# 创建时间轮转处理器
handler = TimedRotatingFileHandler(
    'app.log',
    when='midnight',  # 每天午夜轮转
    interval=1,  # 间隔 1 天
    backupCount=30  # 保留 30 天
)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

logger = logging.getLogger('myapp')
logger.setLevel(logging.INFO)
logger.addHandler(handler)
```

### **2️⃣ 时间轮转参数**

| 参数 | 说明 | 示例 |
|------|------|------|
| `when='S'` | 秒 | `when='S', interval=60` |
| `when='M'` | 分钟 | `when='M', interval=60` |
| `when='H'` | 小时 | `when='H', interval=24` |
| `when='D'` | 天 | `when='D', interval=1` |
| `when='midnight'` | 每天午夜 | `when='midnight'` |
| `when='W0'` | 每周一 | `when='W0'` |

---

## 七、Node.js 应用：日志轮转

### **1️⃣ 使用 winston-daily-rotate-file**

```bash
npm install winston winston-daily-rotate-file
```

#### **配置示例**

```javascript
const winston = require('winston');
const DailyRotateFile = require('winston-daily-rotate-file');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new DailyRotateFile({
            filename: 'logs/app-%DATE%.log',
            datePattern: 'YYYY-MM-DD',
            maxSize: '100m',
            maxFiles: '30d',  // 保留 30 天
            zippedArchive: true  // 压缩旧日志
        })
    ]
});

logger.info('This is a log message');
```

---

## 八、最佳实践

### **1️⃣ 轮转策略选择**

#### **按大小轮转**
* ✅ **适合**：日志量不固定，可能突然增长
* ✅ **优点**：防止单个文件过大
* ⚠️ **注意**：需要合理设置大小阈值

#### **按时间轮转**
* ✅ **适合**：日志量相对稳定
* ✅ **优点**：便于按时间查找日志
* ⚠️ **注意**：需要合理设置保留天数

#### **按大小+时间轮转**
* ✅ **适合**：生产环境推荐
* ✅ **优点**：兼顾大小和时间
* ⚠️ **注意**：配置相对复杂

### **2️⃣ 保留策略**

```bash
# 推荐配置
保留天数：30 天（业务日志）
保留大小：10GB（总大小限制）
保留数量：10-30 个文件
```

### **3️⃣ 压缩策略**

* ✅ **启用压缩**：节省 70-90% 的磁盘空间
* ✅ **延迟压缩**：压缩前一个文件，当前文件不压缩
* ⚠️ **注意**：压缩会增加 CPU 使用，但节省磁盘空间

### **4️⃣ 文件命名规范**

```bash
# 推荐命名格式
app-2025-12-30-0.log.gz
app-2025-12-30-1.log.gz
app-2025-12-30-2.log.gz

# 包含信息
- 应用名
- 日期
- 索引号
- 压缩后缀
```

### **5️⃣ 目录结构**

```bash
logs/
├── app.log              # 当前日志
├── app-2025-12-30-0.log.gz
├── app-2025-12-30-1.log.gz
├── app-2025-12-29-0.log.gz
└── archive/             # 归档目录（可选）
    └── app-2025-12-01-0.log.gz
```

### **6️⃣ 监控和告警**

```bash
# 监控日志目录大小
du -sh /var/log/myapp/

# 监控日志文件数量
ls -1 /var/log/myapp/*.log* | wc -l

# 设置告警
if [ $(du -sm /var/log/myapp | cut -f1) -gt 10000 ]; then
    echo "Log directory exceeds 10GB" | mail -s "Alert" admin@example.com
fi
```

### **7️⃣ 应用重启处理**

```bash
# logrotate postrotate 脚本示例
postrotate
    # 发送信号让应用重新打开日志文件
    /bin/kill -HUP `cat /var/run/myapp.pid 2> /dev/null` 2> /dev/null || true
    
    # 或者使用 systemd
    systemctl reload myapp || true
endscript
```

### **8️⃣ 常见问题排查**

#### **问题 1：日志轮转后应用还在写旧文件**

**原因：** 应用没有重新打开日志文件

**解决：** 在 postrotate 脚本中发送信号让应用重新打开文件

```bash
postrotate
    /bin/kill -HUP `cat /var/run/myapp.pid`
endscript
```

#### **问题 2：磁盘空间仍然不足**

**原因：** 保留策略设置过大

**解决：** 调整保留天数或总大小限制

```bash
rotate 7          # 减少保留天数
totalSizeCap 5GB  # 设置总大小限制
```

#### **问题 3：轮转不生效**

**原因：** 配置文件语法错误或权限问题

**解决：** 检查配置和权限

```bash
# 测试配置
logrotate -d /etc/logrotate.d/myapp

# 检查权限
ls -l /var/log/myapp/
```

---

## 九、完整配置示例

### **1️⃣ logrotate 完整配置**

```bash
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    # 轮转策略
    size 500M
    daily
    rotate 30
    
    # 压缩
    compress
    delaycompress
    compresscmd /bin/gzip
    uncompresscmd /bin/gunzip
    compressext .gz
    
    # 文件处理
    missingok
    notifempty
    create 0644 app app
    
    # 日期后缀
    dateext
    dateformat -%Y%m%d
    
    # 脚本
    sharedscripts
    postrotate
        /bin/kill -HUP `cat /var/run/myapp.pid 2> /dev/null` 2> /dev/null || true
    endscript
}
```

### **2️⃣ Logback 完整配置**

```xml
<configuration>
    <property name="LOG_HOME" value="/var/log/myapp" />
    <property name="LOG_PATTERN" value="%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{50} - %msg%n" />
    
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_HOME}/app.log</file>
        
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>${LOG_HOME}/app.%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
            <maxFileSize>500MB</maxFileSize>
            <maxHistory>30</maxHistory>
            <totalSizeCap>10GB</totalSizeCap>
        </rollingPolicy>
        
        <encoder>
            <pattern>${LOG_PATTERN}</pattern>
        </encoder>
    </appender>
    
    <appender name="ERROR_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_HOME}/error.log</file>
        <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
            <level>ERROR</level>
        </filter>
        
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>${LOG_HOME}/error.%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
            <maxFileSize>100MB</maxFileSize>
            <maxHistory>90</maxHistory>
            <totalSizeCap>5GB</totalSizeCap>
        </rollingPolicy>
        
        <encoder>
            <pattern>${LOG_PATTERN}</pattern>
        </encoder>
    </appender>
    
    <root level="INFO">
        <appender-ref ref="FILE" />
        <appender-ref ref="ERROR_FILE" />
    </root>
</configuration>
```

---

## 十、总结

### **核心要点**

1. **日志轮转是必须的**：防止日志文件无限增长
2. **选择合适的策略**：按大小、按时间或两者结合
3. **合理设置保留策略**：平衡存储成本和历史追溯需求
4. **启用压缩**：大幅节省磁盘空间
5. **处理应用重启**：确保轮转后应用正常写入

### **推荐配置**

```bash
# 通用推荐
轮转条件：大小 500MB 或 每天
保留策略：30 天或 10GB
压缩：启用
文件命名：包含日期和索引
```

### **工具选择**

| 场景 | 推荐工具 |
|------|---------|
| Linux 系统日志 | logrotate |
| Java 应用 | Logback / Log4j2 |
| Python 应用 | logging.handlers |
| Node.js 应用 | winston-daily-rotate-file |

---

### 💡 延伸阅读

- [logrotate 官方文档](https://linux.die.net/man/8/logrotate)
- [Logback 官方文档](http://logback.qos.ch/documentation.html)
- [Log4j2 官方文档](https://logging.apache.org/log4j/2.x/manual/index.html)
- [Python logging 文档](https://docs.python.org/3/library/logging.handlers.html)

---

**如果你觉得这篇文章有用，欢迎收藏！下次遇到日志管理问题时，拿出来对照一下，就能快速配置专业的日志轮转策略。**

