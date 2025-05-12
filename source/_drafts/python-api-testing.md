---
title: python_api_testing
tags:
  - 接口自动化测试
  - python
categories: 自动化测试 & 工具开发（Test Automation & Tool Development）
keywords: 接口测试
description: 用python搭建接口自动化测试平台,
top_img: /img/python_api_testing_m.png
cover: /img/python_api_testing_s.png
date: 2025-03-24 13:34:42
updated: 2025-03-24 13:34:42
---

# **如何用 Python 搭建接口自动化测试？🚀**

在前面的文章中，我们介绍了 **Postman** 和 **Apifox** 这两种 API 测试工具，它们可以帮助我们进行接口测试，提供 **可视化界面、断言检查、请求管理** 等功能，非常适合手工测试和简单的自动化测试。

但在实际工作中，许多测试流程需要更高效的 **自动化执行**，例如：
- 批量运行接口测试（不想手动点来点去）
- 集成到 CI/CD 流程（每次代码更新自动跑测试）
- 满足更灵活的定制化需求（如动态参数、数据驱动）

因此，在我的工作中，我们主要使用 **Python** 进行接口自动化测试。💡  
本文将详细介绍 **如何用 Python 搭建一个可扩展的 API 自动化测试框架**，帮助你从零开始掌握这项技能！🔥

---

## **🔹 1. 为什么选择 Python 进行接口测试？**

### **✅ Postman & Apifox vs Python**

| 工具       | 适合场景           | 主要优势                     | 局限性                   |
|------------|--------------------|------------------------------|--------------------------|
| **Postman**| 手工测试、简单自动化 | 可视化操作、支持环境变量       | 复杂测试不方便           |
| **Apifox** | 接口测试、文档管理   | 结合 API 文档 & 测试           | 需要 GUI，不适合 CI/CD    |
| **Python** | 自动化测试、CI/CD    | 灵活强大、可扩展、支持数据驱动 | 需要编写代码             |

如果你想让测试更 **自动化、可定制、可扩展**，Python 一定是更好的选择！✅

---

## **🔹 2. 搭建 Python 接口自动化测试环境**

### **📌 2.1 安装 Python 依赖**
首先，确保你的系统已经安装了 Python（推荐 Python 3.8+）。  
然后，使用 `pip` 安装需要的库：
```bash
pip install requests pytest pytest-html
```

📌 **工具介绍：**
- **`requests`**：Python 最常用的 HTTP 请求库  
- **`pytest`**：轻量级测试框架，支持断言和参数化  
- **`pytest-html`**：生成 HTML 测试报告

---

## **🔹 3. 用 Python 发送 API 请求**

在正式编写自动化测试用例前，我们先了解如何用 Python 直接请求 API。

### **📌 3.1 发送 GET 请求**
```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)

print("状态码:", response.status_code)
print("返回数据:", response.json())
```
✅ 这段代码会请求一个测试 API，并打印返回的数据。

### **📌 3.2 发送 POST 请求**
```python
import requests

data = {"title": "foo", "body": "bar", "userId": 1}
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=data)

print("状态码:", response.status_code)
print("返回数据:", response.json())
```
💡 这里使用 `json=data` 来发送 JSON 数据，适用于大多数 API 测试场景。

---

## **🔹 4. 用 pytest 编写接口自动化测试**

我们将把 API 请求封装到自动化测试用例中。

### **📌 4.1 创建测试文件 `test_api.py`**
```python
import requests

def test_get_post():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.get(url)

    # 测试断言：检查状态码和返回数据
    assert response.status_code == 200
    assert response.json()["id"] == 1
```
📌 使用 `assert` 语句验证 API 返回结果是否符合预期。

### **📌 4.2 运行测试**
在命令行中执行以下命令来运行测试：
```bash
pytest test_api.py
```
如果一切正常，你会看到测试通过的提示！🎉

---

## **🔹 5. 进阶优化：参数化测试 & 报告生成**

### **📌 5.1 参数化测试多个接口**
```python
import pytest
import requests

@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_get_post(post_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    response = requests.get(url)

    assert response.status_code == 200
    assert response.json()["id"] == post_id
```
✅ 这样可以避免重复编写类似的测试用例，提高测试效率！

### **📌 5.2 生成 HTML 测试报告**
```bash
pytest --html=report.html
```
📌 生成的 `report.html` 文件将包含所有测试结果，方便查看和归档。

---

## **🔹 6. 构建可扩展的接口自动化测试框架**

在实际项目中，构建一个 **可维护、可扩展** 的测试框架非常关键。

### **📌 6.1 API 请求封装**
```python
import requests

class APIClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    @staticmethod
    def get_post(post_id):
        return requests.get(f"{APIClient.BASE_URL}/posts/{post_id}")

    @staticmethod
    def create_post(data):
        return requests.post(f"{APIClient.BASE_URL}/posts", json=data)
```

### **📌 6.2 在测试用例中调用**
```python
from utils.api_client import APIClient

def test_get_post():
    response = APIClient.get_post(1)
    assert response.status_code == 200
```
✅ 这样可以让测试代码更清晰且易于复用。

---

## **🔹 7. 结合 CI/CD 实现自动化**

### **📌 示例 GitHub Actions 工作流 (`ci.yml`)**
```yaml
name: API Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run API tests
        run: pytest --html=reports/report.html
```

---

## **🔹 8. 结语**

📌 现在，你已经掌握了 **Python 接口自动化测试** 的基本技能，赶紧实践一下吧！🚀  
如果觉得这篇文章对你有帮助，欢迎 **点赞 & 分享** 哦！😃
