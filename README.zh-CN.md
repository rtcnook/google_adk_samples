# Google ADK Agent 示例项目

欢迎来到 The AI Language 官方的 Google Agent Development Kit (ADK) 示例应用仓库。本集合旨在提供实用的、亲自动手的示例，展示如何使用 ADK 框架构建强大且富有创造力的智能体 (Agent)。

本仓库的目标是展示不同的架构模式——从简单的单一用途 Agent 到复杂的多 Agent 协作系统。每个项目都包含在各自独立的文件夹中，并配有详细的说明。

---

## 🌱 可用 Agent 项目

本集合正在积极增加中。以下是目前可用的 Agent 示例项目：

### 1. 简单的网站构建器 (`version_1_website_builder_simple`)
*   **架构:** 单 Agent 系统
*   **描述:** 极简的 ADK 应用，接收自然语言指令并生成完整的 HTML 网页。
*   **最适合:** 学习 ADK Agent 的基础指令、工具和基本输入输出。

### 2. 顺序执行的网站构建器 (`version_2_sequential_website_agent`)
*   **架构:** 多 Agent，顺序协作
*   **描述:** 由一个“主”Agent 顺序协调多个专业 Agent (需求分析 -> 设计师 -> 程序员) 来构建网站。

### 3. 智能研究驱动的网站构建器 (`version_3_parallel_research_agent`)
*   **架构:** 多 Agent，顺序 + 并行协作
*   **描述:** 高级系统，结合智能研究和并行处理。通过 6 个 Agent 的流水线将简单的主题转化为全面的研究报告网页。

### 4. 可云端部署的研究型网站构建器 (`version_4_deploy_to_gcloud`)
*   **架构:** 多 Agent，含云端部署
*   **描述:** 面向 Google Cloud Run 部署的优化版本，包含 FastAPI 集成、容器化及云端就绪配置。

### 5. 基于配置的 AI 导师 Agent (`version_5_config_type`)
*   **架构:** 多 Agent，基于 YAML 配置
*   **描述:** 展示 ADK 的基于配置 (YAML) 的 Agent 功能。无需编写 Python 代码即可实现核心逻辑。

### 6. 无代码可视化 Agent 构建器 (`version_6_adk_nocode`)
*   **架构:** 无代码，可视化构建
*   **描述:** 介绍 ADK 的可视化构建界面 (`adk web`)，展示如何通过画布 UI 或者 Gemini 驱动的助手创建 Agent。

### 10. Agent Platform 多 Agent 办公助手 (`version_10_agent_platform_office_team`)
*   **架构:** 多 Agent, Agent Platform
*   **描述:** 基于 Google Cloud Agent Platform 的多 Agent 办公协作团队。包含经理、写手、研究员、质量审查员和导出专员，用于协助处理日常办公文档（支持导出 Markdown、Word、PPT、Excel）。
*   **最适合:** 学习如何构建企业级自动化办公 Agent 团队以及多种办公文件格式导出。
*   **➡️ 详细说明请查看 `version_10_agent_platform_office_team/` 目录。**

---

## 🚀 通用设置说明

本仓库现已配置为 **统一的 `uv` 工作区 (Workspace)**。您**无需**在每个子项目中单独创建虚拟环境，所有项目的依赖由根目录统一管理。

### 1. 克隆仓库

```bash
git clone https://github.com/theailanguage/adk_samples.git
cd adk_samples
```

### 2. 设置 API Key

要使用这些 Agent，您需要配置 Google API 密钥。
1. 进入您想要运行的具体项目文件夹 (例如 `version_10_agent_platform_office_team`)。
2. 在该目录下创建一个 `.env` 文件。
3. 添加您的 API 密钥信息：

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```
*(注意：部分项目可能使用 Vertex AI，请参考其专属 README 设置 `GOOGLE_CLOUD_PROJECT` 等参数)*

### 3. 设置 Python 环境 (全局统一)

只需在**项目根目录**执行一次依赖同步即可：

```bash
# 确保您位于项目根目录
uv sync
```
执行后，`uv` 会自动在根目录创建虚拟环境 `.venv` 并安装整个工作区（包含所有子项目）需要的所有依赖。

---

## 🤖 运行 Agent

在配置好环境后，您可以进入任意项目并通过 `uv run` 来启动 Agent。`uv` 会自动向上寻找根目录的虚拟环境来执行。

```bash
# 进入您想要运行的项目
cd version_10_agent_platform_office_team/

# 方式一：使用 ADK Web 界面运行
uv run adk web ./agents

# 方式二：使用项目自带的代码终端运行 (如果包含 main.py)
uv run main.py
```

### **四种运行 ADK Agent 的方式**

| 序号 | 方式与命令 | 描述 | 适用场景 |
|------|-----------|------|----------|
| 1 | **ADK Web** <br>`uv run adk web ./agents` | 启动浏览器 UI | 调试或快速演示 |
| 2 | **ADK API Server** <br>`uv run adk api_server ./agents` | 启动 HTTP API 服务 | 基于 REST API 的系统集成 |
| 3 | **程序化 Python 脚本** <br>`uv run main.py` | 代码驱动的交互 | 构建 CLI 工具或后端流水线 |
| 4 | **ADK CLI Run** <br>`uv run adk run agents/root_agent` | 命令行直接运行指定的 Agent | 快速测试 |

---

## 📜 许可证

本仓库及代码遵循 **GNU General Public License v3.0**。详情请参阅 `LICENSE` 文件。
