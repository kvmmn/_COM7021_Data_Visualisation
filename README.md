# COM7021 — Data Visualisation

**Arden University Berlin** · MSc Data Science · Student ID **25199053**  
Module: **COM7021SCC Data Visualisation**  
Tutor: Ahmed Hassan

This folder is the working base for the module: lessons, seminar notebooks, and the assignment. The GitHub remote is the copy that stays in sync with it.

Remote: [github.com/kvmmn/_COM7021_Data_Visualisation](https://github.com/kvmmn/_COM7021_Data_Visualisation) (private)

University lecture files and the assessment statement stay in this private repository. They are not for redistribution.

### Assessment Tutor Review Draft (GitHub Pages)
The self-contained interactive assessment draft (Task 1 & Task 2) is published live on GitHub Pages:
👉 **[https://kvmmn.github.io/_COM7021_Data_Visualisation/](https://kvmmn.github.io/_COM7021_Data_Visualisation/)**
- Direct review file path in repository: [`COM7021 - Assignment/COM7021_Draft_Review_25199053.html`](COM7021%20-%20Assignment/COM7021_Draft_Review_25199053.html)


## Layout

| Folder | What it holds |
|---|---|
| `COM7021 - Lessons/` | Lecture notes, transcripts, and lesson datasets |
| `COM7021 - Code Space/` | Weekly seminar notebooks, sample data, and the Week 1 Gestalt review |
| `COM7021 - Assignment/` | Assessment statement, assignment guide, and the visual design guide used for figures |
| `COM7021 - eBooks/` | Reserved for module ebooks (empty for now) |
| `aesth/` | Isolated visualisation library subproject (plotnine + Great Tables + Shiny). Public-grade docs; no lecture PDFs inside. Start at [`aesth/README.md`](aesth/README.md). |

## Lessons and code so far

| Week | Location | Notes |
|---|---|---|
| 1 | `COM7021 - Lessons/Lesson 1 - Introduction to Data Visualisation/` | Lesson PDF, module transcript, Anscombe’s quartet, Python colour palette |
| 1 seminar | `COM7021 - Code Space/COM7021 - Week 1 Seminar/` | Gestalt dashboard review and its assignment-control note |
| 2 | `COM7021 - Lessons/Lesson 2 - Knowing Your Data & Charts/` | Folder ready; materials not added yet |
| 2 | `COM7021 - Code Space/w2-activity-1/` and `w2-activity-2/` | Chart-selection notebook and COVID-19 sample data |
| 3 | `COM7021 - Code Space/w3-activity/` | Mini superstore notebook |
| 4–5 | `COM7021 - Code Space/Week 4 and 5 Data/` | Spatial visualisation deck plus Week 4 and Week 5 notebooks |

The zip archives next to the extracted week folders stay on disk only. Git tracks the extracted notebooks and data, not the duplicate zips.

## How this repo is used

1. New lesson files, notebooks, and assignment drafts go in the matching folder above.
2. Assessed writing follows the module brief first, then `COM7021 - Assignment/VISUAL_DESIGN_GUIDE.md` for figures.
3. After a real change, commit on `main` and push to this remote so GitHub matches the folder.

## Figure colours

[`aesth/`](aesth/README.md) is a separate open-source wrapper over plotnine, Great Tables, and Shiny. It is not part of the assessed EcoMove analysis.
