# ✈️ Multi-Agent Travel Planner Team (Google ADK v2)

An intelligent, hierarchical travel-planning team built using the **Google Agent Development Kit (ADK) v2** and powered by Gemini.

## 🏗️ Architecture Overview
The system features a centralized **Travel Planner Coordinator** managing three specialized sub-agents with varying interaction behaviors:

1. **`travel_planner` (Coordinator)**: Manages delegation and presents final summaries.
2. **`weather_checker` (`single_turn` Mode)**: Autonomously geocodes and fetches weather coordinates without interrupting the conversation.
3. **`flight_booker` (`task` Mode)**: Interactively collects dates/preferences, books the flight, and returns confirmation details.
4. **`itinerary_agent` (`chat` Mode)**: Collaboratively brainstorms a customized vacation itinerary with the user.

---

## 🚀 How to Run the System

### Prerequisites & Installation

We use the fast **`uv`** package manager instead of standard `pip` to manage this project. Follow the instructions below to set up your environment:

#### 1. Initialize and Create Virtual Environment

##### 🍏 macOS
```bash
uv init
uv venv
source .venv/bin/activate
```

##### 🐧 Ubuntu / Linux
```bash
uv init
uv venv
source .venv/bin/activate
```

##### 🪟 Windows (PowerShell)
```powershell
uv init
uv venv
.venv\Scripts\Activate.ps1
```

##### 🪟 Windows (CMD)
```cmd
uv init
uv venv
.venv\Scripts\activate.bat
```

#### 2. Install Dependencies
Run the following command to add and install the required packages:
```bash
uv add -r requirements.txt
```

#### 3. Environment Variables Configuration
We require an environment variable file containing your Gemini API key. Use `.env.example` as a template:

1. Create a `.env` file in the root folder of the project.
2. Open `.env` and add your free Gemini API Key:
```env
GEMINI_API_KEY="your_free_gemini_api_key_here"
```

---

### 1. ADK Web UI
To inspect active sessions, monitor LLM request/response payloads, and review trace spans:
```bash
adk web ./agents
```
Open **`http://127.0.0.1:8000`** in your browser.

---