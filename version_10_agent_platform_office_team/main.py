"""
Maestroffice Lite — 多 Agent 办公助手

用法:
  CLI 交互模式 (CEO Agent，支持自动连续工作): uv run main.py
  CLI 交互模式 (Workflow，单轮全流程):  uv run main.py --workflow
  ADK Web:                           adk web
"""
import os
import json
import sys
import asyncio
import pathlib
from dotenv import load_dotenv

env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

from agents import ceo_agent, office_workflow
from agents.export_manager.tools import create_pptx, get_outputs_dir
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


async def _print_events(runner, user_id, session_id, msg):
    """打印 agent 输出事件，并捕获最终内容。异常不崩溃，只记录。"""
    last_author = None
    all_content = []
    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=msg,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text and part.text.strip():
                        text = part.text.strip()
                        if event.author != last_author:
                            print(f"\n[{event.author}]:")
                            last_author = event.author
                        print(f"  {text[:600]}")
                        all_content.append(text)
            if event.error_code:
                print(f"[Error: {event.error_code}] {event.error_message}", file=sys.stderr)
                # Don't let errors crash the program — continue processing
    except Exception as e:
        print(f"[FatalAgentError] {type(e).__name__}: {e}", file=sys.stderr)
        # Return whatever content we captured, even on error

    return "\n".join(all_content)


def _parse_multi_format_request(user_input: str) -> list:
    """解析用户的多格式请求，返回 [(格式名, 单独的prompt), ...]"""
    import re
    
    # 常见的格式关键词
    format_keywords = {
        'PPT': [r'\bppt\b', r'幻灯片', r'演示文稿', r'powerpoint'],
        'Word': [r'\bword\b', r'文档', r'doc', r'docx'],
        'Excel': [r'\bexcel\b', r'表格', r'xlsx', r'电子表格'],
        'MD': [r'\bmd\b', r'markdown', r'笔记'],
    }
    
    # 检查是否包含多个格式关键词
    found_formats = []
    for fmt_name, patterns in format_keywords.items():
        for pattern in patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                found_formats.append(fmt_name)
                break
    
    # 如果只检测到 0 或 1 个格式，返回原始输入
    if len(found_formats) <= 1:
        return [("单格式", user_input)]
    
    # 提取主题关键词（去掉格式关键词后的部分）
    topic = user_input
    for patterns in format_keywords.values():
        for pattern in patterns:
            topic = re.sub(pattern, '', topic, flags=re.IGNORECASE)
    # Remove common filler words in Chinese
    topic = re.sub(r'[，,。、\s]+', ' ', topic).strip()
    topic = re.sub(r'^(生成|写|创建|制作|做|帮我|请|帮我生成|需要|要)\s*', '', topic, flags=re.IGNORECASE)
    topic = re.sub(r'\s*(的|和|与|以及|还有|也)\s*$', '', topic)
    topic = re.sub(r'\s*(的|和|与|以及|还有|也)\s*', ' ', topic)
    topic = topic.strip()
    
    # 为每个格式生成单独的 prompt
    format_prompts = []
    for fmt in found_formats:
        if fmt == 'PPT':
            format_prompts.append((f"{fmt}(幻灯片)", f"生成一份关于「{topic}」的 PPT 演示文稿，5-8 页，使用 write_temp_json 工具保存 JSON 内容"))
        elif fmt == 'Word':
            format_prompts.append((f"{fmt}(文档)", f"生成一份关于「{topic}」的 Word 文档，包含完整的结构化内容"))
        elif fmt == 'Excel':
            format_prompts.append((f"{fmt}(表格)", f"生成一份关于「{topic}」的 Excel 表格，包含数据对比或统计分析"))
        elif fmt == 'MD':
            format_prompts.append((f"{fmt}(笔记)", f"生成一份关于「{topic}」的 Markdown 笔记，使用清晰的标题和列表结构"))
    
    return format_prompts


def _try_build_ppt_from_content(content: str, filename: str = "output.pptx") -> bool:
    """If the content contains a slides JSON, auto-build the PPT."""
    # Try to extract JSON from the content
    json_str = content.strip()
    
    # Remove markdown code blocks if any
    if json_str.startswith("```"):
        lines = json_str.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        json_str = "\n".join(lines).strip()
    
    # Try to find a JSON object or array in the content
    start = json_str.find("{")
    if start == -1:
        start = json_str.find("[")
    if start != -1:
        json_str = json_str[start:]
        # Find matching close
        depth = 0
        end = -1
        in_str = False
        escape = False
        for i, c in enumerate(json_str):
            if escape:
                escape = False
                continue
            if c == "\\":
                escape = True
                continue
            if c == '"':
                in_str = not in_str
                continue
            if in_str:
                continue
            if c in "{[":
                depth += 1
            elif c in "}]":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end != -1:
            json_str = json_str[:end]
    
    try:
        data = json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        return False
    
    # Check if it looks like slides data (array of slides, or object with slides key)
    slides = None
    theme = "dark"
    if isinstance(data, list):
        slides = data
    elif isinstance(data, dict):
        theme = data.get("theme", "dark")
        slides = data.get("slides", data.get("slides_json", None))
        if slides is None and any(k in data for k in ["layout", "title", "cards", "steps"]):
            slides = [data]
    
    if not slides or not isinstance(slides, list) or len(slides) == 0:
        return False
    
    # Build the PPT
    final_filename = filename.replace(".pptx", "") + ".pptx"
    result = create_pptx(final_filename, theme, json_str)
    print(f"\n{'='*50}")
    print(f"✅ PPT 已自动生成!")
    print(f"   {result}")
    print(f"{'='*50}")
    return True


async def chat_ceo():
    """CEO Agent 模式 — 带自动推进的交互循环"""
    session_service = InMemorySessionService()
    runner = Runner(app_name="maestroffice", agent=ceo_agent, session_service=session_service)

    user_id = "default_user"
    session_id = "default_session"

    await session_service.create_session(
        app_name="maestroffice", user_id=user_id, session_id=session_id,
    )

    print("Welcome to Maestroffice Lite (CEO Mode)!")
    print("Type 'exit' to quit.\n")

    output_dir = pathlib.Path(__file__).parent / "outputs"

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        # 解析多格式请求
        format_prompts = _parse_multi_format_request(user_input)

        if len(format_prompts) > 1:
            print(f"\n📋 检测到多格式请求，将分 {len(format_prompts)} 轮执行：")
            for i, (fmt, prompt) in enumerate(format_prompts, 1):
                print(f"   {i}. {fmt}: {prompt[:80]}...")
            print()

        for fmt, prompt in format_prompts:
            if len(format_prompts) > 1:
                print(f"\n{'='*60}")
                print(f"🔄 正在生成 {fmt} 格式...")
                print(f"{'='*60}\n")

            # Track output files before this round
            existing_files = set(f.name for f in output_dir.iterdir()) if output_dir.exists() else set()

            # Run the CEO agent
            initial_content = await _print_events(
                runner, user_id, session_id,
                types.Content(parts=[types.Part(text=prompt)], role="user"),
            )

            # Auto-advance steps (only break when NEW file created)
            for step in range(5):
                await asyncio.sleep(1)

                current_files = set(f.name for f in output_dir.iterdir()) if output_dir.exists() else set()
                newly_created = current_files - existing_files
                if any(ext in f for f in newly_created for ext in ['.pptx', '.docx', '.xlsx', '.md']):
                    break

                advance_prompts = [
                    "请继续自动完成下一步（research → writer → qa → export），不要停。",
                    "继续下一步。", "请继续推进。", "还有未完成的步骤，继续。", "继续执行工作流。",
                ]
                await _print_events(
                    runner, user_id, session_id,
                    types.Content(
                        parts=[types.Part(text=advance_prompts[min(step, len(advance_prompts) - 1)])],
                        role="user",
                    ),
                )

            # Check what new files were created
            current_files = set(f.name for f in output_dir.iterdir()) if output_dir.exists() else set()
            new_files = current_files - existing_files

            # Fallback
            if not new_files:
                try:
                    _try_build_ppt_from_content(initial_content)
                except Exception as e:
                    print(f"[Fallback] PPT auto-build failed: {e}", file=sys.stderr)

        # Display all output files
        for pattern in ["*.pptx", "*.docx", "*.xlsx", "*.md"]:
            files = sorted(output_dir.glob(pattern), key=lambda f: f.stat().st_mtime, reverse=True)
            if files:
                print(f"\nSaved: {files[0].name} ({files[0].stat().st_size / 1024:.1f} KB)")
        print()


async def chat_workflow():
    """Workflow 模式 — 单轮全流程，兼容 Web"""
    session_service = InMemorySessionService()
    runner = Runner(app_name="maestroffice", agent=office_workflow, session_service=session_service)

    user_id = "default_user"
    session_id = "default_session"

    await session_service.create_session(
        app_name="maestroffice", user_id=user_id, session_id=session_id,
    )

    print("Welcome to Maestroffice Lite (Workflow Mode)!")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        await _print_events(
            runner, user_id, session_id,
            types.Content(parts=[types.Part(text=user_input)], role="user"),
        )

        # Try auto-build PPT from captured content
        try:
            session = await session_service.get_session(
                app_name="maestroffice", user_id=user_id, session_id=session_id,
            )
        except Exception:
            session = None

        output_dir = pathlib.Path(__file__).parent / "outputs"
        ppt_files = sorted(output_dir.glob("*.pptx"), key=lambda f: f.stat().st_mtime, reverse=True)

        if not ppt_files and session and hasattr(session, 'state') and session.state:
            state = session.state
            for key in ["final_content", "draft_content"]:
                if key in state:
                    val = state[key]
                    if isinstance(val, str) and len(val) > 50:
                        if "slides" in val or "layout" in val:
                            if _try_build_ppt_from_content(val):
                                break

        for pattern in ["*.pptx", "*.docx", "*.xlsx", "*.md"]:
            files = sorted(output_dir.glob(pattern), key=lambda f: f.stat().st_mtime, reverse=True)
            if files:
                print(f"\nSaved: {files[0].name} ({files[0].stat().st_size / 1024:.1f} KB)")
        print()


def main():
    if "--workflow" in sys.argv or "-w" in sys.argv:
        asyncio.run(chat_workflow())
    else:
        asyncio.run(chat_ceo())


if __name__ == "__main__":
    main()
