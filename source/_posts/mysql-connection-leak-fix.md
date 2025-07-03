---
title: 🐛一次数据库连接数暴涨的排查实录：我在测试平台踩的坑
date: 2025-06-30 15:29:25
tags:
  - MySQL
  - 数据库连接
  - 连接泄露
  - 连接池
  - SQLAlchemy
categories: 项目实战 & 测试经验（Testing Practices & Case Studies）
updated: {{current_date_time}}
keywords: MySQL, 数据库连接, 连接泄露, 连接池, SQLAlchemy
description: '记录一次测试平台中 MySQL 连接数暴涨问题的排查过程，分享使用连接池和自动释放机制解决连接泄露的方案，并给出优化建议！'
top_img: /img/mysql-connection-leak-fix.png
cover: /img/mysql-connection-leak-fix.png
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
abcjs: false
noticeOutdate: falsetags
---


# 🐛一次数据库连接数暴涨的排查实录：我在测试平台踩的坑

> 在开发测试平台的过程中，我遇到一次 **MySQL 连接数暴涨** 并引发服务报错的线上问题。排查后发现，是因为部分代码在使用数据库连接后 **未显式断开**，导致连接不断累积。本文记录这个从“出问题”到“彻底解决”的过程。

---

## 一、现象：MySQL 报错 Too many connections

平台部署后运行一段时间，日志频繁出现如下报错：

```bash
pymysql.err.OperationalError: (1040, 'Too many connections')
```

通过登录 MySQL 执行以下命令查看连接数：

```sql
SHOW STATUS LIKE 'Threads_connected';
```

发现连接数达到了 150+，已经逼近 MySQL 配置的最大连接数（默认为 151）！

而实际上平台此时访问量并不大，很可能是代码中连接未及时关闭。

---

## 二、问题定位：数据库连接未释放

我检查了部分数据库操作代码，发现如下问题：

```python
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='xxx', db='test')
cursor = conn.cursor()
cursor.execute("SELECT * FROM test_case")
result = cursor.fetchall()
# ❌ 没有 conn.close()，也没有 cursor.close()
```

这些连接在任务执行后 **未被关闭**，导致连接不断积压，最终耗尽数据库可用连接资源。

---

## 三、解决方案：连接池 + 自动释放机制

### ✅ 1. 使用连接池管理 MySQL 连接

我们引入了 `SQLAlchemy` 创建连接池来复用连接资源，控制连接总数：

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "mysql+pymysql://root:password@localhost:3306/test",
    pool_size=10,        # 保持的连接池大小
    max_overflow=5,      # 最大溢出连接数（总共最多15个连接）
    pool_recycle=1800,   # 自动回收空闲连接（秒）
    pool_pre_ping=True   # 检查连接可用性
)

Session = sessionmaker(bind=engine)
```

这样就能 **自动维护连接数量，避免频繁创建与泄露**。

---

### ✅ 2. 使用 with 自动管理连接释放

我们统一将数据库操作封装为上下文管理器形式，让连接在退出作用域后自动释放：

```python
def get_test_cases():
    with engine.connect() as conn:
        result = conn.execute("SELECT * FROM test_case")
        return result.fetchall()
```

或者使用 ORM：

```python
def add_case(data):
    with Session() as session:
        new_case = TestCase(**data)
        session.add(new_case)
        session.commit()
```

这样可以保证：

* 即使中间发生异常，连接也能被正常释放
* 没有手动 close() 也不会泄露资源

---

## 四、优化建议：记录数据库操作日志

为方便排查数据库问题，我们为关键操作加上了**数据库操作日志**，包括：

* 执行时间戳
* SQL 内容（脱敏处理）
* 执行是否成功
* 异常信息（如有）

示例代码如下：

```python
import logging

logger = logging.getLogger("db")

def safe_query(sql):
    try:
        logger.info(f"[SQL] 执行：{sql}")
        with engine.connect() as conn:
            result = conn.execute(sql)
            logger.info("[SQL] 执行成功")
            return result.fetchall()
    except Exception as e:
        logger.error(f"[SQL] 执行失败: {e}")
        raise
```

这为后续排查 SQL 性能问题、错误日志等提供了有力支持。

---

## 五、总结：三个教训

1. **MySQL 有连接数上限**（默认151），一旦泄露很容易导致服务崩溃；
2. **不要相信开发自己会记得手动关闭连接**，一劳永逸的办法是使用 `with` 自动释放；
3. **日志是定位问题的利器**，尤其是数据库类问题。

---

## 🧩 Checklist：MySQL 编程实践建议

* [x] 使用连接池限制最大连接数
* [x] 所有连接都使用 `with` 包裹
* [x] 记录每次数据库操作日志（SQL + 时间 + 结果）
* [x] 设置 `pool_recycle` 避免 MySQL 自动断开空闲连接
* [x] 对异常处理时也确保连接被释放

---

> 你遇到过类似数据库连接爆满的问题吗？欢迎评论区一起交流！

