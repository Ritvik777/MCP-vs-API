# MCP vs API — Building an MCP Server from Scratch

A hands-on technical walkthrough comparing traditional API integration with the **Model Context Protocol (MCP)**. Includes a polished blog post and fully working code you can run yourself.

**[Read the blog post](https://ritvik777.github.io/MCP-vs-API/)**

**Video Tutorial -> (https://www.loom.com/share/36a2f8478321432092c597c7666ac1e7)**

---

## What's Inside

| File | Description |
|------|-------------|
| `index.html` | The full blog post (hosted via GitHub Pages) |
| `server.py` | A working MCP server wrapping the National Weather Service API |
| `client.py` | An MCP client that discovers and calls tools from the server |
| `agent_old_way.py` | The traditional approach — direct API calls, no protocol |

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### 1. Clone the repo

```bash
git clone https://github.com/Ritvik777/MCP-vs-API.git
cd MCP-vs-API
```

### 2. Install dependencies

With uv (recommended):
```bash
uv venv && uv pip install -r requirements.txt
```

With pip:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the examples

**The Old Way** — direct API integration (no MCP):
```bash
python agent_old_way.py
```

**The MCP Way** — client auto-discovers and calls server tools:
```bash
python client.py
```

This starts the MCP server (`server.py`) as a subprocess, connects to it, discovers the available tools, and calls `get_forecast` and `get_alerts`.

### 4. Use in Claude Desktop

Add this to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/absolute/path/to/MCP-vs-API/server.py"]
    }
  }
}
```

Then ask Claude: *"What's the weather in New York?"* — it will discover and use the tools automatically.

---

## Key Concepts

- **API** = a contract for software-to-software communication
- **MCP** = a universal protocol for AI-to-tool communication
- MCP doesn't replace APIs — it gives AI a **standard way to use them**

## Author

**Ritvik Gaur** · January 2026
