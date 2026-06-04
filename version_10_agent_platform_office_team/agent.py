"""ADK Web entry point — uses Workflow for single-round full pipeline."""
import pathlib
import sys
from dotenv import load_dotenv

project_dir = pathlib.Path(__file__).parent.resolve()
env_path = project_dir / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# 确保项目目录和 agents 目录在 sys.path 中
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

agents_dir = str(project_dir / "agents")
if agents_dir not in sys.path:
    sys.path.insert(0, agents_dir)

# 直接从子 agent 模块导入，构建 Workflow
from google.adk.workflow import Edge, START, Workflow
from research_agent.agent import root_agent as _research_agent
from writer_agent.agent import root_agent as _writer_agent
from qa_reviewer.agent import root_agent as _qa_reviewer
from export_manager.agent import root_agent as _export_manager

office_workflow = Workflow(
    name="office_workflow",
    description="办公助手工作流：调研→写作→审核→导出。",
    edges=[
        Edge(from_node=START, to_node=_research_agent, route=None),
        Edge(from_node=_research_agent, to_node=_writer_agent, route=None),
        Edge(from_node=_writer_agent, to_node=_qa_reviewer, route=None),
        Edge(from_node=_qa_reviewer, to_node=_export_manager, route=None),
    ],
)

root_agent = office_workflow
