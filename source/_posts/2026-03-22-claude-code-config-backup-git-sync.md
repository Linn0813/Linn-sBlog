---
title: Claude Code 配置备份：用 Git 私有仓库跨机同步
date: 2026-03-22 20:00:00
updated: 2026-03-22 20:00:00
categories:
  - 🧠 LLM/Agent 从入门到精通：告别浅尝辄止
  - AI与研究
tags:
  - Claude Code
  - 配置备份
  - Git
  - 多机同步
keywords: Claude Code, 配置备份, Git 同步, settings.json, agents, skills, CLAUDE.md
description: '用 Git 私有仓库备份 Claude Code 的完整配置（settings、agents、skills、CLAUDE.md），换电脑后执行 restore.sh 即可恢复。'
top_img: /img/claude-config-backup.png
cover: /img/claude-config-backup.png
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

在使用 Claude Code 搭配 LiteLLM 代理（或直连 Anthropic）时，配置会散落在 `~/.claude/` 和 `~/.claude.json` 里。换电脑、重装系统后，这些配置都要重新配一遍。**用 Git 私有仓库做配置备份**，可以一次搭建、多机同步，新电脑上执行 `./restore.sh` 即可恢复。

本文分享一套完整的备份方案：备份内容、脚本逻辑、使用流程，以及和 LiteLLM 代理的配合方式。

> **平台说明**：本文脚本适用于 **macOS 和 Linux**。Windows 用户需在 Git Bash 或 WSL 中运行，并确认 Claude Code 的配置路径是否与 `~/.claude` 一致。

---

## 备份什么？

Claude Code 的配置主要分布在两个位置：

| 路径 | 说明 |
|------|------|
| `~/.claude/settings.json` | 代理地址、Token、环境变量（如 `ANTHROPIC_BASE_URL`） |
| `~/.claude/agents/` | 自定义 Subagent（如 `/my-agent`） |
| `~/.claude/skills/` | 自定义 Skill（如 `/my-skill`） |
| `~/.claude/CLAUDE.md` | 用户级全局上下文，注入到所有会话 |
| `~/.claude.json` | 全局配置：主题、MCP、项目信任等 |

**不备份**：`sessions/`、`history.jsonl`、`plugins/`（会话历史和插件可重新安装）。

---

## 项目结构

创建一个 Git 仓库（如 `claude-config`），结构如下：

```
claude-config/
├── backup.sh          # 备份脚本：~/.claude → 仓库
├── restore.sh         # 恢复脚本：仓库 → ~/.claude
├── settings.json      # 从 ~/.claude/settings.json 同步
├── claude.json        # 从 ~/.claude.json 同步
├── CLAUDE.md          # 从 ~/.claude/CLAUDE.md 同步（可选）
├── CLAUDE.md.example  # 模板，首次可复制为 CLAUDE.md
├── agents/            # 自定义 Subagent
│   └── .gitkeep
├── skills/            # 自定义 Skill
│   └── .gitkeep
├── .gitignore
└── README.md
```

---

## 备份脚本（backup.sh）

核心逻辑：从 `~/.claude` 和 `~/.claude.json` 复制到仓库，然后 `git add`、`git commit`，有远程则 `git push`。

```bash
#!/bin/bash
# 一键备份：从 ~/.claude 复制全部配置到仓库
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
HOME_JSON="$HOME/.claude.json"

echo "备份 Claude Code 配置..."

# 1. settings.json（必需）
if [ -f "$CLAUDE_DIR/settings.json" ]; then
  cp "$CLAUDE_DIR/settings.json" "$SCRIPT_DIR/settings.json"
  echo "✓ settings.json"
else
  echo "✗ 未找到 ~/.claude/settings.json"
  exit 1
fi

# 2. 自定义 Subagents
mkdir -p "$SCRIPT_DIR/agents"
if [ -d "$CLAUDE_DIR/agents" ] && [ -n "$(ls -A $CLAUDE_DIR/agents 2>/dev/null)" ]; then
  for f in "$SCRIPT_DIR/agents"/*; do [ -e "$f" ] && [ "$(basename "$f")" != ".gitkeep" ] && rm -rf "$f"; done 2>/dev/null || true
  cp -r "$CLAUDE_DIR/agents/"* "$SCRIPT_DIR/agents/" 2>/dev/null || true
  echo "✓ agents/"
fi

# 3. 自定义 Skills
mkdir -p "$SCRIPT_DIR/skills"
if [ -d "$CLAUDE_DIR/skills" ] && [ -n "$(ls -A $CLAUDE_DIR/skills 2>/dev/null)" ]; then
  for f in "$SCRIPT_DIR/skills"/*; do [ -e "$f" ] && [ "$(basename "$f")" != ".gitkeep" ] && rm -rf "$f"; done 2>/dev/null || true
  cp -r "$CLAUDE_DIR/skills/"* "$SCRIPT_DIR/skills/" 2>/dev/null || true
  echo "✓ skills/"
fi

# 4. 用户级 CLAUDE.md
if [ -f "$CLAUDE_DIR/CLAUDE.md" ]; then
  cp "$CLAUDE_DIR/CLAUDE.md" "$SCRIPT_DIR/CLAUDE.md"
  echo "✓ CLAUDE.md"
fi

# 5. 全局配置 .claude.json（MCP、主题等）
if [ -f "$HOME_JSON" ]; then
  cp "$HOME_JSON" "$SCRIPT_DIR/claude.json"
  echo "✓ claude.json (.claude.json)"
fi

cd "$SCRIPT_DIR"
git add settings.json agents/ skills/
[ -f CLAUDE.md ] && git add CLAUDE.md
[ -f claude.json ] && git add claude.json

if git diff --staged --quiet 2>/dev/null; then
  echo "  无变更，跳过提交"
else
  git commit -m "backup: Claude Code 配置 $(date +%Y-%m-%d)"
  echo "✓ 已提交"
  if git remote -q 2>/dev/null | grep -q .; then
    git push
    echo "✓ 已推送"
  else
    echo "  提示: 添加远程仓库后执行 git push"
  fi
fi

echo ""
echo "备份完成！"
```

要点：

- `agents/`、`skills/` 为空时只保留 `.gitkeep`，不报错
- 清理目标目录时排除 `.gitkeep`，避免误删占位文件
- 无变更时跳过提交；有远程则自动推送

---

## 恢复脚本（restore.sh）

新电脑上克隆仓库后，执行 `./restore.sh` 将配置复制回 `~/.claude` 和 `~/.claude.json`。

```bash
#!/bin/bash
# Claude Code 配置恢复脚本（全面恢复）
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
HOME_JSON="$HOME/.claude.json"

echo "恢复 Claude Code 配置到 $CLAUDE_DIR"

mkdir -p "$CLAUDE_DIR"

# 1. settings.json
if [ -f "$SCRIPT_DIR/settings.json" ]; then
  cp "$SCRIPT_DIR/settings.json" "$CLAUDE_DIR/settings.json"
  echo "✓ settings.json"
else
  echo "✗ 未找到 settings.json"
fi

# 2. 自定义 Subagents
if [ -d "$SCRIPT_DIR/agents" ] && [ "$(ls -A $SCRIPT_DIR/agents 2>/dev/null)" ]; then
  mkdir -p "$CLAUDE_DIR/agents"
  cp -r "$SCRIPT_DIR/agents/"* "$CLAUDE_DIR/agents/" 2>/dev/null || true
  echo "✓ agents/"
fi

# 3. 自定义 Skills
if [ -d "$SCRIPT_DIR/skills" ] && [ "$(ls -A $SCRIPT_DIR/skills 2>/dev/null)" ]; then
  mkdir -p "$CLAUDE_DIR/skills"
  cp -r "$SCRIPT_DIR/skills/"* "$CLAUDE_DIR/skills/" 2>/dev/null || true
  echo "✓ skills/"
fi

# 4. 用户级 CLAUDE.md
if [ -f "$SCRIPT_DIR/CLAUDE.md" ]; then
  cp "$SCRIPT_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
  echo "✓ CLAUDE.md"
fi

# 5. 全局配置 .claude.json
if [ -f "$SCRIPT_DIR/claude.json" ]; then
  cp "$SCRIPT_DIR/claude.json" "$HOME_JSON"
  echo "✓ .claude.json"
fi

echo ""
echo "恢复完成！"
echo "提示: 请检查 ~/.claude/settings.json 中的 ANTHROPIC_AUTH_TOKEN"
echo "提示: .claude.json 中的 projects 路径为新机器路径，首次打开项目时会更新"
```

---

## 使用流程

### 日常备份（修改配置后）

```bash
cd ~/claude-config
./backup.sh
```

自动完成：复制 → 提交 → 推送（若已配置远程）。

### 新电脑恢复

```bash
git clone <你的私有仓库地址> ~/claude-config
cd ~/claude-config
./restore.sh
```

然后编辑 `~/.claude/settings.json`，确认 `ANTHROPIC_AUTH_TOKEN` 正确（若用私有仓库直接提交了 Token，可跳过）。

### 首次使用

若还没有 `agents/`、`skills/`、`CLAUDE.md`，目录已预留（`.gitkeep`），之后创建即可。备份时会自动同步。

**CLAUDE.md**：用户级全局上下文，只需在 `~/.claude/CLAUDE.md` 维护一份，Claude Code 会自动读取，无需在每个项目里复制。可从 `CLAUDE.md.example` 复制一份作为起点。

---

## 与 LiteLLM 代理的配合

若你已按 [LiteLLM 代理：协议不兼容时的「翻译官」](/LiteLLM-代理：协议不兼容时的「翻译官」/) 搭建了本地代理，`settings.json` 中会类似：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:4000",
    "ANTHROPIC_AUTH_TOKEN": "sk-proxy-master-xxx"
  }
}
```

备份后，新电脑上只需：

1. 执行 `./restore.sh` 恢复配置
2. 启动 LiteLLM 代理（`cd claude-code-openai-proxy && ./run.sh`）
3. 运行 `claude --model gpt-5.2-chat`

代理地址和 Token 已从备份恢复，无需重新配置。

---

## 安全说明

| 项目 | 说明 |
|------|------|
| **ANTHROPIC_AUTH_TOKEN** | 恢复后需确认正确；私有仓库也可直接提交 |
| **claude.json** | 含 `projects` 的本机绝对路径，新电脑上首次打开项目时会更新 |
| **仓库** | 建议使用私有仓库，避免配置泄露 |

---

## 小结

用 Git 私有仓库备份 Claude Code 配置，可以：

- 一次搭建，多机同步
- 换电脑后 `git clone` + `./restore.sh` 即可恢复
- 与 LiteLLM 代理、自定义 agents/skills 无缝配合

备份脚本只同步实际存在的文件，`agents/`、`skills/`、`CLAUDE.md` 为空时不会报错，之后创建即可自动纳入备份。
