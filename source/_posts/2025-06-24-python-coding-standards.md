---
title: 🐍写好 Python 的第一步：一份通俗易懂又不啰嗦的编码规范指南 ✨
date: 2025-06-24 15:24:11
tags:
  - Python
  - 编码规范
  - 编程指南
categories:
  - 技术学习 & 行业趋势（Learning & Industry Trends）
  - 开发实践
  - 编程规范
updated: {{current_date_time}}
keywords: Python, 编码规范, 编程指南
description: '分享Python关键编码规范，涵盖命名、缩进、注释、导入、函数设计等方面，适合初学者和项目开发者参考。'
top_img: /img/python-coding-standards.png
cover: /img/python-coding-standards.png
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

# 🐍写好 Python 的第一步：一份通俗易懂又不啰嗦的编码规范指南 ✨

> 💡“一份靠谱的代码规范，不仅让团队协作更顺畅，也能帮你未来不被自己写的代码气哭。”

作为一个经历过「昨天写的代码今天看不懂」的 Python 开发者，我深刻体会到什么叫“规范是自由的前提”。今天这篇文章，我想以分享的角度，带你快速了解并掌握 Python 中最关键的编码规范，包括命名、缩进、注释、导入、函数设计等。无论你是初学者，还是正在做项目的开发者，都能从中找到值得优化的地方。

---

## 1️⃣ 代码编码格式：请从 UTF-8 开始 👊

Python 默认使用 ASCII 编码，一旦代码中包含中文或特殊字符就很容易报错。因此，一定要在代码开头加上这句：

```python
# -- coding: utf-8 --
```

这不是装饰，这是你代码能跑的保证🔥。

---

## 2️⃣ 命名规范：统一风格，读你千遍也不厌倦 🧠

不同类型的对象有不同的命名方式，记住这几条就够用了：

| 类型       | 命名规范                    | 示例                     |
| -------- | ----------------------- | ---------------------- |
| 项目名 / 类名 | 大驼峰命名（首字母大写）            | `TestCase` |
| 包名 / 模块名 | 小写字母 + 下划线              | `user_manage.py`       |
| 变量名      | 小写字母 + 下划线              | `file_path`            |
| 常量       | 全部大写 + 下划线              | `COLOR_WHITE`          |
| 私有变量     | `_xxx` 或 `__xxx`（前缀下划线） | `_token`, `__id`       |
| 专有变量     | `__xxx__`               | `__init__`, `__doc__`  |
| 函数名      | 小写字母 + 下划线              | `get_user_name()`      |

📌 Tip：不要随便混用风格，代码风格杂乱是团队协作最大雷区之一。

---

## 3️⃣ 缩进规范：靠对齐才能走得更远 🧱

Python 是靠缩进来分清代码结构的，不像 Java 和 C 那样有大括号，所以“对齐”就成了圣旨！

* 每层缩进用 **4 个空格**
* 不要混用 Tab 和空格（会爆炸）
* 所有流程控制语句（if、for、def 等）后面记得加冒号 `:`

```python
def say_hello(name):
    if name:
        print(f"Hello, {name}!")
```

一眼下去，结构清晰；缩进乱了，Bug满天飞🌪️。

---

## 4️⃣ 注释规范：未来的你会感谢现在的你 📝

有三种注释方式：

### 🔹 行注释（代码后跟注释）

```python
count += 1  # 计数器加一
```

👉 行内注释和代码之间要有 **两个空格**

### 🔹 块注释（解释代码段目的）

```python
# 对用户信息进行校验
# 包括用户名、邮箱和密码格式
check_user_info(data)
```

### 🔹 文档注释（用于函数、类、模块的说明）

```python
def login(username, password):
    """
    登录接口
    :param username: 用户名
    :param password: 密码
    """
```

✍️ 写注释的诀窍是：“解释你为什么这么写”，而不是“你写了什么”。

---

## 5️⃣ 空行使用：给代码透透气 🧘‍♀️

* 顶层函数和类之间空两行
* 类中方法之间空一行
* 函数内部逻辑上有分隔需求时空一行，但别空太多

```python
class User:
    def __init__(self):
        pass

    def login(self):
        pass
```

空行 ≠ 空白，空行代表“逻辑的停顿感”，让代码更有节奏🎵。

---

## 6️⃣ 引号使用规范：别让引号打架 🗣️

* 自然语言用 **双引号**，机器标识用 **单引号**
* 正则表达式也用双引号
* 文档注释用 `""" 三个双引号 """`

保持同文件中风格一致即可，例如：

```python
name = "RingConn"
token = 'abc123'
pattern = r"\d+"
```

---

## 7️⃣ 模块导入：从通用到专用 📦

导入顺序推荐如下：

```python
# 标准库
import os
import sys

# 第三方库
import requests

# 本地模块
import my_app.settings
```

✅ 每个导入独占一行
❌ 不推荐：`import os, sys`

⚠️ 别用 `from xxx import *`，一看就没读规范手册。

---

## 8️⃣ main 函数：模块自测靠它守门 🚪

每个可执行脚本都应该包含：

```python
if __name__ == '__main__':
    main()
```

这样模块在被导入时不会误执行主逻辑，同时也方便写测试。

---

## 9️⃣ 函数设计规范：写出好函数的秘诀🧩

好函数的标准是：**短小、专一、独立**。

* 函数尽量控制在一屏之内
* 不要嵌套太深（≤3层）
* 参数少而清晰，默认值要合理
* 使用 return 明确输出
* 减少对全局变量的依赖

一个函数一件事，代码才容易测试、复用、重构，不然写一天，改三天😭。

---

## 🔟 分号不要乱加 🤦‍♀️

Python 不需要行尾分号。也别把两句代码写在一行，用分号分开，太难读。

```python
# 错误示范：
x = 1; y = 2

# 推荐写法：
x = 1
y = 2
```

---

## 🔠 每行不超 80 字：真的不是为了美观

* Python 社区一直推荐 80 字以内一行
* 特殊情况除外：比如 URL、长模块导入等
* 不要用反斜杠续行，可以使用括号隐式连接

```python
result = (
    long_variable_name_1
    + long_variable_name_2
    + long_variable_name_3
)
```

---

## 🧾 总结一句话：

> 编码规范是代码的“体面”，也是你在团队中的“标签”。

遵循一套规范，代码更可读、可维护、可扩展。对于个人而言，养成好习惯，对日后的职业发展也是一大助力。

---

💬 **最后的话**

欢迎把这份 Python 编码规范收藏在你的工具库，也欢迎分享给你的小伙伴。

