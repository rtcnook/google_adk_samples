# =============================================================================
# FILE: agent.py
# PURPOSE:
#   This file defines the root LLM agent for the website builder use case.
#   The agent takes a user's natural language prompt describing a simple website,
#   generates a complete HTML+CSS+JS webpage, and uses a tool to save it as a file.
# =============================================================================

import os
import sys
# 步骤 1：把项目根目录加入模块搜索路径，保证 tools 和 utils 可以被导入。
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import the base class for a language-model-powered agent from Google ADK.
from google.adk.agents import LlmAgent

# Import the custom tool that handles writing content to a timestamped .html file.
from tools.file_writer_tool import write_to_file

# Import a utility function that reads instruction and description files from disk.
from utils.file_loader import load_instructions_file

# -----------------------------------------------------------------------------
# Define the root LLM agent for this app. It is a single-agent app (no sub-agents).
# -----------------------------------------------------------------------------
# 步骤 2：创建单 Agent。这个 Agent 直接接收用户网页需求并生成完整页面代码。
root_agent = LlmAgent(
    name="website_builder_simple",  # Unique name for the agent; also shown in the UI.

    model="gemini-2.5-flash",   # The ID of the Gemini model used to generate responses.

    # 步骤 3：从 instructions.txt 读取系统提示词，约束 Agent 输出 HTML/CSS/JS。
    # The prompt/instruction that tells the agent what kind of behavior to exhibit.
    # It is loaded from a file
    instruction=load_instructions_file("agents/website_builder_simple/instructions.txt"),

    # 步骤 4：从 description.txt 读取说明，供 ADK UI 展示和 Agent 选择时参考。
    # A short summary of what the agent does.
    # It is loaded from a file
    description=load_instructions_file("agents/website_builder_simple/description.txt"),

    # 步骤 5：注册写文件工具，让 Agent 可以把生成的网页保存到 output 目录。
    # A list of tools the agent can invoke during execution.
    # In this case, just one: a function that writes the generated HTML to a file.
    tools=[write_to_file],
)
