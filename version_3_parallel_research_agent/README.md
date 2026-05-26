# Google ADK Agent Samples

Welcome to The AI Language official repository for Google Agent Development Kit (ADK) sample applications. This collection is designed to provide practical, hands-on examples of how to build powerful and creative agents using the ADK framework.

The goal of this repository is to showcase different architectural patterns—from simple, single-purpose agents to complex, multi-agent systems. Each project is self-contained and includes a detailed `README.md` with specific setup and usage instructions.

---

## 🌱 Available Agent Projects

This collection is actively growing. Below are the current agent examples available.

### 1. Simple Website Builder (`version_1_website_builder_simple`)

*   **Architecture:** Single-Agent System
*   **Description:** A minimal ADK application featuring a single LLM-powered agent. It takes a natural language prompt (e.g., "create a page with a blue button") and generates a complete, self-contained HTML file.
*   **Best for:** Understanding the fundamentals of an ADK agent, including instructions, tools, and basic I/O.
*   **➡️ For detailed instructions, see the `README.md` inside the [`version_1_website_builder_simple/`](./version_1_website_builder_simple/) directory.**

### 2. Sequential Website Builder (`version_2_sequential_website_agent`)

*   **Architecture:** Multi-Agent, Sequential Orchestration
*   **Description:** A more advanced system where a "root" agent orchestrates a team of specialized agents in a sequence to build a website. This mimics a real-world development workflow: `Requirements Writer` -> `Designer` -> `Code Writer`.
*   **Best for:** Learning how to build complex workflows by chaining agents together, where the output of one agent becomes the input for the next.
*   **➡️ For detailed instructions, see the `README.md` inside the [`version_2_sequential_website_agent/`](./version_2_sequential_website_agent/) directory.**

### 3. Intelligent Research-Driven Website Builder (`version_3_intelligent_research_website_builder`)

*   **Architecture:** Multi-Agent, Sequential + Parallel Orchestration
*   **Description:** An advanced system that combines intelligent research capabilities with parallel processing. Takes a simple topic input and transforms it into a comprehensive research report webpage through a 6-agent pipeline: `Questions Generator` -> `5 Parallel Research Agents` -> `Query Generator` -> `Requirements Writer` -> `Designer` -> `Code Writer`.
*   **Best for:** Learning parallel agent execution, Google search integration, research-driven development, and complex multi-agent orchestration with both sequential and parallel patterns.
*   **➡️ For detailed instructions, see the `README.md` inside the [`version_3_intelligent_research_website_builder/`](./version_3_intelligent_research_website_builder/) directory.**

We will be adding more agents over time to demonstrate other patterns like parallel execution, agents with memory, and more complex tool usage.

---

## 🚀 General Setup Instructions

While each project has its own specific dependencies, the following setup steps are common to all agents in this repository.

### 1. Clone the Repository

```bash
git clone https://github.com/theailanguage/adk_samples.git
```

### 2. Set Up Your API Key

To use the agents, you need a Google API key.

1.  Navigate into the specific project folder you want to run (e.g., `version_2_sequential_website_agent` or `version_3_intelligent_research_website_builder`).
2.  Create a file named `.env` in that directory.
3.  Add your API key to the `.env` file:

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

You can get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### 3. Set Up the Python Environment

Each project should be run in its own virtual environment to manage dependencies.

```bash
# Navigate to the project you want to run
cd path/to/specific_agent_project

# Create and activate a virtual environment using uv
uv venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate.bat

# Install the project's dependencies
uv sync --all-groups
```

---

## 🤖 Running an Agent

After completing the setup for a specific project, you can run its agent(s) using the ADK web interface.

1.  Make sure you are in the project's root directory in your terminal.
2.  Launch the ADK web server:

```bash
# For projects with a flat agent structure (like v1)
cd version_1_website_builder_simple/
adk web ./agents

# For projects with a main.py entrypoint (like v2 and v3)
cd version_2_sequential_website_agent/
adk web ./agents

# For the intelligent research-driven builder (v3)
cd version_3_intelligent_research_website_builder/
adk web ./agents
```

3.  Open your browser and go to `http://localhost:8000`.
4.  Select the desired agent from the dropdown menu and start interacting with it!

---

### **Four Ways to Run Your ADK Agent**

| S.No. | Method & Command | Description | When to Use |
|------:|------------------|-------------|-------------|
| 1 | **ADK Web**  <br>`adk web ./agents` | - Launches a browser-based UI | - Ideal for debugging or quick demos |
| 2 | **ADK API Server** <br>`adk api_server ./agents` | - Starts an HTTP API server | - Useful for REST API-based automation. |
| 3 | **Programmatic Python Script** <br>`uv run python3 -m agent_runner` | - Fully code-driven interaction using Python and the ADK SDK | - Ideal for building your own CLI tools or backend pipelines |
| 4 | **ADK CLI Run** <br>`adk run agents/root_website_builder` | - Command-line way to run a specific agent directly | - Great for quick runs or testing |

---

## 📜 License

This repository and the code within are licensed under the **GNU General Public License v3.0**. See the `LICENSE` file for full details.