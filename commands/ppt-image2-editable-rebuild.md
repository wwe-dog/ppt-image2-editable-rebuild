---
description: Rebuild image2 or imagegen reference slides as editable PowerPoint decks.
---

# /ppt-image2-editable-rebuild

Use the bundled `$ppt-image2-editable-rebuild` skill and follow its workflow exactly.

## Intent

Create or continue an editable PowerPoint rebuild from a source document, prompt, or per-slide image2/imagegen reference PNGs.

## Required Behavior

1. Load and follow the `ppt-image2-editable-rebuild` skill.
2. Keep final PowerPoint slides meaningfully editable.
3. Never paste a full reference slide as the final PPT page.
4. Use bounded local crops only for complex visual fragments that are unreliable to recreate.
5. Keep ordinary titles, body text, tables, cards, arrows, labels, explanation boxes, conclusion bars, and footer chrome editable whenever practical.
6. Work one slide at a time when single-slide references exist.
7. Render and inspect previews before delivery.

## Expected Inputs

- A source document or prompt for generating reference PNGs, or
- Existing single-slide reference PNGs for editable PPT reconstruction, plus any target deck or output path requirements.

## Output

Return the editable PPTX path, preview paths, and a short QA summary covering slide count, full-slide screenshot avoidance, line-break checks, and media/crop checks.
