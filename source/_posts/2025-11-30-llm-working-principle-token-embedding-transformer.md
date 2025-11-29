---
title: 🧠 1/15｜LLM 工作原理深度解析：Token、向量、Transformer，到底在算什么？
date: 2025-11-30 18:00:00
series: LLM/Agent系列教程
categories:
  - 技术学习与行业趋势
  - AI与研究
tags:
  - LLM
  - Transformer
  - Token
  - Embedding
  - 大语言模型
  - 深度学习
keywords: LLM, Token, Embedding, Transformer, Self-Attention, BPE, 大语言模型, 工作原理, 深度学习
description: '深度解析 LLM 工作原理：从 Token 分词、Embedding 向量化到 Transformer 架构，用通俗易懂的方式理解大语言模型如何"读懂"和生成语言'
top_img: /img/llm-working-principle-token-embedding-transformer.png
cover: /img/llm-working-principle-token-embedding-transformer.png
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

> **这是《LLM/Agent 核心知识体系》系列第 1 篇。**

> 未来 14 篇，我们将从 Prompt、RAG、Embedding、Agent 到模型微调，带你系统理解"AI 是怎么运作的"。

---

# 🚀 导言：理解大模型最重要的三件事

当你对 ChatGPT 问一句："给我写一篇晚会主持稿"，它几秒内能生成近千字内容。

这不是魔法，本质上，它只是在执行一件事：

> **根据输入，预测下一个最可能出现的 Token。**

而理解它如何预测，你只需要掌握三件事：

1. **Token（语言最小粒度）**

2. **Embedding（文字转数字的向量空间）**

3. **Transformer（让模型"看懂上下文"的架构）**

搞懂它们，你就搞懂了 LLM 的底层"物理学"。

---

# 🧩 一、最小单位：Tokenization（分词）

## 1. 什么是 Token？

Token ≠ 字

Token ≠ 词

Token 是 **模型处理语言的最小单位**。

它可以是：

* 一个单词：`apple`

* 一个词根：`tion`

* 一个汉字：`你`

* 一个空格：`_`

* 一个符号：`.`

**为什么不用"字"或"词"？**

因为：

* 英语中单词拆分更灵活（如：international → inter / nation / al）

* 中文没有天然分词

* 需要处理各种语言、表情、符号（🌈🔥💡）

所以模型需要一种统一的编码方式 → **Tokenization**。

---

## 2. 主流分词技术：BPE（Byte Pair Encoding）

大多数 LLM（GPT、Llama）都用 BPE 或改进方案（SentencePiece、Unigram-LM）。

**BPE 怎么工作？**

1. 先把所有文本拆成**单个字节**

2. 统计出现频率最高的 **相邻组合**

3. 将它合并成一个新的 Token

4. 重复上面步骤直到词表达到固定大小（如 32k、50k）

最终效果：

* 高频词 → 少量 Token

  例：`hello` → `["hello"]`

* 生僻词 → 多个 Token

  例：`antidisestablishmentarianism` → 8~12 个 Token

---

## 3. 不同模型 Tokenizer 的差异（重要！）

同一句话在不同模型中 Token 数量不同。

| 模型            | Tokenizer     | 特点           |
| ------------- | ------------- | ------------ |
| GPT-4 / GPT-3 | BPE（tiktoken） | 英语友好，分词更细    |
| Llama 系列      | SentencePiece | 无需空格分词，适配多语言 |
| Claude 系列     | Unigram LM    | 更稳健处理非英语文本   |

**为什么重要？**

因为 Token 数影响：

* 费用（按 Token 计费）

* 上下文窗口占用

* 生成速度

实际做 RAG、Agent 时必须知道。

---

# 🔢 二、数字语言：Embedding（向量化）

Token 是符号，计算机不理解，所以必须转成数字 → **向量（Vector）**。

## 1. 什么是 Embedding？

Embedding = 一个 **高维浮点数向量**

如：

```
[0.12, -0.98, 1.23, ... 共 4096 个数字]
```

它的意义是：

> **把 Token 映射到一个可计算的空间，使相似词距离更近。**

例：

* "国王" 和 "皇帝" 的向量距离很近

* "猫" 和 "狗" 的方向接近但不完全重叠

* "国王 - 男人 + 女人 ≈ 女王"

这不是巧合，而是模型从海量文本中学到的语义结构。

---

## 2. Embedding 不是一种，而是三种（很重要）

### ✔ (1) Token Embedding

词汇的基本语义编码

→ 输入层使用

### ✔ (2) Position Embedding

告诉模型"顺序"是谁在前谁在后

→ 因为 Transformer 不具备顺序概念

### ✔ (3) Sentence Embedding

一句话/段落的语义编码

→ 用于 RAG、搜索、聚类、推荐系统

这部分常被新手混淆，你的文章加入后读者会瞬间清楚。

---

## 3. 为什么 Embedding 是 LLM 的"灵魂"？

因为模型所有计算都围绕向量进行：

1. 输入 Token → 查 Embedding

2. Transformer 对所有向量进行矩阵计算

3. 输出向量 → 映射为 Token 概率 → 选择最高概率输出

总结一句话：

> **Embedding 决定模型知道什么；Transformer 决定模型怎样使用这些知识。**

---

# 🏗️ 三、核心架构：Transformer

Transformer 是 Google 2017 年提出的架构（论文：*Attention Is All You Need*）。

它为什么革命性？

因为它解决了 RNN/LSTM 的两大痛点：

* **不能并行（必须顺序处理）**

* **难以记住长距离依赖**

Transformer 则完全相反：

> **一次性处理所有 Token，能看到更长的上下文。**

---

# 🔍 四、Self-Attention：让模型"看懂上下文"的关键

## 1. 什么是 Self-Attention？

一句话解释：

> **让每个 Token 计算它应该关注句子中其他哪些 Token。**

例：

> "小明把苹果递给小红，她接住了。"

"她"到底指谁？

Self-Attention 能算出它更依赖 "小红"。

---

## 2. Self-Attention 的内部细节（通俗解释）

每个 Token 会生成三个向量：

* **Q（Query）**：我想找谁？

* **K（Key）**：别人能被匹配吗？

* **V（Value）**：别人的信息是什么？

过程如下：

```
注意力分数 = Q · K^T

权重 = Softmax(注意力分数)

输出 = 权重 × V
```

这就是 Self-Attention，数学优雅，效果惊人。

---

# 🔁 五、Transformer 的完整计算流程（极简心智图）

```
Token → Embedding

↓ 加位置编码

Q/K/V 生成

↓ Self-Attention

带上下文的向量

↓ FFN（前馈网络）

↓ 残差连接 + LayerNorm

输出给下一层

（重复几十层）

↓

最终向量 → Softmax → 预测下一个 Token
```

现代 GPT 模型通常堆叠 **几十到上百层** Transformer Block。

---

# 🚩 六、几个常见误区（一定要懂）

### ❌ 误解 1：LLM 是"理解语言"的

✔ 真相：

> 它只是学习"哪些 Token 后面最容易跟哪些 Token"。

### ❌ 误解 2：Transformer 看到的是"整句"

✔ 真相：

GPT（Decoder-only）只能看到**左侧 Token**，右侧是被 Mask 掉的。

### ❌ 误解 3：Embedding = Sentence Embedding

✔ 真相：

二者完全不同。

### ❌ 误解 4：Attention 越多越好

✔ 真相：

太多头会训练不稳定，模型设计都有平衡。

---

# 🎯 七、一句话总结（每节一个重点）

* **Token：**把人类语言拆成模型能处理的最小颗粒

* **Embedding：**把 Token 映射成可以计算的向量

* **Transformer：**让模型在向量空间里"理解上下文"

* **Self-Attention：**每个 Token 决定该关注其他 Token 的程度

* **LLM 本质：**根据上下文概率预测下一个 Token

---

# 📚 八、延伸阅读（含可直接访问链接）

### Transformer

* Attention Is All You Need（论文）

  [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)

* Illustrated Transformer

  [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/)

### Tokenization

* BPE 论文

  [https://arxiv.org/abs/1508.07909](https://arxiv.org/abs/1508.07909)

* SentencePiece

  [https://github.com/google/sentencepiece](https://github.com/google/sentencepiece)

### Embedding

* Word2Vec 论文

  [https://arxiv.org/abs/1301.3781](https://arxiv.org/abs/1301.3781)

* Illustrated Word2Vec

  [https://jalammar.github.io/illustrated-word2vec/](https://jalammar.github.io/illustrated-word2vec/)

### Transformer/LLM 实战

* Hugging Face NLP Course

  [https://huggingface.co/learn/nlp-course](https://huggingface.co/learn/nlp-course)

* Transformer Explainer

  [https://poloclub.github.io/transformer-explainer/](https://poloclub.github.io/transformer-explainer/)

---

# 🔔 下一篇预告

第二篇将带你理解：

> **为什么模型能理解你的提示？

> 什么是 Prompt？

> 什么是上下文学习（In-Context Learning）？**

标题是：

### **《2/15｜理解 LLM 的"语言"：Prompt、上下文与 In-Context Learning》**

