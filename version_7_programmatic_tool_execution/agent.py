# ------------------------------------------------------------------------------
# FILE: agent.py
# ------------------------------------------------------------------------------
# PURPOSE:
# Defines the AgentWrapper class that loads and constructs a Google ADK LLM Agent.
#
# NEW CAPABILITIES:
# - Includes a 'run_python_code' tool.
# - Dynamically fetches tools from MCP toolsets at runtime, wraps them as 
#   native Python async functions, and injects them into the script scope.
# - Enforces return values from the Python script back to the LLM.
# ------------------------------------------------------------------------------
# Sample query:  Can you write a python code that uses your MCP tools and run it 
# to first add two numbers 5 and 7, then multiply the sum by 2 then subtract 4 
# from the product and then divide the difference by 5

import asyncio
import textwrap
import traceback
from typing import Any, List, Dict, Callable, Optional, Union

from rich import print  # Used for colorful terminal logging

# ADK's built-in LLM agent class
from google.adk.agents.llm_agent import LlmAgent
# Tool wrapper to convert python func to ADK tool
from google.adk.tools import FunctionTool
# Type hint for ADK tools
from google.adk.tools import BaseTool

# Provides access to tools hosted on MCP servers
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

# Connection settings for different types of MCP servers
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool import StdioConnectionParams

# Custom parameters for local STDIO-based MCP servers
from mcp import StdioServerParameters

# Utility function to read the config.json file
from utilities import read_config_json


# ------------------------------------------------------------------------------
# CLASS: AgentWrapper
# ------------------------------------------------------------------------------
class AgentWrapper:
    def __init__(self, tool_filter: Optional[List[str]] = None) -> None:
        """
        Initializes the wrapper but does NOT build the agent yet.
        Call `await self.build()` after this to complete setup.

        Args:
            tool_filter (Optional[List[str]]): Optional list of tool names to allow.
        """
        self.tool_filter: Optional[List[str]] = tool_filter
        self.agent: Optional[LlmAgent] = None          # Will hold the final LlmAgent after building
        self._toolsets: List[MCPToolset] = []          # Store all loaded toolsets for later cleanup


    async def build(self) -> None:
        """
        Builds the LlmAgent by:
        - Connecting to all MCP servers.
        - Defining the 'run_python_code' tool.
        - Initializing the ADK agent with strict instructions on using the Python tool.
        """
        # 步骤 1：先连接配置文件中的 MCP Server，并把可用工具集保存下来。
        # Load toolsets (connections are established here)
        self._toolsets = await self._load_toolsets()

        # 步骤 2：在 Agent 内部定义一个 Python 执行工具，后续会包装成 ADK FunctionTool。
        # --- Define the Python Execution Function Locally ---
        
        async def run_python_code(code: str) -> str:
            """
            Executes the provided Python code string asynchronously.
            
            IMPORTANT GUIDELINES:
            1. You have access to connected MCP tools as local async functions (e.g., `await read_file(path='...')`).
            2. Do NOT use standard Python APIs (like `open()`) if an MCP tool (like `read_file`) is available.
            3. Your code MUST end with a `return` statement. 
            4. The return value should be a descriptive string explaining what was done and the result.
            
            Args:
                code (str): Valid python code. Must include a 'return' statement at the end.
                
            Returns:
                str: The result of the execution or error message.
            """
            print(f"[bold blue]🐍 Executing Python Code:[/bold blue]\n{code}")
            
            # 步骤 3：为即将执行的 Python 代码准备独立作用域。
            # 1. Prepare the execution scope
            scope: Dict[str, Any] = {}

            # 步骤 4：每次执行前重新从 MCP toolset 获取工具，确保工具列表是最新的。
            # 2. Dynamic Tool Retrieval
            current_tools: List[BaseTool] = []
            
            for toolset in self._toolsets:
                try:
                    # fetch tools from the session
                    ts_tools: List[BaseTool] = await toolset.get_tools()
                    current_tools.extend(ts_tools)
                except Exception as e:
                    print(f"[yellow]⚠️ Warning: Could not fetch tools from a toolset during python exec:[/yellow] {e}")

            # 步骤 5：把每个 MCP 工具包装成 Python async 函数，供 LLM 生成的代码 await 调用。
            # 3. Helper to create a native python async function that calls the MCP tool
            def create_wrapper(tool_instance: BaseTool) -> Callable[..., Any]:
                async def wrapped_mcp_call(**kwargs: Any) -> Any:
                    # Log the call internally
                    print(f"[dim]  -> Calling tool: {tool_instance.name} with args: {kwargs}[/dim]")
                    # Execute the MCP tool
                    return await tool_instance.run_async(args=kwargs, tool_context=None)
                return wrapped_mcp_call

            # 步骤 6：把包装后的工具注入到执行作用域中，例如 add_numbers、read_file。
            # 4. Inject tools into scope
            for tool in current_tools:
                # Sanitize tool name for python variable (replace - with _)
                safe_name: str = tool.name.replace("-", "_")
                scope[safe_name] = create_wrapper(tool)

            # 步骤 7：把 LLM 生成的代码包进 async 函数，这样代码内部可以使用 await。
            # 5. Wrap the user's code in an async function to allow 'await'
            indented_code: str = textwrap.indent(code, "    ")
            wrapper_code: str = f"async def _main():\n{indented_code}"

            try:
                # 步骤 8：先执行函数定义，再调用 _main 得到最终结果。
                # Execute the definition of _main in the scope
                exec(wrapper_code, scope)
                
                # Retrieve and await the _main function
                if "_main" in scope:
                    result: Any = await scope["_main"]()
                    
                    # Handle cases where the agent forgot to return anything
                    if result is None:
                        return (
                            "Execution successful, but the Python script returned 'None'. "
                            "Did you forget to add a `return` statement at the end of your code? "
                            "Please rewrite the code to return a descriptive string."
                        )
                    return str(result)
                else:
                    return "Error: Could not define main execution block."

            except Exception:
                # Return the traceback so the Agent knows what went wrong and can retry
                err: str = traceback.format_exc()
                print(f"[red]❌ Python Execution Failed:[/red]\n{err}")
                return f"Python Execution Error:\n{err}"

        # 步骤 9：把 run_python_code 包装成 ADK 工具，交给 LlmAgent 使用。
        # --- Create the Tool ---
        python_tool: FunctionTool = FunctionTool(run_python_code)

        # 步骤 10：最终 Agent 同时拥有 MCP toolset 和 Python 执行工具。
        # Construct the ADK LLM Agent
        combined_tools: List[Union[MCPToolset, FunctionTool]] = self._toolsets + [python_tool] # type: ignore

        self.agent = LlmAgent(
            model="gemini-2.5-flash",
            name="enterprise_assistant",
            instruction=(
                "你是企业助手，负责帮助用户完成文件系统和 MCP 服务器相关任务。"
                "始终用中文回答用户；工具名、代码、路径、错误信息和必要技术术语可以保留英文。"
                "你有一个强大的工具叫 `run_python_code`。"
                "当你需要串联多个工具、执行逻辑/数学处理或处理数据时使用它。"
                "\n\n"
                "Python 代码规则：\n"
                "1. 所有已连接的 MCP 工具都可以作为本地异步函数使用，例如 `await read_file(path='...')`。"
                "   能用 MCP 工具时，优先使用它们，而不是标准 Python 库。\n"
                "2. 生成的 Python 脚本必须以 `return` 语句结束。\n"
                "3. 返回字符串应使用中文总结执行了什么操作以及得到什么结果。"
                "4. 不要使用默认 API 或臆造接口；只按必需参数调用真实工具，例如 `add_numbers`。"
            ),
            tools=combined_tools
        )


    async def _load_toolsets(self) -> List[MCPToolset]:
        """
        Reads config, connects to servers, and returns the list of Toolsets.

        Returns:
            List[MCPToolset]: A list of initialized MCP toolsets.
        """
        config: Dict[str, Any] = read_config_json()
        toolsets: List[MCPToolset] = []

        server_config: Dict[str, Any]
        for name, server_config in config.get("mcpServers", {}).items():
            try:
                conn: Union[StreamableHTTPServerParams, StdioConnectionParams]

                # 步骤 A：根据配置判断 MCP Server 是 HTTP 方式还是 stdio 方式。
                # Determine connection method
                if server_config.get("type") == "http":
                    conn = StreamableHTTPServerParams(url=server_config["url"])

                elif server_config.get("type") == "stdio":
                    conn = StdioConnectionParams(
                        server_params=StdioServerParameters(
                            command=server_config["command"],
                            args=server_config["args"]
                        ),
                        timeout=5
                    )
                else:
                    raise ValueError(f"[red]❌ Unknown server type: '{server_config.get('type')}'[/red]")

                # 步骤 B：创建 MCPToolset。这里还没有执行业务工具，只是在建立工具连接。
                # Connect
                toolset = MCPToolset(
                    connection_params=conn,
                    tool_filter=self.tool_filter
                )

                # 步骤 C：拉取工具列表，既用于验证连接，也用于后续动态注入。
                # Fetch tools (activates the session and validates connection)
                tools: List[Any] = await toolset.get_tools()
                
                # Logging
                tool_names: List[str] = [tool.name for tool in tools]
                print(f"[bold green]✅ Tools loaded from [cyan]'{name}'[/cyan]:[/bold green] {tool_names}")

                toolsets.append(toolset)

            except Exception as e:
                print(f"[bold red]⚠️  Skipping server '{name}':[/bold red] {e}")

        return toolsets


    async def close(self) -> None:
        """
        Gracefully shuts down each loaded toolset.
        """
        for toolset in self._toolsets:
            try:
                await toolset.close()
            except Exception as e:
                print(f"[yellow]⚠️ Error closing toolset:[/yellow] {e}")

        await asyncio.sleep(1.0)
