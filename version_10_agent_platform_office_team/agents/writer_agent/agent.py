"""
Writer Agent
"""
import pathlib
import sys
from google.adk.agents import Agent

current_dir = pathlib.Path(__file__).parent.resolve()
instruction_path = current_dir / "instruction.txt"
with open(instruction_path, "r", encoding="utf-8") as f:
    instruction_text = f.read()

# Import write_temp_json from export_manager tools
parent_agents_dir = current_dir.parent
if str(parent_agents_dir) not in sys.path:
    sys.path.insert(0, str(parent_agents_dir))
from export_manager.tools import write_temp_json

root_agent = Agent(
    name="writer_agent",
    model="gemini-2.5-flash",
    instruction=instruction_text,
    tools=[write_temp_json],
    description="负责根据收集的资料撰写正式文档、周报、邮件的文字工作者。",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_key="draft_content",
)
