# Config-Based AI Tutor Agent (v5)

**Educational Code Demonstrating YAML-Based Agent Creation with Google ADK**

This project showcases the powerful **config-based agent** feature of the Google Agent Development Kit (ADK). It demonstrates how to build a complete multi-agent system where the agent logic, structure, and instructions are defined entirely in YAML files, requiring **zero Python code** for the core agent implementation.

The system features a main "root" agent that acts as an intelligent router, delegating user questions to one of two specialized sub-agents: a `python_tutor_agent` for programming questions and a `physics_tutor_agent` for scientific inquiries. This project is a foundational example of creating modular, maintainable, and code-light AI systems with ADK.

**Note: This is educational code designed to demonstrate the `config` type agent architecture and the power of defining agents declaratively.**

---

## 📦 Features

- ✅ **Zero-Code Agent Logic:** The core behavior, instructions, and relationships of all agents are defined purely in `.yaml` files.
- ✅ **Multi-Agent System:** A 3-agent hierarchy with a root orchestrator and two specialized tutors.
- ✅ **Intelligent Task Delegation:** The `root_agent` analyzes user prompts and routes them to the correct sub-agent (Python or Physics).
- ✅ **Declarative & Modular:** Agents are defined as simple, human-readable configuration files, making the system incredibly easy to understand, modify, and extend.
- ✅ **Specialized Expertise:** Each tutor agent has a unique, detailed set of instructions tailored to its specific domain for high-quality responses.
- ✅ **Gemini 1.5 Flash Powered:** Leverages the speed and capability of Google's Gemini models.
- ✅ **Ready for Deployment:** Includes a `main.py` FastAPI entry point, making the agent system ready to be containerized and deployed as a web service.

---

## 📂 Project Structure

```text
./version_5_config_type/
├── my_agent/                      # Directory containing the agent configurations
│   ├── python_tutor_agent.yaml    # Agent 1: Specializes in Python programming
│   ├── physics_tutor_agent.yaml   # Agent 2: Specializes in physics concepts
│   └── root_agent.yaml            # Orchestrator: Routes questions to the correct tutor
├── main.py                        # FastAPI application entry point for deployment
├── pyproject.toml                 # Project dependencies and configuration
├── uv.lock                        # Pinned dependency versions for reproducibility
└── README.md                      # This documentation file
```

---

## 🚀 Quickstart

### Local Development

### 1. Clone or Download the Project

```bash
# If cloning from a repository
git clone <your-repository-url>
cd version_5_config_type

# Or if you have the project locally
cd version_5_config_type
```

### 2. Set Up Python Environment
**Required:** Python 3.11+, uv, and Git.

```bash
# Navigate to the project root
cd version_5_config_type

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate.bat on Windows

# Install all dependencies
uv sync
```

### 3. Add Your API Key

Create a `.env` file in the `version_5_config_type` project root:

```env
GOOGLE_API_KEY="your-google-api-key"
```

You can get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

---

### 4. Run the Agent

With a config-based agent, point the ADK CLI to the parent directory that contains your agent app folder. In this project, the app folder is `my_agent/`, and it contains `root_agent.yaml`.

```bash
# Run the web UI
adk web .
```

Then open `http://localhost:8000` in your browser and select **`my_agent`**. You can now ask it questions about Python or Physics.

---

### **Run Your ADK Agent**

**ADK CLI Run** <br>`adk run ./my_agent` | - Runs the agent directly in your command-line terminal | - Great for quick, scriptable tests without a UI |

---

## 🧠 How It Works

This project demonstrates an elegant and simple multi-agent workflow orchestrated entirely through YAML configuration. The logic flows as follows:

1.  **User Input**: You provide a prompt to the `root_agent`, which is the entry point to the system.
2.  **Intelligent Routing**: The `root_agent.yaml` contains an `instruction` that explicitly tells the LLM its job: to determine if the user's question is about "Python, programming, or coding" or about "physics concepts, laws, or problems."
3.  **Task Delegation**: Based on its analysis, the `root_agent` delegates the task to the appropriate sub-agent, which is defined in its `sub_agents` list.
    -   If it's a coding question, it passes control to the `python_tutor_agent`.
    -   If it's a science question, it passes control to the `physics_tutor_agent`.
4.  **Specialized Response**: The selected tutor agent (e.g., `physics_tutor_agent`) receives the prompt. It then uses its own highly specific `instruction` (e.g., "Explain physics laws and theories clearly with real-world examples") to generate a detailed, expert-level response.
5.  **Inheritance**: The sub-agents automatically inherit the `model` (`gemini-flash-latest`) from the `root_agent`, reducing configuration duplication.

This entire sophisticated workflow is achieved without a single line of Python agent code, highlighting the power and simplicity of the ADK's config-based approach.

---

## 💬 Example Prompts

Try asking the `root_agent` questions from different domains to see the routing in action.

**Python Questions (Handled by `python_tutor_agent`):**
```
Explain list comprehensions in Python with an example.
What is the difference between a list and a tuple?
How do I handle exceptions using a try-except block?```

**Physics Questions (Handled by `physics_tutor_agent`):**
```
What is Newton's Second Law of Motion?
Can you explain the concept of entropy in simple terms?
How does general relativity describe gravity?
```

---


Happy building with ADK! 🛠
