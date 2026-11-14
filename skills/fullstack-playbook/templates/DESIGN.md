# Design

The single source of truth for how this product looks and feels. Code uses only the tokens defined here; a test compares them with the code.

A product with surfaces that look different (for example an app, a public site and an admin) keeps one source per surface: a section per surface here, or a table here pointing to one file per surface in `docs/design/`. Never two sources for the same surface.

## Tokens
Colors by role (surface, text, action, focus, border, semantic, data), type scale, spacing scale, radius, elevation, motion.

## Named rules
Short rules with a name, a reason and an example (for example: no text below the contrast minimum).

## Components
Each shared component: purpose, variants, states (default, hover, focus, active, disabled, loading, error, empty).

## Layout
Grid, maximum widths, breakpoints, safe areas.
