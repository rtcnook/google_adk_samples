"""
Travel planner coordinator agent declaration.

This is the central orchestration/coordinator agent that acts as a manager 
and delegates specialized tasks to its sub-agents.
"""

# Import pathlib for clean cross-platform path resolution.
import pathlib

# Import sys to allow runtime modification of Python's module search path (sys.path).
import sys

# Import the core Agent class from Google ADK.
from google.adk.agents import Agent

# --- Sys Path Modification & Peer Sub-package Imports ---
# 步骤 1：定位当前 travel_planner 目录。
# Get the absolute path of the directory containing this script.
current_dir = pathlib.Path(__file__).parent.resolve()

# 步骤 2：找到 agents 根目录，后面要从这里导入其他子 Agent。
# Go up one level to find the root 'agents' package directory.
parent_dir = current_dir.parent

# In Python, relative imports between separate subfolders (packages) can sometimes 
# cause issues depending on how the execution entry point is called. By dynamically 
# adding the parent 'agents' directory to sys.path, we can perform clean, robust, 
# absolute imports of peer subagent modules from any context.
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# 步骤 3：导入三个专业子 Agent，分别负责天气、航班和行程规划。
# Clean absolute imports of peer sub-agents.
# Since we added 'parent_dir' to sys.path, these packages can be resolved absolutely.
from weather_checker.agent import root_agent as weather_checker
from flight_booker.agent import root_agent as flight_booker
from itinerary_agent.agent import root_agent as itinerary_agent

# --- Load Instructions ---
# 步骤 4：读取主协调 Agent 的指令，定义它如何委派任务和汇总结果。
instruction_path = current_dir / "instruction.txt"
with open(instruction_path, "r", encoding="utf-8") as f:
    instruction_text = f.read()

# --- Coordinator Agent Initialization ---
# 步骤 5：创建主协调 Agent。它不直接完成所有任务，而是根据用户需求委派给子 Agent。
root_agent = Agent(
    # Unique name for system orchestration.
    name="travel_planner",
    
    # Specify the core Gemini language model that powers the coordinator.
    # The coordinator receives user prompts and determines which subagent 
    # to delegate to based on their descriptions.
    model="gemini-2.5-flash",  # Canonical Gemini model
    
    # 步骤 6：注册可管理的专业子 Agent，ADK 会根据描述和上下文进行委派。
    # Registers the specialized worker sub-agents that this coordinator can manage.
    # When the coordinator agent requires specific sub-tasks, it relies on the ADK's 
    # hierarchical delegation to hand off conversation contexts to these sub-agents.
    sub_agents=[weather_checker, flight_booker, itinerary_agent],
    
    # 步骤 7：instruction 控制旅行规划的整体流程，例如先查天气，再订航班，再规划行程。
    # System instructions guiding the coordination flow.
    instruction=instruction_text,
    
    # Explanatory description of the coordinator.
    description="中文旅行规划主协调 Agent，负责管理并委派天气、航班和行程子 Agent。",
)
