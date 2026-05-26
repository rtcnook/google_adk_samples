import os
import sys
from google.adk.agents import SequentialAgent

# 步骤 1：把项目根目录加入模块搜索路径，保证能导入所有研究和网页生成子 Agent。
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..","..")))
from utils.file_loader import load_instructions_file

# 步骤 2：导入研究阶段 Agent：先生成问题，再并行研究，再合成网页生成查询。
from agents.questions_generator.agent import questions_generator_agent
from agents.questions_researcher.agent import questions_researcher_agent
from agents.query_generator.agent import query_generator_agent

# 步骤 3：导入生成阶段 Agent：把研究结果转成需求、设计和最终代码。
from agents.requirements_writer.agent import requirements_writer_agent
from agents.designer.agent import designer_agent
from agents.code_writer.agent import code_writer_agent

# 步骤 4：根 Agent 负责串起完整研究型网页生成流水线。
root_agent = SequentialAgent(
    name="root_website_builder_agent",

    # 步骤 5：执行顺序为研究问题 -> 并行研究 -> 查询合成 -> 需求 -> 设计 -> 代码。
    sub_agents=[
        questions_generator_agent,
        questions_researcher_agent,
        query_generator_agent,
        requirements_writer_agent,
        designer_agent,
        code_writer_agent
    ],

    # 步骤 6：描述文件用于告诉 ADK UI 这个根 Agent 的用途。
    description=load_instructions_file("agents/root_website_builder/description.txt")
)
