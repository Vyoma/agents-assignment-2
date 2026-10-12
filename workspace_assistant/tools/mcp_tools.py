"""
Part 2: GitHub MCP Integration

Configure McpToolset to connect to the GitHub MCP server.

Required: Direct configuration in Python code
Optional: File-based configuration from config/mcp_servers.json
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()

# Path to MCP server configuration (for Option B)
MCP_CONFIG_PATH = Path(__file__).parent.parent / "config" / "mcp_servers.json"


# =============================================================================
# REQUIRED: Direct Configuration
# =============================================================================
# TODO: Implement get_github_mcp_toolset()
# Configure the GitHub MCP server directly in Python code.
#
# Example structure:
#
# def get_github_mcp_toolset() -> McpToolset:
#     token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
#     if not token:
#         raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN not set in .env")
#
#     server_params = StdioServerParameters(
#         command="npx",
#         args=["-y", "@modelcontextprotocol/server-github"],
#         env={"GITHUB_PERSONAL_ACCESS_TOKEN": token}
#     )
#
#     return McpToolset(
#         connection_params=StdioConnectionParams(server_params=server_params)
#     )


# =============================================================================
# OPTIONAL: File-based Configuration
# =============================================================================
def load_mcp_config() -> dict:
    """Load MCP server configuration from JSON file."""
    if not MCP_CONFIG_PATH.exists():
        raise FileNotFoundError(f"MCP config not found: {MCP_CONFIG_PATH}")

    with open(MCP_CONFIG_PATH) as f:
        config = json.load(f)

    # Replace environment variable placeholders
    github_config = config.get("mcpServers", {}).get("github", {})
    env = github_config.get("env", {})
    for key, value in env.items():
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            env[key] = os.getenv(env_var, "")

    return config


# TODO: Implement get_github_mcp_toolset_from_config()
# Load configuration from config/mcp_servers.json
#
# Example structure:
#
# def get_github_mcp_toolset_from_config() -> McpToolset:
#     config = load_mcp_config()
#     github = config["mcpServers"]["github"]
#
#     token = github["env"].get("GITHUB_PERSONAL_ACCESS_TOKEN")
#     if not token:
#         raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN not set in .env")
#
#     server_params = StdioServerParameters(
#         command=github["command"],
#         args=github["args"],
#         env=github["env"]
#     )
#
#     return McpToolset(
#         connection_params=StdioConnectionParams(server_params=server_params)
#     )


# =============================================================================
# BONUS (+25 points) - Tool Search Pattern
# =============================================================================
# Goal: don't declare all 26 GitHub MCP tools up front. Start with a search tool
# plus at most 2 always-loaded GitHub tools, search for the tool you need, use it.
#
# Note: McpToolset has no defer_loading parameter. That name comes from
# Anthropic's Messages API, and passing it to McpToolset raises TypeError.
# Build the pattern with tool_filter + session state (see README).
#
# Points (README "Bonus: Tool Search Pattern", B1 to B5):
# - B1 (5): first model call declares only your search helper(s) and at most
#   2 always-loaded GitHub tools (Part 1 tools don't count)
# - B2 (5): search_github_tools searches get_tools() (3), ranked, max 5 results (2)
# - B3 (8): a found tool can be run (4), with its real input schema (2), within
#   the same user message (2)
# - B4 (2): create_agent_with_tool_search() builds (1) and keeps Part 1 tools (1)
# - B5 (5): measured token comparison in your reflection
#
# Steps:
# 1. get_github_mcp_toolset_deferred(): McpToolset with tool_filter=<function>.
#    ADK calls it as fn(tool, readonly_context) whenever it lists tools for the
#    model. Return True only for your always-loaded tools and for names your search
#    stored in readonly_context.state. With no context, return True, so that
#    toolset.get_tools() (no argument) gives your search the full catalog.
#    Create the toolset once so search and the agent share one server process.
# 2. search_github_tools(query, tool_context): rank the full catalog by keyword,
#    store the best matches' names in tool_context.state, and return each match's
#    name, description and input schema
#    (tool.raw_mcp_tool.model_dump(by_alias=True)["inputSchema"]).
# 3. ADK 2.x lists a toolset's tools once per user message, so a tool unlocked
#    mid-message is only declared from the next message. To use it in the same
#    message, either add call_github_tool(tool_name, arguments, tool_context) that
#    runs it with McpTool.run_async(args=arguments, tool_context=tool_context), or
#    set toolset._use_invocation_cache = False (private ADK attribute: comment it).
#
# REQUIRED (B5): measure, don't estimate. Run create_agent() and
# create_agent_with_tool_search() on the same query and record the prompt tokens
# Gemini reports (event.usage_metadata.prompt_token_count, or Gemini countTokens).
# The README has a measurement script. Fill in the "Bonus: Token Comparison" table
# in docs/reflection_template.md, with your ADK version and model.
# There is no expected value.
#
# Example structure:
#
# import functools
# from google.adk.tools import ToolContext
#
# UNLOCKED = "unlocked_github_tools"  # session-state key
# ALWAYS_LOADED = {"search_repositories"}  # at most 2
#
#
# def _is_unlocked(tool, readonly_context=None) -> bool:
#     if readonly_context is None:  # no context: full catalog, used by search
#         return True
#     # TODO: True for ALWAYS_LOADED and for names in readonly_context.state.get(UNLOCKED, [])
#
#
# async def search_github_tools(query: str, tool_context: ToolContext) -> dict:
#     """Search for available GitHub tools by keyword.
#
#     Args:
#         query: Search term (e.g., "list issues", "create issue", "pull request")
#
#     Returns:
#         dict with matching tool names, descriptions and input schemas
#     """
#     # TODO: catalog = await get_github_mcp_toolset_deferred().get_tools()
#     # TODO: rank by keyword, store the top matches in tool_context.state[UNLOCKED]
#     pass
#
#
# @functools.cache  # create it once: search and the agent share one npx process
# def get_github_mcp_toolset_deferred() -> McpToolset:
#     """GitHub toolset that declares only always-loaded and searched-for tools."""
#     # TODO: build server_params as in get_github_mcp_toolset(), then return
#     #   McpToolset(connection_params=..., tool_filter=_is_unlocked)
#     pass


mcp_tools = [
    # Add your McpToolset here after implementing one of the options above
    # Example: get_github_mcp_toolset()
    # Example: get_github_mcp_toolset_from_config()
]
