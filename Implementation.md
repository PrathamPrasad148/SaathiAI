# Saathi AI Implementation Guide

## Local Setup

```powershell
py -3.12 -m pip install -r requirements.txt
ollama pull qwen2.5:7b
ollama pull qwen3:14b
ollama pull qwen3:4b-instruct
py -3.12 main.py
```

Alternatively run `Start-Saathi.bat` after dependencies and Ollama are installed.

## Adding a New Desktop Tool

1. Add the function schema to `TOOLS_SCHEMA`.
2. Add the execution branch in `execute_tool`.
3. Decide whether the action needs `confirm_action` or protected-path checks.
4. Add a direct shortcut only when the intent is unambiguous and safe.
5. Return useful success and error strings.
6. Add status/action reporting if the operation is slow.
7. Update `README.md`, `progress.txt`, and `Schema.md` when behavior is user-visible.

## Adding a Web Component Pattern

1. Identify the product goal and target stack.
2. Use UI/UX Pro Max for design-system and UX guidance.
3. Use the 21st.dev skill for component category and interaction patterns.
4. Create local source files in the requested project.
5. For static projects, use HTML/CSS/vanilla JavaScript; do not emit JSX.
6. For React projects, use local reusable components and existing project utilities.
7. Implement responsive, focus, loading, empty, error, and reduced-motion states.
8. Open or preview the result and verify the primary interaction.

## Testing Strategy

- Syntax check: `python -m py_compile main.py`.
- Prompt loading check: import/execute only the module setup with a supplied `__file__`; do not start Tkinter in headless validation.
- Manual smoke test: launch the app, check Ollama status, send a message, create a note, set a reminder, and test one safe file operation.
- Website smoke test: create a project, open its HTML, resize the browser, and test keyboard focus and primary controls.

## Change Discipline

Keep UI changes in `build_ui`, `configure_theme`, or the relevant UI helper. Keep model protocol changes near `TOOLS_SCHEMA` and `_reply_worker`. Avoid blocking network or audio work on the Tkinter thread.
