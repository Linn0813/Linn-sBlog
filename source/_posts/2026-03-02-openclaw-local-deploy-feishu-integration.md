---
title: 把 Claude/GPT 搬进飞书：OpenClaw 本地部署与接入完整指南
date: 2026-03-02 10:00:00
updated: {{current_date_time}}
categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - 技术学习与行业趋势
tags:
  - OpenClaw
  - 飞书
  - AI助手
  - 本地部署
  - 飞书机器人
  - 测试
  - 研发效率
keywords: OpenClaw, 飞书, 本地部署, AI助手, 飞书机器人, 开源AI, WebSocket, 测试用例, PRD, 研发流程
description: '从动机到落地：详解为什么要搭建 OpenClaw、本地部署的好处、飞书接入的完整操作步骤，以及 PRD 拆测试点、接口用例生成、日志分析等实际使用场景'
top_img: /img/openclaw-feishu.png
cover: /img/openclaw-feishu.png
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

> **摘要**：OpenClaw 是一款开源的自托管 AI 助手网关，能将 Claude、GPT 等大模型接入飞书、Telegram、Discord 等聊天平台。本文从「为什么要搭建」讲起，拆解本地部署的核心优势、飞书接入的完整流程，以及接入后的实际使用方式，帮你把 AI 助手「搬进」日常办公场景。

**OpenClaw 的本质**：它是一个**自托管的 AI 消息网关**——负责把聊天平台的消息路由到 LLM，再把 LLM 的回复发回聊天平台。它本身不提供模型能力，需要你配置 Claude、GPT 等 API Key。与飞书自带的 AI 助手、Coze 机器人不同，OpenClaw 数据全在你自己的机器上，可深度定制。

---

## 🧐 一、为什么要搭建 OpenClaw + 飞书？

在动手部署之前，先搞清楚：**这件事能解决什么问题？**

### 1.1 痛点：AI 和办公场景是割裂的

很多人已经习惯用 ChatGPT、Claude 写代码、查资料，但存在几个现实问题：

| 痛点 | 描述 |
|------|------|
| **切换成本高** | 写文档、开会、沟通在飞书，查 AI 要切到浏览器或独立 App |
| **数据隐私顾虑** | PRD、接口文档、测试策略、内部流程等敏感信息直接丢给公网 AI，存在泄露风险 |
| **无法团队共享** | 每个人各用各的，无法在群聊里统一调用同一个 AI 助手 |
| **公网部署麻烦** | 传统 Webhook 需要公网 URL、备案、HTTPS，内网环境很难搞 |

### 1.2 更深层的诉求：把 AI 嵌进工作流

搭建本地 AI 服务，不只是「多一个聊天工具」，而是：

- **数据安全**：所有对话、文档留在本地或自建服务器，不产生外部调用记录
- **成本可控**：一次部署长期使用，无 token 计费、QPS 限制
- **可定制化**：可接入内部知识库、测试用例系统、CI 数据，从「聊天工具」升级为「团队智能助手」（飞书知识库集成思路见 [飞书开放平台深度集成全指南](/2025-11-28-feishu-ai-knowledge-integration-guide/)）
- **工作流自动化**：PRD → 自动拆测试点、接口文档 → 自动生成用例、日志 → 自动分析异常

### 1.3 解决方案：把 AI 搬进飞书

OpenClaw 的核心价值是：**在你已经高频使用的飞书里，接入一个可自托管的 AI 助手**。

- **数据在你自己的机器上**：对话、配置、日志都在本地或自建服务器，不经过第三方
- **无需公网暴露**：飞书支持 WebSocket 长连接，OpenClaw 主动连飞书，内网即可运行
- **团队共享**：把机器人拉进群，@ 一下就能用，无需每人单独配置

---

## 🛠️ 二、本地部署 OpenClaw

### 2.1 部署前准备

#### 环境要求

| 项目 | 要求 |
|------|------|
| Node.js | **22+**（必须，20 以下不支持） |
| 内存 | 最低 2GB，推荐 4GB+ |
| 存储 | 至少 5GB |
| API Key | 至少一个：Anthropic（Claude）、OpenAI（GPT）或 Google（Gemini） |

#### 检查 Node.js 版本

在终端执行：

```bash
node --version
```

若显示 `v22.x.x` 或更高即可。若版本不足，详见文末 [「Node.js 版本不足」专项说明](#nodejs-版本不足)。

---

### 2.2 macOS 部署

#### 方式一：一键安装（推荐）

1. 打开「终端」（Terminal）或 iTerm
2. 执行：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

3. 脚本会自动检测 Node.js，若未安装或版本不足会提示安装，全程约 5 分钟

![OpenClaw 安装脚本执行效果：检测到 macOS，通过 Homebrew 升级 Node.js](/img/openclaw-install-macos.png)

> **⚠️ 若在 [2/3] Installing OpenClaw 阶段出现 `npm install failed`**（常见于 Mac，可能为 sharp 与 libvips 冲突，或 npm 缓存权限异常），详见文末 [「npm install 失败」专项排查](#npm-install-失败mac-常见)。

4. 若不想同时运行引导向导，可加参数：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

#### 方式二：npm 安装

若已安装 Node.js 22+：

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

> **若 Node.js 版本不足**，详见文末 [「Node.js 版本不足」专项说明](#nodejs-版本不足)。

#### 验证安装（macOS）

```bash
openclaw --version
openclaw doctor
```

---

### 2.3 Windows 部署

#### 方式一：PowerShell 一键安装（推荐）

1. 以**管理员身份**打开 PowerShell（右键「以管理员身份运行」）
2. 若提示执行策略限制，先执行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. 执行安装脚本：

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

4. 若不想同时运行引导向导：

```powershell
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
```

#### 方式二：WSL2 + Linux 方式（推荐，兼容性更好）

Windows 上推荐使用 WSL2 运行 OpenClaw，可避免不少兼容性问题。

1. **安装 WSL2**：以管理员身份打开 PowerShell，执行：

```powershell
wsl --install
```

2. 重启电脑后，打开「Ubuntu」或「WSL」终端
3. 在 WSL 终端中执行（与 Linux 相同）：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

4. 安装完成后，在 Windows 浏览器访问 `http://localhost:18789` 即可使用 Web 控制面板（WSL2 会自动转发 localhost）

#### 方式三：npm 安装（需先装 Node.js）

1. 安装 Node.js 22+（从 [nodejs.org](https://nodejs.org/) 下载，或详见文末 [「Node.js 版本不足」专项说明](#nodejs-版本不足)）
2. 打开「命令提示符」或 PowerShell，执行：

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

#### 验证安装（Windows）

```bash
openclaw --version
openclaw doctor
```

若提示「找不到 openclaw」，可能是 npm 全局目录未加入 PATH，可将 `C:\Users\你的用户名\AppData\Roaming\npm` 加入系统环境变量。

---

### 2.4 初始化与验证（所有平台通用）

安装完成后，执行：

```bash
openclaw onboard --install-daemon
```

安装脚本会自动进入初始化引导步骤。

#### 操作方式

使用 **左方向键（←）** 和 **右方向键（→）** 切换选项；多选时按 **空格键** 勾选，按 **回车键** 进入下一步。

#### 引导配置项说明

| 配置项 | 描述 | 建议配置 |
|--------|------|----------|
| **I understand this is powerful and inherently risky. Continue?** | 提醒用户该功能有高权限风险，确认后才允许继续 onboarding | 勾选 **Yes**，明确知晓风险后继续 |
| **Onboarding mode** | 初次引导模式，用于快速完成基础配置（模型、渠道、hooks 等） | 选 **QuickStart**，快速上手并生成默认配置 |
| **Model/auth provider** | 选择大模型提供商及认证方式，用于 OpenClaw 调用大模型 API | 选 **Skip for now** 跳过，后续在飞书接入前再配置 |
| **Filter models by provider** | 是否仅显示选定提供商的模型 | 选 **All providers** |
| **Default model** | 启动后默认使用的模型 | 使用默认（如 `anthropic/claude-opus-4-6`），或按需选择 |
| **Select channel (QuickStart)** | 初始渠道选择，用于快速部署和测试消息收发 | 选 **Skip for now**，后续用 `openclaw channels add` 添加飞书 |
| **Configure skills now? (recommended)** | 是否立即配置 agent 技能（自定义指令、工具链等） | 选 **No**，后续按需配置 |
| **Enable hooks?** | 是否启用内部 hooks（command-logger、session-memory 等） | 按空格勾选后回车。建议勾选：① **command-logger**（记录执行命令，便于审计/调试）；② **session-memory**（提供上下文记忆能力） |
| **Gateway service already installed** | 检测到已安装网关时的处理 | 选 **reset** 重新安装，或保持现有 |
| **How do you want to hatch your bot** | 完成引导后的操作 | 选 **Open the Web UI**，适合新手在浏览器中体验 |

> **若在引导中跳过了 Model/auth**：完成引导后，需在接入飞书前配置 API Key。可重新运行 `openclaw configure` 或编辑 `~/.openclaw/openclaw.json` 添加 `ANTHROPIC_API_KEY` 等。

**引导完成后**：浏览器会自动打开 Web 控制台（如 `http://127.0.0.1:18789/chat?session=agent%3Amain%3Amain`）。此时**还不能正常对话**，因为大模型 API 尚未配置。请按下方 [2.5 配置大模型 API](#25-配置大模型-api) 完成配置后，聊天功能才会生效。

![OpenClaw 控制台：引导完成后打开聊天页，需先配置 API 才能对话](/img/openclaw-dashboard-chat.png)

**验证安装**：

```bash
openclaw doctor    # 检查健康状态
openclaw status   # 查看网关状态
openclaw dashboard  # 启动 Web 控制面板（可选）
```

完成 API 配置后即可进入飞书接入步骤。

---

### 2.5 配置大模型 API

OpenClaw 本身不提供模型，需配置至少一个 API Key 才能对话。将你已有的 Anthropic、OpenAI 等 API Key 配置进来即可。

#### 配置方式一：命令行向导（推荐）

1. 在终端执行：

```bash
openclaw configure
```

2. 若向导询问配置范围，选择 **auth** 或 **models**（或直接进入完整向导）
3. 按提示依次操作：
   - **选择提供商**：如 `anthropic`（Claude）或 `openai`（GPT）
   - **输入 API Key**：粘贴你的密钥（Anthropic 格式 `sk-ant-...`，OpenAI 格式 `sk-...`）
   - **选择默认模型**：如 `anthropic/claude-sonnet-4-5`、`openai/gpt-4o` 等
4. 完成后，若网关已在运行，配置会自动生效；否则执行 `openclaw gateway` 启动网关
5. 刷新 Web 聊天页 `http://127.0.0.1:18789`，发送消息验证是否正常回复

#### 配置方式二：Web 控制台

1. 打开 `http://127.0.0.1:18789`，确保网关已启动
2. 左侧菜单点击「设置」→「配置」
3. 在配置页中找到 **env** 或 **Auth / Models** 相关区域：
   - 若有 **env** 区块：添加 `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY`，值为你的密钥
   - 若有 **agents.defaults.model**：将 `primary` 设为如 `anthropic/claude-sonnet-4-5`
4. 点击保存（部分主题为「Apply」或「应用」）
5. 返回「聊天」页，发送一条消息测试

#### 配置方式三：手动编辑配置文件

1. 打开 `~/.openclaw/openclaw.json`（Mac/Linux 为 `~`，Windows 为 `C:\Users\你的用户名\.openclaw\`）
2. 在根级加入 `env` 和 `agents` 配置（若已有则合并）：

**Anthropic 示例：**

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-你的密钥"
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-5"
      }
    }
  }
}
```

**OpenAI 示例：**

```json
{
  "env": {
    "OPENAI_API_KEY": "sk-你的密钥"
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "openai/gpt-4o"
      }
    }
  }
}
```

3. 保存文件后，网关会自动热加载配置（若未生效可执行 `openclaw gateway restart`）
4. 刷新聊天页验证

> ⚠️ **安全建议**：可将 API Key 放在 `~/.openclaw/.env` 中（每行 `ANTHROPIC_API_KEY=sk-ant-xxx`），OpenClaw 会自动读取，`openclaw.json` 中只需配置 `agents.defaults.model.primary`。执行 `chmod 600 ~/.openclaw/.env` 限制文件权限。

配置完成后，在 Web 聊天页或飞书中即可正常对话。

---

### 2.6 云部署选项（可选）

若不想在本地长期跑网关，可考虑云部署，目前较火的方案有：

| 方案 | 特点 | 适用场景 |
|------|------|----------|
| **Coze 编程** | 在 [code.coze.cn](https://code.coze.cn/home) 找到 OpenClaw 案例，点击「创建副本」即可，约 1 分钟跑通；需开通 Coze 高阶版（约 49 元/月起） | 快速体验、非技术用户 |
| **腾讯云 Lighthouse** | 轻量应用服务器提供 OpenClaw 应用镜像，新购或重装时选「AI 智能体 → OpenClaw」，3–5 分钟部署；支持腾讯混元、DeepSeek、通义等国内模型，飞书/钉钉/企微/QQ 可视化配置 | 7×24 运行、多 IM 接入、国内模型 |

云部署与本地部署的飞书接入流程一致：创建飞书应用、配置权限、`openclaw channels add` 或填入凭证。区别在于网关跑在云端，需放通 18789 端口并确保公网可访问（若用 Webhook 模式）。更多细节可参考 [Coze 编程 OpenClaw 案例](https://code.coze.cn/home)、[腾讯云 OpenClaw 一键部署](https://cloud.tencent.com/developer/article/2624003)。

---

## 📱 四、飞书接入完整步骤

### Step 1：安装飞书插件

在终端执行（Mac / Windows / WSL 通用）：

```bash
openclaw plugins install @openclaw/feishu
```

看到安装成功提示即可进入下一步。

---

### Step 2：创建飞书应用

1. 打开 [飞书开放平台](https://open.feishu.cn/app)（海外用户用 [Lark](https://open.larksuite.com/app)）
2. 使用飞书账号登录，点击「创建企业自建应用」
3. 填写：
   - **应用名称**：如「AI 小助手」
   - **应用描述**：如「团队 AI 助手，支持 PRD 拆解、用例生成等」
   - **应用图标**：上传一张图片（可选）
4. 创建完成后，进入应用详情页
5. 左侧菜单找到「凭证与基本信息」，复制：
   - **App ID**（格式为 `cli_xxxxxxxxxx`）
   - **App Secret**（点击「显示」后复制）

> ⚠️ App Secret 务必保密，切勿泄露或提交到代码仓库。

---

### Step 3：配置权限

1. 在飞书应用后台，左侧菜单进入「权限管理」
2. 点击「批量导入」或「添加权限」
3. 在批量导入框中，**完整粘贴**以下 JSON（不要漏掉任何字符）：

```json
{
  "scopes": {
    "tenant": [
      "aily:file:read",
      "aily:file:write",
      "application:application.app_message_stats.overview:readonly",
      "application:application:self_manage",
      "application:bot.menu:write",
      "contact:user.employee_id:readonly",
      "corehr:file:download",
      "event:ip_list",
      "im:chat.access_event.bot_p2p_chat:read",
      "im:chat.members:bot_access",
      "im:message",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:readonly",
      "im:message:send_as_bot",
      "im:resource"
    ],
    "user": ["aily:file:read", "aily:file:write", "im:chat.access_event.bot_p2p_chat:read"]
  }
}
```

### Step 4：启用机器人能力

1. 左侧菜单进入「应用能力」
2. 找到「机器人」卡片，点击「启用」
3. 设置**机器人名称**（如「AI 小助手」），用户 @ 时会显示此名称
4. 保存

---

### Step 5：配置 OpenClaw 连接飞书（必须先做）

⚠️ **关键顺序**：必须先完成本步骤（配置 OpenClaw + 启动网关），再去做 Step 6（在飞书后台保存长连接）。否则飞书无法验证连接，长连接会保存失败。

1. 在终端执行：

```bash
openclaw channels add
```

2. 按提示选择「Feishu」或「飞书」
3. 依次输入：
   - App ID（刚才复制的 `cli_xxx`）
   - App Secret
4. 配置完成后，**保持终端打开**，执行：

```bash
openclaw gateway
```

5. 看到类似 `Gateway running on ws://127.0.0.1:xxxxx` 的提示，表示网关已启动

**或手动编辑配置文件**：打开 `~/.openclaw/openclaw.json`（Mac/Linux 为 `~`，Windows 为 `C:\Users\你的用户名\.openclaw\openclaw.json`），在 `channels` 中加入：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "accounts": {
        "main": {
          "appId": "cli_你的AppID",
          "appSecret": "你的AppSecret",
          "botName": "AI 小助手"
        }
      }
    }
  }
}
```

---

### Step 6：配置事件订阅（长连接）

在**网关已启动**的前提下：

1. 回到飞书开放平台，左侧菜单进入「事件与回调」
2. 找到「事件订阅」或「请求地址」相关设置
3. 选择「**长连接（Socket Mode）**」或「使用长连接接收事件」
4. 在「订阅事件」中添加：`im.message.receive_v1`
5. 点击「保存」

若保存失败，检查：
- 网关是否在运行（`openclaw gateway` 的终端不能关）
- 是否已完成 `openclaw channels add` 并填写了正确的 App ID 和 Secret

---

### Step 7：发布应用

1. 左侧菜单进入「版本管理与发布」
2. 点击「创建版本」，填写版本说明（如「首次发布」）
3. 选择本次更新涉及的权限（勾选刚才配置的权限）
4. 提交审核
5. 企业自建应用通常会自动通过，通过后点击「发布」
6. 发布成功后：
   - **私聊测试**：在飞书搜索你的机器人名称，发起私聊，发一条消息
   - **群聊测试**：创建一个群，在「群设置」→「群机器人」→「添加机器人」中搜索并添加你的应用，在群内 @ 机器人发消息

---

## 🎯 五、接入之后可以如何使用？

### 5.1 基础用法：私聊与群聊

**私聊**：直接给机器人发消息，即可获得 AI 回复，适合个人查询、代码辅助、文档总结等。

**群聊**：将机器人拉入群聊，**默认需要 @ 机器人** 才会触发回复，避免刷屏。可在配置中为特定群设置 `requireMention: false`（慎用）。

### 5.2 落地场景：测试与研发工作流

接入飞书后，AI 不再只是「聊天工具」，而是可以参与日常研发流程的助手。以下是几种典型用法：

#### 场景一：PRD → 自动生成测试点

在群内 @ 机器人：

```
@AI 这是新功能 PRD 链接，帮我拆测试点
```

AI 可输出：功能点拆解、边界场景、异常场景、数据验证等，可显著减少测试设计时间。若需更精细的 Prompt 设计，可参考 [测试用例生成 Prompt 的完整设计](/2026-02-27-test-case-generation-prompt-design/)。

#### 场景二：接口文档 → 自动生成 API 用例

```
@AI 根据以下接口文档生成接口测试用例
```

输出可包含：正常流程、参数校验、权限校验、边界值、异常码验证等。

#### 场景三：日志分析

粘贴报错日志：

```
@AI 分析以下报错原因
```

AI 可识别异常类型、分析可能原因、给出排查方向。

#### 场景四：回归测试数据生成

```
@AI 生成 10 条边界测试数据
```

适用于参数 fuzz、表单测试、输入验证测试等场景。

#### 场景五：内部知识问答

若接入 RAG 知识库，可实现：

```
@AI 公司发布流程是什么？
```

直接返回内部流程说明，无需翻文档。

### 5.3 升级玩法：构建 AI 测试平台

进一步扩展，可实现：

- 飞书机器人触发 Jenkins 构建
- 自动生成测试报告并推送群内
- 用例自动入库
- API 自动化测试脚本生成

这就不是简单的聊天机器人，而是**真正参与团队研发流程的 AI 助手**。

### 5.4 多 Agent 路由（进阶）

可为不同用户或群组绑定不同的 AI Agent，实现「千人千面」：

```json
{
  "agents": {
    "list": [
      { "id": "main" },
      { "id": "code-helper", "workspace": "/path/to/code-agent" }
    ]
  },
  "bindings": [
    {
      "agentId": "main",
      "match": { "channel": "feishu", "peer": { "kind": "direct", "id": "ou_xxx" } }
    },
    {
      "agentId": "code-helper",
      "match": { "channel": "feishu", "peer": { "kind": "group", "id": "oc_yyy" } }
    }
  ]
}
```

### 5.5 常用管理命令

| 命令 | 说明 |
|------|------|
| `openclaw gateway` | 启动网关 |
| `openclaw gateway status` | 查看网关状态 |
| `openclaw logs --follow` | 实时查看日志 |
| `openclaw doctor` | 健康检查 |
| `openclaw channels add` | 添加/修改频道配置 |

---

## 🔧 六、常见问题与排查

### 部署阶段

| 问题 | 可能原因 | 解决思路 |
|------|----------|----------|
| `openclaw` 命令找不到 | npm 全局目录未加入 PATH | 执行 `npm prefix -g` 查看路径，将 `该路径/bin` 加入环境变量；Mac 可执行 `export PATH="$(npm prefix -g)/bin:$PATH"` 并写入 `~/.zshrc` |
| Node.js 版本不足 | 当前版本低于 22 | 见下方 [「Node.js 版本不足」专项说明](#nodejs-版本不足) |
| Mac 上 npm install failed | sharp 与 libvips 冲突或 npm 缓存权限 | 见下方 [「npm install 失败」专项排查](#npm-install-失败mac-常见) |
| Windows 执行策略限制 | PowerShell 禁止运行脚本 | 执行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| WSL2 无法访问 localhost | 网络转发问题 | 在 WSL 内执行 `hostname -I` 获取 IP，在 Windows 浏览器用 `http://<该IP>:18789` 访问 |

#### Node.js 版本不足

OpenClaw 要求 Node.js **22+**。执行 `node --version` 若低于 v22，需先升级。

**macOS：**

**方式一：Homebrew**

```bash
brew install node@22
brew link --overwrite node@22
```

**方式二：nvm**（推荐，便于多版本切换）

```bash
# 安装 nvm（若未安装）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
# 重启终端后
nvm install 22
nvm use 22
nvm alias default 22
```

**Windows：**

- **方式一**：从 [nodejs.org](https://nodejs.org/) 下载 Node.js 22+ 安装包并安装
- **方式二**：使用 WSL2，在 WSL 内按 Linux 方式安装（一键脚本会自动处理）

#### npm install 失败（Mac 常见）

若一键安装脚本在 `[2/3] Installing OpenClaw` 阶段报 `npm install failed`，或手动执行 `npm install -g openclaw@latest` 时报错，常见原因：① sharp 图像库与 Homebrew libvips 冲突；② npm 缓存目录权限异常（`EACCES`、`Your cache folder contains root-owned files`）。

![OpenClaw 安装失败：npm install failed for openclaw@latest](/img/openclaw-install-npm-failed.png)

按顺序尝试以下方案：

| 方案 | 操作 |
|------|------|
| **一** | 修复 npm 缓存权限（EACCES 时必做） |
| **二** | 手动安装并强制使用预编译二进制 |
| **三** | 安装 Xcode 命令行工具后重试 |
| **四** | 改用 nvm 管理 Node |
| **五** | 临时解除 Homebrew libvips 链接 |

**方案一：修复 npm 缓存权限**（若报 `EACCES`、`Your cache folder contains root-owned files`）

```bash
sudo chown -R $(whoami) ~/.npm
```

修复后再执行方案二的安装命令。

**方案二：手动安装并强制使用预编译二进制**

```bash
export PATH="/opt/homebrew/opt/node@22/bin:$PATH"
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
openclaw onboard --install-daemon
```

**方案三：若仍失败，先安装 Xcode 命令行工具**

```bash
xcode-select --install
npm install -g node-gyp
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
```

**方案四：改用 nvm 管理 Node**（避免与 Homebrew 冲突）

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
# 重启终端后
nvm install 22
nvm use 22
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
```

**方案五：临时解除 Homebrew libvips 链接**

```bash
brew unlink vips 2>/dev/null
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
```

### 飞书接入阶段

| 问题 | 可能原因 | 解决思路 |
|------|----------|----------|
| 长连接无法保存 | 网关未启动 | 先运行 `openclaw gateway`，再在飞书后台保存；保存时终端不能关 |
| 403 / 无权限 | 权限未生效 | 在「版本管理与发布」中创建新版本并发布，权限需随版本生效 |
| 群聊里机器人不回复 | 未 @ 机器人 | 默认需 @ 提及才会响应；检查是否已把机器人加入该群 |
| App Secret 泄露 | 误分享 | 在飞书后台「凭证与基本信息」中重置 Secret，并更新 `openclaw.json` 中的 `appSecret` |

---

## 📚 七、延伸资源

**官方文档**：
- [OpenClaw 官方文档](https://open-claw.bot/docs/)
- [OpenClaw 飞书接入指南](https://open-claw.bot/docs/channels/feishu/)
- [飞书开放平台](https://open.feishu.cn/document/)

**本博客相关**：
- [飞书开放平台深度集成全指南](/2025-11-28-feishu-ai-knowledge-integration-guide/) — 飞书知识库与 RAG 的深度集成
- [AI 生成测试用例工具设计](/2026-02-25-ai-test-case-generation-tool-design/) — 测试用例生成的流程化设计

---

## ✍️ 结语

OpenClaw + 飞书的组合，本质上是把 **自托管的 AI 能力** 嵌进 **日常办公的沟通场景**。数据在你手里，部署在内网即可，无需公网暴露，适合对隐私和合规有要求的团队。

真正的价值在于：**把 AI 嵌入到日常研发流程中，而不是单纯用它聊天**。当你把 OpenClaw 接入飞书后，AI 不再是一个网页工具，而是你团队的一部分。

从「为什么搭」到「怎么搭」再到「怎么用」，希望这篇指南能帮你少踩坑，快速把 AI 助手搬进飞书。
