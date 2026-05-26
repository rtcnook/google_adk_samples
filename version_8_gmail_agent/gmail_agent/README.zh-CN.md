# Gmail 助手 Agent

这是一个基于 Google ADK 的 Gmail 助手示例。它通过 Google OAuth2 和 Gmail API 连接用户邮箱，可以查询邮件、列出邮件并使用 Gemini 进行摘要。

仅用于学习和演示，不建议直接用于生产环境。

---

## 功能

- 按时间范围、发件人或关键词查询邮件
- 使用 Gemini 对邮件内容进行摘要
- 使用 ADK 的 `AuthenticatedFunctionTool` 处理 OAuth 授权
- 使用 Gmail 只读权限，不发送或删除邮件

---

## Google Cloud 准备工作

1. 在 Google Cloud Console 创建项目。
2. 启用 Gmail API。
3. 配置 OAuth consent screen：
   - User Type 选择 `External`
   - 把你的邮箱加入 Test User
   - 添加 scope：`https://www.googleapis.com/auth/gmail.readonly`
4. 创建 OAuth Client：
   - 类型选择 `Web Application`
   - Authorized redirect URIs 添加 `http://localhost:8000/auth/callback`
5. 保存 `Client ID` 和 `Client Secret`。

---

## 安装依赖

```bash
cd version_8_gmail_agent
uv venv
uv pip install -r gmail_agent/requirements.txt
```

---

## 环境变量

在 `.env` 中配置：

```env
GOOGLE_API_KEY=your-google-api-key
OAUTH_CLIENT_ID=your-oauth-client-id
OAUTH_CLIENT_SECRET=your-oauth-client-secret
```

如果使用 Vertex AI，也可以配置：

```env
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
GOOGLE_CLOUD_LOCATION=us-central1
OAUTH_CLIENT_ID=your-oauth-client-id
OAUTH_CLIENT_SECRET=your-oauth-client-secret
```

---

## 运行

```bash
cd version_8_gmail_agent/gmail_agent
adk web agents
```

打开 `http://localhost:8000`。第一次调用 Gmail 工具时，页面会要求你完成 Google 授权。

---

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

---

## 授权说明

如果 Agent 回复需要授权，这是正常现象。请在 ADK Web UI 中点击 Authorize、Login 或授权链接，完成 Google OAuth 登录后再继续原请求。

---

## 安全说明

该示例只使用 `gmail.readonly` 权限。访问令牌保存在本地，不会主动分享给第三方。
