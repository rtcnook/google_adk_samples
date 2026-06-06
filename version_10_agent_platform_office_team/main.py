"""
Maestroffice Lite — 多 Agent 办公助手

用法:
  CLI 交互模式 (CEO Agent，支持自动连续工作): uv run main.py
  CLI 交互模式 (Workflow，单轮全流程):  uv run main.py --workflow
  ADK Web:                           adk web
"""
import os
import json
import asyncio
import pathlib
import sys
from dotenv import load_dotenv

env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

from agents import ceo_agent, office_workflow
from agents.export_manager.tools import create_pptx, get_outputs_dir
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


async def _print_events(runner, user_id, session_id, msg):
    """打印 agent 输出事件，并捕获最终内容"""
    last_author = None
    all_content = []
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
            print(f"[Error: {event.error_code}] {event.error_message}")

    return "\n".join(all_content)


def _try_build_ppt_from_content(content: str, filename: str = "Hermes_Agent_介绍.pptx") -> bool:
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

        # Run the CEO agent and capture the initial final content (before auto-advance)
        initial_content = await _print_events(
            runner, user_id, session_id,
            types.Content(parts=[types.Part(text=user_input)], role="user"),
        )

        # Track output files before auto-advance
        output_dir = pathlib.Path(__file__).parent / "outputs"
        existing_files = set(f.name for f in output_dir.iterdir()) if output_dir.exists() else set()

        # Auto-advance steps
        for step in range(5):
            await asyncio.sleep(1)

            recent = sorted(
                list(output_dir.glob("*.pptx")) + list(output_dir.glob("*.docx")) +
                list(output_dir.glob("*.xlsx")) + list(output_dir.glob("*.md")),
                key=lambda f: f.stat().st_mtime, reverse=True,
            )
            if recent:
                break

            prompts = [
                "请继续自动完成下一步（research → writer → qa → export），不要停。",
                "继续下一步。", "请继续推进。", "还有未完成的步骤，继续。", "继续执行工作流。",
            ]
            await _print_events(
                runner, user_id, session_id,
                types.Content(
                    parts=[types.Part(text=prompts[min(step, len(prompts) - 1)])],
                    role="user",
                ),
            )

        # Check what new files were created
        current_files = set(f.name for f in output_dir.iterdir()) if output_dir.exists() else set()
        new_files = current_files - existing_files

        # Fallback: if export_manager didn't create any file, try to auto-build PPT from initial LLM content
        if not new_files:
            _try_build_ppt_from_content(initial_content)

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
