"""
CEO / Project Manager Agent
"""
import pathlib
import sys
from google.adk.agents import Agent

current_dir = pathlib.Path(__file__).parent.resolve()
parent_dir = current_dir.parent

if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from research_agent.agent import root_agent as research_agent
from writer_agent.agent import root_agent as writer_agent
from qa_reviewer.agent import root_agent as qa_reviewer
from export_manager.agent import root_agent as export_manager

instruction_path = current_dir / "instruction.txt"
with open(instruction_path, "r", encoding="utf-8") as f:
    instruction_text = f.read()

root_agent = Agent(
    name="ceo_agent",
    model="gemini-2.5-flash",
    sub_agents=[research_agent, writer_agent, qa_reviewer, export_manager],
    instruction=instruction_text,
    description="公司的CEO兼项目经理，负责接收用户任务并协调下属员工（收集资料、写文章、审查、导出）。",
    rerun_on_resume=True,
)
