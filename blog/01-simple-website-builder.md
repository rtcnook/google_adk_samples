# 项目 1：Simple Website Builder 教程

## 你会学到什么

这个项目演示 ADK 最小可用形态：一个 LLM Agent 接收自然语言需求，生成完整 HTML 页面，
再通过工具把结果写入本地文件。

项目目录：

```text
version_1_website_builder_simple/
```

## 核心架构

这个示例只有一个主 Agent：

- `agents/website_builder_simple/agent.py`：定义 `root_agent`。
- `agents/website_builder_simple/instructions.txt`：告诉 Agent 如何生成网页。
- `tools/file_writer_tool.py`：把生成的 HTML 写入 `output/`。
- `utils/file_loader.py`：读取 instruction 和 description 文件。

执行链路：

```text
用户需求 -> website_builder_simple Agent -> 生成 HTML/CSS/JS -> write_to_file 工具 -> output/*.html
```

## 环境准备

进入项目目录：

```bash
cd version_1_website_builder_simple
```

创建虚拟环境并安装依赖：

```bash
uv venv
.venv\Scripts\activate
uv sync --all-groups
```

创建 `.env`：

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

## 运行项目

启动 ADK Web UI：

```bash
adk web ./agents
```

打开：

```text
http://localhost:8000
```

选择 `website_builder_simple`，输入：

```text
Create a webpage with a pink background and a green heading that says Hello ADK.
Write this to an output file using the tool.
```

运行后检查：

```text
version_1_website_builder_simple/output/
```

## 代码理解

这个项目的重点是理解三件事：

1. Agent 的能力主要来自 instruction。
2. Tool 是 Agent 和外部世界交互的接口。
3. ADK Web 可以直接加载 `agents/` 目录里的 Agent。

如果要扩展，可以加入新的工具，例如截图工具、HTML 校验工具，或者把输出改成 React 组件。
