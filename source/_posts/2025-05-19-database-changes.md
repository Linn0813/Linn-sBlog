---
title: 手把手教你：数据库新增字段与调整唯一约束实战指南 📚
date: 2025-05-19 17:47:59
updated: {{current_date_time}} 
categories:
  - 自动化测试与工具开发 / Test Automation & Tool Development
  - 工具与平台开发 / Tools & Platform Development
  - 数据库设计与维护 / Database Design & Maintenance
tags:
  - 数据库维护
  - MySQL
  - 字段新增
  - 唯一约束调整
  - 自动化测试平台
keywords: 数据库维护, MySQL, 新增字段, 调整唯一约束, 自动化测试平台
description: '以实际项目为例，详细介绍自动化测试平台数据库新增 `is_del` 字段、调整 `username` 唯一约束的全流程，包含需求分析、SQL 操作步骤、应用代码修改及测试验证。'
top_img: /img/database-changes.png
comments: true  
cover: /img/database-changes.png
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
abcjs: false  
noticeOutdate: false 
---

# 手把手教你：数据库新增字段与调整唯一约束实战指南 📚

在数据库的日常维护和功能扩展中，我们常常会遇到需要新增字段和调整唯一约束的情况。就像我最近在自动化测试平台项目中就碰到了这样的问题，现在我就把整个解决过程分享给大家，希望能帮助大家在遇到类似场景时顺利应对。

## 一、新增 `is_del` 字段：为用户权限管理添砖加瓦 🧱

### 需求背景：灵活控制用户权限的钥匙 🔑
在我们的自动化测试平台里，有这样一个需求：要能够灵活地收回用户的权限，但又不想直接删除用户数据。这就好比我们有一个房间，虽然暂时不想让某些人进去，但又不想把他们的信息从入住记录里完全删掉。这时候，添加一个 `is_del` 字段到用户表（`users`）中就成了一个很好的解决方案。通过设置这个字段的值，比如 0 表示正常，1 表示权限已收回，我们就可以轻松地控制用户的访问权限，就像给房间的门装了一把灵活的锁。

### 操作步骤：SQL 语句实现字段添加 💻
在 MySQL 中，我们可以使用 `ALTER TABLE` 语句来完成这个操作。具体的 SQL 语句如下：
```sql
-- 在 users 表中添加 is_del 字段，初始值为 0 表示正常
ALTER TABLE users
ADD COLUMN is_del TINYINT(1) DEFAULT 0 NOT NULL;
```
#### 代码解释 📝
- `ALTER TABLE users`：告诉数据库我们要对 `users` 表进行修改。
- `ADD COLUMN is_del`：表示我们要在这个表中添加一个名为 `is_del` 的字段。
- `TINYINT(1)`：指定了 `is_del` 字段的数据类型为 `TINYINT`，括号里的 1 表示这个字段占用 1 个字节的存储空间，通常用来存储布尔值或者小整数。
- `DEFAULT 0`：设置该字段的默认值为 0，也就是说新添加的用户默认处于正常状态。
- `NOT NULL`：表示这个字段不能为空，确保每条记录都有一个明确的 `is_del` 值。

#### 可能遇到的问题及解决办法 ❓
- **权限问题**：如果执行这条 SQL 语句时提示没有足够的权限，你需要联系数据库管理员，让他们给你分配相应的权限。
- **表结构冲突**：如果表中已经存在名为 `is_del` 的字段，就会出现冲突。这时你需要先检查并删除或者重命名已有的字段。

## 二、调整 `username` 唯一约束：解决注册与权限管理的矛盾 🤝

### 问题分析：唯一约束带来的注册难题 🚧
在之前的数据库设计中，为了确保每个用户名在系统中是唯一的，我们把 `username` 字段设置成了唯一约束。但当我们添加了 `is_del` 字段用于标识用户权限状态后，就出现了一个问题：已删除用户的用户名在重新注册时无法使用。这就好比一个人退房后，他的房间号就不能再被其他人使用了，显然这不符合我们的业务需求。所以，我们需要对 `username` 唯一约束进行调整。

### 操作步骤：取消 `username` 唯一约束 💾
在 MySQL 中，我们可以使用 `ALTER TABLE` 语句来取消 `username` 字段的唯一约束。具体的 SQL 语句如下：
```sql
-- 取消 users 表中 username 字段的唯一约束
ALTER TABLE users
DROP INDEX username;
```
#### 代码解释 📝
- `ALTER TABLE users`：同样是告诉数据库我们要对 `users` 表进行修改。
- `DROP INDEX username`：表示要删除 `username` 字段上的唯一索引，也就是取消它的唯一约束。

#### 可能遇到的问题及解决办法 ❓
- **索引不存在**：如果执行这条语句时提示索引不存在，可能是之前没有为 `username` 字段创建唯一索引，或者索引名称不是 `username`。你需要先确认索引的实际名称。
- **数据一致性问题**：取消唯一约束后，可能会出现重复的用户名。为了保证正常用户的用户名仍然唯一，我们需要在应用程序层面进行额外的逻辑处理。

### 应用程序代码修改：确保数据一致性 🖥️
取消 `username` 唯一约束后，我们要在应用程序里添加一些逻辑来保证正常用户的用户名唯一性。以下是一些示例代码：

#### 1. 用户表结构更新（新增角色和软删除字段） 📄
```python
# 修改用户表结构，增加 role 和 is_del 字段
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20),              -- 角色字段，默认为 Normal
    is_del TINYINT(1) DEFAULT 0    -- 软删除标志，默认未删除
);
```
#### 代码解释 📝
这里我们不仅添加了 `is_del` 字段，还新增了 `role` 字段，用于标识用户的角色。这样可以让我们对用户进行更细致的管理。

#### 2. 注册用户时默认插入角色和软删除状态 📝
```python
# 在注册用户时，默认插入角色为 "Normal"，is_del 为 0（未删除）
cursor.execute('INSERT INTO users (username, password, role, is_del) VALUES (%s, %s, %s, %s)', 
               (username, hashed, "Normal", 0))
```
#### 代码解释 📝
在用户注册时，我们将用户的角色默认设置为 "Normal"，并将 `is_del` 字段的值设置为 0，表示用户处于正常状态。这样可以保证新注册的用户有一个明确的角色和状态。

#### 3. 查询用户时增加软删除判断 🔎
```python
# 查询用户时过滤掉已软删除的记录
cursor.execute('SELECT * FROM users WHERE username = %s AND is_del = 0', (username,))
```
#### 代码解释 📝
在查询用户信息时，我们增加了对 `is_del` 字段的判断，只返回 `is_del` 为 0 的用户记录，即正常状态的用户。这样可以确保我们查询到的用户都是有效的。

## 三、测试与验证：确保修改万无一失 ✅
在完成数据库表结构的修改和应用程序代码的修改后，我们需要进行全面的测试和验证，以确保这些修改的正确性和稳定性。以下是一些可以进行的测试：

### 1. 新用户注册测试 🆕
注册一个新用户，验证用户名是否唯一（仅检查 `is_del` 为 0 的用户）。如果注册成功，说明我们在应用程序层面的逻辑处理起到了作用，保证了正常用户的用户名唯一性。

### 2. 已删除用户用户名重新注册测试 🗑️
注册一个已删除用户的用户名，验证是否可以成功注册。如果可以成功注册，说明我们取消 `username` 唯一约束的操作达到了预期效果。

### 3. 用户登录测试 🔑
登录不同状态的用户，验证登录逻辑是否正确。确保正常用户可以顺利登录，而权限已收回的用户无法登录。

通过以上这些步骤和测试，我们就可以在数据库中成功新增字段和调整唯一约束，解决实际业务中遇到的问题。希望大家在遇到类似场景时，能够参考这个指南，轻松应对。 🚀