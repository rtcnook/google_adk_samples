# 多 Agent 旅行规划团队

这是一个使用 Google ADK 构建的分层旅行规划团队示例。根 Agent 作为旅行规划协调器，根据任务类型把请求交给天气、航班和行程规划等子 Agent。

---

## 架构

- `travel_planner`：协调器，负责理解用户需求、调度子 Agent，并汇总最终结果。
- `weather_checker`：天气检查 Agent，负责获取目的地天气信息。
- `flight_booker`：航班预订 Agent，负责收集日期和偏好，并模拟预订。
- `itinerary_agent`：行程规划 Agent，负责与用户协作生成旅行计划。

---

## 安装依赖

```bash
cd version_9_adk_agent_team
uv venv
uv pip install -r requirements.txt
```

---

## 环境变量

如果使用 Vertex AI：

```env
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

如果使用 Gemini API Key：

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

项目中的协调器模型为：

```text
gemini-2.5-flash
```

---

## 运行

```bash
adk web ./agents
```

打开：

```text
http://127.0.0.1:8000
```

选择旅行规划相关 Agent 开始对话。

---

## 示例问题

```text
Plan a 5-day trip to Tokyo. Check the weather, suggest an itinerary, and help me book a flight.
```

---

## 说明

本项目中的航班、天气和景点工具主要用于演示多 Agent 协作模式，部分外部服务是模拟实现。
