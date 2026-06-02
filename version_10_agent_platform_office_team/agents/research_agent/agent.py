"""
Research Agent
"""
import pathlib
from google.adk.agents import Agent

current_dir = pathlib.Path(__file__).parent.resolve()
instruction_path = current_dir / "instruction.txt"
with open(instruction_path, "r", encoding="utf-8") as f:
    instruction_text = f.read()

root_agent = Agent(
    name="research_agent",
    model="gemini-2.5-flash",
    instruction=instruction_text,
    description="负责资料收集、数据分析以及任务大纲整理的员工。",
)
