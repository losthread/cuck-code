import tempfile
import unittest
from pathlib import Path

from app.core.agent import (
    PROJECT_ROOT,
    _edit_file_tool,
    _extract_tool_call_invocations,
    _list_files_tool,
    _read_file_tool,
    _resolve_absolute_path,
)


class ToolCallParserTest(unittest.TestCase):
    def test_single_call(self):
        self.assertEqual(
            _extract_tool_call_invocations('tool: read_file({"filename": "a.py"})'),
            [("read_file", {"filename": "a.py"})],
        )

    def test_multiple_calls_and_noise(self):
        text = "\n".join([
            "sure, doing that now",
            'tool: read_file({"filename": "a.py"})',
            "```",
            'tool: list_files({"path": "."})',
        ])
        self.assertEqual(
            _extract_tool_call_invocations(text),
            [("read_file", {"filename": "a.py"}), ("list_files", {"path": "."})],
        )

    def test_malformed_ignored(self):
        for bad in [
            "tool: read_file",              # no parens / json
            "tool: read_file({",            # unterminated
            'tool: read_file("a.py")',      # args not a dict
            'tool:read_file({"a":1})',      # missing space after colon
        ]:
            self.assertEqual(_extract_tool_call_invocations(bad), [], bad)


class PathGuardTest(unittest.TestCase):
    def test_rejects_outside_project(self):
        with self.assertRaises(ValueError):
            _resolve_absolute_path("/etc/hosts")


class FileToolTest(unittest.TestCase):
    def test_create_read_edit_list(self):
        with tempfile.TemporaryDirectory(dir=PROJECT_ROOT) as d:
            rel = str(Path(d).relative_to(PROJECT_ROOT) / "n.txt")

            self.assertEqual(_edit_file_tool(rel, "", "hello"), {"path": str(Path(d) / "n.txt"), "action": "created_file"})
            self.assertEqual(_read_file_tool(rel)["content"], "hello")

            self.assertEqual(_edit_file_tool(rel, "hello", "hi")["action"], "edited")
            self.assertEqual(_read_file_tool(rel)["content"], "hi")

            self.assertEqual(_edit_file_tool(rel, "zzz", "x")["action"], "old_str not found")
            self.assertEqual(_read_file_tool(rel)["content"], "hi")

            names = {f["filename"] for f in _list_files_tool(rel.rsplit("/", 1)[0])["files"]}
            self.assertIn("n.txt", names)


if __name__ == "__main__":
    unittest.main()
