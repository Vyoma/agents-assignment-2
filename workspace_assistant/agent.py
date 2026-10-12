"""
Google Workspace Assistant - Main Agent Definition

Part 1: Implement tools and system instruction for Calendar OR Tasks
Part 2: Add McpToolset for GitHub integration
"""

import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from config.settings import Settings

# TODO: Import your chosen tool set
# from tools.calendar_tools import calendar_tools
# from tools.tasks_tools import tasks_tools

# TODO Part 2: Import MCP tools
# from tools.mcp_tools import mcp_tools


def create_agent() -> LlmAgent:
    """Create the Workspace Assistant agent."""
    settings = Settings()

    # TODO Part 1: Write your system instruction

    # TODO Part 2: Create McpToolset for GitHub

    # TODO: Create and return your LlmAgent
    raise NotImplementedError("Implement create_agent")


def create_agent_with_tool_search() -> LlmAgent:
    """BONUS: Create the agent with GitHub tool search instead of all GitHub tools.

    Keep your Part 1 tools. Add search_github_tools and the deferred GitHub toolset
    from tools/mcp_tools.py (plus call_github_tool if you use one), so the first model
    call declares only the search helpers and at most 2 GitHub tools. See the README
    section "Bonus: Tool Search Pattern".
    """
    raise NotImplementedError("Bonus: Implement tool search pattern")
