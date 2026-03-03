---
name: Bug Report
description: Report a reproducible bug or incorrect output in any SONARIS module
title: "[BUG] "
labels: ["bug", "needs-triage"]
assignees: []
---

## What Happened

Describe the bug clearly. State what you did, what you expected to happen, and what actually happened instead.

**Expected behavior:**


**Actual behavior:**


---

## Steps to Reproduce

Provide the minimum steps needed to reproduce the issue reliably.

1.
2.
3.

If the bug is triggered by specific input parameters (vessel dimensions, propeller geometry, URN spectrum values), include them here.

---

## Environment

| Field | Your value |
|---|---|
| Operating System | |
| Python version | |
| Virtual environment active? | Yes / No |
| SONARIS version or commit hash | |

**Relevant package versions** (paste output of `pip show packagename` for the packages involved):

```
paste here
```

**SONARIS module where the bug occurred:**

- [ ] Module 1: Design Input Engine
- [ ] Module 2: URN Prediction Core
- [ ] Module 3: IMO Compliance Checker
- [ ] Module 4: Marine Bioacoustic Impact Module
- [ ] Module 5: Mitigation Recommendation Engine
- [ ] Module 6: Open URN Database
- [ ] General / Setup / Dependencies

> If you are running Python 3.14, check whether the issue is a known incompatibility with a third-party library before filing. pyaudio and spectrum are not supported on Python 3.14 and have been intentionally removed from requirements.txt.

---

## Full Error Output

Paste the complete traceback here. Do not truncate it.

```
paste traceback here
```

---

## Additional Context

Add anything else that might help narrow down the cause: screenshots, links to related issues, input files, or specific parameter values that trigger the bug.

---

- [ ] I have searched the existing issues and this bug has not been reported before.