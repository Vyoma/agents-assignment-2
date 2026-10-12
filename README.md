# Assignment 2: Google Workspace Assistant + MCP Server

**UCLA Extension - Agentic AI Course**

---

## Overview

| Part | Focus | Points |
|------|-------|--------|
| **Part 1** | Build a Google Workspace agent with ADK | 70 |
| **Part 2** | Connect to GitHub via MCP Server | 30 |

## Project Structure

```
workspace_assistant/
├── agent.py                  # STUDENT: Main agent definition
├── main.py                   # Given: CLI entry point
├── tools/
│   ├── auth.py               # Given: Google OAuth helper
│   ├── calendar_tools.py     # STUDENT (Option A): Calendar tools
│   ├── tasks_tools.py        # STUDENT (Option B): Tasks tools
│   └── mcp_tools.py          # STUDENT: GitHub MCP integration
├── config/
│   ├── settings.py           # Given: Configuration from .env
│   ├── mcp_servers.json      # Given: MCP server config (optional)
│   └── credentials/          # Your OAuth files (gitignored)
├── tests/
│   ├── test_tools.py         # Part 1 verification
│   └── test_mcp.py           # Part 2 verification
└── docs/
    ├── google_auth_setup.md  # Google OAuth setup guide
    ├── github_mcp_setup.md   # GitHub token setup guide
    └── reflection_template.md
```

### Files You Edit

| File | What to implement |
|------|-------------------|
| `tools/calendar_tools.py` | Option A: 3+ calendar tools |
| `tools/tasks_tools.py` | Option B: 3+ tasks tools |
| `agent.py` | System instruction + `LlmAgent` with your tools |
| `tools/mcp_tools.py` | Part 2: GitHub `McpToolset` configuration |

### Files Provided (Do Not Edit)

| File | What it provides |
|------|-----------------|
| `tools/auth.py` | `get_calendar_service()` and `get_tasks_service()` — authenticated Google API clients |
| `config/settings.py` | `Settings` class — loads model name, credentials path, and options from `.env` |
| `main.py` | CLI with `--interactive` mode using `rich` |
| `tests/test_tools.py` | Checks tool count, docstrings, type hints, naming, error handling |
| `tests/test_mcp.py` | Checks GitHub token and `McpToolset` presence in agent |

---

# Part 1: Google Workspace Assistant (70 points)

Build an AI agent using **Agent Development Kit (ADK)**.

**Choose ONE option:**

| Option | Focus |
|--------|-------|
| **A** | Calendar Assistant - Schedule meetings, find free time, manage conflicts |
| **B** | Tasks Manager - Create tasks, track to-dos, manage deadlines |

## Requirements

1. **Minimum 3 tools** with clear names and descriptions
2. **Error handling** with user-friendly messages
3. **System instruction** that guides the agent's behavior

## Provided: Authentication Helpers

The `tools/auth.py` file is **already implemented** and gives you authenticated Google API clients:

```python
from tools.auth import get_calendar_service  # Option A
from tools.auth import get_tasks_service     # Option B

# Use inside your tools:
service = get_calendar_service()  # Returns authorized Calendar API client
service = get_tasks_service()     # Returns authorized Tasks API client
```

First-time use triggers an OAuth browser flow. See [docs/google_auth_setup.md](workspace_assistant/docs/google_auth_setup.md) for setup.

## How to Implement Tools

Define each tool as a plain Python function with a clear docstring and type hints — ADK reads these to build the tool schema and auto-wraps the function when you pass it to the agent. Each tool should call the Google API and return a dict:

```python
from tools.auth import get_calendar_service

def list_upcoming_events(max_results: int = 10) -> dict:
    """List upcoming calendar events.

    Args:
        max_results: Maximum number of events to return.

    Returns:
        dict with 'status' and 'events' keys.
    """
    try:
        service = get_calendar_service()
        events_result = service.events().list(
            calendarId='primary', maxResults=max_results, ...
        ).execute()
        return {"status": "success", "events": events_result.get("items", [])}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

Add your completed tools to the list at the bottom of the file:

```python
calendar_tools = [list_upcoming_events, find_available_slots, create_event]
```

## Option A: Calendar Tools

Implement in **`tools/calendar_tools.py`** using `get_calendar_service()`:

| Tool | Purpose |
|------|---------|
| `list_upcoming_events` | Get events for a date range |
| `find_available_slots` | Find free time between participants |
| `create_event` | Schedule a new meeting |
| `check_conflicts` | Detect scheduling conflicts |
| `reschedule_event` | Move an existing event |

## Option B: Tasks Tools

Implement in **`tools/tasks_tools.py`** using `get_tasks_service()`:

| Tool | Purpose |
|------|---------|
| `list_tasks` | Get tasks from a list |
| `create_task` | Add a new task |
| `complete_task` | Mark a task as done |
| `update_task` | Modify task details |
| `delete_task` | Remove a task |

## Creating Your Agent

In **`agent.py`**, wire your tools into an `LlmAgent`:

```python
from google.adk.agents import LlmAgent
from config.settings import Settings
from tools.calendar_tools import calendar_tools  # or tasks_tools

def create_agent() -> LlmAgent:
    settings = Settings()

    instruction = """You are a Google Workspace assistant that helps users
    manage their calendar. You can list events, find free time, create
    meetings, check for conflicts, and reschedule events. Always confirm
    before making changes..."""

    return LlmAgent(
        name="workspace_assistant",
        model=settings.model_name,
        instruction=instruction,
        tools=calendar_tools,
    )
```

---

# Part 2: GitHub MCP Server (30 points)

Extend your agent to interact with GitHub using **McpToolset**.

## What You Need to Do

1. Create a GitHub Personal Access Token with `repo` scope
2. Configure `McpToolset` to connect to the GitHub MCP server
3. Update your system instruction to include GitHub capabilities

## Key Classes

```python
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
```

## GitHub MCP Server

### Required: Direct Configuration
```python
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={"GITHUB_PERSONAL_ACCESS_TOKEN": token}
)

toolset = McpToolset(
    connection_params=StdioConnectionParams(server_params=server_params)
)
```

### Optional: File-based Configuration
Alternatively, load from `config/mcp_servers.json`:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

Use the provided `load_mcp_config()` helper to load and parse this config.

## Required GitHub Functionality

Your agent should handle:
1. "List my GitHub repositories"
2. "Show open issues in [repo]"
3. "Create an issue in [repo] about [topic]"

---

## Evaluation Rubric

### Part 1: Google Workspace (70 pts)

| Component | Points |
|-----------|--------|
| Tool Design | 18 |
| Agent Instructions | 14 |
| Error Handling | 14 |
| Functionality | 14 |
| Code Quality | 10 |

### Part 2: GitHub MCP (30 pts)

| Component | Points |
|-----------|--------|
| McpToolset Configured | 10 |
| GitHub Queries Work | 15 |
| Error Handling | 5 |

**Bonus (+25):** Tool search: load GitHub tools on demand (B1 to B5 below)

### Bonus: Tool Search Pattern (+25 pts)

**What:** Don't declare every GitHub MCP tool to the model up front (`@modelcontextprotocol/server-github` has 26). Start with a search tool plus at most 2 always-loaded GitHub tools. The agent searches for the tool it needs, then uses it.

**Why:** Every declared tool's name, description and input schema is sent on every model call. Fewer declared tools means a smaller prompt. How much smaller is something you measure (B5).

**Correction (Oct 11):** An earlier version of this section said to configure McpToolset with `defer_loading=True`. Google ADK has no such parameter. Passing it raises `TypeError: McpToolset.__init__() got an unexpected keyword argument 'defer_loading'` (checked on google-adk 1.18.0, the minimum in `requirements.txt`, and 2.11.0, the latest release on Oct 11). `defer_loading` is a field in Anthropic's Messages API, not in ADK. Build the pattern with the ADK pieces below. No points depend on the name `defer_loading`.

**ADK building blocks:**
- **Deferred toolset:** `McpToolset(..., tool_filter=fn)`. `tool_filter` can be a function `fn(tool, readonly_context=None) -> bool`. ADK calls it whenever it lists tools for the model, and `readonly_context.state` is the session state. Return True for your always-loaded tools and for the names your search stored in state. Also return True when `readonly_context` is None: then `await toolset.get_tools()` with no argument returns every tool, which is the catalog your search needs.
- **Search tool:** `search_github_tools(query: str, tool_context: ToolContext) -> dict`. A tool function can take a `tool_context: ToolContext` parameter: ADK fills it in and hides it from the model. Rank the catalog against the query, store the names you found in `tool_context.state`, and return each match's name, description and input schema.
- **Input schema:** `tool.raw_mcp_tool.model_dump(by_alias=True)["inputSchema"]` gives an MCP tool's input schema on both mcp 1.x and 2.x.
- **Same-message use:** ADK 2.x (what `pip install -r requirements.txt` installs today) lists each toolset's tools once per user message, so a tool your filter unlocks mid-message is only declared from the user's next message. ADK 1.x re-lists before every model call. To search for a tool and use it within one user message on 2.x, do one of these:
  - add a proxy tool `call_github_tool(tool_name: str, arguments: dict, tool_context: ToolContext)` that looks the tool up in `await toolset.get_tools()` and runs it with `await tool.run_async(args=arguments, tool_context=tool_context)`, or
  - set `toolset._use_invocation_cache = False` so ADK re-lists before every model call. It is a private ADK attribute that can change between releases, so add a comment, or
  - pin `google-adk` to 1.x in `requirements.txt`.

**Points (+25):**

| # | What is checked | Points |
|---|---|---|
| B1 | Small upfront tool set: the first model request of `create_agent_with_tool_search()` declares only your search helpers (`search_github_tools`, plus `call_github_tool` if you add one) and at most 2 always-loaded GitHub tools. Part 1 tools don't count. | 5 |
| B2 | `search_github_tools`: searches the tool list the MCP server returns (`get_tools()`), not a hand-written list (3). Returns at most 5 matches, best first: "list issues" and "create issue" give `list_issues` and `create_issue` first (2). | 5 |
| B3 | Found tools are usable: a tool returned by search can be run (4), the model has its real input schema when it calls it (2), and search then use completes within one user message on the ADK version your `requirements.txt` installs (2). | 8 |
| B4 | `create_agent_with_tool_search()` in `agent.py`: builds without error (1) and keeps your Part 1 Calendar/Tasks tools (1). | 2 |
| B5 | Measured token comparison in your reflection: both agents measured on the same query, with ADK version and model (3), % reduction computed from your numbers (1), one limit you noticed (1). | 5 |

See `tools/mcp_tools.py` for scaffolding.

#### B5: Measure the token savings (don't estimate)

Run `create_agent()` and `create_agent_with_tool_search()` on the same query and record the prompt tokens Gemini reports. Use either:
- `event.usage_metadata.prompt_token_count` on the events from `runner.run_async(...)`, as in the script below, or
- Gemini's `countTokens` API on the same request.

Estimates, such as characters / 4, don't count. There is no expected value: the numbers depend on your ADK version, model, instruction and query. Earlier versions of this README showed example token numbers that were never measured, so don't reuse them.

```python
# measure_tokens.py: run from workspace_assistant/ with your real .env
import asyncio

import google.adk
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

from agent import create_agent, create_agent_with_tool_search

QUERY = "Show open issues in octocat/Hello-World"  # same query for both agents


async def prompt_tokens(agent) -> list[int]:
    """Prompt tokens of each model call in one user message."""
    runner = InMemoryRunner(agent=agent, app_name="measure")
    session = await runner.session_service.create_session(app_name="measure", user_id="u")
    message = types.Content(role="user", parts=[types.Part(text=QUERY)])
    counts = []
    async for event in runner.run_async(user_id="u", session_id=session.id, new_message=message):
        if event.usage_metadata and event.usage_metadata.prompt_token_count:
            counts.append(event.usage_metadata.prompt_token_count)
    await runner.close()
    return counts


async def main():
    load_dotenv()
    print(f"google-adk {google.adk.__version__}, query: {QUERY!r}")
    for build in (create_agent, create_agent_with_tool_search):
        agent = build()
        counts = await prompt_tokens(agent)
        print(f"{build.__name__} ({agent.model}): first call {counts[0]}, "
              f"whole turn {sum(counts)} over {len(counts)} model calls")


asyncio.run(main())
```

Put the results in the "Bonus: Token Comparison" table in [docs/reflection_template.md](workspace_assistant/docs/reflection_template.md): ADK version, model, query, and first-call and whole-turn prompt tokens for both agents, then the % reduction and one limit you noticed. For example, the search adds a model call, so whole-turn savings are smaller than first-call savings.

---

## Getting Started

### Step 1: Environment Setup

```bash
conda create -n workspace-agent python=3.11 -y
conda activate workspace-agent
pip install -r requirements.txt
cp .env.example .env
```

### Step 2: Google OAuth Setup

Follow [docs/google_auth_setup.md](workspace_assistant/docs/google_auth_setup.md) to:
1. Create a Google Cloud project with Calendar/Tasks API enabled
2. Download OAuth credentials to `config/credentials/credentials.json`
3. The first tool call will open a browser for authorization

### Step 3: Implement Part 1

1. Implement 3+ tools in `tools/calendar_tools.py` or `tools/tasks_tools.py`
2. Create your agent in `agent.py` with system instruction + tools
3. Verify:

```bash
cd workspace_assistant
python -m tests.test_tools
```

4. Test interactively:

```bash
adk web                        # ADK Web UI
# or
python main.py --interactive   # CLI mode
```

### Step 4: Implement Part 2

1. Get a GitHub Personal Access Token (see [docs/github_mcp_setup.md](workspace_assistant/docs/github_mcp_setup.md))
2. Add `GITHUB_PERSONAL_ACCESS_TOKEN=ghp_...` to `.env`
3. Implement `get_github_mcp_toolset()` in `tools/mcp_tools.py`
4. Add the toolset to your agent in `agent.py` and update the system instruction
5. Verify:

```bash
python -m tests.test_mcp
```

---

## Testing with ADK Web UI

ADK provides a built-in web interface for testing your agent interactively.

### Start the Web UI

```bash
cd workspace_assistant
adk web
```

This launches a local web server (typically at `http://localhost:8000`).

### Using the Web UI

1. **Select your agent** from the dropdown (should show your `workspace_assistant`)
2. **Type queries** in the chat interface to test your tools
3. **View tool calls** - the UI shows which tools are invoked and their responses
4. **Debug errors** - see full error messages and stack traces

### Test Queries to Try

**Part 1 - Calendar (Option A):**
- "What meetings do I have tomorrow?"
- "Find a free slot for a 1-hour meeting next week"
- "Schedule a team sync for Monday at 2pm"

**Part 1 - Tasks (Option B):**
- "Show my tasks"
- "Add a task: Review PR by Friday"
- "Mark the first task as complete"

**Part 2 - GitHub MCP:**
- "List my GitHub repositories"
- "Show open issues in octocat/Hello-World"
- "Create an issue in my-repo about fixing the login bug"

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not appearing | Ensure `agent.py` has a valid `create_agent()` function |
| Tools not showing | Check that tools are added to the agent's `tools` list |
| MCP connection failed | Verify `GITHUB_PERSONAL_ACCESS_TOKEN` in `.env` |
| Import errors | Run `pip install -r requirements.txt` |

---

## Submission

This assignment uses **GitHub Classroom**. Your work is submitted by pushing to your repository's `main` branch.

### Steps

1. Test your agent with `adk web` and verify all functionality works
2. Run the verification tests:
   ```bash
   cd workspace_assistant
   python -m tests.test_tools
   python -m tests.test_mcp
   ```
3. Complete `docs/reflection_template.md`
4. Commit and push your changes:
   ```bash
   git add -A
   git commit -m "Submit assignment 2"
   git push origin main
   ```
5. Verify your submission on GitHub — go to your repository page and confirm all files are present

### How Grading Works

- Your submission is graded from the code pushed to `main` in your repository
- You can push multiple times before the deadline; the latest state on `main` at the deadline is what's graded
- Make sure your final code is committed and pushed before the deadline

### Important

- **Do NOT commit sensitive files** — `credentials/`, `token.json`, and `.env` are already in `.gitignore`
- Make sure your code passes the local tests before pushing

---

## Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK MCP Tools](https://google.github.io/adk-docs/tools-custom/mcp-tools/)
- [Google Calendar API](https://developers.google.com/calendar/api)
- [Google Tasks API](https://developers.google.com/tasks)
- [GitHub MCP Server](https://github.com/modelcontextprotocol/servers)
