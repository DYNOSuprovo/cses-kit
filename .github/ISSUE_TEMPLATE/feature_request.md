---
name: Feature request
about: Propose a change to the unofficial CSES CLI
title: "[feat] "
labels: enhancement
---

**Problem**

What is awkward or missing in the current workflow?

**Proposal**

What should `cses` do? Name the command or files you would touch if you know them
(`scripts/cses_lib.py`, `scripts/run.sh`, templates, …).

**Scope**

- Languages: C++17 must keep working
- Prefer stdlib + `curl` (no new pip deps unless justified)
- Do not scrape CSES faster than the existing sync delay
- Do not commit `.env`, cookies, or `problems/`
