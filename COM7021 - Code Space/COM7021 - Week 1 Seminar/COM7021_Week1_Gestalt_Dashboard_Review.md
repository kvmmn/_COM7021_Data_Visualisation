# COM7021 Week 1 Task 1: Gestalt Principles and Visual Design

**Module:** COM7021SCC  
**Activity:** Seminar review of a student performance dashboard  
**Audience:** University management team  
**Student ID:** 25199053

The dashboard mixes attendance, assessment marks, submission status, engagement, and academic support. The review below selects three of the listed design issues, names the Gestalt principle at work, states what a manager is likely to misread, and proposes a concrete change. One improvement is then stress-tested, and a single pre-presentation change is chosen.

## Three issues

| Issue | Gestalt principle | Problem for the viewer | Suggested improvement |
|---|---|---|---|
| 1. Similar information is presented using different colours and styles. | **Similarity.** Viewers group items that share colour, shape, or style, and treat items that look different as different categories. | A manager may think two attendance views (or two mark views) are unrelated metrics, or that a style change marks a different status. They may also fail to scan related fields as one story. | Encode each measure type with one consistent visual language: one colour and mark style for attendance, one for marks, one for submission status, and so on. Reserve a separate, unused colour for alerts. |
| 2. Some unrelated charts are grouped together in the same panel. | **Common region** (with **proximity**). Items inside the same border or cluster are read as belonging together. | The viewer may assume a causal or sequential link that the data do not support, for example treating engagement and academic-support charts as one process. They may also miss the intended comparison because the panel mixes questions. | Put each panel around one management question (for example “who is at risk this week”). Separate unrelated charts with whitespace and headings. Do not share a box unless the measures answer the same question. |
| 3. Warning indicators do not stand out clearly from normal information. | **Figure–ground.** The important signal should separate from the background so it is seen first. | At-risk cases can be treated as ordinary variation. On a busy dashboard this is the most costly miss: a student who needs intervention looks like everyone else. | Give warnings a single reserved treatment: stronger contrast, a distinct hue not used elsewhere, slightly larger marks, and a small isolated “exceptions” strip at the top. Keep routine KPIs quieter so alerts become the figure. |

## Challenge one solution

**Chosen improvement:** grouping charts by management question (issue 2).

**Could this create another problem?**  
Yes. Stronger grouping can invent a relationship. If attendance and assessment marks sit in one “performance” panel, a manager may read attendance as the cause of marks, or treat a combined colour scale as one risk score. That is the same Gestalt mechanism (common region and proximity) working against the data.

**How to avoid this?**  
Group only where the question is shared, not where the variables merely feel academic. Label the panel with the question, not a vague title such as “Overview”. Keep axes, units, and time windows explicit so two charts in one area are still read as two measures. Do not add arrows, shared colour legends, or a single summary number unless that relationship has been defined. If two measures must appear nearby for convenience, use a light divider and a one-line note that they are shown together for comparison, not as a proven link.

## Final decision: one change before presentation

**Priority change:** make warning indicators visually distinct from routine information (figure–ground).

**Why this one?**  
A management dashboard is used under time pressure. Inconsistent styling and messy grouping cause confusion, but a missed warning causes a wrong action (or no action). If only one change is allowed, the first job is that exceptions are seen. A reserved alert style at the top of the page does not require a full redesign, and it reduces the chance that colour, clutter, or nearby charts bury the students who need support.

The other two issues still matter. After the briefing, I would next standardise encodings (similarity) and then split unrelated panels, taking care not to imply false relationships.

## Ready to share (60 seconds)

- **Most important issue:** warnings do not stand out from normal information.
- **Gestalt principle:** figure–ground (the alert should be the figure; routine KPIs should recede).
- **Change:** one reserved, high-contrast exception treatment, isolated at the top, not reused for ordinary categories.
- **Why it improves the visualisation:** managers notice at-risk students first, which is the decision the dashboard is for. Grouping and consistent styling can follow, but only if they do not invent relationships the data do not support.
