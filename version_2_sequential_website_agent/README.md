# Sequential Website Builder Agent (v2)

This project demonstrates a multi-agent system using the Agent Development Kit (ADK). It uses a team of specialized, sequentially-invoked agents to build complete HTML+CSS+JS web pages from a single natural language prompt. This approach mimics a real-world development workflow: gathering requirements, creating a design, and then writing the code.

The generated web page is saved to a timestamped `.html` file in the `output/` directory.

---

## 📦 Features

- ✅ **Sequential Multi-Agent Workflow:** A root agent orchestrates a team of specialists:
    1.  `requirements_writer`: Clarifies the user's request.
    2.  `designer`: Plans the visual layout and structure.
    3.  `code_writer`: Generates the final HTML/CSS/JS code.
- ✅ Gemini-powered LLM agents using Google ADK.
- ✅ Takes a high-level natural language query (e.g., “build me a portfolio site”).
- ✅ Generates clean, complete HTML pages with inline CSS/JS.
- ✅ Saves the final output as a timestamped `.html` file.
- ✅ Highly modular and easily extendable.

---

## 📂 Project Structure

```text
version_2_sequential_website_agent/
├── agents/
│   ├── root_website_builder/      # Orchestrator: Manages the agent sequence.
│   │   ├── agent.py
│   │   ├── instructions.txt
│   │   └── description.txt
│   ├── requirements_writer/       # Agent 1: Gathers and defines requirements.
│   │   ├── agent.py
│   │   ├── instructions.txt
│   │   └── description.txt
│   ├── designer/                  # Agent 2: Creates a design plan from requirements.
│   │   ├── agent.py
│   │   ├── instructions.txt
│   │   └── description.txt
│   └── code_writer/               # Agent 3: Writes HTML/CSS/JS from the design plan.
│       ├── agent.py
│       ├── instructions.txt
│       └── description.txt
├── tools/
│   └── file_writer_tool.py        # Tool used by the root agent to save the final code.
├── utils/
│   └── file_loader.py             # Utility for reading prompt files.
├── output/                        # Auto-generated folder with the final HTML output.
│   └── 250618_143021_generated_page.html # Example output file
├── main.py                        # Entry point for the ADK application.
└── pyproject.toml                 # Project dependencies.
```

---

## 🚀 Quickstart

### 1. Clone the Repo

```bash
git clone https://github.com/theailanguage/adk_samples.git
```

### 2. Set Up Python Environment
**Required:** Python 3.11+, uv, VS Code, and Git.

```bash
cd adk_samples/version_2_sequential_website_agent
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate.bat on Windows
uv sync --all-groups
```

### 3. Add Your API Key

Create a `.env` file in the `version_2_sequential_website_agent` project root:

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

You can get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

---

### 4. Run the Agent UI

```bash
cd adk_samples/version_2_sequential_website_agent
adk web ./agents
```

Then open `http://localhost:8000` in your browser. From the agent dropdown list, select **`root_website_builder`**. This is the main entry point that will run the entire sequence.

---

### **Four Ways to Run Your ADK Agent**

| S.No. | Method & Command | Description | When to Use |
|------:|------------------|-------------|-------------|
| 1 | **ADK Web**  <br>`adk web ./agents` | - Launches a browser-based UI | - Ideal for debugging or quick demos |
| 2 | **ADK API Server** <br>`adk api_server ./agents` | - Starts an HTTP API server | - Useful for REST API-based automation. |
| 3 | **Programmatic Python Script** <br>`uv run python3 -m agent_runner` | - Fully code-driven interaction using Python and the ADK SDK | - Ideal for building your own CLI tools or backend pipelines |
| 4 | **ADK CLI Run** <br>`adk run agents/root_website_builder` | - Command-line way to run a specific agent directly | - Great for quick runs or testing |

---

## 💬 Example Prompt

Provide a high-level goal to the `root_website_builder` agent:

```
Create a simple landing page for a new coffee shop called "The Grind". It should have a warm, inviting feel with a brown and cream color palette. Include a large heading, a short paragraph about our fresh beans, and a "Contact Us" button.
```

The agent system will process this and generate a complete `.html` file in the `output/` folder.

---

## 🧠 How It Works

This project demonstrates a sequential "chain-of-thought" process using multiple agents, orchestrated by a root agent.

1.  You submit your prompt to the **`root_website_builder`** agent.
2.  The `root_website_builder` first invokes the **`requirements_writer`** agent, passing it your prompt. This agent refines the request into a structured list of technical and design requirements.
3.  The `root_website_builder` then takes the output from the `requirements_writer` and passes it to the **`designer`** agent. This agent creates a high-level plan for the page's structure, layout, and style.
4.  Next, the `root_website_builder` passes the design plan to the **`code_writer`** agent. This specialist agent generates the final, clean HTML, CSS, and JavaScript code.
5.  Finally, the `root_website_builder` receives the generated code and uses the `write_to_file` tool to save it as a timestamped `.html` file in the `output/` directory.

---

## 🛠️ Extending the Project

The modular, sequential design makes this project easy to extend:

-   **Add a QA Agent:** Insert a `qa_testing_agent` into the sequence after the `code_writer` to validate the generated HTML.
-   **Swap a Specialist:** Replace the `code_writer` with a `react_component_writer` to generate React code instead of plain HTML.
-   **Add New Tools:** Provide agents with new tools, like an image generation tool for the `designer` to create custom assets.

---

## 📜 License

This repository is licensed under the **GNU General Public License v3.0**. See the `LICENSE` file for full details.

---

Happy building with ADK! 🛠