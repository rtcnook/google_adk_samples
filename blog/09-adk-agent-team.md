# 项目 9：ADK Agent Team 教程

## 你会学到什么

这个项目演示一个分层旅行规划团队：主协调 Agent 管理多个专业子 Agent，
分别处理天气、航班和行程规划。

项目目录：

```text
version_9_adk_agent_team/
```

## 核心架构

主 Agent：

- `agents/travel_planner/agent.py`

子 Agent：

- `weather_checker`：查询目的地天气。
- `flight_booker`：收集航班信息并模拟预订。
- `itinerary_agent`：协作生成旅行行程。

执行链路：

```text
用户旅行请求
-> travel_planner 判断任务
-> 委派 weather_checker
-> 委派 flight_booker
-> 需要时委派 itinerary_agent
-> travel_planner 汇总结果
```

## 子 Agent 交互模式

README 中描述了三种不同子 Agent 行为：

- `weather_checker` 使用 `single_turn` 风格，自动完成天气查询。
- `flight_booker` 使用 `task` 风格，会追问日期和偏好。
- `itinerary_agent` 使用 `chat` 风格，和用户协作完善行程。

这个项目的价值在于展示：不是所有子任务都应该用同一种交互模式。

## 环境准备

```bash
cd version_9_adk_agent_team
uv venv
.venv\Scripts\activate
uv add -r requirements.txt
```

`.env`：

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

如果你本地 ADK 配置使用 `GOOGLE_API_KEY`，也可以按项目依赖实际要求统一调整。

## 运行项目

```bash
adk web ./agents
```

打开：

```text
http://127.0.0.1:8000
```

选择 `travel_planner`。

## 示例输入

```text
帮我规划一次去巴黎的旅行。
```

或者更具体：

```text
我想下个月从上海去东京玩 5 天，帮我查天气、安排航班并设计行程。
```

## 这个项目的关键点

项目 2 的多 Agent 是固定顺序流水线。
项目 9 更像真实团队：

- 主协调者根据上下文决定找谁。
- 子 Agent 可以主动追问。
- 任务完成后控制权回到主 Agent。
- 最终由主 Agent 汇总成用户可读的旅行方案。

这种模式适合复杂业务助手，例如企业 IT 支持、销售助理、客服工单处理和个人助理。
