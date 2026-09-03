# Saathi AI Product Requirements Document

## 1. Product Summary

Saathi is a Windows desktop assistant that lets people communicate in natural Hinglish through text or voice. It runs the language model locally through Ollama and can answer questions, manage files, launch applications and URLs, create projects, manage notes and reminders, and provide selected live information.

## 2. Problem

Everyday computer actions are scattered across menus, file explorers, browsers, and separate utilities. Users need a conversational interface that is useful without surrendering control of risky operations or sending private conversations to a remote service.

## 3. Goals

- Provide a friendly Hinglish conversational experience.
- Execute useful desktop actions through explicit tools.
- Keep conversation history, notes, and reminders on the local machine.
- Require confirmation for destructive or system-impacting actions.
- Generate complete, functional web projects when requested.
- Keep the assistant accessible through the main window, dock, and system tray.

## 4. Non-Goals

- Cloud-hosted multi-user collaboration.
- Silent unrestricted computer control.
- Guaranteed support for every operating system.
- Bundling the complete 21st.dev source catalog into Saathi.
- Replacing a full IDE or general-purpose automation platform.

## 5. Users

- Windows users who prefer natural-language computer control.
- Developers who want local coding and website generation assistance.
- Users who value local-first storage and visible action confirmation.

## 6. Functional Requirements

1. Users can send text messages and receive model responses.
2. Users can select an Ollama model or use automatic routing.
3. Users can use microphone input and Indian-English speech output when dependencies are available.
4. Saathi can create, read, list, move, delete, and organize files with permission checks.
5. Saathi can launch applications, URLs, and local files.
6. Saathi can run terminal commands only after confirmation.
7. Saathi can retrieve weather, currency, and Wikipedia data.
8. Saathi can save reminders and notes locally.
9. Saathi can read or summarize clipboard content and capture screenshots.
10. Saathi can create local web projects and open generated HTML in the browser.
11. Saathi can adapt 21st.dev-inspired component patterns to the target project stack.

## 7. Safety and Quality Requirements

- Destructive operations require confirmation and protected paths remain blocked.
- Command execution must show the exact command before execution.
- Tool failures must be reported clearly in the conversation.
- UI actions must remain usable when Ollama or optional audio dependencies are unavailable.
- Generated web projects should include responsive layout, keyboard focus, meaningful states, and reduced-motion handling where applicable.

## 8. Success Metrics

- Core app starts successfully on a supported Windows Python environment.
- A user can complete a chat, file, reminder, and website-generation workflow without leaving Saathi.
- Risky actions are never executed silently.
- Local state survives restart without corrupting history or reminders.
- Generated pages work when opened directly in a browser.
