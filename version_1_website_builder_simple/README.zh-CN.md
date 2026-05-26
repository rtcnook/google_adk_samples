# 简单网站生成 Agent

这是一个最小化的 Google Agent Development Kit (ADK) 示例项目。它使用单个 LLM Agent，根据用户的自然语言描述生成完整的 HTML、CSS 和 JavaScript 页面，并把生成结果保存为带时间戳的 `.html` 文件。

---

## 功能

- 使用 Google ADK 构建 Gemini 驱动的 LLM Agent
- 支持类似“创建一个带红色按钮的落地页”的自然语言需求
- 生成完整、可直接打开的 HTML 页面，样式和脚本内联
- 自动把结果保存为带时间戳的 `.html` 文件
- 结构简单，便于继续扩展子 Agent 或工具

---

## 项目结构

```text
version_1_website_builder_simple/
├── agents/
│   └── website_builder_simple/
│       ├── agent.py             # 主 Agent 定义
│       ├── __init__.py
│       ├── instructions.txt     # Agent 指令
│       └── description.txt      # Agent 描述
├── tools/
│   ├── __init__.py
│   └── file_writer_tool.py      # 保存 HTML 文件的工具
├── utils/
│   ├── __init__.py
│   └── file_loader.py           # 读取指令文件的工具函数
├── output/                      # 自动生成的 HTML 输出目录
├── .env                         # API / Vertex AI 环境配置
└── pyproject.toml               # Python 项目依赖配置
```

---

## 快速开始

### 1. 进入项目目录

```bash
cd adk_samples/version_1_website_builder_simple
```

### 2. 安装依赖

需要 Python 3.11+ 和 `uv`。

```bash
uv sync --all-groups
```

如果需要手动激活虚拟环境：

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. 配置环境变量

在当前项目目录下创建或编辑 `.env` 文件。

如果使用 Vertex AI：

```env
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

如果使用 Google AI Studio API Key：

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

当前项目代码里的模型名是：

```text
gemini-2.5-flash
```

---

## 运行 Agent UI

```bash
adk web ./agents
```

然后在浏览器打开：

```text
http://localhost:8000
```

在 Agent 列表中选择 `website_builder_simple` 后即可开始对话。

---

## 其他运行方式

| 序号 | 方式 | 命令 | 适用场景 |
|---:|---|---|---|
| 1 | ADK Web UI | `adk web ./agents` | 浏览器调试和演示 |
| 2 | ADK API Server | `adk api_server ./agents` | 通过 REST API 调用 Agent |
| 3 | Python 脚本 | `uv run python -m agent_runner` | 在自定义脚本或后端流程中调用 |
| 4 | ADK CLI | `adk run agents/website_builder_simple` | 命令行快速测试 |

---

## 示例提示词

```text
创建一个粉色背景的网页，页面中有一个绿色标题，标题文字是 Hello ADK! 请使用工具把结果保存为 HTML 文件。
```

Agent 会生成完整的 HTML，并把文件保存到 `output/` 目录。

---

## 实现原理

1. ADK 加载 `agents/website_builder_simple/agent.py` 中的 `root_agent`。
2. `root_agent` 使用 `instructions.txt` 和 `description.txt` 作为提示词配置。
3. 用户输入需求后，Gemini 根据提示词生成网页代码。
4. Agent 调用 `save_html_to_file` 工具保存 HTML。
5. 输出文件写入 `output/` 目录。

---

## 扩展方向

你可以继续添加：

- 需求分析 Agent
- 页面设计 Agent
- React / Tailwind 输出
- 浏览器预览工具
- 图片生成或素材搜索工具

---

## 许可证

本项目使用 **GNU General Public License v3.0**。详情见根目录的 `LICENSE` 文件。
