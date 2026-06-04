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
