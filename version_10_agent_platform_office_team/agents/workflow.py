"""
Office Workflow — sequential multi-agent pipeline for ADK Web compatibility.

research_agent → writer_agent → qa_reviewer → export_manager
"""
import pathlib
import sys

from google.adk.workflow import Edge, START, Workflow

current_dir = pathlib.Path(__file__).parent.resolve()
# 把 agents/ 目录加入 sys.path，确保能 import research_agent, writer_agent 等
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from research_agent.agent import root_agent as research_agent
from writer_agent.agent import root_agent as writer_agent
from qa_reviewer.agent import root_agent as qa_reviewer
from export_manager.agent import root_agent as export_manager

office_workflow = Workflow(
    name="office_workflow",
    description="办公助手工作流：自动依次执行 调研→写作→审核→导出。",
    edges=[
        Edge(from_node=START, to_node=research_agent, route=None),
        Edge(from_node=research_agent, to_node=writer_agent, route=None),
        Edge(from_node=writer_agent, to_node=qa_reviewer, route=None),
        Edge(from_node=qa_reviewer, to_node=export_manager, route=None),
    ],
)
