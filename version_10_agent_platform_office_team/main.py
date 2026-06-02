import os
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()

from agents import ceo_agent
from google.adk.cli.chat import run_chat_loop

def main():
    print("Welcome to Maestroffice Lite (Agent Platform Edition)!")
    print("Type 'exit' to quit.")
    # 我们直接与 ceo_agent 交互
    run_chat_loop(ceo_agent)

if __name__ == "__main__":
    main()
