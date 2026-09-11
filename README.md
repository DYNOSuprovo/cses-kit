# CSES kit

Unofficial toolkit to fetch [CSES](https://cses.fi/problemset/) statements, test
a solution locally, and submit from the terminal. Not affiliated with CSES, and
not the University of Helsinki [cses-cli](https://github.com/csesfi/cses-cli).

C++17 is the only language wired today. The point of publishing this is so
others can add languages, templates, and features (progress, leaderboard, …)
without each person rebuilding the scrape/login/submit loop.

Problem statements belong to CSES and are **not** in this repo. After cloning,
run `./scripts/sync.sh` to download them into `problems/`.

## Setup

macOS or Linux with `g++`, `python3`, and `curl`. Nothing else to install.

```bash
chmod +x scripts/*.sh
cp .env.example .env    # only needed to submit
```

`.env` (gitignored):

```
CSES_NICK=your_username
CSES_PASS=your_password
```

On macOS, `include/bits/stdc++.h` is a small shim so `#include <bits/stdc++.h>`
works with Apple clang.

## Usage

```bash
./scripts/sync.sh                                    # all problems
./scripts/sync.sh --category introductory            # one section
./scripts/new.sh introductory missing-number https://cses.fi/problemset/task/1083

./scripts/run.sh problems/introductory/missing-number
./scripts/run.sh problems/introductory/missing-number -i   # type input by hand

./scripts/submit.sh problems/introductory/trailing-zeroes
```

Each problem is `problems/<category>/<slug>/`:

- `sol.cpp` — your code (copied from `template.cpp` on first sync)
- `statement.md` — fetched statement
- `tests/*.in` / `tests/*.out` — **sample** cases from the public page (not hidden tests)

`sync.sh` never overwrites an existing `sol.cpp`. Re-run it when CSES adds tasks.

`submit.sh` posts `sol.cpp` as C++17, prints the verdict, and writes it into
`statement.md`. On **ACCEPTED** the terminal plays a short confetti animation
(`python3 scripts/cses.py celebrate` to preview; `CSES_NO_ANIM=1` to skip).
On a failed judge run it prints the **first failing test** (input / expected /
got) and writes a summary plus failed-test details to `last-submit.txt` in that
problem folder. Passed tests are listed by id only.

In VS Code / Cursor, open `sol.cpp` and press **Cmd+Shift+B** to run local tests,
or **Run Task → CSES: submit current problem**.

## Testing notes

- `run.sh` uses `-std=gnu++17 -O2` plus AddressSanitizer and UBSan.
- Output compare ignores trailing whitespace, like CSES.
- Sanitizer timings are slower than a real submission.

## Contributing

PRs are welcome. Useful directions:

- **Languages** — detect `sol.py` / `sol.rs` / …, compile or run them locally, and
  map CSES `lang` / `option` on submit. Keep C++17 working as the default.
- **Templates** — extra starters under something like `templates/<lang>/`, used
  when `sync.sh` first creates a folder.
- **Features** — `status` (solved vs remaining), next unsolved, stress tests,
  a local TLE timeout, or a **leaderboard / profile** view from the public CSES
  pages. Say in the PR if you add network calls or new dependencies.

Please keep `.env`, `.cses/`, and `problems/` out of git. Prefer the existing
stdlib + `curl` stack; if you need a package, say why. Leave the 0.2s delay
(or gentler) on bulk fetches so CSES is not hammered.

## License

MIT for this tooling. CSES content remains © its authors; fetch it yourself.
