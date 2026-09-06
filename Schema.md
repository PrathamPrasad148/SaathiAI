# Saathi AI — Data Schema & Tool Contract
### Architected by **Pratham Prasad**

```text
================================================================================
                       SAATHI AI DATA SCHEMA DEFINITIONS
                          Architected by Pratham Prasad
================================================================================
```

## 1. Local Storage Schema

All local persistence files are stored under the root `data/` directory using standard UTF-8 encoding.

### A. Conversation History (`data/history.json`)
Stores recent multi-turn conversation dialogues between the user and Saathi.

```json
[
  ["user", "Open Projects folder and check recent builds."],
  ["action", "[FILE] Directory listed: 3 items found."],
  ["assistant", "Main aapke Projects folder ko dekh chuka hoon. 3 items maujood hain."]
]
```
- Supported Roles: `user`, `assistant`, `action`, `system`.
- Retention Policy: Automatically capped to the last 20 messages upon save to ensure lightweight memory overhead and optimal inference token budgets.

### B. Reminders & Task Schedules (`data/reminders.json`)
Stores autonomous scheduled reminders monitored by the background cron loop.

```json
[
  {
    "text": "Review architecture documents with team",
    "when": "2026-09-06T18:00:00",
    "done": false
  }
]
```
- `text` *(string)*: The reminder directive to be spoken and displayed.
- `when` *(string, ISO 8601)*: Local timestamp indicating when the reminder triggers.
- `done` *(boolean)*: Completion flag preventing duplicate alerts.

### C. Persistent Notes Ledger (`data/notes.txt`)
Append-only timestamped notepad for quick user thoughts and directives.

```text
[2026-09-06 10:30] Deploy Saathi AI HUD v2.0 update to GitHub repository
```

---

## 2. Agent Tool Specification Contract

All agent tools exposed to the local Ollama LLM follow the strict JSON schema specification:

```json
{
  "type": "function",
  "function": {
    "name": "<tool_name>",
    "description": "<Clear explanation of utility and constraints>",
    "parameters": {
      "type": "object",
      "properties": {
        "<param_name>": {
          "type": "<string|number|boolean>",
          "description": "<Parameter role>"
        }
      },
      "required": ["<required_param>"]
    }
  }
}
```

### Supported Core Tools:
- `create_file`: Writes source code or text files under allowed directories.
- `read_file`: Reads local file contents with size safety caps.
- `list_directory`: Traverses directories and returns folder structure.
- `open_target`: Launches local folders, files, or external URLs via Windows shell.
- `run_command`: Executes terminal commands with human-in-the-loop approval.
- `get_weather`: Retrieves real-time weather reports for any city.
- `get_currency`: Real-time currency conversions via live exchange endpoints.
- `get_wikipedia`: Fetches concise encyclopedic knowledge summaries.
- `add_reminder`: Schedules an autonomous spoken desktop reminder.
- `add_note`: Appends a timestamped entry to the notes ledger.
- `take_screenshot`: Captures current screen display to active workspace.
