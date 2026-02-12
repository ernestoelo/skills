#!/usr/bin/env python3
"""
Auto Skill Loader MCP Server.

This MCP server provides automatic loading of skills based on conversation context.
It analyzes messages and loads relevant skill instructions to enhance OpenCode conversations.
"""

import json
from typing import Optional, List
from pathlib import Path
from enum import Enum
import re
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("auto_skill_loader_mcp")

# Constants
SKILLS_DIR = Path.home() / ".config" / "opencode" / "skills"


# Enums
class ResponseFormat(str, Enum):
    """Output format for responses."""

    TEXT = "text"
    JSON = "json"


# Pydantic Models
class AnalyzeMessageInput(BaseModel):
    """Input model for message analysis."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    message: str = Field(
        ..., description="The message to analyze for skill activation", min_length=1
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.TEXT, description="Output format"
    )


class LoadSkillInput(BaseModel):
    """Input model for loading specific skills."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    skill_name: str = Field(..., description="Name of the skill to load", min_length=1)
    response_format: ResponseFormat = Field(
        default=ResponseFormat.TEXT, description="Output format"
    )


# Skill definitions with activation patterns
SKILL_PATTERNS = {
    "architect": {
        "patterns": [
            r"(scaffold|create|build).*skill",
            r"skill.*(structure|template)",
            r"(architect|design).*skill",
            r"new.*skill",
            r"skill.*framework",
        ],
        "description": "Scaffolding skills and agents for AI platforms",
    },
    "dev-workflow": {
        "patterns": [
            r"(commit|push|pull|merge)",
            r"git.*(workflow|process)",
            r"development.*workflow",
            r"ci.*cd",
            r"version.*control",
        ],
        "description": "Development workflows and best practices",
    },
    "pdf": {
        "patterns": [
            r"pdf.*(process|extract|convert)",
            r"(read|parse).*pdf",
            r"document.*processing",
            r"pdf.*text",
            r"file.*pdf",
        ],
        "description": "PDF processing and text extraction",
    },
    "web-scraper": {
        "patterns": [
            r"(scrape|extract).*web",
            r"web.*(scraper|crawler)",
            r"(fetch|get).*url",
            r"html.*markdown",
            r"website.*content",
        ],
        "description": "Web scraping and content extraction",
    },
    "sys-env": {
        "patterns": [
            r"system.*(environment|config)",
            r"arch.*linux",
            r"hyprland",
            r"wayland",
            r"package.*manager",
        ],
        "description": "Arch Linux system environment management",
    },
    "code-review": {
        "patterns": [
            r"code.*review",
            r"review.*code",
            r"(bug|error).*fix",
            r"security.*vulnerability",
            r"code.*quality",
            r"lint.*check",
            r"revisar.*código",  # Spanish: review code
        ],
        "description": "Code analysis and quality assurance",
    },
    "recursive-context": {
        "patterns": [
            r"recursive.*context",
            r"unlimited.*context",
            r"rlm.*model",
            r"context.*processing",
            r"iterative.*processing",
        ],
        "description": "Recursive context processing for unlimited input handling",
    },
    "mcp-builder": {
        "patterns": [
            r"mcp.*server",
            r"server.*mcp",
            r"model.*context.*protocol",
            r"external.*service",
            r"api.*integration",
            r"mcp.*tool",
            r"construir.*servidor.*mcp",  # Spanish: build MCP server
        ],
        "description": "Building MCP servers for external service integration",
    },
    "orchestrator": {
        "patterns": [
            r"orchestrate.*workflow",
            r"pipeline.*skills",
            r"multi.*skill.*task",
            r"interconnect.*skills",
            r"state.*machine",
        ],
        "description": "Universal master skill for orchestrating workflows and pipelines",
    },
}


def load_skill_content(skill_name: str) -> Optional[str]:
    """Load the content of a specific skill."""
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    if skill_path.exists():
        try:
            with open(skill_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error loading skill {skill_name}: {str(e)}"
    return None


def analyze_message_for_skills(message: str) -> List[str]:
    """Analyze a message and return relevant skill names."""
    relevant_skills = []
    message_lower = message.lower()

    for skill_name, skill_info in SKILL_PATTERNS.items():
        for pattern in skill_info["patterns"]:
            if re.search(pattern, message_lower, re.IGNORECASE):
                if skill_name not in relevant_skills:
                    relevant_skills.append(skill_name)
                break  # Found a match, no need to check other patterns

    return relevant_skills


def format_skill_response(
    skill_name: str, content: str, format_type: ResponseFormat
) -> str:
    """Format skill content for response."""
    if format_type == ResponseFormat.JSON:
        return json.dumps(
            {
                "skill_name": skill_name,
                "content": content,
                "description": SKILL_PATTERNS.get(skill_name, {}).get(
                    "description", ""
                ),
            },
            indent=2,
        )

    # Text format
    return f"""# {skill_name.upper()} SKILL LOADED

{content}
"""


# Tool definitions
@mcp.tool(
    name="analyze_message_for_skills",
    annotations={
        "title": "Analyze Message for Skill Activation",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def analyze_message_for_skills_tool(params: AnalyzeMessageInput) -> str:
    """Analyze a message to determine which skills should be activated.

    This tool examines the content of a message and identifies relevant skills
    that should be loaded based on keywords and context patterns.

    Args:
        params (AnalyzeMessageInput): Input containing the message to analyze

    Returns:
        str: List of relevant skills or detailed analysis
    """
    relevant_skills = analyze_message_for_skills(params.message)

    if not relevant_skills:
        if params.response_format == ResponseFormat.JSON:
            return json.dumps(
                {
                    "relevant_skills": [],
                    "message": "No skills matched the message content",
                }
            )
        return "No skills matched the message content. Available skills include: architect, dev-workflow, pdf, web-scraper, sys-env, code-review, recursive-context, mcp-builder"

    if params.response_format == ResponseFormat.JSON:
        skills_info = []
        for skill in relevant_skills:
            skills_info.append(
                {
                    "name": skill,
                    "description": SKILL_PATTERNS.get(skill, {}).get("description", ""),
                    "matched_patterns": SKILL_PATTERNS.get(skill, {}).get(
                        "patterns", []
                    ),
                }
            )
        return json.dumps(
            {"relevant_skills": skills_info, "count": len(relevant_skills)}, indent=2
        )

    # Text format
    response = f"Found {len(relevant_skills)} relevant skill(s) for the message:\n\n"
    for skill in relevant_skills:
        description = SKILL_PATTERNS.get(skill, {}).get("description", "")
        response += f"- **{skill}**: {description}\n"
    response += "\nUse load_skill tool to load the full skill content."
    return response


@mcp.tool(
    name="load_skill",
    annotations={
        "title": "Load Specific Skill Content",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def load_skill_tool(params: LoadSkillInput) -> str:
    """Load the full content of a specific skill.

    This tool retrieves the complete SKILL.md content for a given skill name,
    allowing the AI to access all instructions and workflows.

    Args:
        params (LoadSkillInput): Input containing the skill name to load

    Returns:
        str: Full skill content or error message
    """
    content = load_skill_content(params.skill_name)

    if content is None:
        available_skills = list(SKILL_PATTERNS.keys())
        if params.response_format == ResponseFormat.JSON:
            return json.dumps(
                {
                    "error": f"Skill '{params.skill_name}' not found",
                    "available_skills": available_skills,
                },
                indent=2,
            )
        return f"Skill '{params.skill_name}' not found. Available skills: {', '.join(available_skills)}"

    return format_skill_response(params.skill_name, content, params.response_format)


@mcp.tool(
    name="load_relevant_skills",
    annotations={
        "title": "Load Relevant Skills for Message",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def load_relevant_skills_tool(params: AnalyzeMessageInput) -> str:
    """Analyze a message and load all relevant skills automatically.

    This tool combines message analysis with skill loading to provide
    automatic skill activation based on conversation context.

    Args:
        params (AnalyzeMessageInput): Input containing the message to analyze

    Returns:
        str: Combined content of all relevant skills
    """
    relevant_skills = analyze_message_for_skills(params.message)

    if not relevant_skills:
        if params.response_format == ResponseFormat.JSON:
            return json.dumps(
                {
                    "message": "No skills matched the message content",
                    "loaded_skills": [],
                }
            )
        return "No skills matched the message content."

    loaded_skills = []
    combined_content = ""

    for skill_name in relevant_skills:
        content = load_skill_content(skill_name)
        if content:
            loaded_skills.append(skill_name)
            if params.response_format == ResponseFormat.JSON:
                combined_content += (
                    format_skill_response(skill_name, content, ResponseFormat.JSON)
                    + "\n"
                )
            else:
                combined_content += (
                    format_skill_response(skill_name, content, ResponseFormat.TEXT)
                    + "\n\n---\n\n"
                )

    if params.response_format == ResponseFormat.JSON:
        return json.dumps(
            {
                "loaded_skills": loaded_skills,
                "count": len(loaded_skills),
                "content": combined_content.strip(),
            },
            indent=2,
        )

    header = f"Loaded {len(loaded_skills)} skill(s): {', '.join(loaded_skills)}\n\n"
    return header + combined_content.strip()


@mcp.tool(
    name="list_available_skills",
    annotations={
        "title": "List All Available Skills",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def list_available_skills() -> str:
    """List all available skills with their descriptions.

    This tool provides an overview of all skills that can be loaded,
    including their purpose and activation patterns.

    Returns:
        str: Formatted list of all available skills
    """
    response = "# Available Skills\n\n"
    for skill_name, skill_info in SKILL_PATTERNS.items():
        response += f"## {skill_name}\n"
        response += f"**Description**: {skill_info['description']}\n"
        response += f"**Activation Patterns**: {', '.join(skill_info['patterns'])}\n\n"

    return response


if __name__ == "__main__":
    mcp.run()
