# 项目 10 重写计划：Google Cloud Agent Platform 多 Agent 办公助手

> 状态：计划稿（先不写代码）。
>
> 目标：在项目 10 中重新实现一个类似 `E:\CodeArea\AICode\maestroffice` 思路的办公自动化 Agent 项目，并参考项目 9 的多 Agent 目录结构与 Gemini/Vertex AI 环境变量配置方式。

---

## 1. 背景与约束

### 1.1 已知需求

- 项目 10 目前“做了一部分但没有完成”，需要重写为一个更完整、结构清晰、可运行的示例项目。
- 新项目需要借鉴本地 `maestroffice` 的代码思路：围绕办公任务进行多 Agent 协作，例如理解用户需求、拆解任务、生成/编辑文档、汇总结果等。
- 新项目需要使用 Google Cloud 的 Agent Platform / Agent Runtime / Vertex AI Agent Engine 能力，支持从本地 ADK 调试迁移到云端部署。
- 可以参考项目 9 的结构和 API key / Vertex AI 环境变量配置方式。

### 1.2 当前环境限制

- 当前仓库中没有 `E:\CodeArea\AICode\maestroffice`，我无法直接读取该 Windows 本地目录代码。
- 因此第一版会按“办公自动化多 Agent”的通用架构重写；如果后续你把 `maestroffice` 关键文件贴出来或复制进仓库，我再把其中的具体业务逻辑、提示词、工具函数迁移进项目 10。

---

## 2. 项目定位

项目 10 建议命名为：

```text
version_10_agent_platform_office_team
```

一句话定位：

> 一个基于 Google ADK + Google Cloud Agent Platform 的多 Agent 办公助手示例，演示如何把“办公任务理解、资料整理、文档生成、审阅修改、结果导出”拆成多个专业 Agent，并支持本地运行与云端 Agent Runtime 部署。

---

## 3. 参考依据

### 3.1 参考项目 9 的部分

项目 9 的关键思想是：

- 一个主协调 Agent 负责接收用户请求、判断任务类型、委派给子 Agent。
- 子 Agent 分别负责专业任务。
- 目录采用 `agents/<agent_name>/agent.py + instruction.txt + tools.py` 的清晰结构。
- 环境变量同时支持：
  - Vertex AI：`GOOGLE_GENAI_USE_VERTEXAI=True`、`GOOGLE_CLOUD_PROJECT`、`GOOGLE_CLOUD_LOCATION`
  - Gemini API Key：`GOOGLE_API_KEY`、`GOOGLE_GENAI_USE_VERTEXAI=FALSE`

项目 10 会复用这种工程组织方式，但将“旅行规划团队”替换为“办公协作团队”。

### 3.2 参考 Google Cloud Agent Platform 的部分

后续实现会优先按 ADK 官方部署路线设计：

- 本地：`adk web ./agents`
- 云端：使用 ADK/Agent Platform 的 Agent Runtime 或 Agent Engine 部署路径
- 依赖：`google-adk` 与 `google-cloud-aiplatform[adk,agent_engines]`
- 云端环境：`GOOGLE_CLOUD_PROJECT`、`GOOGLE_CLOUD_LOCATION`、`GOOGLE_GENAI_USE_VERTEXAI=True`

参考文档：

- ADK Agent Runtime / Agent Engine 部署文档：https://adk.dev/deploy/agent-engine/
- ADK 部署总览：https://adk.dev/deploy/
- Google Cloud ADK 概览：https://docs.cloud.google.com/agent-builder/agent-development-kit/overview

---

## 4. 推荐功能范围

### 4.1 第一版必须完成

第一版不追求复杂 Office 文件二进制编辑，而是先把多 Agent 工作流跑通：

1. 用户输入办公任务，例如：
   - “帮我写一份项目周报”
   - “把这些会议纪要整理成行动项”
   - “生成一份产品方案大纲”
   - “把下面内容改成正式邮件”
2. 主 Agent 分析任务类型并拆解。
3. 子 Agent 分工处理：
   - 需求理解
   - 信息整理
   - 文档撰写
   - 审阅润色
   - 导出 Markdown / HTML / JSON
4. 结果保存到本地 `outputs/` 目录。
5. 支持本地 ADK Web 运行。
6. 提供 Agent Platform / Agent Runtime 部署说明或部署脚本。

### 4.2 第二版再增强

后续可继续增加：

- `.docx` 生成与读取
- `.pptx` 大纲生成
- `.xlsx` 表格摘要与分析
- Google Drive / Gmail / Calendar 集成
- Vertex AI Search / RAG 知识库
- 用户身份与权限控制
- 云端长期会话与任务状态管理

---

## 5. 多 Agent 架构设计

建议设计为 1 个主协调 Agent + 5 个专业子 Agent。

```text
office_coordinator
├── task_analyzer
├── research_summarizer
├── document_writer
├── document_reviewer
└── export_manager
```

### 5.1 `office_coordinator`

职责：

- 接收用户办公需求。
- 判断任务类型：写作、总结、邮件、方案、报告、表格分析、导出等。
- 委派给对应子 Agent。
- 汇总最终结果。
- 控制中文输出格式。

### 5.2 `task_analyzer`

职责：

- 抽取用户目标、受众、语气、长度、截止时间、输出格式。
- 如果信息不足，生成澄清问题。
- 输出结构化任务说明。

### 5.3 `research_summarizer`

职责：

- 整理用户提供的原始材料。
- 提取主题、关键事实、风险、行动项。
- 为写作 Agent 准备素材。

第一版先只处理用户输入文本，不接外部搜索，避免引入不必要复杂度。

### 5.4 `document_writer`

职责：

- 生成周报、方案、邮件、会议纪要、项目计划等正文。
- 按任务要求控制语气、层级、格式。
- 输出 Markdown 草稿。

### 5.5 `document_reviewer`

职责：

- 检查逻辑、表达、格式、一致性。
- 给出修改建议。
- 可输出“修订版”。

### 5.6 `export_manager`

职责：

- 将最终内容保存到 `outputs/`。
- 支持 Markdown / HTML / JSON 三类导出。
- 返回文件路径。

---

## 6. 目录结构计划

建议新建如下结构：

```text
version_10_agent_platform_office_team/
├── README.md
├── README.zh-CN.md
├── PROJECT_PLAN.zh-CN.md
├── pyproject.toml
├── requirements.txt
├── main.py
├── deploy_agent_engine.py
├── .env.example
├── outputs/
│   └── .gitkeep
├── agents/
│   ├── __init__.py
│   ├── office_coordinator/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── instruction.txt
│   ├── task_analyzer/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── instruction.txt
│   │   └── types.py
│   ├── research_summarizer/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── instruction.txt
│   ├── document_writer/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── instruction.txt
│   ├── document_reviewer/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── instruction.txt
│   └── export_manager/
│       ├── __init__.py
│       ├── agent.py
│       ├── instruction.txt
│       └── tools.py
└── tools/
    ├── __init__.py
    ├── document_export.py
    └── text_utils.py
```

---

## 7. 云端部署设计

### 7.1 本地运行

本地调试沿用项目 9 的方式：

```bash
cd version_10_agent_platform_office_team
uv venv
uv pip install -r requirements.txt
adk web ./agents
```

### 7.2 Gemini API Key 模式

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

适合快速本地演示。

### 7.3 Vertex AI / Agent Platform 模式

```env
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

适合部署到 Google Cloud Agent Platform。

### 7.4 Agent Runtime / Agent Engine 部署脚本

计划新增：

```text
deploy_agent_engine.py
```

职责：

- 初始化 Vertex AI。
- 打包 ADK agent。
- 创建或更新 Agent Runtime / Agent Engine 资源。
- 输出远程 resource name，方便后续调用。

第一版可以先提供可读部署脚本和 README 步骤；如果本地环境没有 gcloud 登录或 Google Cloud 项目权限，则只做静态检查，不实际部署。

---

## 8. 关键实现步骤

### 阶段 1：清理与骨架创建

- 检查现有项目 10 残留内容。
- 新建 `version_10_agent_platform_office_team/`。
- 写入 README、依赖文件、环境变量示例。
- 搭建 `agents/` 多 Agent 目录。

### 阶段 2：实现本地 ADK 多 Agent

- 实现 `office_coordinator`。
- 实现 5 个子 Agent。
- 按项目 9 的方式动态导入 peer sub-agent。
- 先使用 mock / 轻量工具保证功能可跑。

### 阶段 3：实现办公工具

- `save_markdown(content, filename)`
- `save_html(content, filename)`
- `save_json(data, filename)`
- `sanitize_filename(name)`
- `build_document_metadata(...)`

### 阶段 4：接入 Agent Platform 部署

- 增加 `deploy_agent_engine.py`。
- 增加部署 README。
- 增加 `.env.example`。
- 明确本地 API Key 与 Vertex AI 两种模式。

### 阶段 5：测试与验证

计划运行：

```bash
python -m compileall version_10_agent_platform_office_team
python -m pytest  # 如果后续增加测试
adk web ./agents  # 需要人工浏览器验证时再运行
```

如果没有真实 Google Cloud 凭证，则不执行云端部署，只验证脚本语法和文档完整性。

---

## 9. 示例交互目标

### 示例 1：生成周报

用户：

```text
帮我根据下面内容写一份中文项目周报，语气正式，给技术经理看：
1. 完成 Gmail Agent OAuth 调试
2. 多 Agent 旅行项目已跑通
3. 项目 10 需要改造成办公助手
```

期望：

- Coordinator 调用 analyzer 提取任务。
- Summarizer 整理材料。
- Writer 写周报。
- Reviewer 润色。
- Export Manager 保存 Markdown。

### 示例 2：会议纪要整理

用户：

```text
把下面会议记录整理成：结论、待办事项、负责人、风险。
```

期望：

- 输出结构化 Markdown。
- 可额外导出 JSON 便于系统集成。

---

## 10. 风险与处理

| 风险 | 处理方式 |
| --- | --- |
| 无法读取 `maestroffice` 本地代码 | 先按办公助手通用架构实现；后续拿到代码后再迁移细节 |
| Google Cloud 凭证不可用 | 本地只做 API Key / 静态验证；部署脚本写清楚但不强制执行 |
| Agent Platform 文档版本变化 | 以官方 ADK / Google Cloud 文档为准，部署相关命令保持可替换 |
| Office 二进制文件处理复杂 | 第一版先导出 Markdown / HTML / JSON，第二版再加 docx/pptx/xlsx |
| 多 Agent 委派不可控 | 每个 Agent 的 instruction 限定职责，并让 coordinator 明确流程 |

---

## 11. 预期交付物

第一轮代码交付预计包含：

- 完整项目目录：`version_10_agent_platform_office_team/`
- 中文/英文 README
- 多 Agent 代码骨架
- 可运行的办公任务示例
- 文档导出工具
- Agent Platform 部署脚本/说明
- 环境变量示例
- 基础语法检查通过

---

## 12. 下一步

如果你确认这个计划，我下一步会开始正式重写项目 10：

1. 创建项目 10 完整目录。
2. 按项目 9 的多 Agent 结构写代码。
3. 加入 Google Cloud Agent Platform 部署入口。
4. 保留 API Key 和 Vertex AI 两套运行方式。
5. 跑基础检查并提交代码。
