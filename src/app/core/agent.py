import inspect
import json
import os

from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from typing import Any

"""
  This is a naive implementation of claude code in under 200 lines.
  It contains the core agent loop and 3 tool calls for reading, editing and listing files.
  A part of the coursework in CS146S: The Modern Software Developer by Stanford
"""

load_dotenv()

ROUTER9_API_KEY = os.getenv("ROUTER9_API_KEY")
OPENAI_SDK_CLIENT = OpenAI(api_key=ROUTER9_API_KEY)

SYSTEM_PROMPT = ""

USER_COLOR = "\u001b[94m"
AGENT_COLOR = "\u001b[93m"
PRESET_COLOR = "\u001b[0m"


def _resolve_absolute_path(path_str: str) -> Path:
  """
    file.py -> /Users/home/your_name/python/file.py
  """
  path = Path(path_str).expanduser()
  if not path.is_absolute():
    path = (Path.cwd() / path).resolve()
  return path


def _read_file_tool(filename: str) -> dict[str]:
  pass

def _edit_file_tool(path: str, old_str: str, new_str: str) -> dict[str]:
  pass

def _list_files_tool(path: str) -> dict[str]:
  pass

TOOL_REGISTERY = {
  "read_file": _read_file_tool,
  "edit_file": _edit_file_tool,
  "list_files": _list_files_tool
}

def _get_tool_str_representation(tool_name: str) -> str:
  pass


def _get_full_system_prompt():
  pass


def _extract_tool_call_invocations(text: str) -> list[tuple[str, dict[str, Any]]]:
  """
    Return a list of (tool_name, args) requested in 'tool: name({...})' lines.
    The parser expects single-line, compact JSON in parentheses.
  """
  pass


def _execute_llm_call(conversation: list[dict[str, str]]):
  pass


def   run_agent_loop():
  pass