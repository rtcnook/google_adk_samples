# 项目 7：Programmatic Tool Execution 教程

## 你会学到什么

这个项目演示如何让 ADK Agent 在运行时连接 MCP Server，动态加载工具，
再通过 Python 代码把多个工具调用编排起来。

项目目录：

```text
version_7_programmatic_tool_execution/
```

## 核心结构

关键文件：

- `agent.py`：定义 `AgentWrapper`，加载 MCP 工具，并提供 `run_python_code`。
- `client.py`：封装 ADK Runner、session 和消息发送。
- `cmd.py`：命令行聊天循环。
- `utilities.py`：读取配置和打印响应。
- `theailanguage_config.json`：MCP Server 配置。

## 工作流程

```text
启动程序
-> 读取 theailanguage_config.json
-> 连接 MCP Server
-> 获取 MCP 工具列表
-> 包装成 Python async 函数
-> 注入 run_python_code 执行作用域
-> LLM 生成 Python 代码
-> 执行工具调用并返回结果
```

## 配置 MCP Server

示例配置：

```json
{
  "mcpServers": {
    "server1": {
      "type": "http",
      "url": "http://localhost:3000/mcp"
    },
    "server2": {
      "type": "http",
      "url": "http://localhost:3001/mcp"
    }
  }
}
```

需要先启动对应的 MCP Server，否则项目会跳过连接失败的 server。

## 环境准备

```bash
cd version_7_programmatic_tool_execution
uv venv
.venv\Scripts\activate
uv sync --all-groups
```

`.env`：

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

## 运行项目

```bash
uv run python main.py
```

示例输入：

```text
Can you write Python code that uses your MCP tools to add 5 and 7,
multiply the sum by 2, subtract 4, and divide the result by 5?
```

## 核心设计解释

`run_python_code` 是这个项目的关键。
它不是简单地让 Agent 直接调用一个工具，而是让 Agent 写一段 Python 逻辑：

- 可以 `await add_numbers(...)`。
- 可以把前一步结果传给下一步。
- 可以做条件判断、循环和数据处理。
- 最后必须 `return` 一个描述性结果。

这种方式适合需要串联多个工具的场景，例如文件处理、数据清洗、批量 API 调用和自动化工作流。

## 风险和改进

这个示例会执行 LLM 生成的 Python 代码，生产环境必须加入沙箱、权限控制、超时控制和审计日志。
当前项目更适合学习 MCP 工具注入和程序化执行机制。
