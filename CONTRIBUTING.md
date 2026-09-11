# Contributing

Thanks for helping with this unofficial CSES toolkit. Please be polite to CSES
(keep the sync delay) and never commit `.env`, `.cses/`, or `problems/`.

## Prerequisites

macOS or Linux with `g++`, `python3`, and `curl`. No pip packages.

```bash
git clone https://github.com/YOUR_USER/cses-kit.git
cd cses-kit
chmod +x cses scripts/run.sh
cp .env.example .env   # only if you will submit
```

Until `cses` is on your `PATH`, run `./cses` from the repo root.

## How to run the project

```bash
./cses sync --category introductory
./cses run trailing-zeroes
./cses submit trailing-zeroes
```

See the README for Python (`sol.py`), login, and install.

## How to run tests

From the repo root (stdlib `unittest` only):

```bash
python3 -m unittest discover -s tests -v
```

CI runs the same command. Add or update tests when you change behavior.

## Workflow

1. **Fork** the repository on GitHub.
2. **Clone** your fork.
3. **Branch** from `main`: `git checkout -b feat/short-name`.
4. **Change** only what the issue/PR needs.
5. **Tests:** run the command above; extend `tests/` for new behavior.
6. **PR** against `main`. Fill in the PR template.

Prefer stdlib + `curl`. If you need a new dependency, explain why in the PR.

## Pull requests

- Tests added or updated when behavior changes.
- `python3 -m unittest discover -s tests -v` passes.
- README / CONTRIBUTING updated if the CLI or setup changed.
- No unrelated files, secrets, or CSES problem statements.

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
