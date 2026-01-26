---
title: "🗺️ 用 Python 操作 XMind：从读懂到生成的完整入门指南"
date: 2026-01-21 15:00:00
updated: {{current_date_time}}
categories:
  - 🏗️ 测试平台开发实战手记
  - 测试开发工具
tags:
  - Python
  - XMind
  - 测试自动化
  - 脑图生成
  - XML/JSON
keywords: Python操作XMind, xmindparser, xmind-sdk-python, 脑图自动生成, 测试用例导出, content.json, content.xml
description: '深入解析 XMind 文件底层结构，覆盖 XMind 8 (XML) 与 XMind 2024 (JSON) 两种架构，手把手教你如何用 Python 读取、修改并自动生成思维导图。'
top_img: /img/python-xmind-operation-guide.png
cover: /img/python-xmind-operation-guide.png
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

# 🧠 用 Python 操作 XMind：从读懂到生成的完整入门指南

很多人都会用 XMind 画思维导图，但一旦进入“工程化”阶段，往往会遇到这些问题：

* 想把 XMind 转成 Markdown / CSV / 测试用例
* 想根据 Excel、接口数据自动生成一份脑图
* 想在测试平台或内部工具中实现“一键导出 .xmind 文件”

这篇文章的目标很明确：

> **讲清楚 XMind 文件是什么、它在程序中长什么样，以及如何用 Python 读取和生成 XMind 文件。**

---

## 1. XMind 文件是什么

在写任何代码之前，首先要回答一个问题：**XMind 文件在技术层面到底是什么？**

### 1.1 `.xmind` 的本质

`.xmind` 文件本质上是一个 **ZIP 压缩包**。

你可以直接验证：将 `demo.xmind` 重命名为 `demo.zip` 并解压查看内容。

需要特别注意的是，不同版本的 XMind，核心内容文件并不相同：

* **XMind 8（经典版 / Legacy）**：主要内容在 `content.xml`
* **XMind Zen / 2024（新版）**：主要内容在 `content.json`

> 换句话说，真正的思维导图结构，一定存在于 XML 或 JSON 文件中。

---

## 2. XMind 的数据结构

理解 XMind 的第二步，是理解它在程序中的数据形态。

### 2.1 思维导图是一棵树

无论底层是 XML 还是 JSON，XMind 在逻辑上都是一棵**树结构（Tree）**。

例如，一个简单的脑图：

```text
测试计划
 ├── 功能测试
 │    ├── 登录
 │    └── 注册
 └── 性能测试
```

在 Python 中，可以用类似下面的结构表示：

```python
{
  "title": "测试计划",
  "topics": [
    {
      "title": "功能测试",
      "topics": [
        {"title": "登录"},
        {"title": "注册"}
      ]
    },
    {"title": "性能测试"}
  ]
}
```

只要把 XMind 理解为「节点 + 子节点」的树结构，
后续的读取、转换和生成，本质上都是**树的遍历和重组**。

---

## 3. 将 XMind 解析为可编程数据

在理解文件结构之后，下一步是：**如何把 XMind 转成程序可以直接处理的数据结构**。

### 3.1 使用 xmindparser

`xmindparser` 是一个用于解析 `.xmind` 文件的 Python 开源库，支持旧版和新版 XMind。

```bash
pip install xmindparser
```

### 3.2 解析为 Python 字典

```python
from xmindparser import xmind_to_dict

# 它会自动识别 XML 或 JSON 格式并返回统一的 Python List/Dict
xmind_data = xmind_to_dict("demo.xmind")

# 返回结果通常是 list，每个元素对应一个画布（sheet）
print(xmind_data[0]["topic"]["title"])
```

解析完成后，你得到的是标准的 Python `dict / list` 结构，可以继续用于：

* 导出 Markdown / CSV
* 生成测试用例
* 接入自动化或测试平台系统

---

## 4. 使用 Python 生成 XMind

当你可以解析 XMind 之后，反向生成就是一个自然的问题：

> **如何根据结构化数据，生成一个可以正常打开的 XMind 文件。**

### 4.1 通过 XML 生成 XMind（XMind 8）

下面示例展示的是一个**最小可用版本**，只保证层级结构正确，不包含样式、图标、备注等高级能力。

```python
import xml.etree.ElementTree as ET
import zipfile
import json


def build_content_xml(tree_data):
    root = ET.Element("xmap-content", {"version": "2.0"})
    sheet = ET.SubElement(root, "sheet", {"id": "sheet-1"})

    root_topic = ET.SubElement(sheet, "topic", {"id": "root"})
    ET.SubElement(root_topic, "title").text = tree_data["title"]

    def add_topics(parent, topics):
        if not topics:
            return
        children = ET.SubElement(parent, "children")
        topics_el = ET.SubElement(children, "topics", {"type": "attached"})
        for i, t in enumerate(topics):
            topic = ET.SubElement(topics_el, "topic", {"id": f"t-{i}"})
            ET.SubElement(topic, "title").text = t["title"]
            add_topics(topic, t.get("topics", []))

    add_topics(root_topic, tree_data.get("topics", []))
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def save_as_xmind(filename, xml_content):
    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("content.xml", xml_content)
        # 必须包含 manifest.json 声明，否则 XMind 打不开
        z.writestr(
            "manifest.json",
            json.dumps({"file-entries": {"content.xml": {}, "manifest.json": {}}})
        )
```

---

### 4.2 使用 SDK 生成 XMind（新版）

对于 XMind Zen / 2024，更推荐使用官方 SDK。

```bash
pip install XMind-SDK-Python
```

```python
import xmind

workbook = xmind.load("new.xmind")
sheet = workbook.getPrimarySheet()
root_topic = sheet.getRootTopic()
root_topic.setTitle("自动化测试计划")

sub = root_topic.addSubTopic()
sub.setTitle("接口测试")
sub.setMarkerId("priority-1") # 设置优先级图标

xmind.save(workbook, "test_plan.xmind")
```

---

## 5. 工程实践：模板注入法

在真实项目中，纯代码生成样式的维护成本很高，更常见、也更稳定的做法是**模板注入法**。

### 5.1 为什么使用模板

* 样式由人工在 XMind 中维护
* 程序只负责生成结构数据
* 模板调整不会影响代码逻辑

### 5.2 基本流程

1. 手动制作 `template.xmind`
2. 解压并读取模板文件
3. 动态生成 `content.xml / content.json`
4. 重新打包为 `.xmind`

这种方式非常适合测试平台、自动化工具以及企业内部系统。

---

## 6. 总结

* `.xmind` 是一个 ZIP 文件，核心内容是 XML / JSON
* 思维导图在程序中是标准的树结构
* 可以使用 `xmindparser` 将 XMind 解析为可编程数据
* 可以通过 XML 或 SDK 反向生成 XMind 文件
* 模板注入法是工程中最稳定、最易维护的方案

