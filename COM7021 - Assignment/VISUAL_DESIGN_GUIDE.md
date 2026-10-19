# Visual design guide

Reusable graphic system taken from the COM7020 Big Data and Cloud Computing portfolio (MetroEnergy Solutions proof of concept, student 25199053). Use this as the baseline for COM7021 Data Visualisation and later assignments.

Source files analysed:

- `_COM7020_Big_Data_and_Cloud_Computing/COM7020 - Assignment/_poc/scripts/mes_pandas_charts.py`
- `_COM7020_Big_Data_and_Cloud_Computing/COM7020 - Assignment/_poc/scripts/render_architecture_diagrams.py`
- `_COM7020_Big_Data_and_Cloud_Computing/COM7020 - Assignment/_poc/brand/PALETTE.md`
- `_COM7020_Big_Data_and_Cloud_Computing/COM7020 - Assignment/_brain/VISUAL_STANDARD.md`
- The exported PNGs and SVGs in `_poc/output/figures/`

The system has two production paths that share one palette. Data charts are matplotlib. Structural figures (architecture, flows, matrices, KPI strips) are hand-authored SVG, then rasterised. Both look like the same brand because colour, type, corner radius, shadow, and label length are locked.

---

## 1. Principle

The prose carries the argument. The figure carries one visual job.

- Short labels inside the artwork. No sentences, no essay captions baked into the image.
- Interpretation lives in the report body, under a numbered figure caption.
- One job per figure. A chart does not also try to be a diagram. A screenshot does not also try to be a chart.
- Highlight one thing. Tiffany marks the claim. Midnight is the structural ink. Everything else stays quiet.
- British English in any label that appears (`visualisation`, `colour`, `organised`), when the module expects it.
- Avoid the default “AI chart” look: no purple glow, no rainbow categorical palette, no 3D, no heavy gradients, no chartjunk.

---

## 2. Colour

The palette is the Arden University logo pair, plus a small derived working set. Do not invent a new hue family.

### 2.1 Locked tokens

| Token | Hex | Role |
|---|---|---|
| `midnight` | `#002B49` | Titles, axis labels, primary series, dark headers, structural ink |
| `tiffany` | `#66C9BA` | Accent series, soft fills, highlight bars, emphasis strokes |
| `tiffany_deep` | `#3AA89A` | Secondary accent, recommended-column headers, marker fills, emphasis arrows |
| `midnight_soft` | `#1A4A6B` | Alternate series, quieter bars, alternate pills on a midnight bar |
| `teal` | `#0E7C8B` | Third categorical series only. Used for Birmingham in the regional chart. Stay inside this teal; do not add orange, purple, or red |
| `mist` | `#E6F5F2` | Lane backgrounds, highlighted cards, zebra rows, soft fills |
| `paper` | `#F7FAFB` | Plot and canvas background |
| `white` | `#FFFFFF` | Cards, figure surround, bar edges |
| `mute` | `#5A6B75` | Tick labels, secondary text, default arrows, subtitles inside cards |
| `grid` / `line` | `#D5DEE3` / `#C9D5DD` | Chart grid uses `#D5DEE3`. Diagram strokes use `#C9D5DD` |

`grid` and `line` are the same job (quiet structure) at two slightly different values. Charts use `grid`. Diagram boxes use `line`.

### 2.2 How colour is allowed to mean something

| Meaning | Treatment |
|---|---|
| The thing the sentence is about | Tiffany fill, Tiffany stroke, or Tiffany-deep marker |
| The recommended or active path | Tiffany-deep header or stroke (`sw=2`), mist fill |
| Structure, sequence, default series | Midnight |
| Context that is present but not the claim | Midnight-soft, or a white card with a `#C9D5DD` stroke |
| A time window or a band of interest | `axvspan` in Tiffany at alpha `0.12` |
| An area under a line | Tiffany fill at alpha `0.35`, Midnight line on top |
| A dark footer (governance, controls) | Midnight bar, pills alternating Tiffany-deep and Midnight-soft |

Alpha values are part of the brand. Use `0.12` for a background band and `0.35` for an area fill. Do not use `0.5`–`0.8` washes; they turn Tiffany muddy.

### 2.3 Series order

When a chart needs more than one series, assign colours in this order and stop at five. A sixth series means the chart should be split or faceted.

1. `#002B49` midnight
2. `#3AA89A` tiffany deep
3. `#0E7C8B` teal
4. `#1A4A6B` midnight soft
5. `#66C9BA` tiffany

Tiffany is last on purpose: it stays available as the highlight if one series is the point of the figure. If every series is equal, Tiffany may be used as series 5, as in the regional demand chart (Manchester).

Lines that sit close together (the regional profiles do) stay distinguishable because the five colours alternate dark navy and mid teal. Do not put two light teals next to each other in the legend.

### 2.4 Contrast

- Midnight on paper, white, or mist: body text and titles.
- White on midnight or on tiffany / tiffany-deep: chips, circle labels, column headers.
- Mute (`#5A6B75`) only for secondary text at 10–11 px. It is too light for titles.
- Do not put midnight body text on tiffany. Do not put white text on mist or paper.

---

## 3. Typography

One family on both production paths: **Microsoft Aptos**. Charts and diagrams use the same face, so a report page does not switch type between a plot and a flow.

Aptos ships with Microsoft 365. Install the family where both matplotlib and `rsvg-convert` can see it (`~/Library/Fonts` on macOS). After installing, rebuild the matplotlib font cache once (`matplotlib.font_manager.fontManager.addfont` on each file, or delete the cache and restart the interpreter). If Aptos is missing, the figure is wrong. Do not substitute DejaVu, Helvetica, Arial, or Calibri.

### 3.1 Which Aptos face

| Face | Use in this system |
|---|---|
| **Aptos** | Every label at the sizes in this guide: titles, axes, ticks, legends, cards, chips, lane titles |
| **Aptos Display** | A title set at 18 pt or larger only. Chart titles here are 13 pt, so they stay in Aptos, not Display |
| **Aptos Narrow** | A chip or matrix cell that would overflow its box. Not the default |
| **Aptos Mono** | A literal filename, identifier, or code token inside a figure |
| **Aptos Serif** | Not used in figures |

### 3.2 Weights

Aptos cuts used here are Regular (400), SemiBold (600), and Bold (700). There is no 500 weight in the family, so secondary diagram text is Regular, not a synthetic medium.

| Role | Face | Weight |
|---|---|---|
| Chart title | Aptos | Bold |
| Axis label | Aptos | SemiBold |
| Tick, legend, in-plot note | Aptos | Regular |
| Card title, header on a dark or Tiffany bar (`.lab`, `.labw`) | Aptos | SemiBold |
| Lane title, pill, step number (`.zone`, `.chip`, `.num`) | Aptos | Bold |
| Qualifier line, KPI caption (`.small`, `.tiny`) | Aptos | Regular |

### 3.3 Chart type scale

Set the family once, through `rcParams` (`font.family = "Aptos"`):

| Element | Size | Weight | Colour |
|---|---|---|---|
| Title | 13 pt | Bold | midnight |
| Axis label | 11 pt | SemiBold | midnight |
| Tick | 10 pt | Regular | mute |
| Legend | 9 pt | Regular | midnight, no frame |
| In-plot annotation | 9 pt | Regular | mute for a window label, midnight for a data label |

Title padding is `pad=14`. That gap is what keeps the bold title off the top spine.

### 3.4 Diagram type scale

SVG `font-family` is `Aptos` on every class.

| Class | Role | Size | Weight | Colour |
|---|---|---|---|---|
| `.lab` | card title | 14 px | 600 SemiBold | midnight |
| `.labw` | title on a dark or Tiffany header | 13 px | 600 SemiBold | white |
| `.small` | cell text, KPI caption | 11 px | 400 Regular | mute |
| `.tiny` | second line inside a card | 10–11 px | 400 Regular | mute |
| `.chip` / `.num` | pills and step numbers | 10–12 px | 700 Bold | white |
| `.zone` | lane title | 12 px | 700 Bold | midnight |

Card titles are a short noun phrase (`Curated zone`, `Event bus`). The second line is a qualifier (`raw / immutable`, `Kafka API`), never a sentence.

---

## 4. Chart geometry

Every analytical chart in the COM7020 set uses the same frame.

| Property | Value |
|---|---|
| Figure size | `(10.5, 5.2)` for lines, `(10.5, 5.0)` for bars and area charts |
| Figure face | white |
| Axes face | `#F7FAFB` |
| `figure.dpi` | 160 (on-screen) |
| `savefig.dpi` | 220 |
| `savefig.bbox` | `tight` |
| `savefig.pad_inches` | 0.25 |
| Spines | top and right hidden; left and bottom `#D5DEE3` |
| Grid | horizontal only, `#D5DEE3`, linewidth 1, drawn under the data (`set_axisbelow(True)`) |
| Vertical grid | off |
| Legend | `frameon=False` |
| Line cap | `solid_capstyle="round"` |

The plot sits on a cool off-white field. The saved file has a white margin around it because `figure.facecolor` is white and `bbox` is tight. That white margin is what makes the figure sit cleanly on a report page.

### 4.1 Axes method

Apply this to every axes before plotting:

- Hide top and right spines.
- Colour the remaining spines with the grid token, so the frame is quieter than the data.
- Colour ticks mute, labels and title midnight.
- Turn on a y-grid only.
- Put the grid behind marks.

X ticks on a 24-hour axis are every 2 hours (`range(0, 24, 2)`), not every hour. Date axes use `dd Mon` (`%d %b`) and `fig.autofmt_xdate()`.

Y axes start at zero when the mark is a bar or an area (the peak-hour chart and the error area both do). A line chart of a level (demand by hour, daily totals) may use a tight scale, because the shape of the level is the point. Do not force a zero baseline on those lines if it flattens the pattern the figure exists to show.

---

## 5. Chart recipes

These four recipes are the whole analytical language of the COM7020 figures. New COM7021 charts should be one of these, or a disciplined combination of two.

### 5.1 Multi-series line

Used for: mean half-hourly demand by region.

- One line per category, linewidth `2.4`, round caps.
- Colour from the series order in section 2.3.
- No markers on the line. Markers are reserved for a second encoding (see 5.2).
- Direct highlight of a window with `axvspan(start, end, color=tiffany, alpha=0.12, zorder=0)`.
- A short window label in mute, 9 pt, centred on the band, near the top of the axes (`0.96` of the y limit).
- Legend in one row when there are about five series: `ncol=5`, `loc="upper left"`, `frameon=False`, 9 pt.
- Sort category names before drawing so legend order is stable.

Place the window label where the legend is not. On the regional chart the words “Evening peak window” collide with the legend. Keep the band; move the label into the caption, or drop the legend to the lower left, or put the label inside the band clear of other text.

### 5.2 Single series line with a point encoding

Used for: daily total demand, weekends marked.

- The line is midnight, linewidth `2.0`, `zorder=3`.
- The second encoding is a scatter on a subset only (weekend days): size `s=22`, fill tiffany-deep, edge midnight, edge width `0.3`, `zorder=4`.
- Legend names the points (`Weekend days`), not the line. The line is the base and does not need a legend entry when it is the only series.
- Legend at `upper right`, no frame.

The point is small on purpose. It marks membership. It does not compete with the line.

### 5.3 Bar with one highlighted state

Used for: distribution of the daily peak hour.

- Bar width `0.85`.
- Edge colour white, so neighbouring bars separate without a dark stroke.
- Default fill midnight-soft. Highlight fill tiffany. The highlight is a rule (`hour in (17, 21)`), not a hand-coloured bar.
- Direct labels only on the highlighted bars: value plus unit (`68 days`), 9 pt, midnight, centred, `va="bottom"`, sitting `1.5` data units above the bar.
- Headroom: `ylim` top is `max(values) * 1.18`, so the label is inside the axes.
- No legend. Colour is explained by the labels and the caption.
- Zero baseline.

If every bar is the same colour, the chart has no claim. If every bar is tiffany, the highlight is gone. Highlight the bars the paragraph discusses.

### 5.4 Line with area fill

Used for: naive baseline error by hour.

- `fill_between` from zero to the series, tiffany, alpha `0.35`.
- Line on top in midnight, linewidth `2.4`.
- No markers, no legend, no in-plot annotation. The title names the measure.
- Zero baseline, because the filled area is the quantity.

Use the area when the magnitude under the curve is the reading. Use a plain line when the comparison between series is the reading.

### 5.5 What these charts refuse

- Dual y-axes.
- Pie charts, donut charts, 3D bars, radar charts.
- A legend and direct labels for the same series.
- Gridlines on both axes.
- More than one highlight colour.
- Titles that restate the axis labels in a full sentence. Titles are noun phrases: “Mean half-hourly demand by region”.

---

## 6. Diagram geometry

Diagrams are SVG strings written by Python, then converted to PNG with `rsvg-convert`. The drawing is not matplotlib. That split is deliberate: matplotlib is for data, SVG is for layout.

### 6.1 Canvas

| Figure kind | ViewBox width | Raster width |
|---|---|---|
| Concept row (five circles, data modes) | 900–1000 | 1400 px |
| Flow, roadmap, governance | 980 | 1500 px |
| KPI strip | 1040 | 1600 px |
| Comparison matrix, constraint pairs | 1020 | 1600 px |
| Architecture overview, dataflow | 1040–1280 | 1700 px |
| Detailed architecture | 1290 | 1800 px |

Canvas fill is always `paper` (`#F7FAFB`). There is no title inside the SVG. The report caption is the title.

Outer margin is about 30–40 px. Content does not touch the canvas edge.

### 6.2 Corner radius

Radius is a brand constant. Do not mix sharp rectangles into this system.

| Element | `rx` |
|---|---|
| Lane (the tinted zone) | 18 |
| Card | 12 |
| KPI card, roadmap card | 14 |
| Column header | 10 |
| Inner matrix cell | 8 |
| Governance footer | 14–16 |
| Pill | half the pill height (fully round ends) |

### 6.3 Shadow

One filter, used on cards, circles, KPI tiles, and step boxes:

```xml
<feDropShadow dx="0" dy="2" stdDeviation="2.4"
              flood-color="#002B49" flood-opacity="0.10"/>
```

The shadow is a 2 px drop, very soft, tinted with midnight at 10% opacity. It is not a glow. Lanes and the full-width footer do not take the shadow; only objects that sit on top of a lane or the canvas do.

Apply the filter on a `<g>`, not on the text, so the label stays sharp.

### 6.4 Strokes

| Role | Stroke | Width |
|---|---|---|
| Default card | `#C9D5DD` | 1.5 |
| Lane boundary | `#C9D5DD` | 1 |
| Emphasis card (the path that matters) | `#66C9BA` | 1.5, or 2 when it is the PoC scope |
| Structural emphasis (batch, a named constraint) | `#002B49` | 1.5 |
| Connector, default | `#5A6B75` | 2 |
| Connector, the path that matters | `#3AA89A` | 2 |
| Governance link between cards | `#66C9BA` | 3 |

Arrows are filled triangles, 8 by 6, matching the stroke colour (`marker-end`). Default arrows are mute. Tiffany-deep arrows are the emphasised flow (stream into the lake, response column, the drop into the govern bar).

### 6.5 Cards, pills, lanes

**Card.** White fill, 12 px radius, shadow, label centred. Optional second line in `.tiny`, mute. A highlighted card uses mist fill and a tiffany or midnight stroke. Sub-label sits about 8 px under the title; each extra line is 14 px further down.

**Pill.** Height 22–26 px, fully rounded, white bold label. Midnight for the default chip, tiffany-deep for the active chip. On a midnight footer, pills alternate tiffany-deep and midnight-soft so the row does not become a single green slab.

**Lane.** Mist fill, 18 px radius, 1 px `#C9D5DD` stroke, no shadow. The lane title is `.zone`, 16 px in from the left, about 22 px down. Lanes are the only large tinted regions. They group a column or a swimlane. They are not boxes inside boxes inside boxes.

**Step number.** A midnight circle, radius 14–18, white bold number, sitting on or just above the card. Numbers are `01`–`05` when the sequence is a procedure, and `1`–`5` when it is a short roadmap. Pick one style per figure.

**Scope chip.** A small tiffany-deep pill (`PoC scope`, `Recommended path`) placed on the object that is in scope. One chip per figure.

### 6.6 Diagram recipes

**Column architecture.** Four or five lanes left to right. Cards stacked inside each lane. Arrows only for the flows that matter, not from every box to every box. A midnight footer spans the full width and holds the control chips. This is `fig_arch_mes_overview` and `fig_arch_detailed`.

**Swimlanes.** Two horizontal lanes (batch, stream) on the left, one shared lane on the right. Batch connectors are mute. The stream connector that joins the shared system is tiffany-deep. This is `fig_arch_hybrid_lanes`.

**Dataflow row.** One lane, five equal cards, arrows between them. Cards that are the analytical core get mist fill and a tiffany stroke. Engine chips (PySpark, Dataproc, GCS) sit centred under the row. This is `fig_arch_dataflow`.

**Numbered procedure.** Circle number, card, arrow, repeat on one horizontal line. This is the PoC workflow and the roadmap. The first roadmap card may take a tiffany stroke to mark “you are here” or “start here”.

**Pair map.** Two headers (midnight for the problem, tiffany-deep for the response). Each row is a white card, a tiffany-deep arrow, and a mist card with a tiffany stroke. Row pitch is 52 px. This is the constraint-response figure.

**Comparison matrix.** Midnight header chips, the recommended column in tiffany-deep. Body rows alternate white and mist, `rx=10`, height 48, pitch 52. The recommended column’s inner cells get a white fill and a tiffany stroke of width 2. Other cells have no stroke. A single pill under the recommended column says why (`Recommended path`). This is the provider-fit figure.

**KPI strip.** Six tiles in a row. White card, 14 px radius, shadow, value in `.lab`, caption in `.small`. The one or two tiles that are the result (MAE, MAPE) get a tiffany stroke of width 2. The others keep the quiet `#C9D5DD` stroke. No icons.

**Concept row.** Equal circles, radius 55, alternating tiffany and midnight, white labels, shadow. Used when the figure is a set of named ideas and not a flow. Five items is the maximum for this pattern.

**Linked controls.** Equal cards in mist with a midnight stroke, joined by a tiffany bar of width 3. Used for a chain (IAM → encrypt → residency → audit → lineage), not for a choice.

---

## 7. Spacing

Diagram spacing in the COM7020 figures is regular enough to copy as a grid.

| Measure | Value |
|---|---|
| Canvas padding | 30–40 px |
| Lane gap | about 30–40 px |
| Card width, standard | 150–180 px |
| Card height, one line | 36–44 px |
| Card height, title plus one sub-line | 60–80 px |
| Card height, title plus two sub-lines | 90 px |
| Vertical step inside a column | 45 px for tight stacks, 52 px for matrix rows, 85 px when each card has a sub-line |
| Arrow gap | the arrow starts about 4–8 px after the source edge and ends 4–8 px before the target |
| Pill height | 22–26 px |
| Footer height | 64–70 px |

Centre a row of equal cards inside its lane. Do not left-align a five-step flow and leave a hole on the right.

---

## 8. Annotation rules

- A highlight band gets at most one short label, and only if it does not touch the legend or a line.
- A highlighted bar gets a direct label. Unhighlighted bars do not.
- A diagram card gets a title and at most two qualifier lines.
- Numbers in a KPI tile are the value (`5.29`, `3.08%`, `518,400`). The unit is the caption under it (`MAE kWh`), not part of a sentence.
- Thousands separators on large counts.
- Units on the axis, not repeated on every tick (`Mean interval demand (kWh)`).
- Time zone in the axis when it matters (`Hour of day (UTC)`).
- No arrows with paragraph explanations. If a relationship needs a sentence, the sentence goes in the report.

---

## 9. Toolchain

| Job | Library or tool | Why it is in the system |
|---|---|---|
| Tabular data | `pandas` | Grouping, date parts, the frame the chart reads |
| Numerics | `numpy` | Error metrics only. Charts themselves do not need a numpy style layer |
| Charts | `matplotlib` (`pyplot`, `matplotlib.dates`) | Full control of spines, grid, colour, and export. No seaborn theme, because seaborn would restyle the axes away from this standard |
| Diagrams | Python f-strings writing SVG | Exact radius, shadow, and type. No diagramming GUI in the pipeline |
| Raster | `rsvg-convert` (librsvg) | SVG to a wide PNG at a set pixel width |
| Export | PNG at 220 dpi for charts; PNG at 1400–1800 px wide for diagrams. SVG kept beside the PNG as the source |

Install note for a new environment: `pandas`, `numpy`, `matplotlib`, the `librsvg` CLI (`rsvg-convert`), and the **Microsoft Aptos** family installed for the user account. No seaborn, no plotly, no pillow pipeline. Plotly is a reasonable later choice only if the assignment requires an interactive view, and even then the colour tokens and the Aptos scale in this guide still apply.

Figures are reproducible from code. The COM7020 habit was: data script, chart script, diagram script, outputs under `output/figures/`. Keep that split.

Suggested layout for a new assignment:

```text
assignment/
  data/
  scripts/
    charts.py          # matplotlib, imports the style module
    diagrams.py        # SVG builders
  style/
    palette.py         # the tokens below
  output/
    figures/           # png + svg
```

---

## 10. Baseline code

Copy this module and import it. Change the data. Do not restyle it per chart.

```python
"""Arden Midnight / Tiffany figure style. Import; do not restyle per chart."""

from __future__ import annotations

import matplotlib.pyplot as plt

MIDNIGHT = "#002B49"
TIFFANY = "#66C9BA"
TIFFANY_DEEP = "#3AA89A"
MIDNIGHT_SOFT = "#1A4A6B"
TEAL = "#0E7C8B"
MIST = "#E6F5F2"
PAPER = "#F7FAFB"
MUTE = "#5A6B75"
GRID = "#D5DEE3"
LINE = "#C9D5DD"
WHITE = "#FFFFFF"

# Five-series order. Tiffany stays last so it can still be the highlight.
SERIES = [MIDNIGHT, TIFFANY_DEEP, TEAL, MIDNIGHT_SOFT, TIFFANY]


def apply_rcparams() -> None:
    plt.rcParams.update(
        {
            "font.family": "Aptos",
            "axes.titleweight": "bold",
            "axes.labelweight": "semibold",
            "figure.facecolor": "white",
            "axes.facecolor": PAPER,
            "text.color": MIDNIGHT,
            "axes.labelcolor": MIDNIGHT,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "figure.dpi": 160,
            "savefig.dpi": 220,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.25,
        }
    )


def style_axes(ax) -> None:
    ax.set_facecolor(PAPER)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTE, labelsize=10)
    ax.yaxis.label.set_color(MIDNIGHT)
    ax.xaxis.label.set_color(MIDNIGHT)
    ax.yaxis.label.set_fontweight("semibold")
    ax.xaxis.label.set_fontweight("semibold")
    ax.title.set_color(MIDNIGHT)
    ax.title.set_fontweight("bold")
    ax.title.set_fontfamily("Aptos")
    ax.grid(True, axis="y", color=GRID, linewidth=1)
    ax.set_axisbelow(True)


def save(fig, path) -> None:
    fig.savefig(path)
    plt.close(fig)
```

Chart calls that match the COM7020 figures:

```python
apply_rcparams()
fig, ax = plt.subplots(figsize=(10.5, 5.2))
style_axes(ax)

ax.plot(x, y, color=MIDNIGHT, linewidth=2.4, solid_capstyle="round")
ax.axvspan(17, 22, color=TIFFANY, alpha=0.12, zorder=0)
ax.fill_between(x, y, color=TIFFANY, alpha=0.35)
ax.bar(hours, counts, color=colors, width=0.85, edgecolor="white")
ax.scatter(x, y, s=22, color=TIFFANY_DEEP, edgecolors=MIDNIGHT, linewidths=0.3, zorder=4)

ax.set_title("Noun phrase that names the view", pad=14, fontfamily="Aptos", fontweight="bold")
ax.legend(frameon=False, fontsize=9)
save(fig, "output/figures/fig01_name.png")
```

SVG shadow and type, copied from the diagram script:

```python
DEFS = f"""
<defs>
  <filter id="shadow" x="-6%" y="-6%" width="118%" height="118%">
    <feDropShadow dx="0" dy="2" stdDeviation="2.4"
                  flood-color="{MIDNIGHT}" flood-opacity="0.10"/>
  </filter>
  <style>
    .lab  {{ font: 600 14px Aptos, sans-serif; fill: {MIDNIGHT}; }}
    .labw {{ font: 600 13px Aptos, sans-serif; fill: {WHITE}; }}
    .small{{ font: 400 11px Aptos, sans-serif; fill: {MUTE}; }}
    .tiny {{ font: 400 10px Aptos, sans-serif; fill: {MUTE}; }}
    .chip {{ font: 700 10px Aptos, sans-serif; fill: {WHITE}; }}
    .zone {{ font: 700 12px Aptos, sans-serif; fill: {MIDNIGHT}; }}
    .num  {{ font: 700 12px Aptos, sans-serif; fill: {WHITE}; }}
  </style>
</defs>
"""
```

Rasterise with:

```bash
rsvg-convert -w 1600 -o output/figures/name.png output/figures/name.svg
```

---

## 11. Choosing a figure

| You need to show | Use | Highlight |
|---|---|---|
| Several categories over a shared axis | Multi-series line, linewidth 2.4 | One `axvspan` if a window matters |
| One measure over time, plus a subset | Midnight line plus small tiffany-deep points | The subset only |
| A distribution or a count by category | Bars, midnight-soft, white edges | Tiffany on the categories the text discusses, direct labels on those bars only |
| Magnitude of a single series | Area alpha 0.35 plus midnight line | The fill is the highlight |
| A process from left to right | Numbered cards and mute arrows | Tiffany stroke on the current or in-scope step |
| Two kinds of input joining one system | Swimlanes | Tiffany-deep arrow on the path that is the point |
| A system in layers | Lanes, cards, one footer | Mist plus tiffany stroke on the in-scope boxes |
| A before / after or problem / response | Pair map | Right-hand column is mist with tiffany stroke |
| A comparison across options | Matrix, zebra rows | Recommended column header in tiffany-deep, cell stroke tiffany |
| A handful of results | KPI strip | Tiffany stroke on the result tiles only |
| A set of named ideas, no order | Alternating circles | No extra labels |

If a new chart type is required (scatter of two measures, heatmap, small multiples), keep the frame in section 4 and the tokens in section 2. A heatmap should run from mist (`#E6F5F2`) through tiffany to midnight, not from white through yellow to red. Small multiples share one scale, one highlight rule, and no repeated legends.

---

## 12. Report placement

- Continuous figure numbers across the document.
- Caption under the figure, in the report style, not inside the image.
- The caption says what the reader should notice. The image does not repeat that sentence.
- One figure, one claim. A second claim gets a second figure.
- Export PNG for the document. Keep SVG for diagrams so a later edit does not start from a flattened image.
- Screenshots of tools (consoles, notebooks) stay in a separate class: cropped, sharp, captioned. They are evidence. They are not restyled to look like the charts, and they are not a substitute for a chart of the same view.

---

## 13. Checklist before a figure is finished

- Palette is only the tokens in section 2. No extra hue.
- One highlight, and it is the thing the paragraph is about.
- Title is a short noun phrase, midnight, Aptos Bold, 13 pt on charts. Diagrams have no internal title.
- All figure text is Microsoft Aptos (Regular, SemiBold, or Bold). No stand-in sans.
- Top and right spines are gone on charts. Grid is horizontal only.
- Legend has no frame. If direct labels exist, the legend does not repeat them.
- Labels do not collide with the legend, the line, or the band.
- Card text is a title plus at most two short qualifiers.
- Shadow is the midnight 10% drop, or there is no shadow. No glow.
- Corner radii match section 6.2.
- Chart PNG is 220 dpi. Diagram PNG is at least 1400 px wide, with the SVG saved beside it.
- The figure still makes its point in greyscale well enough that midnight and tiffany-deep remain distinct. They do: navy stays dark, tiffany-deep stays mid. Tiffany and mist will collapse together, so never encode a difference with those two alone.

---

## 14. Worked inventory

These are the COM7020 figures, named by the pattern to reuse rather than by the energy-systems content.

| File stem | Pattern |
|---|---|
| `fig01_region_hour_profile` | Multi-series line, five-colour order, evening band at alpha 0.12 |
| `fig02_daily_system_demand` | Midnight line, tiffany-deep points with a midnight edge for the subset |
| `fig03_peak_hour_hist` | Bars, midnight-soft default, tiffany highlight, direct labels, 18% headroom |
| `fig04_baseline_error_by_hour` | Tiffany area at alpha 0.35, midnight line at linewidth 2.4 |
| `fig_wf_data_modes` | Two rows of cards; mist plus tiffany stroke marks the timing row |
| `fig_wf_five_vs` | Five circles, tiffany and midnight alternating, white labels, shadow |
| `fig_wf_provider_fit` | Matrix, zebra mist rows, recommended column in tiffany-deep |
| `fig_wf_constraint_response` | Pair map, midnight header against tiffany-deep header |
| `fig_wf_poc_metrics` | KPI strip, tiffany stroke on the result tiles |
| `fig_wf_governance` | Mist cards, midnight stroke, tiffany connectors |
| `fig_workflow_poc` | Numbered circles plus cards in a row |
| `fig_wf_roadmap` | Numbered cards; first step stroked in tiffany |
| `fig_arch_mes_overview` | Four lanes, dual ingest, midnight govern footer |
| `fig_arch_detailed` | Five lanes, scope pill, controls footer |
| `fig_arch_dataflow` | One lane, five stages, engine pills centred underneath |
| `fig_arch_hybrid_lanes` | Batch lane and stream lane into a shared column; stream arrow in tiffany-deep |
