"""
Export Manager Agent
"""
import pathlib
from google.adk.agents import Agent
from .tools import save_document, save_docx, save_pptx, save_excel

current_dir = pathlib.Path(__file__).parent.resolve()
instruction_path = current_dir / "instruction.txt"
with open(instruction_path, "r", encoding="utf-8") as f:
    instruction_text = f.read()

root_agent = Agent(
    name="export_manager",
    model="gemini-2.5-flash",
    instruction=instruction_text,
    tools=[save_document, save_docx, save_pptx, save_excel],
    description="负责将最终版的文档保存为各种本地文件格式(md, txt, docx, pptx, xlsx)的导出专员。",
)
