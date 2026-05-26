# 无代码可视化 Agent 构建器

这是一个展示 ADK Visual Agent Builder 的示例。它通过 `adk web` 提供浏览器中的可视化画布，让你用低代码或无代码方式创建、配置和测试 Agent。

---

## 功能

- 通过浏览器可视化创建 Agent
- 用表单配置 `LlmAgent`
- 自动生成标准 ADK YAML 配置文件
- 可直接在 ADK Web UI 中测试 Agent
- 包含一个网页生成 Agent 示例

---

## 安装依赖

本项目需要 Python 3.12+。

```bash
cd version_6_adk_nocode
uv sync
```

---

## 环境变量

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

---

## 启动可视化构建器

```bash
adk web
```

打开终端输出的地址，通常是：

```text
http://localhost:8000
```

---

## 手动创建网页生成 Agent

在 ADK Web UI 中创建新 Agent，例如 `web_page_generator_2`，配置：

- Agent Type: `LlmAgent`
- Model: `gemini-2.5-flash`
- Description: `single page website builder agent`
- Instruction: `Build a single unified HTML + CSS + JS document that is a webpage as per the user query`

保存后，ADK 会生成对应的 `root_agent.yaml`。

---

## 注意

Visual Agent Builder 和 Builder Assistant 仍属于较新的实验能力。手动配置通常更稳定，AI 辅助构建功能可能出现文件未完整写入等问题。
