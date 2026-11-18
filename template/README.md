# Report template: "Cobalt"

A white Quarto HTML theme with cobalt blue frames, used with `theme: none`.

| File | Role |
|------|------|
| `custom.css` | colour tokens, typography, content column, TOC, callouts, figure cards, tables, code folding |
| `header.html` | cobalt header band (include before body) |
| `footer.html` | footer with author details (include after body) |

## Usage

```yaml
format:
  html:
    theme: none
    css: template/custom.css
    include-before-body: template/header.html
    include-after-body: template/footer.html
```

With `theme: none` Quarto emits no wrapper element, so the content column is set on `body > *` (all top-level elements except header and footer). Width and side gutters come from `--content-width` and `--gutter` in `:root`.

The colour tokens live in `:root`: change `--cobalt` and its tints to rebrand the whole report. The matplotlib palette in `report.qmd` uses the same values.
