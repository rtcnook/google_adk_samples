import os
import sys
from google.adk.agents import SequentialAgent

# 步骤 1：把项目根目录加入模块搜索路径，Cloud Run 和本地运行时都能找到同级模块。
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..")))
from utils.file_loader import load_instructions_file

# 步骤 2：研究阶段 Agent：负责把一个主题扩展成可用于网页生成的研究材料。
from agents.questions_generator.agent import questions_generator_agent
from agents.questions_researcher.agent import questions_researcher_agent
from agents.query_generator.agent import query_generator_agent

# 步骤 3：生成阶段 Agent：把研究材料转为需求、设计方案和最终 HTML 代码。
from agents.requirements_writer.agent import requirements_writer_agent
from agents.designer.agent import designer_agent
from agents.code_writer.agent import code_writer_agent

# 步骤 4：部署版仍然使用 SequentialAgent，方便本地 ADK Web 和云端服务复用同一套流程。
root_agent = SequentialAgent(
    name="root_website_builder_agent",

    # 步骤 5：这里定义完整的云部署版研究网页生成流水线。
    sub_agents=[
        questions_generator_agent,
        questions_researcher_agent,
        query_generator_agent,
        requirements_writer_agent,
        designer_agent,
        code_writer_agent
    ],

    # 步骤 6：描述文件用于 ADK Web/API 展示入口 Agent 的职责。
    description=load_instructions_file("agents/root_website_builder/description.txt")
)
