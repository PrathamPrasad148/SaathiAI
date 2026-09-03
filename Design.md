# Saathi AI Design Specification

## Design Direction

Saathi uses a compact, high-contrast dark desktop interface with a neon mint action color and cool blue tool status. The visual language should feel technical and focused, while Hinglish copy keeps the product approachable.

## Tokens

- Background: `#0a0a0f`
- Header: `#0f0f14`
- Panel: `#12121f`
- Border: `#2a2a3a`
- Primary action: `#00cc6a`
- Primary highlight: `#00ff88`
- Text: `#e8e8f0`
- Muted text: `#8a8aa0`
- Tool status: `#38bdf8`
- Warning: `#ffaa00`
- Error: `#ff5555`

## Main Layout

- Header: product name, model selector, Ollama status.
- Notebook: Chat & Agent, Projects & Tools, Settings.
- Chat: scrollable transcript above a persistent input/action row.
- Dock: compact bottom utility with show/hide controls.

## Interaction Rules

- Primary actions use the mint accent.
- Status and tool activity use blue or amber, never color alone.
- Focus should be visible on inputs, buttons, tabs, and selectors.
- Long messages wrap; controls must not resize unpredictably.
- Destructive actions need clear confirmation wording.
- Animation is subtle in the native desktop shell; generated web projects may use richer motion.

## Web Generation Rules

For generated websites, Saathi should create a coherent design system rather than mix unrelated demos. 21st.dev patterns may inspire heroes, cards, AI chat, navigation, search, dashboards, and message docks. Use semantic HTML or local React components according to the target stack. Include responsive breakpoints, hover/focus states, empty/loading/error states where relevant, and `prefers-reduced-motion` support.

## Accessibility

Use readable contrast, keyboard-operable controls, descriptive labels, logical focus order, and text alternatives for meaningful visuals. Never use emoji as the only icon or state indicator in generated production UI.
