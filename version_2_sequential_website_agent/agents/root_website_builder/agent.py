import os
import sys
from google.adk.agents import SequentialAgent

# 步骤 1：把项目根目录加入模块搜索路径，方便导入 utils、tools 和各个子 Agent。
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..")))
from utils.file_loader import load_instructions_file

# 步骤 2：导入三个专业子 Agent，它们会按照列表顺序依次执行。
from agents.requirements_writer.agent import requirements_writer_agent
from agents.designer.agent import designer_agent
from agents.code_writer.agent import code_writer_agent

# 步骤 3：使用 SequentialAgent 组织流水线：需求分析 -> 设计方案 -> 代码生成。
root_agent = SequentialAgent(
    name="root_website_builder_agent",

    # 步骤 4：sub_agents 的顺序就是执行顺序，前一个 Agent 的输出会进入后续流程。
    sub_agents=[requirements_writer_agent, designer_agent, code_writer_agent],

    # 步骤 5：根 Agent 的描述从文件加载，供 ADK Web UI 展示。
    description=load_instructions_file("agents/root_website_builder/description.txt")
)
