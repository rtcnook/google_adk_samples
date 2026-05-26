# 项目 3：Parallel Research Agent 教程

## 你会学到什么

这个项目在网页生成之前加入“研究阶段”，演示顺序编排和并行研究的结合。

项目目录：

```text
version_3_parallel_research_agent/
```

## 核心架构

项目包含这些 Agent：

- `root_website_builder`：总编排入口。
- `questions_generator`：围绕用户主题生成关键研究问题。
- `questions_researcher`：并行研究多个问题。
- `query_generator`：把研究结果合成为网页生成需求。
- `requirements_writer`：写结构化需求。
- `designer`：写视觉设计方案。
- `code_writer`：生成最终 HTML/CSS/JS。

整体流程：

```text
主题输入
-> 生成研究问题
-> 并行研究问题
-> 合成网页开发查询
-> 需求整理
-> 视觉设计
-> 代码生成
-> 输出 HTML
```

## 环境准备

```bash
cd version_3_parallel_research_agent
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
renewable energy
```

或者：

```text
artificial intelligence in healthcare
```

## 这个项目的关键点

项目 2 是“用户给需求，Agent 直接设计和编码”。
项目 3 则多了一层“先研究，再生成”：

- 输入可以很短，只给一个主题。
- 系统会自动拆解研究问题。
- 研究结果会进入后续需求和设计阶段。
- 最终页面更像一篇研究型专题网页。

## 适合迁移到哪里

这种模式适合：

- 自动生成行业报告。
- 自动生成主题学习页。
- 自动生成 SEO 内容页。
- 自动生成产品调研摘要。

如果要提高质量，可以给研究 Agent 加入更可靠的数据源工具，例如学术搜索、内部知识库或行业数据库。
