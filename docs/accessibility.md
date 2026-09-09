# WCAG 2.1 AA Accessibility Guide

CivicResolve Guardian is designed to be accessible to all citizens, including senior citizens and individuals using assistive technologies.

## 1. Compliance Checklist
- **Contrast Ratios**: All text and interactive elements satisfy a minimum 4.5:1 contrast ratio against their background.
- **Keyboard Navigation**: All interactive elements (inputs, select dropdowns, buttons, modals, tabs) are fully reachable via the `Tab` key and activatable via `Enter` or `Space`.
- **Visible Focus Rings**: Active elements feature a high-contrast focus ring (`focus:ring-2 focus:ring-sky-500`).
- **Screen Reader Labels**: Interactive icons and dropdowns include explicit `aria-label` attributes (e.g. `aria-label="Toggle language"`).
- **Semantic HTML**: Proper use of `<header>`, `<main>`, `<nav>`, `<footer>`, `<form>`, `<label>`, and heading hierarchies (`<h1>`, `<h2>`, `<h3>`).
- **Multilingual Font Support**: Natively loads Google Fonts `Outfit` (Latin) and `Noto Sans Tamil` (Tamil script) for crisp readability across mobile and desktop displays.
