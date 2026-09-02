# Saathi

Saathi is a personal desktop helper for Windows that you talk to in Hinglish — a natural mix of Hindi and English, the way people actually speak. Think of it as a friendly assistant that lives on your laptop: you can chat with it, ask it to open things, have it manage files for you, or just ask it questions, and it answers back in text or a spoken voice.

Everything runs on your own laptop. There's no monthly subscription and no company reading your conversations on a server somewhere — the "brain" behind the chat (called Ollama) runs locally, so your chats stay on your machine.

## What it can do today

**Talk with you naturally.** Type or speak, and Saathi replies in casual Hinglish, like a friend would. It automatically switches between a quick-response mode for everyday chat and a slower, more careful mode when you ask for something complicated like writing code.

**Open things for you.** Say "open YouTube," "play some Brazilian funk on Spotify," or "launch Notepad," and it happens immediately — no digging through menus.

**Handle your files.** Ask it to list what's in a folder, read a text file, create a new file or folder, move something, or delete something — all through plain typed instructions instead of digging through File Explorer.

**Run computer commands.** For anyone comfortable with basic technical tasks, you can ask Saathi to run a command on your behalf, and it will show you exactly what it's about to do before running it.

**Look things up for you, for real.** Ask about today's weather somewhere, convert currency, look up a word's meaning, get a quick Wikipedia summary, hear a joke or a quote, get a random piece of advice, check today's top tech headlines, translate a phrase into another language, or find your computer's public IP address — Saathi fetches this from live, free sources on the internet instead of just guessing from memory.

**Remember things for you.** Say "remind me to call mom in 20 minutes" or "remind me to submit the assignment at 6pm," and Saathi will pop up a reminder and read it out loud when the time comes — even if you're not looking at the chat window. Jot down quick thoughts with "note: buy milk tomorrow," and read them all back later with "show notes."

**Tidy up your files automatically.** Say "organize Downloads" and Saathi sorts everything in that folder into tidy subfolders — Images, Documents, Videos, Music, Installers, Archives — after showing you exactly what it's about to do.

**Work with your clipboard and screen.** "Read clipboard" shows you what you last copied; "summarize clipboard" has Saathi read and summarize it for you. "Take a screenshot" saves a snapshot of your screen straight into your Projects folder.

**Stay within reach.** A small chat panel sits pinned to the right edge of your screen at all times, so you don't need to reopen the whole program every time you want to ask something quick. There's also a system tray icon so closing the main window doesn't shut Saathi down — it just steps out of the way.

**Listen and speak.** Saathi can listen through your microphone and reply out loud in a natural-sounding Indian-English voice.

## Keeping you in control

Saathi asks before doing anything that could go wrong. There's one simple switch to let it open apps, websites, and read/create files without asking every single time — handy once you trust it. But a few things always ask you first, no exceptions: deleting or moving a file, and running any command on your computer. You'll always see exactly what it's about to do before it does it. A short list of especially risky actions (like wiping a hard drive) is blocked outright and can't be approved even by accident.

## Where this project is headed

This is very much a living project, and the plan is to keep growing it in stages:

1. **Right now — the foundation.** Chat, voice, memory of past conversations, safe file and app control, and live information lookups. This part is done and working.

2. **Next — a true daily companion.** Teaching Saathi to recognize your voice specifically (a "wake word," so you can just say its name to get its attention instead of clicking a button), and giving it a simple dashboard showing your day at a glance — weather, reminders, and quick shortcuts, all in one glance without needing to ask.

3. **After that — actually getting things done for you.** Letting Saathi handle small recurring chores on its own once you approve them — for example, automatically organizing downloaded files into folders, or reminding you about things at set times, the way a very organized assistant would.

4. **Longer term — reaching your phone too.** Extending Saathi so it can talk to an Android phone connected by cable, letting you, for example, transfer files or trigger simple actions between your phone and laptop without needing a separate app. This will be rolled out carefully, one approved action at a time, rather than opening full access all at once.

5. **Eventually — real personalization.** Saathi remembering more about your habits and preferences over time (with your control over what it keeps), understanding more languages and accents, and connecting to more of the free online tools and information sources out there so it becomes genuinely useful for a wider range of everyday questions, not just the ones it's specifically been taught to answer.

6. **The guiding idea throughout.** Saathi should feel less like software you have to operate, and more like someone helpful you can just talk to — while always being upfront and honest about what it actually did, and never doing anything permanent or risky without your say-so first.

## Getting it running

From the project folder, open Command Prompt and run:

```
py -3.12 -m pip install -r requirements.txt
ollama pull qwen3:14b
ollama pull qwen3:4b-instruct
py -3.12 main.py
```

Or just double-click `Start-Saathi.bat` once everything above is installed.

The first time you use the microphone, Saathi downloads a small free speech-recognition model automatically — no extra sign-up or account needed. Voice recognition works fine on any laptop's regular processor; you don't need a fancy graphics card. Spoken replies do need an internet connection (to generate the voice), but nothing else about the assistant does.
