# 21st.dev Component Integration Skill

Use 21st.dev as a source of React component patterns, templates, and shadcn-compatible themes when generating web interfaces. The library is source-first: components are copied and adapted into the user's project, not consumed as a runtime service.

## Workflow

1. Detect the target project stack from its files before choosing an implementation.
2. For React, Next.js, or shadcn projects, prefer 21st.dev-style source components with local ownership. Preserve the project's existing Tailwind, utility, and component conventions.
3. For plain HTML/CSS/JavaScript projects, translate the interaction and visual pattern into semantic HTML, CSS, and vanilla JavaScript. Do not paste JSX or install React into a static project.
4. For Tkinter or other native desktop UI, do not import web components. Apply the same design intent only when it fits the native toolkit, keeping keyboard behavior and platform conventions intact.
5. Adapt colors, typography, spacing, motion, responsive behavior, and accessibility to the project's design system. Never blindly copy a demo's branding.
6. Use Lucide or the project's existing icon library for icons. Do not use emoji as interface icons.
7. Keep components self-contained, avoid unnecessary dependencies, and explain any package that must be installed.
8. Validate responsive states, keyboard focus, reduced motion, loading, empty, and error states before finishing.

## 21st.dev Component Selection

Choose components by intent: hero, navigation, AI chat, card/grid, command/search, dashboard, form, modal, or footer. Treat the 21st.dev page as inspiration and source material; the resulting code must be edited into the target repository and match its existing architecture.

## Output Rules

- React/Next.js: produce reusable local components and wire them into the existing route/page.
- HTML projects: produce complete working HTML/CSS/JS with no JSX syntax.
- Existing applications: preserve behavior and public APIs while improving the requested surface.
- When the user asks for a component without naming a specific 21st.dev URL, choose a fitting category and create a complete local version rather than stopping at a recommendation. Good defaults for Saathi projects include animated hero, glowing search, AI chat, message dock, command menu, card grid, dashboard panel, and footer patterns.
- Treat animation as part of the component contract: implement purposeful entrance, hover, focus, loading, and state-transition motion where relevant, with `prefers-reduced-motion` support and no motion that blocks interaction.
- Do not claim a component was installed from 21st.dev unless its source was actually added to the project.
- Prefer one distinctive, coherent visual direction over mixing unrelated demos.
