---
title: 🧠 主题1｜LLM 工作原理深度解析：Token、向量、Transformer，到底在算什么？
date: 2025-12-02 18:00:00
updated: {{current_date_time}}

categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
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

> **这是[《🧠 LLM/Agent 从入门到精通：告别浅尝辄止》](/categories/🧠-LLM-Agent-从入门到精通：告别浅尝辄止/)系列第 1 篇。**

> 本篇将深入解析 LLM 的工作原理：从 Token 分词、Embedding 向量化到 Transformer 架构。未来，我们将继续探讨 Prompt 工程、RAG、Agent 等核心概念，带你系统理解"AI 是怎么运作的"。

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

## 4. 什么是 SentencePiece 和 Unigram-LM？

**SentencePiece（SP）**：

* **核心改进**：将文本视为**原始 Unicode 字符序列**，不需要预先分词（不需要空格）
* **为什么更好**：
  * 适合中文、日文等**没有空格分隔**的语言
  * 可以处理**任意 Unicode 字符**（包括 emoji、特殊符号）
  * 训练时把空格也当作普通字符处理，更灵活
* **工作原理**：
  1. 把文本转成 Unicode 字符序列
  2. 使用 BPE 或 Unigram 算法学习子词单元
  3. 可以反向解码回原始文本（包括空格）
* **典型应用**：Llama、T5、mT5 等模型

**Unigram-LM（语言模型分词）**：

* **核心改进**：不是从下往上合并（BPE），而是**从上往下拆分**
* **为什么更好**：
  * 基于**概率模型**，选择最可能的分词方式
  * 对**非英语文本**（中文、阿拉伯文等）更稳健
  * 可以处理**多分词候选**，选择最优解
* **工作原理**：
  1. 先初始化一个大的词表（包含所有可能的子词）
  2. 用语言模型计算每个子词的概率
  3. 逐步移除概率最低的子词，直到词表达到目标大小
  4. 分词时选择**概率乘积最大**的分词方案
* **典型应用**：Claude（Anthropic）、ALBERT 等模型

**三种方案对比**：

| 特性 | BPE | SentencePiece | Unigram-LM |
| --- | --- | --- | --- |
| 方向 | 自下而上合并 | 可配合 BPE/Unigram | 自上而下拆分 |
| 多语言支持 | 一般 | 优秀 | 优秀 |
| 需要空格 | 是 | 否 | 否 |
| 概率模型 | 否 | 可选 | 是 |
| 训练复杂度 | 低 | 中 | 高 |

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

### ✔ (1) Token Embedding（词嵌入）

**是什么**：

Token Embedding 是**每个 Token 对应的语义向量**，是模型理解词汇含义的基础。

**工作原理**：

1. 模型有一个**词表（Vocabulary）**，比如包含 50,000 个 Token
2. 每个 Token 都有一个**固定的向量表示**（通常是 [4096 维或 768 维](#vector-dimension)）
3. 输入文本时，模型通过**查表**的方式，把每个 Token 转换成对应的向量

**例子**：

```
输入："我喜欢苹果"
Token 化：["我", "喜欢", "苹果"]
↓ Token Embedding 查表
向量：
  "我"    → [0.12, -0.45, 0.78, ...]
  "喜欢"  → [0.34, 0.21, -0.56, ...]
  "苹果"  → [-0.12, 0.89, 0.23, ...]
```

**关键点**：

* 这是**模型的第一层**，所有 Token 进入模型前都要经过这一步
* 这些向量是**训练时学习到的**，相似词（如"苹果"和"水果"）的向量距离更近
* 同一个 Token 在不同位置**向量相同**（不考虑上下文）

---

### ✔ (2) Position Embedding（位置编码）

**为什么需要**：

Transformer 使用**并行处理**，所有 Token 同时输入，**没有天然的顺序概念**。

但语言是有顺序的！"猫吃鱼" ≠ "鱼吃猫"

**工作原理**：

Position Embedding 给每个**位置**（第 1 个、第 2 个...）分配一个**固定的向量**，加到 Token Embedding 上。

**例子**：

```
输入："我喜欢苹果"
Token Embedding：
  "我"    → [0.12, -0.45, 0.78, ...]
  "喜欢"  → [0.34, 0.21, -0.56, ...]
  "苹果"  → [-0.12, 0.89, 0.23, ...]

Position Embedding：
  位置 0  → [0.01, 0.02, 0.03, ...]  (正弦/余弦编码)
  位置 1  → [0.02, 0.04, 0.06, ...]
  位置 2  → [0.03, 0.06, 0.09, ...]

最终输入 = Token Embedding + Position Embedding
  "我"    → [0.12, -0.45, 0.78, ...] + [0.01, 0.02, 0.03, ...]
  "喜欢"  → [0.34, 0.21, -0.56, ...] + [0.02, 0.04, 0.06, ...]
  "苹果"  → [-0.12, 0.89, 0.23, ...] + [0.03, 0.06, 0.09, ...]
```

**两种实现方式**：

* **绝对位置编码**（原始 Transformer）：用数学公式（正弦/余弦）生成固定位置向量
* **相对位置编码**（现代模型如 GPT-3）：可学习的参数，更灵活

**关键点**：

* 没有 Position Embedding，模型无法区分"我喜欢你"和"你喜欢我"
* 位置信息会**贯穿整个模型**，影响 [Self-Attention](#self-attention) 的计算

> **什么是 Self-Attention？**（简单理解）
> 
> Self-Attention 是让模型"看懂上下文"的核心机制。它让每个词（Token）能够**关注句子中其他相关的词**。
> 
> 例如在句子"小明把苹果递给小红，她接住了"中，Self-Attention 帮助模型理解"她"应该指向前面的"小红"，而不是"小明"。
> 
> 位置信息在 Self-Attention 中很重要，因为模型需要知道哪些词是相邻的、哪些词在前面，才能正确建立词与词之间的关系。
> 
> 详细说明请参考本文 [第四部分：Self-Attention](#self-attention)。

---

### ✔ (3) Sentence Embedding（句子嵌入）

**是什么**：

Sentence Embedding 是**整个句子或段落的单一向量表示**，用于捕获整体语义。

**与 Token Embedding 的区别**：

| 特性 | Token Embedding | Sentence Embedding |
| --- | --- | --- |
| 粒度 | 单个 Token | 整个句子/段落 |
| 数量 | 每个 Token 一个 | 每个句子一个 |
| 用途 | 模型内部计算 | 外部应用（搜索、相似度） |
| 生成方式 | 查表 | 通过模型计算（平均、CLS token、特殊层） |

**工作原理**：

有几种常见方法：

1. **平均池化**：把句子中所有 Token 的向量**求平均**
   ```
   "我喜欢苹果" → 平均(["我", "喜欢", "苹果"]的向量)
   ```

2. **CLS Token**：BERT 等模型在句子开头加一个特殊 Token `[CLS]`，它的最终向量代表整个句子

3. **特殊层**：模型最后一层专门输出句子级别的向量

**实际应用场景**：

* **RAG（检索增强生成）**：
  ```
  用户问题 → Sentence Embedding → 在向量数据库中搜索相似文档
  ```

* **语义搜索**：
  ```
  搜索"如何学习 Python" → 找到包含"Python 教程"、"编程入门"的文档
  ```

* **文本聚类**：
  ```
  把相似主题的文章自动分组
  ```

* **推荐系统**：
  ```
  根据用户历史文本的 Sentence Embedding，推荐相似内容
  ```

**例子**：

```python
# 伪代码示例
sentence = "我喜欢吃苹果"
token_embeddings = [embed("我"), embed("喜欢"), embed("吃"), embed("苹果")]
sentence_embedding = mean(token_embeddings)  # 或使用其他方法

# 现在可以用这个向量做相似度计算
similarity = cosine_distance(sentence_embedding, other_sentence_embedding)
```

**关键点**：

* Sentence Embedding 是**从 Token Embedding 衍生出来的**，不是独立存在的
* 它主要用于**模型外部**的应用，而不是模型内部的推理过程
* 不同模型生成 Sentence Embedding 的方法不同，效果也不同

---

**总结对比**：

| Embedding 类型 | 作用 | 使用阶段 | 典型维度 |
| --- | --- | --- | --- |
| Token Embedding | 表示词汇语义 | 模型输入层 | 4096 / 768 |
| Position Embedding | 表示位置信息 | 模型输入层（与 Token 相加） | 4096 / 768 |
| Sentence Embedding | 表示句子语义 | 模型输出后 | 4096 / 768 |

这部分常被新手混淆，理解它们的区别对后续学习 RAG、Agent 等应用至关重要。

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

Transformer 是 Google 2017 年提出的架构（论文：[*Attention Is All You Need*](https://arxiv.org/abs/1706.03762)）。

它为什么革命性？

因为它解决了 [RNN/LSTM](#rnn-lstm) 的两大痛点：

* **不能并行（必须顺序处理）**

* **难以记住长距离依赖**

Transformer 则完全相反：

* **一次性处理所有 Token，能看到更长的上下文。**

> **什么是 RNN/LSTM？**（简单理解）
> 
> **RNN（循环神经网络）** 和 **LSTM（长短期记忆网络）** 是 Transformer 出现之前，处理序列数据（如文本）的主流模型。
> 
> **它们的特点**：
> 
> * **顺序处理**：必须一个词一个词地处理，不能同时处理所有词
>   * 就像读文章必须从左到右逐字阅读，不能一眼看完
> * **记忆有限**：虽然能记住一些上下文，但距离太远的词容易"忘记"
>   * 就像人读很长的文章，前面的内容可能记不清了
> 
> **为什么这成为问题？**
> 
> * **速度慢**：必须顺序处理，无法利用 GPU 的并行计算能力
> * **理解受限**：长句子中，前面的词对后面的影响会逐渐减弱
> 
> **Transformer 的突破**：
> 
> * ✅ **并行处理**：所有词同时输入，充分利用 GPU 算力
> * ✅ **长距离依赖**：通过 Self-Attention 机制，能直接关注到句子中任意位置的词
> 
> 这就是为什么 Transformer 能成为现代 LLM 的基础架构。

---

## Transformer 的三种架构

Transformer 主要有三种架构：

### 1. Encoder-Only（只用编码器）

**用途**：文本分类、情感分析、问答等**理解类任务**

**结构**：
```
输入 → Encoder → 输出（分类/分析结果）
```

**特点**：
* 只使用 Transformer 的 **Encoder 部分**
* **双向理解**：能看到整个输入序列（左右两侧）
* 主要用于理解文本，不生成新文本

**典型应用**：[BERT](#bert-t5)

---

### 2. Encoder-Decoder（编码器-解码器）

**用途**：翻译、摘要等需要"理解输入 + 生成输出"的任务

**结构**：
```
输入 → Encoder（理解） → Decoder（生成） → 输出
```

**特点**：
* 使用完整的 **Encoder + Decoder** 结构
* Encoder：能看到整个输入序列（双向）
* Decoder：生成时只能看到左侧已生成的内容（单向）

**典型应用**：[T5](#bert-t5)

> **"整个输入序列" vs "左侧已生成的内容"是什么意思？**
> 
> 这是理解 Encoder 和 Decoder 的关键区别，用例子说明：
> 
> **场景：翻译任务 "I love apples" → "我喜欢苹果"**
> 
> **Encoder（理解阶段）**：
> 
> * 输入："I love apples"（整个句子已经存在）
> * Encoder 能**同时看到所有词**：`I`、`love`、`apples`
> * 可以**双向理解**：理解 `love` 时，能看到前面的 `I` 和后面的 `apples`
> * 就像读一篇文章，可以前后翻看，理解整体意思
> 
> **Decoder（生成阶段）**：
> 
> * 生成过程是**逐步的**，每次只生成一个词
> * 生成第 1 个词"我"时：只能看到输入 "I love apples"（来自 Encoder）
> * 生成第 2 个词"喜欢"时：只能看到 "我"（已生成）+ 输入 "I love apples"
> * 生成第 3 个词"苹果"时：只能看到 "我喜欢"（已生成）+ 输入 "I love apples"
> * **不能看到未来**：生成"喜欢"时，还不知道后面会生成"苹果"
> * 就像写文章，只能看到已经写好的部分，不能看到还没写的内容
> 
> **关键区别**：
> 
> | 阶段 | 能看到什么 | 比喻 |
> | --- | --- | --- |
> | Encoder | 整个输入序列（所有词同时存在） | 读完整篇文章 |
> | Decoder | 左侧已生成的内容（逐步生成，不能看未来） | 写文章，只能看已写部分 |
> 
> 这就是为什么 Encoder 是"双向"的（能看到左右两侧），而 Decoder 是"单向"的（只能看到左侧）。

---

### 3. Decoder-Only（现代 LLM 主流）

**用途**：文本生成、对话、代码生成等

**结构**：
```
输入 → Decoder → 输出
```

**特点**：
* 只有 Decoder 部分
* 生成时只能看到左侧内容（单向）
* 通过自回归方式逐个生成 Token

**典型应用**：GPT 系列、Llama、Claude

**为什么 Decoder-Only 成为主流？**

* ✅ **更适合生成任务**：自回归生成更自然
* ✅ **架构更简单**：只需要一个组件
* ✅ **训练更高效**：统一的任务（预测下一个 Token）

---

## Transformer Block 的核心组件

一个 Transformer Block（层）就像是一个"处理单元"，它会对输入的向量进行一系列操作，让模型更好地理解文本。

### Transformer Block 包含什么？

一个 Transformer Block 通常包含 4 个核心组件：

1. **Self-Attention**：让每个 Token 关注其他 Token（详见 [第四部分](#self-attention)）
2. **Feed-Forward Network (FFN)**：对每个 Token 的向量进行非线性变换
3. **残差连接（Residual Connection）**：把输入直接加到输出上，帮助训练
4. **Layer Normalization**：归一化，稳定训练过程

### 工作流程（用例子理解）

假设我们处理句子"我喜欢苹果"，看看一个 Transformer Block 是如何工作的：

```
输入："我"、"喜欢"、"苹果" 的向量
  ↓
【步骤 1】Self-Attention（关注其他 Token）
  - "我" 关注 "喜欢" 和 "苹果"
  - "喜欢" 关注 "我" 和 "苹果"
  - "苹果" 关注 "我" 和 "喜欢"
  - 结果：每个词都带上了上下文信息
  ↓
【步骤 2】残差连接 + LayerNorm
  - 残差连接：把原始输入加回来（防止信息丢失）
  - LayerNorm：归一化（让数值更稳定）
  ↓
【步骤 3】FFN（非线性变换）
  - 对每个词的向量进行复杂的数学变换
  - 增加模型的表达能力
  ↓
【步骤 4】残差连接 + LayerNorm
  - 再次把输入加回来
  - 再次归一化
  ↓
输出：处理后的向量（传给下一层）
```

### 每个组件的作用（通俗解释）

#### 1. Self-Attention（自注意力）

**作用**：让每个词"看到"句子中其他相关的词

**例子**：
* 在"小明把苹果递给小红，她接住了"中
* "她"通过 Self-Attention 知道应该关注"小红"
* 这样模型就能理解"她"指的是谁

**比喻**：就像读文章时，遇到代词会回头看前面提到的内容

---

#### 2. Feed-Forward Network (FFN)（前馈网络）

**作用**：对每个词的向量进行"深度加工"，增加模型的表达能力

**通俗理解**：
* Self-Attention 让词之间建立了关系
* FFN 则对每个词本身进行"升级改造"
* 就像给每个词增加了更丰富的"特征"

**例子**：
```
输入向量：[0.1, 0.2, 0.3, ...]
  ↓ FFN 处理
输出向量：[0.5, -0.3, 0.8, ...]  （数值变了，但保留了语义）
```

**比喻**：就像给照片加滤镜，虽然样子变了，但内容还是那个内容，只是更"好看"了

---

#### 3. 残差连接（Residual Connection）

**作用**：把输入直接加到输出上，防止信息在传递过程中丢失

**工作原理**：
```
原始输入：X
经过处理：Y = Self-Attention(X) 或 Y = FFN(X)
残差连接：输出 = X + Y  （把原始输入加回来）
```

**为什么需要？**

* **防止信息丢失**：深层网络中，信息可能在传递过程中逐渐丢失
* **帮助训练**：让模型更容易学习，梯度能更好地传播
* **保留原始信息**：即使处理后的结果不好，至少还保留了原始输入

**比喻**：就像写文章时保留草稿，即使修改后不满意，还能回到原来的版本

**实际例子**：
```
输入："我" 的向量 = [0.1, 0.2, 0.3]
经过 Self-Attention 后 = [0.5, 0.6, 0.7]
残差连接后 = [0.1, 0.2, 0.3] + [0.5, 0.6, 0.7] = [0.6, 0.8, 1.0]
```

---

#### 4. Layer Normalization（层归一化）

**作用**：把向量中的数值"标准化"，让训练更稳定

**通俗理解**：
* 神经网络中，数值可能会变得很大或很小
* LayerNorm 把数值调整到合适的范围
* 就像把音量调到一个合适的水平

**工作原理**（简化）：
```
输入向量：[100, -50, 200, ...]  （数值很大，不稳定）
  ↓ LayerNorm
输出向量：[0.5, -0.3, 0.8, ...]  （数值标准化，稳定）
```

**为什么需要？**

* **稳定训练**：防止数值过大或过小导致训练失败
* **加速收敛**：让模型更快找到最优解
* **提高性能**：让模型表现更好

**比喻**：就像调节空调温度，让环境保持在一个舒适的范围内

---

### 为什么需要这些组件？（总结）

| 组件 | 作用 | 比喻 |
| --- | --- | --- |
| Self-Attention | 理解上下文关系 | 读文章时回头看相关内容 |
| FFN | 增加表达能力 | 给照片加滤镜，增强效果 |
| 残差连接 | 防止信息丢失 | 保留草稿，防止丢失原始信息 |
| LayerNorm | 稳定训练 | 调节温度，保持稳定 |

### 多层堆叠的效果

现代 GPT 模型通常堆叠 **几十到上百层**这样的 Transformer Block。

**为什么需要这么多层？**

* **第 1 层**：学习简单的词与词之间的关系
* **第 10 层**：学习更复杂的语法结构
* **第 50 层**：学习深层的语义和逻辑关系
* **第 100 层**：学习非常抽象和高级的模式

每一层都在前一层的基础上，提取更高级的特征，最终让模型能够理解复杂的语言。

**比喻**：就像盖房子，每一层都在前一层的基础上建造，最终建成高楼大厦。

---

# 🔍 四、Self-Attention：让模型"看懂上下文"的关键<a id="self-attention"></a>

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

## 3. Multi-Head Attention（多头注意力）

**什么是 Multi-Head？**

实际应用中，模型不是只做一次 Self-Attention，而是**同时做多次**，每次关注不同的"方面"。

**例子**：

在句子"小明把苹果递给小红，她接住了"中：

* **Head 1**：关注"语法关系"（"她"是主语）
* **Head 2**：关注"语义关系"（"她"指向前面的"小红"）
* **Head 3**：关注"位置关系"（"她"在"小红"后面）
* **Head 4**：关注"动作关系"（"接住"和"递给"相关）

**工作原理**：

```
输入向量
  ↓
分成多个 Head（如 8 个、16 个）
  ↓
每个 Head 独立计算 Self-Attention
  ↓
把所有 Head 的结果拼接起来
  ↓
输出向量
```

**为什么需要多个 Head？**

* ✅ **关注不同方面**：每个 Head 可以学习不同类型的依赖关系
* ✅ **表达能力更强**：多个视角比单一视角更全面
* ✅ **并行计算**：多个 Head 可以同时计算，不增加太多时间

**典型配置**：

| 模型 | Head 数量 | 说明 |
| --- | --- | --- |
| GPT-2 | 12 个 | 中等模型 |
| GPT-3 | 96 个 | 大模型 |
| Llama-2 | 32 个 | 开源大模型 |

**注意**：Head 数量不是越多越好，太多会导致训练不稳定，需要根据模型大小平衡。

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

---

# 🚩 六、几个常见误区（一定要懂）

### ❌ 误解 1：LLM 是"理解语言"的

✔ 真相：它只是学习"哪些 Token 后面最容易跟哪些 Token"。

### ❌ 误解 2：Transformer 看到的是"整句"

✔ 真相：GPT（Decoder-only）只能看到**左侧 Token**，右侧是被 Mask 掉的。

### ❌ 误解 3：Embedding = Sentence Embedding

✔ 真相：二者完全不同。

### ❌ 误解 4：Attention 越多越好

✔ 真相：太多头会训练不稳定，模型设计都有平衡。

---

# 📚 七、延伸阅读（含可直接访问链接）

以下资源按主题分类，每个资源都附有简要说明，帮助你选择合适的学习材料。

## 🔬 Transformer 核心

* [**Attention Is All You Need（原始论文）**](https://arxiv.org/abs/1706.03762)：Transformer 架构的开山之作，Google 2017 年发表。适合有一定数学基础的读者，详细介绍了 Self-Attention 机制和完整架构。

* [**Illustrated Transformer（图解 Transformer）**](https://jalammar.github.io/illustrated-transformer/)：Jay Alammar 的经典图解文章，用可视化方式解释 Transformer 的工作原理。**强烈推荐新手阅读**，比论文更容易理解。

## 🔤 Tokenization（分词）

* [**BPE 论文（Byte Pair Encoding）**](https://arxiv.org/abs/1508.07909)：BPE 算法的原始论文，解释了如何通过统计方法构建子词词表。适合想深入了解分词原理的读者。

* [**SentencePiece（Google 开源工具）**](https://github.com/google/sentencepiece)：Google 开源的统一分词框架，支持 BPE 和 Unigram 算法。适合需要实际使用分词工具的开发者。

## 🔢 Embedding（向量化）

* [**Word2Vec 论文**](https://arxiv.org/abs/1301.3781)：Word2Vec 的经典论文，介绍了如何将词汇映射到向量空间。虽然较老，但思想仍然重要。

* [**Illustrated Word2Vec（图解 Word2Vec）**](https://jalammar.github.io/illustrated-word2vec/)：同样是 Jay Alammar 的图解文章，用可视化方式解释 Word2Vec 的工作原理。**适合新手**。

## 🛠️ Transformer/LLM 实战

* [**Hugging Face NLP Course（NLP 课程）**](https://huggingface.co/learn/nlp-course)：Hugging Face 官方的免费 NLP 课程，从基础到进阶，包含大量实践代码。**强烈推荐**，适合想动手实践的读者。

* [**Transformer Explainer（可视化工具）**](https://poloclub.github.io/transformer-explainer/)：交互式可视化工具，可以动态查看 Transformer 内部的计算过程。适合想直观理解模型工作原理的读者。

## 🔄 RNN/LSTM（Transformer 的前身）

* [**Understanding LSTM Networks（LSTM 详解）**](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)：Christopher Olah 的经典博客文章，用图解方式深入浅出地解释 LSTM。**强烈推荐**，即使不深入研究 RNN，也能帮助你理解为什么需要 Transformer。

* [**The Unreasonable Effectiveness of RNNs（RNN 应用）**](https://karpathy.github.io/2015/05/21/rnn-effectiveness/)：Andrej Karpathy 的博客文章，展示了 RNN 在文本生成等任务上的强大能力。适合想了解 RNN 实际应用的读者。

## 🤖 BERT 和 T5

* [**BERT 论文**](https://arxiv.org/abs/1810.04805)：BERT 的原始论文，介绍了双向编码器的预训练方法。适合想深入了解 BERT 原理的读者。

* [**T5 论文**](https://arxiv.org/abs/1910.10683)：T5 的原始论文，提出了"文本到文本"的统一框架。适合想了解 Encoder-Decoder 架构的读者。

* [**The Illustrated BERT（BERT 图解）**](https://jalammar.github.io/illustrated-bert/)：Jay Alammar 的 BERT 图解文章，用可视化方式解释 BERT 的工作原理。**适合新手**，比论文更容易理解。

## 🏗️ 模型架构对比

* [**The GPT Architecture（GPT 架构详解）**](https://jalammar.github.io/illustrated-gpt2/)：Jay Alammar 的 GPT-2 图解文章，详细解释了 Decoder-Only 架构。**强烈推荐**，帮助理解现代 LLM 的架构。

* [**The Annotated Transformer（带注释的实现）**](http://nlp.seas.harvard.edu/annotated-transformer/)：哈佛大学提供的 Transformer 完整实现，每行代码都有详细注释。**适合想深入理解代码实现的读者**，是学习 Transformer 实现的最佳材料。

## 💻 代码实践

* [**Transformers 库（Hugging Face）**](https://github.com/huggingface/transformers)：Hugging Face 的官方 Transformers 库，提供了几乎所有主流模型的实现。**必备工具**，实际开发中几乎都会用到。

* [**From Zero to Hero: Fine-tuning GPT-2（GPT-2 微调教程）**](https://huggingface.co/blog/fine-tune-gpt2)：Hugging Face 官方的 GPT-2 微调教程，从零开始教你如何微调模型。**适合想动手实践的读者**。

## 🇨🇳 中文资源

* [**李宏毅机器学习课程 - Transformer**](https://www.youtube.com/watch?v=ugWDIIOHtPA)：台湾大学李宏毅教授的机器学习课程，Transformer 部分讲解清晰，有中文字幕。**适合中文读者**，视频形式更容易理解。

* [**动手学深度学习（Transformer 章节）**](https://zh.d2l.ai/chapter_attention-mechanisms/transformer.html)：中文开源教材《动手学深度学习》的 Transformer 章节，包含理论讲解和实践代码。**适合中文读者**，内容全面。

---

# 💡 扩展：什么是向量维度？<a id="vector-dimension"></a>

在文章中多次提到"4096 维"或"768 维"，这到底是什么意思？

## 什么是维度？

**维度（Dimension）**就是向量的**长度**，也就是向量中包含多少个数字。

**例子**：

```
一维向量（1 个数字）：[3.14]
二维向量（2 个数字）：[1.2, 3.4]
三维向量（3 个数字）：[1.2, 3.4, 5.6]
...
4096 维向量（4096 个数字）：[0.12, -0.45, 0.78, ..., 共 4096 个数字]
```

## 为什么是 4096 或 768？

这些数字是模型的**超参数**，在训练前就设定好的：

| 模型 | Embedding 维度 | 说明 |
| --- | --- | --- |
| GPT-3 | 12288 维 | 非常大的模型 |
| GPT-4 | 4096 维 | 大模型常用 |
| BERT-base | 768 维 | 中等模型 |
| BERT-large | 1024 维 | 较大模型 |
| Llama-2 | 4096 维 | 开源大模型 |

**为什么不同模型维度不同？**

* **维度越大**：
  * ✅ 能表达更丰富的语义信息
  * ✅ 模型容量更大，性能通常更好
  * ❌ 计算量更大，需要更多内存和算力

* **维度越小**：
  * ✅ 计算更快，占用内存更少
  * ❌ 表达能力有限，可能丢失细节

## 维度在数学上意味着什么？

想象一下：

* **2 维空间**：平面，可以用 (x, y) 表示一个点
* **3 维空间**：立体，可以用 (x, y, z) 表示一个点
* **768 维空间**：超空间，可以用 768 个数字表示一个"点"（即一个 Token）

**关键理解**：

> 每个 Token 的 Embedding 向量，就是在这个高维空间中的一个"点"。
> 
> 相似的词（如"苹果"和"水果"）在这个空间中的距离很近。
> 
> 不相关的词（如"苹果"和"汽车"）距离很远。

## 实际例子

```python
# 伪代码示例
"苹果" 的 Embedding = [0.12, -0.45, 0.78, ..., 共 768 个数字]
"水果" 的 Embedding = [0.15, -0.42, 0.81, ..., 共 768 个数字]
"汽车" 的 Embedding = [-0.89, 0.23, -0.56, ..., 共 768 个数字]

# 计算距离
distance("苹果", "水果") = 0.05  # 很近
distance("苹果", "汽车") = 1.87  # 很远
```

## 为什么不能太小也不能太大？

* **太小（如 64 维）**：
  * 信息压缩过度，很多词会"挤在一起"，难以区分
  * 就像用 10 个颜色画一幅画，细节会丢失

* **太大（如 100000 维）**：
  * 计算成本极高，训练和推理都很慢
  * 可能过拟合，学到的很多维度是冗余的

* **合适（768-4096 维）**：
  * 在表达能力和计算效率之间取得平衡
  * 经过大量实验验证，是当前的最佳实践

## 总结

* **维度 = 向量中数字的个数**
* **4096 维 = 向量包含 4096 个浮点数**
* **维度越大，表达能力越强，但计算成本也越高**
* **不同模型选择不同维度，是性能与效率的权衡**

理解维度概念后，你就能更好地理解为什么模型需要这么大的参数量，以及为什么不同模型的 Embedding 维度会不同。

---

# 💡 扩展：什么是 RNN/LSTM？<a id="rnn-lstm"></a>

在文章中提到 Transformer 解决了 RNN/LSTM 的痛点，那么 RNN 和 LSTM 到底是什么？

## 什么是 RNN（循环神经网络）？

**RNN（Recurrent Neural Network）** 是处理序列数据（如文本、语音）的经典神经网络架构。

**核心特点**：

* **有记忆能力**：每个时刻的处理结果会传递给下一个时刻
* **顺序处理**：必须一个词一个词地按顺序处理，不能并行

**工作原理（简化）**：

```
时刻 1：处理"我" → 输出结果1 + 隐藏状态1
时刻 2：处理"喜欢" → 使用隐藏状态1 + "喜欢" → 输出结果2 + 隐藏状态2
时刻 3：处理"苹果" → 使用隐藏状态2 + "苹果" → 输出结果3 + 隐藏状态3
```

**问题**：

* ❌ **梯度消失**：当句子很长时，前面的信息在传递过程中会逐渐"衰减"，后面的词很难记住前面的内容
* ❌ **无法并行**：必须等前一个词处理完才能处理下一个，无法利用 GPU 的并行计算能力

## 什么是 LSTM（长短期记忆网络）？

**LSTM（Long Short-Term Memory）** 是 RNN 的改进版本，专门解决 RNN 的"记忆问题"。

**核心改进**：

* ✅ **更好的记忆机制**：通过"门控"机制，可以选择性地记住或忘记信息
* ✅ **解决梯度消失**：能记住更长的序列信息

**但仍有问题**：

* ❌ **仍然无法并行**：还是必须顺序处理
* ❌ **计算复杂**：比 RNN 更复杂，训练更慢

## RNN/LSTM vs Transformer

| 特性 | RNN/LSTM | Transformer |
| --- | --- | --- |
| 处理方式 | 顺序处理（一个接一个） | 并行处理（同时处理所有词） |
| 长距离依赖 | 困难（信息会衰减） | 优秀（Self-Attention 直接关注任意位置） |
| 训练速度 | 慢（无法并行） | 快（充分利用 GPU） |
| 计算复杂度 | 低（但效果有限） | 高（但效果好） |

## 实际例子

**处理句子："小明把苹果递给小红，她接住了。"**

* **RNN/LSTM**：
  * 处理"她"时，可能已经"忘记"了前面的"小红"
  * 需要依赖隐藏状态传递，但信息会衰减

* **Transformer**：
  * 通过 Self-Attention，"她"可以直接"看到"并关注前面的"小红"
  * 不需要依赖隐藏状态传递，信息不会衰减

## 总结

* **RNN/LSTM**：Transformer 出现前的序列模型，有记忆但无法并行，长距离依赖困难
* **Transformer**：革命性架构，并行处理 + Self-Attention，解决了 RNN/LSTM 的痛点
* **现代 LLM**：几乎都基于 Transformer，因为它更快、更强、更灵活

理解 RNN/LSTM 的局限性，能帮助你更好地理解为什么 Transformer 如此重要，以及它为什么能成为现代 AI 的基础架构。

---

# 💡 扩展：什么是 BERT 和 T5？<a id="bert-t5"></a>

在文章中提到 BERT 和 T5 作为 Transformer 架构的典型应用，它们到底是什么？

## 什么是 BERT？

**BERT（Bidirectional Encoder Representations from Transformers）** 是 Google 在 2018 年发布的模型，是 Transformer Encoder 架构的典型代表。

### 核心特点

* **架构**：只使用 Transformer 的 **Encoder 部分**
* **双向理解**：能同时看到句子中**左右两侧**的所有词
* **预训练 + 微调**：先在大量文本上预训练，然后在特定任务上微调

### 工作原理

**预训练阶段**（学习语言知识）：

```
输入："我喜欢[MASK]苹果"
BERT 的任务：预测 [MASK] 位置应该是什么词
答案：可能是"吃"、"买"、"摘"等
```

通过这种方式，BERT 学会了：
* 词汇的语义
* 词与词之间的关系
* 句子的语法结构

**微调阶段**（应用到具体任务）：

* **文本分类**：判断一段文本的情感（正面/负面）
* **问答**：根据文章回答问题
* **命名实体识别**：找出文本中的人名、地名等

### 为什么重要？

* ✅ **双向理解**：比单向模型（如 GPT）更适合理解任务
* ✅ **预训练模型**：可以在特定任务上快速微调，不需要从头训练
* ✅ **开源**：推动了 NLP 领域的发展

### 典型应用

* 搜索引擎（理解用户查询意图）
* 文本分类系统（垃圾邮件检测、情感分析）
* 信息抽取（从文本中提取结构化信息）

---

## 什么是 T5？

**T5（Text-To-Text Transfer Transformer）** 是 Google 在 2019 年发布的模型，使用完整的 Encoder-Decoder 架构。

### 核心特点

* **架构**：完整的 **Encoder-Decoder** 结构
* **统一框架**：把所有 NLP 任务都转化为"文本到文本"的形式
* **既能理解又能生成**：可以处理理解和生成两类任务

### 工作原理

**统一的任务格式**：

```
翻译：    输入："translate English to German: The house is wonderful."
         输出："Das Haus ist wunderbar."

摘要：    输入："summarize: 长篇文章..."
         输出："摘要内容..."

问答：    输入："question: 问题内容 context: 文章内容"
         输出："答案内容"
```

**工作流程**：

```
输入文本 → Encoder（理解）→ Decoder（生成）→ 输出文本
```

### 为什么重要？

* ✅ **统一框架**：一个模型可以处理多种任务
* ✅ **灵活性强**：既能理解又能生成
* ✅ **效果好**：在多个任务上达到当时的最佳性能

### 典型应用

* **机器翻译**：中英文翻译
* **文本摘要**：长文本压缩为短摘要
* **文本改写**：改写句子保持原意
* **对话系统**：生成回复

---

## BERT vs T5 vs GPT

| 特性 | BERT | T5 | GPT（Decoder-Only） |
| --- | --- | --- | --- |
| 架构 | Encoder-only | Encoder-Decoder | Decoder-only |
| 方向 | 双向（能看到整个输入） | 双向理解 + 单向生成 | 单向（只能看到左侧） |
| 主要用途 | 理解任务 | 理解 + 生成任务 | 生成任务 |
| 能否生成文本 | 否 | 是 | 是 |
| 典型任务 | 分类、问答、NER | 翻译、摘要、改写 | 对话、代码生成 |
| 预训练方式 | Masked LM | 文本到文本 | 自回归生成 |

## 现代发展

虽然 BERT 和 T5 都是重要的里程碑，但现代 LLM 的主流是 **Decoder-Only 架构**（如 GPT、Llama、Claude），因为：

* ✅ **更适合生成任务**：自回归生成更自然
* ✅ **架构更简单**：只需要一个组件
* ✅ **训练更高效**：统一的任务（预测下一个 Token）

但 BERT 和 T5 的思想（预训练、微调、统一框架）仍然影响着现代 LLM 的发展。

## 总结

* **BERT**：Encoder-only，双向理解，适合理解类任务（分类、问答）
* **T5**：Encoder-Decoder，既能理解又能生成，适合需要理解+生成的任务（翻译、摘要）
* **GPT 系列**：Decoder-only，单向生成，适合生成类任务（对话、代码生成）

理解这些模型的区别，能帮助你更好地理解 Transformer 架构的不同应用场景，以及为什么现代 LLM 选择了 Decoder-Only 架构。

---

# 🔔 下一篇预告

第二篇将带你理解：

> 为什么模型能理解你的提示？

> 什么是 Prompt？

> 什么是上下文学习（In-Context Learning）？

