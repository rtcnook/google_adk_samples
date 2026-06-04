"""
QA Reviewer Agent
"""
import pathlib
from google.adk.agents import Agent

current_dir = pathlib.Path(__file__).parent.resolve()
instruction_path = current_dir / "instruction.txt"
with open(instruction_path, "r", encoding="utf-8") as f:
    instruction_text = f.read()

root_agent = Agent(
    name="qa_reviewer",
    model="gemini-2.5-flash",
    instruction=instruction_text,
    description="负责审查文档质量，进行逻辑检查和语言润色的审核员。",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_key="final_content",
)
