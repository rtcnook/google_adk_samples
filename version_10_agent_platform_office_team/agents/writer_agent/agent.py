"""
Writer Agent
"""
import pathlib
from google.adk.agents import Agent

current_dir = pathlib.Path(__file__).parent.resolve()
instruction_path = current_dir / "instruction.txt"
with open(instruction_path, "r", encoding="utf-8") as f:
    instruction_text = f.read()

root_agent = Agent(
    name="writer_agent",
    model="gemini-2.5-flash",
    instruction=instruction_text,
    description="负责根据收集的资料撰写正式文档、周报、邮件的文字工作者。",
)
