---
name: ui-ux-pro-max
description: "UI/UX Pro Max - Advanced Design System & Frontend Intelligence for Saathi AI. Applied automatically when designing, creating, or refactoring web interfaces, landing pages, and components. Delivers award-winning aesthetic standards, extreme color harmony, 21st.dev interactive components, and smooth hardware-accelerated motion."
---

# UI/UX Pro Max — Design Intelligence & Animation Standard

This skill equips Saathi AI with elite frontend design intelligence, 21st.dev component architecture, and production-grade UI standards. Every interface generated must look like an award-winning digital product.

---

## 1. Extreme Color Theory & Visual Depth

Never settle for default AI templates or flat gray backgrounds. Use layered depth, ambient lighting, and accessible contrast:

### Core Color Systems
- **Tricolor Sovereign (Patriotic / National)**:
  - Saffron: `#FF6F00` | Pure White: `#FFFFFF` | Green: `#00C853` | Ashok Navy: `#0033AA`
  - Background: Obsidian Space `#04040A` | Card Glass: `rgba(18, 18, 30, 0.75)`
- **Cyberpunk 2077 (Gaming / High-Tech)**:
  - Primary: `#FF007F` (Hot Pink) | Secondary: `#00F0FF` (Laser Cyan) | Electric Purple: `#7928CA`
  - Background: Deep Void `#07060F` | Card Glass: `rgba(16, 14, 28, 0.8)`
- **Imperial Gold (Luxury / FinTech / Sovereign)**:
  - 24k Gold: `#D4AF37` | Champagne: `#F3E5AB` | Bronze: `#996515`
  - Background: Midnight Obsidian `#0A090D` | Card Glass: `rgba(22, 20, 26, 0.8)`
- **Emerald Aurora (Wellness / Nature / Bio-Tech)**:
  - Neon Emerald: `#00FFAA` | Sky Cyan: `#00B4D8` | Ultraviolet: `#7000FF`
  - Background: Deep Oceanic `#050C14` | Card Glass: `rgba(10, 20, 30, 0.75)`
- **Electric Nebula (Modern SaaS / AI Startup)**:
  - Electric Indigo: `#6366F1` | Cyber Rose: `#EC4899` | Sky Cyan: `#06B6D4`
  - Background: Nightfall `#05060F` | Card Glass: `rgba(14, 16, 32, 0.75)`

### Depth Hierarchy
1. **Base Layer**: Deep, rich dark-mode background (`#04040A` to `#0A0B16`).
2. **Atmospheric Layer**: Blurred ambient gradient orbs (`filter: blur(140px); opacity: 0.2; pointer-events: none;`) floating smoothly.
3. **Interactive Layer**: Hardware-accelerated HTML5 particle constellation canvas or SVG geometric mesh.
4. **Card Surfaces**: Glassmorphic backdrops (`backdrop-filter: blur(16px); background: rgba(...); border: 1px solid rgba(255,255,255,0.08);`).
5. **Focal Accents**: Shimmering gradient text, glowing badge pills, and animated border highlights.

---

## 2. 21st.dev Component Patterns (Mandatory Architecture)

Every website or frontend component created by Saathi must incorporate signature 21st.dev patterns:

### A. Dynamic Spotlight Mouse-Tracking Cards
Cards must dynamically calculate cursor coordinates `(x, y)` on `mousemove` and render a radial spotlight glow directly underneath the pointer:
```css
.spotlight-card {
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    background: rgba(16, 18, 32, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s, box-shadow 0.3s;
}
.spotlight-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    background: radial-gradient(450px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(var(--accent-rgb), 0.18), transparent 70%);
    opacity: 0;
    transition: opacity 0.4s ease;
    pointer-events: none;
    z-index: 1;
}
.spotlight-card:hover::before { opacity: 1; }
.spotlight-card:hover {
    transform: translateY(-6px);
    border-color: rgba(var(--accent-rgb), 0.5);
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6);
}
```

```javascript
document.querySelectorAll('.spotlight-card').forEach(card => {
    card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        card.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
        card.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
    });
});
```

### B. Browser-Native Web Audio Synthesizer
Never rely on external audio files that could fail to load. Synthesize crisp, futuristic UI audio feedback using standard `AudioContext`:
- **Hover blip**: Sine oscillator sweeping from 480Hz to 720Hz over 50ms.
- **Click sound**: Triangle oscillator from 340Hz to 120Hz over 80ms.
- **Victory Fanfare**: Simultaneous harmonic chord (C5, E5, G5, C6) with gentle exponential decay.
- Provide a visible **Mute/Unmute** toggle in the navigation dock.

### C. Physics Confetti Celebration Canon
Primary call-to-action buttons must trigger a multi-particle physics explosion:
- 70–90 particles with randomized palette colors, velocity, gravity drift, and 3D rotation.
- Automatically cleaned up after 2.5 seconds.

### D. Asymmetric Bento Grid
Organize information with high visual rhythm using a 12-column grid:
- **Hero Card (Span 8)**: Signature feature, large headline, prominent metric counter.
- **Stat Card (Span 4)**: Real-time counter, glowing status pill, concise value proposition.
- **Feature Cards (Span 4 or 6)**: Clear icons, punchy descriptions, interactive hover lift.

### E. Floating Glassmorphic Navigation
- Sticky pill navbar centered with `backdrop-filter: blur(16px)`.
- Brand logo with pulsing status dot.
- Smooth anchor link scrolling with hover blips.

---

## 3. Motion & Animation Principles

All motion must feel purposeful, smooth, and physically grounded:
- **Duration**: 200–350ms for micro-interactions; 500–800ms for page entrances.
- **Easing**: Natural decelerating curve (`cubic-bezier(0.16, 1, 0.3, 1)` or `ease-out`).
- **Scroll Reveals**: Use native `IntersectionObserver` to trigger staggered entrance animations (`data-reveal`).
- **Living Atmosphere**: Subtle continuous background animations (breathing glows, particle motion, text shimmer).
- **Reduced Motion**: Always respect `@media (prefers-reduced-motion: reduce)` by immediately displaying final static states.

---

## 4. Typography & Layout Systems

- **Display Headings**: Use expressive Google Fonts (`Cinzel` for sovereign/luxury, `Plus Jakarta Sans` or `Outfit` for tech/modern) with letter-spacing from -0.5px to 1px.
- **Fluid Typography**: Use `clamp()` for responsive titles (`clamp(2.5rem, 6vw, 4.8rem)`).
- **Body Text**: 15–16px, line-height 1.65, readable muted foreground (`#94A3B8` to `#CBD5E1`).
- **No Broken Assets**: Never use random external image URLs that can result in broken image icons. Use inline SVG shapes, pure CSS illustrations, or Canvas rendering.

---

## 5. Saathi AI Execution Rules

When the user asks Saathi to create or build any website:
1. **Write Complete, Working Code**: Never output placeholders, `// TODO`, or incomplete snippets.
2. **Integrate All God-Level Features**: Extreme color tokens, 21st.dev spotlight cards, particle canvas, web audio sound FX, and confetti.
3. **Save to File**: Always write the complete code to `Projects/<Project_Name>/index.html`.
4. **Launch Automatically**: Immediately open the file in the user's default browser.
5. **Clean Response**: Provide an energetic Hinglish confirmation with feature highlights instead of flooding the chat with raw code.
