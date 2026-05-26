# Google ADK Samples 博客教程

这个目录把仓库里的 9 个 Google ADK 示例项目整理成中文 Markdown 教程。每篇文章对应一个项目，重点说明项目目标、核心架构、关键文件、运行方式和适合扩展的方向。

这些教程适合按顺序阅读，因为项目能力是逐步递进的：从最小单 Agent，到多 Agent 编排、并行研究、云部署、YAML 配置、可视化构建、MCP 工具执行、Gmail OAuth 集成，再到团队式 Agent 协作。

## 文章目录

| 序号 | 教程 | 对应项目 | 重点 |
| --- | --- | --- | --- |
| 01 | [Simple Website Builder](./01-simple-website-builder.md) | `version_1_website_builder_simple` | 单 Agent、instruction、文件写入工具 |
| 02 | [Sequential Website Builder](./02-sequential-website-builder.md) | `version_2_sequential_website_agent` | 顺序多 Agent、需求/设计/代码职责拆分 |
| 03 | [Parallel Research Agent](./03-parallel-research-agent.md) | `version_3_parallel_research_agent` | 研究型流水线、并行研究、主题网页生成 |
| 04 | [Deploy to Google Cloud](./04-deploy-to-gcloud.md) | `version_4_deploy_to_gcloud` | Cloud Run、FastAPI、容器化部署 |
| 05 | [Config Type Agent](./05-config-type-agent.md) | `version_5_config_type` | YAML 声明式 Agent、路由型 Tutor |
| 06 | [ADK No-Code Builder](./06-adk-nocode-builder.md) | `version_6_adk_nocode` | ADK Web 可视化构建器、YAML 输出 |
| 07 | [Programmatic Tool Execution](./07-programmatic-tool-execution.md) | `version_7_programmatic_tool_execution` | MCP 工具动态加载、Python 程序化执行 |
| 08 | [Gmail Agent](./08-gmail-agent.md) | `version_8_gmail_agent` | OAuth2、Gmail API、只读邮件助手 |
| 09 | [ADK Agent Team](./09-adk-agent-team.md) | `version_9_adk_agent_team` | 分层 Agent Team、旅行规划、多模式子 Agent |

## 推荐阅读路线

### 入门阶段

先读项目 1 和项目 2。

项目 1 让你理解 ADK 的最小工作单元：一个 Agent 加一个工具。项目 2 在此基础上加入顺序编排，让多个专业 Agent 共同完成一个网页生成任务。

### 编排阶段

继续读项目 3 和项目 4。

项目 3 展示如何把“研究”放在生成之前，并使用并行 Agent 提高信息收集效率。项目 4 则把类似架构包装成可部署到 Google Cloud Run 的服务。

### 配置阶段

再读项目 5 和项目 6。

项目 5 使用 YAML 声明 Agent，不写 Python Agent 代码。项目 6 使用 ADK Web 的可视化构建器创建 Agent，并观察 UI 配置如何落到本地 YAML 文件。

### 工具和业务集成阶段

最后读项目 7、项目 8 和项目 9。

项目 7 关注 MCP 工具如何在运行时动态注入，并由 Agent 生成 Python 代码串联调用。项目 8 接入真实 Gmail API 和 OAuth2 授权。项目 9 展示更接近业务系统的 Agent Team：主协调者根据任务委派给天气、航班和行程子 Agent。

## 通用环境准备

多数项目需要 Python、`uv` 和 Google API Key。进入具体项目后，通常执行：

```bash
uv venv
.venv\Scripts\activate
uv sync --all-groups
```

常见 `.env` 配置：

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

如果使用 Vertex AI，通常配置：

```env
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

项目 8 还需要 OAuth 客户端信息：

```env
OAUTH_CLIENT_ID=your-oauth-client-id
OAUTH_CLIENT_SECRET=your-oauth-client-secret
```

## 常用运行方式

大部分 ADK 项目可以通过 Web UI 调试：

```bash
adk web ./agents
```

部分配置型项目需要指向项目根目录：

```bash
adk web .
```

项目 8 的 Gmail Agent 入口在子目录中：

```bash
cd version_8_gmail_agent/gmail_agent
adk web agents
```

项目 7 是命令行程序化工具执行示例：

```bash
cd version_7_programmatic_tool_execution
uv run python main.py
```
