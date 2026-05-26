# 项目 4：Deploy to Google Cloud 教程

## 你会学到什么

这个项目在项目 3 的研究型多 Agent 流程基础上，加入 Google Cloud Run 部署结构。

项目目录：

```text
version_4_deploy_to_gcloud/
```

## 核心能力

它仍然是研究驱动网页生成系统，但多了部署相关文件：

- `main.py`：FastAPI 应用入口。
- `Dockerfile`：容器构建配置。
- `requirements.txt`：Cloud Run 部署依赖。
- `agents/`：根 Agent 和多个专业子 Agent。
- `tools/file_writer_tool.py`：保存最终网页。

Agent 流程：

```text
topic
-> questions_generator
-> questions_researcher
-> query_generator
-> requirements_writer
-> designer
-> code_writer
-> output html
```

## 本地运行

```bash
cd version_4_deploy_to_gcloud
uv venv
.venv\Scripts\activate
uv sync --all-groups
```

`.env`：

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

启动：

```bash
adk web ./agents
```

访问：

```text
http://localhost:8000
```

## Cloud Run 部署思路

部署到 Cloud Run 时，通常使用 Vertex AI 配置：

```env
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

部署命令示例：

```bash
gcloud run deploy website-builder-agent \
  --source . \
  --region us-central1 \
  --project your-project-id \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=your-project-id,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=True"
```

## 和项目 3 的区别

项目 3 主要服务于本地学习。
项目 4 更接近生产部署演示：

- 有 HTTP 服务入口。
- 有容器构建文件。
- 有 Cloud Run 部署说明。
- 可以通过云端 URL 访问 Agent UI 或 API。

## 注意事项

- 不要把 `.env` 提交到 Git。
- Cloud Run 环境变量应通过部署命令或 Secret Manager 管理。
- 如果要生产化，需要补充鉴权、日志、配额控制和输出文件存储策略。
