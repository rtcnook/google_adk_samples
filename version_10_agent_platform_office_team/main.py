"""
Maestroffice Lite — 多 Agent 办公助手

用法:
  CLI 交互模式 (CEO Agent，支持自动连续工作): uv run main.py
  CLI 交互模式 (Workflow，单轮全流程):  uv run main.py --workflow
  ADK Web:                           adk web
"""
import os
import asyncio
import pathlib
import sys
from dotenv import load_dotenv

env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

from agents import ceo_agent, office_workflow
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


async def _print_events(runner, user_id, session_id, msg):
    """打印 agent 输出事件"""
    last_author = None
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=msg,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text and part.text.strip():
                    if event.author != last_author:
                        print(f"\n[{event.author}]:")
                        last_author = event.author
                    print(f"  {part.text[:500]}")
        if event.error_code:
            print(f"[Error: {event.error_code}] {event.error_message}")


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

        await _print_events(
            runner, user_id, session_id,
            types.Content(parts=[types.Part(text=user_input)], role="user"),
        )

        # 自动推进后续步骤
        for step in range(5):
            await asyncio.sleep(1)

            output_dir = pathlib.Path(__file__).parent / "outputs"
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

        # 显示输出文件
        output_dir = pathlib.Path(__file__).parent / "outputs"
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

        output_dir = pathlib.Path(__file__).parent / "outputs"
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
