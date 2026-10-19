# ADR 0003 — Documentation standard

**Status:** accepted  
**Date:** 19 October 2026

## Context

aesth is meant to be publishable. Course PDFs, student ID, and EcoMove must not leak into the public tree. Research has to be reconstructable.

## Choice

- British English on all public pages (`visualisation`, `colour`, `organised`).
- Every web claim cites a URL that appears in [SOURCES.md](../SOURCES.md). No remembered URLs.
- Research notes share one outline: purpose, install, API we wrap, API we refuse, fit, risks, worked example in prose.
- Decisions are ADRs: context, options, choice, consequences, links.
- University materials stay in `COM7021 - *` folders. This package never copies them.
- Lesson-scale public examples may use Anscombe or other non-assessed toy frames. EcoMove stays in the assignment folder.
- Palette hexes are not invented in prose. They freeze only after contrast notes and a rendered proof, except `arden`, which is already proven in COM7020/7021.

## Consequences

- Slower writing, fewer silent restyles.
- A later docs site (Quarto or similar) can compile this tree as-is.
- Course README points here; this README does not point at lecture PDFs.
