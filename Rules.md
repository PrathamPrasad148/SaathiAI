# Saathi AI Engineering and Product Rules

## Safety

1. Never execute destructive or system-impacting actions silently.
2. Always confirm command execution and destructive file operations.
3. Keep protected paths protected, even when routine permissions are enabled.
4. Do not expose private files, tokens, or conversation history to external services.
5. Report what an action did; do not imply success when a tool failed.

## Architecture

6. Keep Tkinter work on the main thread.
7. Use worker threads for network, speech, and long-running operations.
8. Communicate worker results through queues or `root.after`.
9. Prefer existing helpers and constants over duplicate behavior.
10. Keep local persistence backward-compatible and UTF-8 encoded.

## Assistant Behavior

11. Speak in natural Roman-script Hinglish unless the user requests another style.
12. Be honest about capabilities, dependencies, and failures.
13. For website requests, create complete files under `Projects/` and open them when appropriate.
14. Use UI/UX Pro Max and 21st.dev guidance as design input, not as permission to add unrelated dependencies.
15. Do not claim a 21st.dev component was installed unless local source was actually added.

## Generated UI

16. Match the implementation to the actual stack.
17. Do not paste JSX into static HTML projects.
18. Make interactive controls keyboard accessible and visibly focused.
19. Support responsive layouts and reduced motion.
20. Use icons appropriately and do not rely on emoji as the only UI affordance.
21. Include meaningful loading, empty, error, and success states when the workflow needs them.

## Delivery

22. Make the smallest focused change that satisfies the request.
23. Run a syntax, test, or behavior-scoped validation after edits.
24. Update documentation when public behavior or setup changes.
25. Never commit or revert user changes unless explicitly requested.
