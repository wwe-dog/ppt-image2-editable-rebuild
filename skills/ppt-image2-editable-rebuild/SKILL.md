---
name: ppt-image2-editable-rebuild
description: "Create editable PowerPoint decks or pages from image2/imagegen reference PNGs while keeping text and structure editable."
---

# PPT Image2 Editable Rebuild

Use this skill for the workflow:

`source document or prompt -> image2 per-slide reference PNGs -> editable PPT rebuild`

The reference image is the visual standard. The final PPT must remain editable.

## Non-Negotiables

- Never paste a full reference slide as the final PPT page.
- Do not use a collage/contact-sheet image as the design source when single-slide reference PNGs exist.
- Do not inspect or reuse an existing same-topic presentation unless the user explicitly asks for reuse.
- Once reference PNGs exist, rebuild from the PNGs, not from the original Word/doc prompt.
- Build one slide at a time unless the user explicitly changes the workflow.
- Do not open or compare multiple reference PNG pages at once when the user requests page-by-page reconstruction.
- Ordinary editable text should be natural paragraphs. Do not hard-code manual `\n` line breaks to force layout.
- If text does not fit, resize the text box, card, icon, layout, or font. Do not let text protrude from its container.

## Two Modes

### Mode A: From Document To References

Use this when no reference PNGs exist yet.

1. Read the user-provided document or detailed prompt.
2. Extract each slide's page number, section, title, body, diagrams, visual assets, and style constraints.
3. Generate one image2/imagegen visual reference PNG per slide.
4. Save references as independent files such as `slide01_reference.png`, `slide02_reference.png`, etc.
5. Treat these PNGs as the only visual source for the rebuild stage.

The document is only for creating references. After references exist, stop using the document for layout decisions unless the user explicitly asks.

### Mode B: From References To Editable PPT

Use this when single-slide reference PNGs already exist.

1. Open only the current slide's single reference PNG.
2. Identify the slide structure: header, title, cards, diagram, icon groups, arrows, explanation panels, conclusion bars, footer.
3. Decide what is editable and what must be cropped from the reference.
4. Crop only local visual assets needed for fidelity.
5. Build the slide with editable PPT text and shapes plus the cropped assets.
6. Append the slide to the current deck.
7. Render the slide preview.
8. Compare preview against the reference and fix issues before moving on.
9. Sync the current PPT only after the page passes preview QA.

## Editable Vs Cropped

Make these editable whenever practical:

- Page numbers, section badges, titles, subtitles
- Body text, bullets, labels, formulas, table text
- Card headings and card body text
- Arrows, dividers, connector lines, outlines
- Rounded cards, title bars, callouts, explanation boxes, conclusion strips

Use reference crops for:

- image2-generated illustrations, maps, river basins, landscapes, icons, badges
- Complex chart cards, especially pie charts, donut/ring charts, and dense radial visuals whose segment proportions or labels would be unreliable if redrawn
- Complex background fragments that cannot be recreated cleanly
- Small icon+title/header visuals when exact matching matters
- Local text that is embedded in a complex visual and would visibly degrade if separated

For pie/donut/ring charts, crop the whole local chart card or chart block, including the chart, its immediate labels, leader lines, icon/title strip, and bottom total band when present. Do not approximate chart sectors with simple editable shapes unless the user explicitly asks for fully editable charts.

Even when a crop contains embedded text, keep surrounding headings, body text, tables, legends outside the crop, and structural elements editable.

## Cropping Rules

Prefer user-provided manual screenshots for complex local assets when available. They are often cleaner than brittle coordinate crops.

If cropping from the reference PNG:

- Crop generously enough to avoid cutting labels, arrows, icon edges, and bottom captions.
- For chart-card crops, include the complete rounded card if possible. This is more reliable than separate icon, label, and chart crops.
- Avoid unrelated neighboring text, borders, or residual artifacts.
- Inspect the crop image itself before using it.
- Inspect the rendered PPT preview after placing it.
- If the crop contains unwanted text residue, recrop, use a cleaner screenshot, or create a transparent-mask asset.
- Never use a crop that is effectively the whole slide.

Use the bundled crop helper when useful:

```bash
python scripts/crop_reference_assets.py \
  --image /path/to/slideXX_reference.png \
  --out-dir /path/to/workspace/assets \
  --spec /path/to/crops-slideXX.json \
  --contact-sheet
```

Spec format:

```json
{
  "assets": [
    { "name": "slide06-basin.png", "box": [60, 210, 930, 520] },
    { "name": "slide06-eco-badge.png", "box": [1510, 30, 1635, 135] }
  ]
}
```

Use pixel boxes by default. Use `relBox` only when reference dimensions may vary.

## PPT Build Rules

- Use the Presentations skill/plugin and `@oai/artifact-tool/presentation-jsx`.
- Keep the final slide in 16:9 unless the user says otherwise.
- Rebuild text and containers with PPT elements; insert only local crops for complex visuals.
- Match the reference layout, color, spacing, and hierarchy closely.
- For dense Chinese academic/defense decks, prefer Microsoft YaHei, Noto Sans CJK SC, or Source Han Sans style typography.
- For green academic decks, preserve the template palette and avoid commercial pitch styling.
- Use rounded rectangles for cards when the reference uses rounded cards.
- If native rounded rectangles do not match enough, use grouped/combined shapes or local patterns that reproduce the rounded-card look.
- Keep repeated slide chrome consistent: chapter badge, top rule, logo/badge, bottom conclusion bar, footer.

## Text Rules

- Ordinary Chinese paragraphs should be written as one natural text string.
- Do not manually insert `\n` in ordinary body text, bullet text, or card copy.
- Let the text box wrap naturally.
- If text overflows, change geometry or font size rather than forcing line breaks.
- Keep padding inside cards and boxes; do not let text touch borders.
- Check compact cards especially carefully for squeezed or protruding text.

## Per-Slide QA Loop

After building each slide:

1. Render a preview PNG.
2. Inspect the preview at readable size.
3. Compare to the reference for:
   - clipped crops, cut labels, missing arrows, missing icons
   - wrong pie/donut/ring chart proportions from manually reconstructed sectors
   - text overflow, text touching borders, body text hidden by images
   - wrong arrow direction or bad connector alignment
   - crop residue from nearby text or shapes
   - style drift from the reference/template
4. Check the slide module for literal `\n` in ordinary text.
5. Fix the slide and rerender until acceptable.
6. Append/sync the deck only after the slide passes.

## Final Deck QA

Before final delivery:

- Confirm slide count.
- Confirm previews exist for all generated slides.
- Generate a contact sheet for quick review when working on many pages.
- Inspect the PPTX package media list and image dimensions.
- Confirm no full-slide screenshot or reference PNG is used as a slide page.
- Confirm media assets are explainable local crops such as icons, illustrations, badges, maps, chart cards, or complex visual fragments.
- Keep useful intermediate deck versions for long jobs, such as page ranges `1-10`, `1-20`, `1-29`.

## Delivery

Return:

- Final editable PPTX path.
- Current synchronized PPTX path when applicable.
- Per-slide previews or the preview directory.
- Contact sheet path for multi-slide jobs.
- Brief QA summary: slide count, no full-slide screenshots, text line-break check, media check, and any residual risk.

## Common Failure Responses

Redo or patch immediately when:

- The slide looks much simpler than the reference.
- Icons or illustrations were manually redrawn when the user asked them to match image2.
- Pie, donut, or ring charts were manually redrawn and the sector proportions are visibly wrong. Replace the chart/card with a bounded reference crop and keep the nearby table editable.
- The final page is a flat full-slide screenshot.
- A crop cuts off labels, arrows, icon edges, or bottom captions.
- A crop includes unrelated neighboring text or visual residue.
- Text protrudes from a card or is hidden by an illustration.
- Manual line breaks were used to compensate for bad layout.
