---
title: 飞书多机器人 + 多 Agent：养龙虾进阶，多个助理各司其职
date: 2026-03-10 10:00:00
updated: {{current_date_time}}
categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - 技术学习与行业趋势
tags:
  - OpenClaw
  - 飞书
  - 多机器人
  - 多Agent
  - 养龙虾
keywords: OpenClaw, 飞书, 多机器人, 多Agent, 飞书机器人, 养龙虾
description: '在飞书上设置多个 OpenClaw 机器人，分别对应不同的 Agent 和角色，实现测试助理、代码助理、通用助理等各司其职，相当于多个专业助理。'
top_img: /img/openclaw-multi-bot-cover.png
cover: /img/openclaw-multi-bot-cover.png
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

> **摘要**：养龙虾进阶实践：在飞书上配置多个机器人，每个机器人对应一个独立的 Agent，拥有不同角色和技能。需先在飞书开放平台创建好应用；创建后，**用自然语言把凭证和角色告诉 OpenClaw**，让它帮你生成 `openclaw.json` 配置，或按本文步骤手动配置。每个机器人完全隔离：独立记忆、独立技能、独立模型，相当于多个专业助理各司其职。

**前置条件**：已按 [把 Claude/GPT 搬进飞书：OpenClaw 本地部署与接入完整指南](/2026-03-02-openclaw-local-deploy-feishu-integration) 完成 OpenClaw 部署、API 配置与首个飞书机器人接入。已了解 [如何养龙虾：OpenClaw 技能教程](/2026-03-07-openclaw-skills-tutorial) 中的技能原理与教法。

---

## 速览

| 模块 | 核心内容 |
|------|----------|
| 推荐方式 | 先在飞书创建应用（Coze 部署可用「重新创建」一键创建）→ 把凭证和角色告诉 OpenClaw → AI 生成配置 |
| 核心原理 | 账号层 → 路由层 → Agent 层，三层完全隔离 |
| 飞书侧 | 创建多个企业自建应用，每个应用一个机器人；回调地址可统一填同一个 |
| OpenClaw 侧 | channels.accounts 配置多账户；agents.list 定义多 Agent；bindings 或 account.agent 做绑定 |
| 隔离优势 | 独立记忆、独立技能、独立模型，不串消息 |

---

## 一、为什么需要多个机器人 + 多 Agent？

单个机器人 + 单 Agent 时，所有对话共用一个「大脑」，技能混在一起，容易出现：

- **意图混淆**：用户说「帮我拆测试点」和「帮我 review 这段代码」，同一个 Agent 要兼顾测试、代码、通用问答，容易顾此失彼
- **上下文臃肿**：技能越多，description 越多，匹配越慢、越不准
- **角色不清**：无法给用户「这是测试专家」「这是代码专家」的明确预期

**多机器人 + 多 Agent** 的思路是：**一个机器人 = 一个专业助理**。用户 @ 测试助理，就只处理测试相关；@ 代码助理，就只处理代码相关。每个 Agent 只加载自己领域的技能，角色清晰、执行稳定。且**记忆完全隔离**：给 A 机器人说的「记住我明天开会」，B 机器人不会知道。

---

## 二、核心原理：账号-路由-Agent 三层架构

OpenClaw 采用 **「账号层 → 路由层 → Agent 层」** 三层分离架构，实现多机器人独立身份、独立记忆、独立能力的完全隔离：

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 飞书机器人 1    │ ──→ │ 路由规则匹配     │ ──→ │ Agent 1 实例     │
│ (独立 appId)    │     │ (accountId→     │     │ (独立记忆/技能)  │
└─────────────────┘     │  agentId)       │     └─────────────────┘
┌─────────────────┐     └─────────────────┘     ┌─────────────────┐
│ 飞书机器人 2    │ ──→ │ 路由规则匹配     │ ──→ │ Agent 2 实例     │
│ (独立 appId)    │     │ (accountId→     │     │ (独立记忆/技能)  │
└─────────────────┘     │  agentId)       │     └─────────────────┘
```

**路由匹配流程**：飞书推送消息时带 `appId` → OpenClaw 找到对应 `accountId` → 遍历 bindings 匹配 `agentId` → 消息交给对应 Agent 处理 → Agent 在自己的工作空间内生成回复 → 通过对应飞书账号发回。

**关键点**：所有机器人的回调地址可**统一填同一个**（如 `https://你的域名/webhook/feishu` 或长连接模式），OpenClaw 通过 `appId` 自动区分是哪个机器人收到的消息。

---

## 三、推荐方式：自然语言生成配置

**说明**：OpenClaw **不会**自动创建飞书机器人，需先在 [飞书开放平台](https://open.feishu.cn/app) 创建好应用并拿到 App ID、App Secret。创建完成后，用自然语言把凭证和角色需求告诉 OpenClaw，让它帮你生成 `openclaw.json` 配置，无需手动改 JSON。

### 3.1 你先做：在飞书创建应用

在飞书开放平台为每个机器人创建独立应用，拿到 App ID 和 App Secret。权限、事件订阅、发布等步骤参考 [部署指南](/2026-03-02-openclaw-local-deploy-feishu-integration) 第四节。所有应用的回调地址填同一个，OpenClaw 通过 appId 自动区分。

**若你是用 Coze 一键部署的 OpenClaw**：可在 Coze 的 OpenClaw 配置弹窗中，找到「渠道配置」下的飞书卡片，点击 **「重新创建」** 按钮，一键创建新的飞书机器人并完成授权，无需手动去飞书开放平台逐个创建应用。创建完成后，再按 3.2 把凭证和角色告诉 OpenClaw 生成多 Agent 配置即可。

![OpenClaw 控制台：设置 → 配置，进入 Agents 等配置管理](/img/openclaw-dashboard-config.png)

![Coze 部署的 OpenClaw：渠道配置中的「重新创建」可一键创建新飞书机器人](/img/openclaw-coze-recreate-feishu.png)

### 3.2 然后跟 OpenClaw 说

在 OpenClaw 的 Web 控制台或飞书聊天中，把已创建的机器人凭证和角色需求告诉它，例如：

```
我在飞书创建了 3 个应用，凭证如下：
1. 呷呷（个人助理）：App ID cli_xxx1，App Secret xxx1
2. Harry（测试组长）：App ID cli_xxx2，App Secret xxx2
3. 客服机器人：App ID cli_xxx3，App Secret xxx3

帮我生成 openclaw.json 配置，让它们分别对应不同的 Agent：
呷呷处理日常事务、写代码、整理文档；Harry 专门写测试用例、分析 Bug；客服机器人只能访问知识库。三个机器人记忆不互通。
```

或分步说：

```
我新建了两个飞书应用，App ID 是 cli_xxx2 和 cli_xxx3，分别叫 Harry 和机器人 1 号。帮我加到 openclaw 配置里，Harry 是测试组长，机器人 1 号做测试沙箱
```

### 3.3 OpenClaw 会帮你做什么

根据你提供的凭证和角色描述，OpenClaw 会生成：

- `channels.feishu.accounts` 中的多账户配置
- `agents.list` 中的多 Agent 定义（含 workspace、identity 等）
- `bindings` 中的路由规则

你只需将生成的内容写入 `~/.openclaw/openclaw.json`，重启网关即可生效。

---

## 四、手动配置：一步步实现

若希望自己掌控配置，或理解底层原理，可按以下步骤手动配置。

### 4.1 整体流程概览

```
飞书用户
    │
    ├─ @测试助理 ──→ 飞书应用 A (appId: cli_xxx1) ──→ OpenClaw account: test-assistant
    │                                                    │
    │                                                    └─→ Agent: test-agent (技能: PRD拆解、用例生成、日志分析)
    │
    ├─ @代码助理 ──→ 飞书应用 B (appId: cli_xxx2) ──→ OpenClaw account: code-assistant
    │                                                    │
    │                                                    └─→ Agent: code-agent (技能: 代码审查、重构建议、Git操作)
    │
    └─ @通用助理 ──→ 飞书应用 C (appId: cli_xxx3) ──→ OpenClaw account: main
                                                         │
                                                         └─→ Agent: main (技能: 通用问答、文档总结)
```

---

### 4.2 飞书侧：创建多个机器人

每个机器人对应一个飞书企业自建应用。若已创建过第一个，按相同流程再创建即可。**所有机器人的回调地址可填同一个**，OpenClaw 通过 `appId` 自动区分。

#### 创建应用

1. 打开 [飞书开放平台](https://open.feishu.cn/app)
2. 点击「创建企业自建应用」
3. 填写应用名称（即机器人名称，如「测试助理」「代码助理」「通用助理」）、描述、图标
4. 创建完成后，在「凭证与基本信息」中复制 **App ID** 和 **App Secret**

#### 配置权限与机器人能力

与单机器人相同：在「权限管理」中批量导入权限 JSON；在「应用能力」中启用机器人并设置机器人名称。权限 JSON 可参考 [部署指南](/2026-03-02-openclaw-local-deploy-feishu-integration) 中的 Step 3。

#### 配置事件订阅与发布

在「事件与回调」中选择长连接、订阅 `im.message.receive_v1`；在「版本管理与发布」中创建版本并发布。**注意**：需先完成 OpenClaw 侧的 `channels add` 并启动网关，再保存长连接。

#### 建议的机器人命名

| 机器人名称 | 角色定位 | 典型技能 |
|------------|----------|----------|
| 测试助理 | 测试工程师助手 | PRD 拆测试点、接口用例生成、日志分析 |
| 代码助理 | 代码审查与重构 | 代码 review、重构建议、Git 操作 |
| 通用助理 | 日常问答与文档 | 通用问答、文档总结、知识检索 |

---

### 4.3 OpenClaw 侧：配置账号层 + Agent 层 + 路由层

编辑 `~/.openclaw/openclaw.json`（Windows 为 `C:\Users\你的用户名\.openclaw\openclaw.json`），配置三个核心块。

#### ① 账号层（channels.feishu.accounts）

将每个飞书应用的凭证加入 `accounts`。可在每个 account 中直接加 `agent` 字段绑定 Agent，或通过 bindings 统一配置：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "defaultAccount": "main",
      "accounts": {
        "main": {
          "appId": "cli_xxx1",
          "appSecret": "secret1",
          "botName": "呷呷",
          "agent": "main"
        },
        "test-assistant": {
          "appId": "cli_xxx2",
          "appSecret": "secret2",
          "botName": "Harry",
          "agent": "test-agent"
        },
        "code-assistant": {
          "appId": "cli_xxx3",
          "appSecret": "secret3",
          "botName": "代码助理",
          "agent": "code-agent"
        }
      }
    }
  }
}
```

`defaultAccount` 指定未匹配时的默认账户。

#### ② Agent 层（agents.list）

为每个角色定义独立的 Agent，可配置 `identity`（名称、emoji）、`workspace`、`model`（不同 Agent 可用不同模型）：

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "identity": { "name": "呷呷", "emoji": "🦞" },
        "workspace": "~/.openclaw/workspace"
      },
      {
        "id": "test-agent",
        "identity": { "name": "Harry", "emoji": "🦉" },
        "workspace": "~/.openclaw/workspace/test-agent",
        "model": "anthropic/claude-sonnet-4-5"
      },
      {
        "id": "code-agent",
        "identity": { "name": "代码助理", "emoji": "🤖" },
        "workspace": "~/.openclaw/workspace/code-agent"
      }
    ]
  }
}
```

可为专业机器人分配更强的模型，普通机器人用轻量模型节省成本。

#### ③ 路由层（bindings）

若未在 account 中配置 `agent`，需在 `bindings` 中配置 accountId → agentId 映射：

```json
{
  "bindings": [
    { "agentId": "main", "match": { "channel": "feishu", "accountId": "main" } },
    { "agentId": "test-agent", "match": { "channel": "feishu", "accountId": "test-assistant" } },
    { "agentId": "code-agent", "match": { "channel": "feishu", "accountId": "code-assistant" } }
  ]
}
```

#### 完整配置示例

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "defaultAccount": "main",
      "accounts": {
        "main": {
          "appId": "cli_xxx1",
          "appSecret": "secret1",
          "botName": "呷呷",
          "agent": "main"
        },
        "test-assistant": {
          "appId": "cli_xxx2",
          "appSecret": "secret2",
          "botName": "Harry",
          "agent": "test-agent"
        },
        "code-assistant": {
          "appId": "cli_xxx3",
          "appSecret": "secret3",
          "botName": "代码助理",
          "agent": "code-agent"
        }
      }
    }
  },
  "agents": {
    "list": [
      { "id": "main", "identity": { "name": "呷呷", "emoji": "🦞" }, "workspace": "~/.openclaw/workspace" },
      { "id": "test-agent", "identity": { "name": "Harry", "emoji": "🦉" }, "workspace": "~/.openclaw/workspace/test-agent" },
      { "id": "code-agent", "identity": { "name": "代码助理", "emoji": "🤖" }, "workspace": "~/.openclaw/workspace/code-agent" }
    ]
  },
  "bindings": [
    { "agentId": "main", "match": { "channel": "feishu", "accountId": "main" } },
    { "agentId": "test-agent", "match": { "channel": "feishu", "accountId": "test-assistant" } },
    { "agentId": "code-agent", "match": { "channel": "feishu", "accountId": "code-assistant" } }
  ]
}
```

---

### 4.4 独立工作空间隔离

每个 Agent 有完全独立的运行环境：

- **独立记忆**：各自的 `MEMORY.md` 长期记忆、`memory/YYYY-MM-DD.md` 每日记忆，互不互通
- **独立技能**：各自 workspace 下的 skills，不会串用
- **独立模型**：可为不同 Agent 分配不同大模型（如专业机器人用 Pro，普通用 Lite）
- **独立会话**：会话历史按 Agent 隔离

---

## 五、为每个 Agent 准备技能

每个 Agent 的 `workspace` 下应有独立的 `skills` 目录，存放该角色专属的技能。

### 5.1 目录结构示例

```
~/.openclaw/workspace/
├── skills/                    # main 的技能（通用）
│   └── ...
├── test-agent/
│   └── skills/                # 测试助理的技能
│       ├── prd-testpoints/
│       │   └── SKILL.md
│       ├── api-testcase-gen/
│       │   └── SKILL.md
│       └── log-analysis/
│           └── SKILL.md
└── code-agent/
    └── skills/                # 代码助理的技能
        ├── code-review/
        │   └── SKILL.md
        └── github/
            └── SKILL.md
```

### 5.2 技能来源

- **手写**：按 [养龙虾教程](/2026-03-07-openclaw-skills-tutorial) 中的方法，为每个 workspace 编写 SKILL.md
- **安装**：`npx clawhub@latest install <skill>` 时指定 `--workspace` 或安装后复制到对应 workspace
- **自然语言生成**：在 Web 控制台选择对应 Agent 的会话，用自然语言让 OpenClaw 生成技能并写入该 workspace

---

## 六、启动与验证

### 6.1 启动网关

```bash
openclaw gateway
```

若已安装为服务，可执行 `openclaw gateway restart` 使配置生效。

### 6.2 验证路由与记忆隔离

1. 在飞书中分别搜索各机器人名称，发起私聊
2. 对测试助理说「帮我拆测试点」，应触发测试相关技能
3. 对代码助理说「帮我 review 这段代码」，应触发代码相关技能
4. 对通用助理说「今天天气怎么样」，应走通用问答
5. **验证记忆隔离**：分别给不同机器人发「记住我的手机号是 138xxxx1234」，再问「我的手机号是多少？」——每个机器人只会记得自己收到的信息，不会串记忆

**实践效果**：分别 @ 不同机器人说「介绍一下自己」，每个机器人会按自己的身份回复——呷呷以全能助理、Harry 以测试组组长等不同人设回应，证明路由正确、身份隔离生效。

![多机器人实践效果：呷呷与 1 号（Harry）分别介绍自己，身份与人设独立](/img/openclaw-multi-bot-practice.png)

### 6.3 查看日志

```bash
openclaw logs --follow
```

可看到消息路由到哪个 `agentId`、哪个 `accountId`，便于排查绑定是否生效。

---

## 七、进阶：按用户或群组路由

除按 `accountId` 路由外，还可按**用户**（`peer.kind: "direct"`）或**群组**（`peer.kind: "group"`）路由，实现「同一机器人、不同用户/群用不同 Agent」。

```json
{
  "bindings": [
    {
      "agentId": "test-agent",
      "match": {
        "channel": "feishu",
        "peer": { "kind": "direct", "id": "ou_用户A的open_id" }
      }
    },
    {
      "agentId": "code-agent",
      "match": {
        "channel": "feishu",
        "peer": { "kind": "group", "id": "oc_代码评审群的chat_id" }
      }
    }
  ]
}
```

用户 ID（`ou_xxx`）和群 ID（`oc_xxx`）可通过 `openclaw logs --follow` 在用户发消息时从日志中获取，或通过 `openclaw pairing list feishu` 查看配对请求中的用户 ID。

---

## 八、常见问题

| 问题 | 可能原因 | 解决思路 |
|------|----------|----------|
| 多个机器人回复都是同一个身份 | bindings 未生效或 account.agent 未配置 | 检查 `accounts` 中每个账号的 `agent` 字段，或 `bindings` 的 `accountId` 是否与 `accounts` 的 key 一致；重启网关 |
| 消息都走 main | bindings 未生效或 accountId 不匹配 | 检查 bindings 是否包含所有账号的映射；重启网关 |
| 机器人收不到消息 | 飞书应用回调地址未配置或长连接未保存 | 检查回调地址是否正确；确保网关已启动后再保存长连接；检查消息接收权限 |
| 机器人发不出消息 | App ID/Secret 错误或权限不足 | 检查凭证是否正确；检查飞书应用是否已申请发送消息权限；确认机器人已加入通讯录/群 |
| 技能未被触发 | Agent 的 workspace 下无对应技能 | 检查 `agents.list` 中该 Agent 的 `workspace` 路径，确认 skills 目录存在且 SKILL.md 有效 |

若遇 bindings 相关 bug（如多账户路由失败），可关注 [OpenClaw 官方 Issue](https://github.com/openclaw/openclaw/issues)，社区有相关修复讨论。

---

## 📚 延伸资源

- [OpenClaw 飞书通道文档](https://docs.openclaw.ai/channels/feishu) — 多账户、Multi-agent routing 官方说明
- [把 Claude/GPT 搬进飞书：OpenClaw 本地部署与接入完整指南](/2026-03-02-openclaw-local-deploy-feishu-integration)
- [如何养龙虾：OpenClaw 技能教程](/2026-03-07-openclaw-skills-tutorial)

---

## ✍️ 结语

多机器人 + 多 Agent 的本质是**分工**：每个机器人对应一个专业助理，每个 Agent 只加载自己领域的技能，用户按需 @ 不同助理，获得更精准、更稳定的回复。**完全隔离**：独立记忆、独立技能、独立模型，不串消息。推荐先用自然语言跟 OpenClaw 对话生成配置，再按需手动微调；单网关可承载多个机器人，成本几乎为零。从单助理到多助理，是养龙虾的进阶实践，适合对角色分离、技能隔离有要求的团队。
