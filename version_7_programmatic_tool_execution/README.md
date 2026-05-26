# Programmatic Tool Calling with Google's Agent Development Kit (ADK)

This project demonstrates **Programmatic Tool Calling** using **Google's Agent Development Kit (ADK)**. It showcases how to dynamically fetch tools from MCP servers, wrap them as native Python async functions, and execute them programmatically within an LLM agent. The example is powered by **Google Gemini**.

---

## Features

- **Dynamic Tool Integration**: Tools are fetched from MCP servers at runtime and injected into the Python execution scope.
- **Python Code Execution**: The `run_python_code` tool allows executing Python scripts programmatically, leveraging connected MCP tools.
- **LLM Agent**: Built using the ADK's `LlmAgent` class, the agent can process user queries and execute complex workflows.

Streamable HTTP MCP Servers Used from Repository
https://github.com/theailanguage/mcp_streamable_http
Refer to 
main/streamable_http_server/1-stateless-streamable/server1.py
AND
main/streamable_http_server/1-stateless-streamable/server2.py

---

## Installation and Setup

### Setup KEY - Create a .env file with
GOOGLE_API_KEY=<KEY_VALUE>

### 1. Create a Virtual Environment

```bash
uv venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
uv sync --all-groups
```

### 3. Configure MCP Servers

Edit the `theailanguage_config.json` file to define your MCP server connections. Example:

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

---

## Usage

### Running the Agent

To start the agent and interact with it:

```bash
uv run python3 main.py
```

Make sure you have run the streamable HTTP MCP servers available at - https://github.com/theailanguage/mcp_streamable_http

### Example Query

You can ask the agent to perform tasks programmatically. For example:

> "Can you write a Python code that uses your MCP tools to add two numbers, multiply the sum, subtract a value, and divide the result?"

The agent will dynamically fetch the required tools, execute the Python code, and return the result.

---

## Key Files

- **`agent.py`**: Defines the `AgentWrapper` class, which initializes the LLM agent and the `run_python_code` tool.
- **`client.py`**: Handles communication with the agent.
- **`utilities.py`**: Provides utility functions, including configuration file parsing.
- **`theailanguage_config.json`**: Configuration file for MCP server connections.

---

## Learn More

For more details on Google's ADK and its capabilities, refer to the official documentation.

## Known Issues

There is an issue where resource cleanup while ending the program leads to and error/exception causing the program to crash. Since this is an educational code, this exception handling has been left as is to demostrate the main concept and might be improved in upcoming changes