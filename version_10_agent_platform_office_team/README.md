# Maestroffice Lite (Agent Platform Edition)

多 Agent 办公助手，CEO 协调下属（调研员、写手、审查员、导出专员）自动完成文档生成任务。

## 快速开始

```bash
# 首次使用：安装依赖
uv sync

# CLI 交互模式（CEO Agent，支持多轮自动推进）
uv run python main.py

# CLI Workflow 模式（单轮全流程，适合简单任务）
uv run python main.py --workflow

# ADK Web 界面（浏览器中操作）
uv run adk web
```

> 统一使用 `uv run` 前缀，确保始终在 venv 环境中运行，避免缺少依赖库。

## 三种运行方式

| 方式 | 命令 | 用途 |
|------|------|------|
| **CLI 交互** | `uv run python main.py` | 终端对话，CEO Agent 多轮自动推进 |
| **ADK Web** | `uv run adk web` | 浏览器 UI，快速调试和演示 |
| **ADK API Server** | `uv run adk api_server` | 对外提供 REST API，供外部系统集成 |

### ADK Web 说明

ADK Web 是 Google ADK 内置的调试/演示用 Web UI。在浏览器中直接与 Agent 对话，实时查看返回内容和工具调用，无需写代码。

启动后访问 `http://localhost:8000`，下拉选择 `office_workflow` 即可使用。

### ADK API Server 对外接口

启动后默认监听 `http://localhost:8000`，提供以下 REST 接口：

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/list-apps` | 列出所有可用 Agent |
| `POST` | `/apps/{app}/users/{user}/sessions` | 创建会话 |
| `POST` | `/run` | 运行 Agent（同步） |
| `POST` | `/run_sse` | 运行 Agent（SSE 流式） |
| `GET` | `/apps/{app}/users/{user}/sessions/{sid}` | 查询会话状态 |

调用示例（生成 PPT）：

```bash
# 创建会话
curl -X POST http://localhost:8000/apps/office_workflow/users/user1/sessions

# 发送任务
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "office_workflow",
    "user_id": "user1",
    "session_id": "<返回的 session_id>",
    "new_message": {
      "parts": [{"text": "做一个关于AI发展趋势的5页PPT"}],
      "role": "user"
    }
  }'
```

可集成到网页、企业微信、钉钉机器人等任何外部系统中。

## 生成文件格式

Agent 会根据你的需求自动选择合适的输出格式：

| 用户描述 | 输出格式 |
|----------|----------|
| "做一个PPT" / "生成幻灯片" | `.pptx` |
| "写一份报告" / "Word文档" | `.docx` |
| "生成表格" / "Excel" | `.xlsx` |
| "写一篇文章" / "Markdown" | `.md` |

## 工作流

```
用户请求 → research_agent（调研提纲）
         → writer_agent（撰写初稿）
         → qa_reviewer（审核润色）
         → export_manager（导出文件）
```

## 项目结构

```
├── agents/
│   ├── ceo_agent/          # CEO 协调员（CLI 模式使用）
│   ├── research_agent/     # 研究员：搜索资料、整理大纲
│   ├── writer_agent/       # 写手：根据资料撰写文档
│   ├── qa_reviewer/        # 审查员：检查逻辑、润色
│   ├── export_manager/     # 导出专员：保存为本地文件
│   ├── workflow.py         # Workflow 图（Web 模式使用）
│   └── __init__.py
├── agent.py                # ADK Web 入口
├── main.py                 # CLI 入口
├── outputs/                # 输出文件目录
├── pyproject.toml
└── .env                    # API Key 配置
```

## 环境配置

`.env` 文件示例：

```
GOOGLE_API_KEY=你的API密钥
GOOGLE_CLOUD_PROJECT=你的项目ID
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=True
```
