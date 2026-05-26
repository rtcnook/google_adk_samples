# 基于 YAML 配置的 AI 导师 Agent

这是一个展示 ADK config-based agent 能力的示例。项目的核心 Agent 逻辑、结构和指令都写在 YAML 文件中，不需要为 Agent 本身编写 Python 代码。

---

## 功能

- 使用 YAML 定义 Agent
- 根 Agent 根据用户问题自动路由
- `python_tutor_agent` 回答 Python 和编程问题
- `physics_tutor_agent` 回答物理概念和题目
- 适合学习声明式、多 Agent 配置方式

---

## 项目结构

```text
version_5_config_type/
├── my_agent/
│   ├── root_agent.yaml
│   ├── python_tutor_agent.yaml
│   └── physics_tutor_agent.yaml
├── main.py
├── pyproject.toml
└── uv.lock
```

---

## 安装依赖

```bash
cd version_5_config_type
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

模型在 `my_agent/root_agent.yaml` 中配置：

```yaml
model: gemini-2.5-flash
```

---

## 运行

```bash
adk web .
```

打开 `http://localhost:8000` 后选择 `my_agent`。不要运行 `adk web ./my_agent`，因为 ADK Web 需要传入包含 agent 应用目录的父目录。

---

## 示例问题

```text
Explain list comprehensions in Python with an example.
```

```text
What is Newton's Second Law of Motion?
```

根 Agent 会根据问题类型自动转交给对应导师 Agent。
