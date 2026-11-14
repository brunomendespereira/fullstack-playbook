# Interface

Rules for anything a user sees, reads or touches. The product's look (brand, tokens, named rules) lives in its `DESIGN.md`; this file says how any interface should behave. Read `DESIGN.md` before designing.

## Structure

- **One goal and one primary action per screen;** reveal the rest progressively. Never make users carry information from one screen to the next in their memory.
- **Squint test:** blur your eyes; the most important thing should still stand out. Group by proximity before adding containers; give more space above a heading than below it.
- **A text column of 45 to 75 characters** for reading.
- **Use the platform's own controls** for navigation and input. A modal is not the first option; an overlay escapes its container and locks the scroll behind it.
- **Refine or redesign, consciously:** refining keeps identity, copy and behavior; redesigning replaces them. Never polish a direction that was already discarded. Add no new primitive to the design system without asking.

Sources: Nielsen Norman Group (usability heuristics, progressive disclosure); Gestalt principles; Bringhurst, *The Elements of Typographic Style* (measure).

## Design system

- **Only tokens** for color, type, spacing, radius, elevation and motion; a raw value needs a comment saying why. A test compares the tokens in code with `DESIGN.md`, including type and spacing, not only colors.
- **A modular type scale** (a fixed ratio between sizes) and a spacing scale on a 4 or 8 point grid. The exact scale is the product's.
- **Color by role** (surface, text, action, focus, border, semantic, data), not a loose palette. A dark theme is composed for dark, not inverted from light.
- **Document the system from what was built,** not from what was planned, and never turn a defect into a rule.

Sources: W3C Design Tokens Community Group format; Material Design (type scale, layout grid).

## States

- **Every screen has four states:** loading (a skeleton), failed with no data (an error and "try again", navigation still visible), failed to refresh (keep the data, show one notice), refreshing. An error never becomes an empty list. Several data sources on one screen merge into one notice.
- **No connection** is one global notice; a server failure is a notice on the screen.
- **Five kinds of empty state,** each with a next step: first use, cleared by the user, no results, no permission, error.
- **Every component has its states:** default, hover, focus, active, disabled, loading, error, empty.
- **Block repeated taps** on an action that creates something while it is sending.
- **Celebrate in proportion** to how often and how much it matters; never fake progress.

## Accessibility

- Contrast at least 4.5:1 for text and 3:1 for controls, icons and focus indicators.
- Touch targets at least 24 by 24 CSS pixels (the platforms recommend 44 points and 48 dp).
- Color is never the only signal; focus is always visible and follows the visual order; the system's text size and zoom are respected.
- Reduced motion removes movement and keeps the feedback.

Sources: WCAG 2.2 AA (1.4.3, 1.4.11, 2.5.8, 1.4.1, 2.4.7, 2.4.3, 1.4.4, 2.3.3); Apple Human Interface Guidelines; Material Design.

## Motion

Motion only with a job: feedback, a change of state, continuity, or attention. Exits are faster than entrances. No bounce by reflex. Content is visible even if the script fails. Durations are a product value.

## Responsive and platforms

- **Adapt by rethinking, not by shrinking.** Detect the kind of input (touch or pointer), not only the width. Hover never carries a function. Respect safe areas and the on-screen keyboard. Keep the same information architecture everywhere.
- **Native apps:** follow each platform's patterns and translate between them instead of transplanting; the system back action always works; draw edge to edge and respect the system insets, including the keyboard; snackbars for transient messages, dialogs only for decisions; test with large system fonts and in dark mode; never lock orientation to dodge a bug.
- **A device feature** (camera, files, location, notifications) has a main path, a fallback, and a log of each failure; on two platforms, both change in the same pull request.

Sources: Apple Human Interface Guidelines; Material Design.

## Languages

Format dates, numbers and currencies with the platform's locale tools; plurals by language rules; whole messages, never concatenated fragments; layouts with room for longer translations; keys typed and tested so every language has the same keys; notifications carry a type and data, and the text comes from the reader's language.

## Details that break products

- **Edge cases:** long and empty text, emoji, very large numbers, more than a thousand items, every error status (401, 403, 404, 429), listeners and timers cleaned up when a screen closes, one broken component not taking the screen down.
- **Theme and language applied before the first paint,** so the screen does not flash.
- **Screen state that matters lives in the address** (filters, open panel), so reload and back work.
- **A clickable card** is clickable as a whole, and its inner controls still work.
- **Tabular numbers** where digits line up; nothing cut off with the longest real content.

## Check it for real

Open the screen in a real browser or device at phone and desktop sizes, in each theme, and compare with the mock and with `DESIGN.md`. A test environment without layout cannot prove a layout. Keep screenshots before and after.
