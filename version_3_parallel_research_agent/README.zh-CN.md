# 研究驱动的网站生成 Agent

这是一个结合顺序编排和并行研究的 Google ADK 多 Agent 示例。用户只需要输入一个主题，系统会先围绕主题生成研究问题，再并行调度多个研究 Agent，最后把研究结果转换成网页需求、设计方案和 HTML 页面。

---

## 功能

- 基于主题自动生成研究问题
- 多个研究 Agent 并行工作，提高研究效率
- 使用 Google 搜索工具获取资料
- 将研究结果合成为网页构建需求
- 自动生成完整 HTML、CSS 和 JavaScript 页面
- 输出文件保存到 `output/` 目录

---

## Agent 流程

1. `questions_generator`：根据主题生成关键研究问题。
2. `questions_researcher`：并行研究每个问题。
3. `query_generator`：把研究结果合成为网页开发请求。
4. `requirements_writer`：整理详细需求。
5. `designer`：生成页面设计方案。
6. `code_writer`：生成最终 HTML/CSS/JS。
7. `root_website_builder`：负责编排整个流程并保存结果。

---

## 安装依赖

```bash
cd version_3_parallel_research_agent
uv sync --all-groups
```

---

## 环境变量

如果使用 Vertex AI：

```env
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

如果使用 Google AI Studio API Key：

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

当前模型名为：

```text
gemini-2.5-flash
```

---

## 运行

```bash
adk web ./agents
```

打开 `http://localhost:8000`，选择 `root_website_builder`。

---

## 示例提示词

```text
人工智能在医疗诊断中的应用
```

系统会先研究该主题，再生成一个研究型网页。
