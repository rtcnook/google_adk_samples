# 项目 5：Config Type Agent 教程

## 你会学到什么

这个项目演示 ADK 的 config-based agent：不用写 Python Agent 代码，
只用 YAML 定义 Agent、子 Agent 和路由关系。

项目目录：

```text
version_5_config_type/
```

## 核心结构

主要文件在：

```text
my_agent/
```

里面包含：

- `root_agent.yaml`：主 Agent，负责判断问题类型并委派。
- `python_tutor_agent.yaml`：Python 编程导师。
- `physics_tutor_agent.yaml`：物理导师。

执行链路：

```text
用户问题
-> root_agent 判断领域
-> Python 问题交给 python_tutor_agent
-> 物理问题交给 physics_tutor_agent
-> 返回专业回答
```

## 环境准备

```bash
cd version_5_config_type
uv venv
.venv\Scripts\activate
uv sync
```

`.env`：

```env
GOOGLE_API_KEY=your-google-api-key
```

## 运行项目

这个项目的 Agent app 目录是 `my_agent/`，因此运行时指向当前目录：

```bash
adk web .
```

打开 `http://localhost:8000`，选择 `my_agent`。

也可以命令行运行：

```bash
adk run ./my_agent
```

## 示例问题

Python 问题：

```text
Explain list comprehensions in Python with an example.
```

物理问题：

```text
What is Newton's Second Law of Motion?
```

## 这个项目的价值

它展示了“声明式 Agent”的优势：

- 结构清晰，适合非 Python 用户维护。
- 修改 Agent 行为只需要改 YAML。
- 子 Agent 关系清楚，容易扩展。
- 很适合客服、教学、问答路由等场景。

如果要继续扩展，可以新增 `math_tutor_agent.yaml`，再把它加入 `root_agent.yaml` 的 `sub_agents`。
