# Cuck Code

A naive implementation of Claude Code in under 300 lines of Python.

Core agent loop + 3 file tools (`read_file`, `edit_file`, `list_files`).
Part of the coursework in CS146S: The Modern Software Developer by Stanford.

## Requirements

- Python >= 3.12
- An OpenAI-compatible endpoint. Default: `ROUTER9_API_KEY` against `http://localhost:20128/v1` (9Router).

## Setup

```sh
cp .env.example .env   # set ROUTER9_API_KEY
uv sync                # or: pip install -e .
```

Set your model in `src/app/core/agent.py`:

```python
MODEL = "allmodels"  # write your own model name
```

## Run

```sh
cc                          # installed console script
# or
uv run python src/app/main.py
```

Interactive REPL: type a request, press Enter. Assistant may call tools across up to `MAX_AGENT_STEPS` (10) rounds per turn. Ctrl-C / Ctrl-D exits.

## Tests

```sh
uv run python -m unittest discover -s src/app/tests -t src
```

## Tools

| Tool | Args | Effect |
|------|------|--------|
| `read_file` | `filename` | Return file contents |
| `edit_file` | `path, old_str, new_str` | Replace first `old_str`; empty `old_str` creates the file |
| `list_files` | `path` | List dir entries (name + type) |

All paths resolve under `PROJECT_ROOT` (`cwd`); outside paths are rejected.

## How it works

1. System prompt lists tool signatures.
2. Model replies with `tool: name({"arg": "value"})`, one call per line.
3. Each call runs; results feed back as `tool_result(...)` messages.
4. Loop ends when the model replies with no tool calls, or steps run out.

The model is asked to emit tool calls as plain text lines, parsed with a small regex-free splitter — no provider function-calling required.

## Layout

```text
src/app/
  main.py            # entrypoint
  core/agent.py      # loop, prompt, tools
```

## License

MIT
