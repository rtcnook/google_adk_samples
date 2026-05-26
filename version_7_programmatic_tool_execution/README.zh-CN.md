# 程序化工具调用示例

这是一个使用 Google ADK 演示程序化工具调用的项目。它可以在运行时从 MCP Server 获取工具，把工具注入到 Python 执行环境中，再由 LLM Agent 生成并执行 Python 代码来完成任务。

---

## 功能

- 动态连接 MCP Server
- 从 MCP Server 获取工具列表
- 把 MCP 工具包装为 Python 可调用对象
- 提供 `run_python_code` 工具执行 Python 代码
- 使用 `LlmAgent` 处理用户请求并编排工具调用

---

## 安装依赖

本项目需要 Python 3.12+。

```bash
cd version_7_programmatic_tool_execution
uv sync --all-groups
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

当前模型名为：

```text
gemini-2.5-flash
```

---

## 配置 MCP Server

编辑 `theailanguage_config.json`：

```json
{
  "mcpServers": {
    "server1": {
      "url": "http://localhost:3000/mcp"
    },
    "server2": {
      "url": "http://localhost:3001/mcp"
    }
  }
}
```

需要先启动对应的 Streamable HTTP MCP Server。

---

## 运行

```bash
uv run python main.py
```

---

## 示例请求

```text
Can you write Python code that uses your MCP tools to add two numbers, multiply the sum, subtract a value, and divide the result?
```

Agent 会根据请求生成 Python 代码，并通过已连接的 MCP 工具执行。

---

## 关键文件

- `agent.py`：定义 `AgentWrapper` 和 Python 执行工具
- `client.py`：与 Agent 通信
- `utilities.py`：配置读取等工具函数
- `theailanguage_config.json`：MCP Server 配置
