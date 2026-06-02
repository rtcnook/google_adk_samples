import os
import pathlib
import json

def get_outputs_dir() -> pathlib.Path:
    current_dir = pathlib.Path(__file__).parent.resolve()
    project_root = current_dir.parent.parent
    outputs_dir = project_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    return outputs_dir

def save_document(filename: str, content: str) -> str:
    """
    保存纯文本或 Markdown 内容到本地文件中。
    Args:
        filename (str): 文件名称，例如 'weekly_report.md'。
        content (str): 要保存的文本内容。
    """
    outputs_dir = get_outputs_dir()
    safe_filename = os.path.basename(filename)
    file_path = outputs_dir / safe_filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"文本/Markdown 文档已成功保存到: {file_path}"

def save_docx(filename: str, content: str) -> str:
    """
    保存内容为 Word (.docx) 文档。
    Args:
        filename (str): 文件名称，必须以 .docx 结尾。
        content (str): 要写入文档的文本内容。内容会按换行符分段。
    """
    try:
        from docx import Document
    except ImportError:
        return "错误: 缺少 python-docx 库，请安装。"
    
    outputs_dir = get_outputs_dir()
    safe_filename = os.path.basename(filename)
    if not safe_filename.endswith(".docx"):
        safe_filename += ".docx"
    file_path = outputs_dir / safe_filename
    
    doc = Document()
    for paragraph in content.split("\n"):
        if paragraph.strip():
            doc.add_paragraph(paragraph.strip())
            
    doc.save(file_path)
    return f"Word 文档已成功保存到: {file_path}"

def save_pptx(filename: str, slides_json: str) -> str:
    """
    保存内容为 PowerPoint (.pptx) 文档。
    Args:
        filename (str): 文件名称，必须以 .pptx 结尾。
        slides_json (str): 幻灯片内容的 JSON 字符串表示。必须是一个列表，每个元素是一个字典，包含 "title" (标题) 和 "content" (正文内容)。
            例如: '[{"title": "第一页标题", "content": "这是内容"}, {"title": "第二页标题", "content": "更多内容"}]'
    """
    try:
        from pptx import Presentation
    except ImportError:
        return "错误: 缺少 python-pptx 库，请安装。"
        
    outputs_dir = get_outputs_dir()
    safe_filename = os.path.basename(filename)
    if not safe_filename.endswith(".pptx"):
        safe_filename += ".pptx"
    file_path = outputs_dir / safe_filename
    
    try:
        slides_data = json.loads(slides_json)
    except json.JSONDecodeError:
        return "错误: slides_json 无法解析为有效的 JSON。"
        
    prs = Presentation()
    for slide_data in slides_data:
        title_slide_layout = prs.slide_layouts[1] # 1 is Title and Content layout
        slide = prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        content_box = slide.placeholders[1]
        
        title.text = slide_data.get("title", "")
        content_box.text = slide_data.get("content", "")
        
    prs.save(file_path)
    return f"PPT 文档已成功保存到: {file_path}"

def save_excel(filename: str, data_json: str) -> str:
    """
    保存内容为 Excel (.xlsx) 文档。
    Args:
        filename (str): 文件名称，必须以 .xlsx 结尾。
        data_json (str): 表格数据的 JSON 字符串表示。必须是一个二维数组 (列表的列表)，第一行通常是表头。
            例如: '[["姓名", "年龄"], ["张三", "30"], ["李四", "25"]]'
    """
    try:
        import openpyxl
    except ImportError:
        return "错误: 缺少 openpyxl 库，请安装。"
        
    outputs_dir = get_outputs_dir()
    safe_filename = os.path.basename(filename)
    if not safe_filename.endswith(".xlsx"):
        safe_filename += ".xlsx"
    file_path = outputs_dir / safe_filename
    
    try:
        data = json.loads(data_json)
    except json.JSONDecodeError:
        return "错误: data_json 无法解析为有效的 JSON。"
        
    wb = openpyxl.Workbook()
    ws = wb.active
    
    for row in data:
        if isinstance(row, list):
            ws.append(row)
            
    wb.save(file_path)
    return f"Excel 文档已成功保存到: {file_path}"
