# 顺序式网站生成 Agent

这是一个基于 Google ADK 的多 Agent 示例。它用一个根 Agent 按顺序调度三个专业 Agent，把用户的一句话网站需求转换为完整的 HTML、CSS 和 JavaScript 页面。

---

## 功能

- 根 Agent 负责编排完整流程
- `requirements_writer` 负责整理和细化需求
- `designer` 负责规划页面结构、布局和视觉风格
- `code_writer` 负责生成最终网页代码
- 最终结果会保存到 `output/` 目录下的 `.html` 文件

---

## 工作流程

1. 用户把高层需求发给 `root_website_builder`。
2. 根 Agent 调用 `requirements_writer`，把需求整理成结构化规格。
3. 根 Agent 把规格交给 `designer`，生成页面设计方案。
4. 根 Agent 把设计方案交给 `code_writer`，生成 HTML/CSS/JS。
5. 根 Agent 调用文件写入工具，把最终页面保存到 `output/`。

---

## 安装依赖

```bash
cd version_2_sequential_website_agent
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
为一家叫 The Grind 的咖啡店创建一个简单落地页。页面要温暖、有吸引力，使用棕色和奶油色配色，包含大标题、鲜烘咖啡豆简介和 Contact Us 按钮。
```

---

## 扩展方向

- 在 `code_writer` 后增加 QA Agent
- 把 `code_writer` 替换成 React 组件生成 Agent
- 为设计阶段增加图片生成或素材搜索工具
