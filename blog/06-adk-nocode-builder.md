# 项目 6：ADK No-Code Builder 教程

## 你会学到什么

这个项目演示 ADK Visual Agent Builder：通过浏览器可视化界面创建 Agent，
底层仍然生成标准 ADK YAML 配置。

项目目录：

```text
version_6_adk_nocode/
```

## 核心结构

重要文件：

- `web_page_generator_2/root_agent.yaml`：手动在 UI 中配置出的 Agent。
- `webgen0/root_agent.yaml`：另一个可视化生成的 Agent 配置。
- `outputs/output1.html`：生成网页示例。

`web_page_generator_2/root_agent.yaml` 定义了一个 `LlmAgent`，
目标是根据用户请求生成单文件 HTML/CSS/JS 页面。

## 环境准备

```bash
cd version_6_adk_nocode
uv venv
.venv\Scripts\activate
uv sync
```

`.env`：

```env
GOOGLE_API_KEY=your-google-api-key
```

## 启动可视化构建器

```bash
adk web
```

打开终端输出的地址，通常是：

```text
http://localhost:8000
```

## 手动创建网页生成 Agent

在 ADK Web UI 中：

1. 点击 Agent 下拉框旁边的 `+`。
2. 新建 Agent，例如 `web_page_generator_2`。
3. Agent Type 选择 `LlmAgent`。
4. Model 填 `gemini-2.5-flash` 或项目 README 中的 Gemini Flash 模型。
5. Description 填 `single page website builder agent`。
6. Instruction 填：

```text
Build a single unified HTML + CSS + JS document that is a webpage as per the user query.
```

保存后，ADK 会在本地生成 `root_agent.yaml`。

## 测试 Agent

选择刚创建的 Agent，输入：

```text
Build a generic landing page template.
```

Agent 会在聊天窗口输出完整 HTML。
可以把内容保存到 `outputs/` 并用浏览器打开。

## 注意事项

Visual Builder 和 Builder Assistant 属于较新的能力。
手动配置通常更稳定，AI 辅助构建可能出现配置文件没有完整写入的问题。

这个项目适合用来理解：

- UI 配置如何映射到 YAML。
- no-code Agent 的边界在哪里。
- 为什么复杂系统仍需要源码级检查。
