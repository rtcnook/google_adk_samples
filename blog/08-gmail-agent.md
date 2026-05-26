# 项目 8：Gmail Agent 教程

## 你会学到什么

这个项目演示 ADK 如何接入真实 Google API，并通过 OAuth2 授权读取用户 Gmail。

项目目录：

```text
version_8_gmail_agent/gmail_agent/
```

## 核心结构

关键文件：

- `agents/gmail_bot/agent.py`：定义 Gmail Agent、OAuth2 配置和工具注册。
- `agents/gmail_bot/tools.py`：实现 Gmail 邮件查询和正文读取。
- `agents/gmail_bot/instruction.txt`：定义中文 Gmail 助手行为。
- `requirements.txt`：依赖列表。

## 工具能力

项目提供两个主要工具：

- `list_gmail_messages`：按天数、发件人、关键词查询邮件列表。
- `get_message_content`：读取指定邮件完整正文，用于总结。

权限范围是：

```text
https://www.googleapis.com/auth/gmail.readonly
```

这意味着 Agent 只能读取邮件，不能发送、删除或修改邮件。

## Google Cloud 准备

1. 在 Google Cloud Console 创建项目。
2. 启用 Gmail API。
3. 配置 OAuth consent screen。
4. User Type 选择 `External`。
5. 把自己的邮箱加入 Test User。
6. 添加 scope：`https://www.googleapis.com/auth/gmail.readonly`。
7. 创建 OAuth Client，类型选 `Web Application`。
8. Authorized redirect URI 添加：

```text
http://localhost:8000/auth/callback
```

保存 `Client ID` 和 `Client Secret`。

## 环境准备

```bash
cd version_8_gmail_agent
uv venv
.venv\Scripts\activate
uv pip install -r gmail_agent/requirements.txt
```

`.env`：

```env
GOOGLE_API_KEY=your-google-api-key
OAUTH_CLIENT_ID=your-oauth-client-id
OAUTH_CLIENT_SECRET=your-oauth-client-secret
```

## 运行项目

```bash
cd gmail_agent
adk web agents
```

打开：

```text
http://localhost:8000
```

第一次请求 Gmail 数据时，ADK Web UI 会出现授权入口。
点击授权并完成 Google 登录后，Agent 会继续执行原请求。

## 示例问题

```text
What emails did I receive yesterday?
```

```text
Find emails from john.doe@example.com about the project.
```

```text
Summarize the last 5 emails I received today.
```

## 安全注意

这个项目展示了真实 OAuth 工具集成，但还不是生产系统。
生产化时至少要补充：

- token 存储策略。
- 用户隔离。
- 审计日志。
- 错误处理。
- 更严格的数据脱敏和展示策略。
