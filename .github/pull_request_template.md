<!--
Before submitting, link any related issue in the Description section below
by writing "Closes #issue_number" so GitHub auto-closes it on merge.
-->

## Description

<!-- What does this PR do and why? Be specific: what problem does it solve,
what approach was taken, and what alternatives were considered and ruled out. -->

Closes #

---

## PR Type

- [ ] Bug fix
- [ ] New feature
- [ ] Data contribution (URN database)
- [ ] Documentation update
- [ ] Model / algorithm improvement
- [ ] Performance improvement
- [ ] Tests
- [ ] Other (describe below)

---

## Modules Affected

- [ ] Module 1 — Design Input Engine
- [ ] Module 2 — URN Prediction Core
- [ ] Module 3 — IMO Compliance Checker
- [ ] Module 4 — Marine Bioacoustic Impact Module
- [ ] Module 5 — Mitigation Recommendation Engine
- [ ] Module 6 — Open URN Database
- [ ] General / Infrastructure

---

## Scientific Basis

<!-- Required if this PR changes any prediction algorithm, bioacoustic
calculation, compliance logic, or data processing pipeline.
Provide either a citation to a published paper or a clear technical
explanation of the methodology. If this PR does not touch any of the
above, write N/A. -->

**N/A**

---

## Testing

<!-- Describe what tests were run, what the results were, and whether any
edge cases were covered. Paste the relevant pytest output below. -->
```
# pytest output here
```

---

## Screenshots / Output

<!-- For UI changes or visualization updates: paste a screenshot.
For model or algorithm changes: paste a before/after metric comparison.
For data contributions: paste a sample row showing the expected data format.
Not applicable for documentation-only PRs. -->

---

## Pre-Merge Checklist

- [ ] Code follows PEP 8 and all new functions include type hints
- [ ] All new functions have docstrings (Google-style)
- [ ] `pytest` passes locally with no new failures
- [ ] No raw data files, `.pt` model weights, or `.env` files are included
- [ ] `CHANGELOG.md` updated under `[Unreleased]` with a summary of changes
- [ ] If any module algorithm or methodology was changed, a scientific reference
      or technical justification is provided in the Scientific Basis section above