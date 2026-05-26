# 可部署到 Google Cloud Run 的研究型网站生成 Agent

这是项目 3 的云部署版本。它保留了研究驱动的 6 阶段多 Agent 流程，并额外加入 FastAPI 入口、Dockerfile 和 Cloud Run 部署配置，用于演示如何把 ADK 多 Agent 系统部署到 Google Cloud。

---

## 功能

- 研究驱动的多 Agent 网站生成流程
- 并行研究多个问题
- Google 搜索集成
- 生成完整 HTML、CSS 和 JavaScript 页面
- 提供 `main.py` FastAPI 应用入口
- 提供 `Dockerfile` 和 `requirements.txt`，便于 Cloud Run 部署

---

## Agent 流程

1. `questions_generator`：生成主题研究问题。
2. `questions_researcher`：并行研究问题。
3. `query_generator`：合成研究结果。
4. `requirements_writer`：整理网页需求。
5. `designer`：设计页面结构和风格。
6. `code_writer`：生成最终页面代码。
7. `root_website_builder`：编排流程并保存结果。

---

## 本地安装

```bash
cd version_4_deploy_to_gcloud
uv sync --all-groups
```

---

## 环境变量

本项目支持 Vertex AI。示例：

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

## 本地运行

```bash
adk web ./agents
```

打开 `http://localhost:8000`，选择 `root_website_builder`。

---

## Cloud Run 部署

先设置环境变量：

```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=True
```

部署：

```bash
gcloud run deploy website-builder-agent \
  --source . \
  --region $GOOGLE_CLOUD_LOCATION \
  --project $GOOGLE_CLOUD_PROJECT \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,GOOGLE_GENAI_USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI"
```

---

## 关键文件

- `main.py`：FastAPI 应用入口
- `Dockerfile`：容器构建配置
- `requirements.txt`：Cloud Run 部署依赖
- `agents/`：多 Agent 定义
- `tools/`：文件写入等工具
- `utils/`：提示词文件读取工具
