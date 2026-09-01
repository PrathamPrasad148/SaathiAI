# Saathi

Saathi is a Windows-first, local Hinglish desktop assistant. It uses Ollama, so ordinary chat and coding help do not need a paid API key.

## Safety model

Saathi has **one permission toggle** that covers opening/launching anything, listing/reading/creating files and folders, and fetching live data — websites, apps, YouTube, Spotify, whatever you name. Grant it once per session and Saathi stops asking for every routine action.

**Always asks separately, no matter what:** deleting a file/folder, moving/renaming, and running any terminal command. Each shows the exact path or command in a confirmation dialog before it runs. A small hard-coded blocklist (`format`, `diskpart`, recursive root deletes, fork bombs) is refused outright — no dialog can override it — and writes/deletes are refused inside Windows/Program Files/ProgramData regardless of permission, so a bad guess can't take down the OS. USB/Android device control is intentionally still out of scope.

## What is ready now

- Hinglish text chat with automatic model routing: fast `qwen3:4b` for everyday talk and `qwen3:14b` for coding or complex tasks (both model names are editable in the Chat tab)
- Startup check that tells you immediately if Ollama isn't running or a model isn't pulled
- **Open or launch anything with one permission**: "open youtube", "play spotify", "launch notepad", "play Brazilian funk on Spotify" (opens a real search for it), "play it on this website" (remembers the last site opened) — all handled instantly without routing through the LLM
- **Files, folders & commands, straight from chat**: "list files in Downloads", "read file notes.txt", "create file report.txt with content: ...", "create folder Projects2", "delete old.pdf" (asks first, goes to Recycle Bin), "move a.txt to b.txt", "run: dir" — same controls are also in the Safe Actions tab
- **Live data from free APIs**, not the model's memory: "weather in Kolkata", "100 USD to INR", "define serendipity", "who is Alan Turing" (Wikipedia), "tell me a joke", "trivia", "quote", "info about country Japan" — easy to extend by adding an entry to `API_ENDPOINTS` and a pattern to `DATA_COMMAND_PATTERNS` in `main.py`
- **Always available**: closing the window minimizes to a system tray icon instead of quitting (needs `pystray`/`pillow`; falls back to a normal close if not installed) — "Show Saathi" from the tray any time. "Always on top" checkbox for quick access while working.
- Optional local microphone transcription (recording length + model size adjustable) and speech output, tuned to a calmer, natural speaking pace
- Copy last reply to clipboard, or regenerate it with one click
- Persistent local chat history

## Run it

From this folder in PowerShell:

```powershell
py -3.12 -m pip install -r requirements.txt
ollama pull qwen3:14b
ollama pull qwen3:4b-instruct
py -3.12 main.py
```

The first microphone use downloads the free `small` multilingual speech-recognition model for better Hinglish accuracy. No Hugging Face token is required.

Voice recognition runs locally on the CPU, so it does not need NVIDIA CUDA. Spoken replies use Microsoft's `en-IN-NeerjaNeural` Indian English neural voice; this part needs an internet connection but does not need an API key.

## Project phases

1. **Core assistant:** chat, voice, history, safety approvals — complete.
2. **Laptop assistance:** trusted apps, file search, browser search — complete starter.
3. **Coding workspace:** project generator, coding prompts, test/run approval workflow — starter ready.
4. **Android/USB:** install Android Platform Tools, validate the connected device, then add only approved ADB/serial commands.
5. **Personalization:** wake word, long-term memory, dashboard, scheduled automations.

## Android/USB phase (do this later)

Install Android Platform Tools from the official Android developer site, enable USB debugging, connect a data cable, and approve the RSA prompt on the phone. We will then add a device-status screen before enabling any command.
