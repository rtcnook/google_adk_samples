# 项目 2：Sequential Website Builder 教程

## 你会学到什么

这个项目把“生成网页”拆成多个专业角色，演示 ADK 的顺序多 Agent 编排。

项目目录：

```text
version_2_sequential_website_agent/
```

## 核心架构

主入口是：

```text
agents/root_website_builder/agent.py
```

它使用 `SequentialAgent` 串联三个子 Agent：

- `requirements_writer`：把用户需求整理成结构化需求。
- `designer`：根据需求生成页面设计方案。
- `code_writer`：根据设计方案生成 HTML/CSS/JS。

实际代码里根 Agent 类似这样：

```python
root_agent = SequentialAgent(
    name="root_website_builder_agent",
    sub_agents=[requirements_writer_agent, designer_agent, code_writer_agent],
    description=...
)
```

执行链路：

```text
用户需求
-> requirements_writer
-> designer
-> code_writer
-> root agent 保存 HTML
```

## 环境准备

```bash
cd version_2_sequential_website_agent
uv venv
.venv\Scripts\activate
uv sync --all-groups
```

`.env`：

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

## 运行项目

```bash
adk web ./agents
```

打开 `http://localhost:8000`，选择 `root_website_builder`。

示例输入：

```text
Create a simple landing page for a new coffee shop called The Grind.
It should feel warm and include a heading, intro paragraph, and Contact Us button.
```

## 为什么要拆成多个 Agent

单 Agent 可以直接生成页面，但容易把需求、设计和代码混在一起。
顺序多 Agent 的好处是每一步职责更清楚：

- 需求层负责“要做什么”。
- 设计层负责“看起来怎样”。
- 代码层负责“如何实现”。

这种模式适合更复杂的内容生产、报告生成、产品原型生成等任务。

## 可扩展方向

- 在 `code_writer` 后增加 `qa_testing_agent` 检查 HTML。
- 把 `code_writer` 替换成 React 或 Vue 代码生成 Agent。
- 给 `designer` 增加图片搜索或配色工具。
