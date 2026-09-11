#!/usr/bin/env python3
"""CSES local workflow: sync the problem set, log in, and submit.

Usage:
    scripts/cses.py sync [--category CAT] [--delay SEC] [--dry-run]
    scripts/cses.py login
    scripts/cses.py whoami
    scripts/cses.py submit <problem-dir>
    scripts/cses.py fetch <cses-task-url> <problem-dir>
    scripts/cses.py celebrate
"""
from __future__ import annotations

import argparse
import getpass
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cses_lib import (
    CurlError,
    celebrate as do_celebrate,
    existing_problems,
    ensure_sol_cpp,
    env_credentials,
    fetch,
    fetch_problem,
    LIST_URL,
    load_dotenv,
    login as do_login,
    parse_problem_list,
    problem_dir_for,
    repo_root,
    slugify_category,
    submit_solution,
    whoami,
)


def cmd_fetch(args: argparse.Namespace) -> int:
    try:
        title, n = fetch_problem(args.url, args.dir)
    except Exception as e:  # noqa: BLE001
        print(f"error: could not fetch {args.url}: {e}", file=sys.stderr)
        return 1
    extra = f"{n} sample test(s)" if n else "no sample tests found"
    print(f"fetched: {title}  ({extra})")
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    print("listing CSES problem set …", flush=True)
    try:
        page = fetch(LIST_URL)
    except Exception as e:  # noqa: BLE001
        print(f"error: could not fetch problem list: {e}", file=sys.stderr)
        return 1
    tasks = parse_problem_list(page)
    if not tasks:
        print("error: parsed 0 problems from the list page", file=sys.stderr)
        return 1

    if args.category:
        want = args.category.replace("-", "_").lower()
        tasks = [
            t
            for t in tasks
            if t["category"] == want or slugify_category(t["section"]) == want
        ]
        if not tasks:
            print(f"error: no problems in category {args.category!r}", file=sys.stderr)
            return 1

    by_id = existing_problems()
    created = refreshed = failed = 0
    total = len(tasks)
    print(f"{total} problem(s) to sync", flush=True)

    for i, task in enumerate(tasks, start=1):
        dest = problem_dir_for(task, by_id)
        by_id.setdefault(task["id"], dest)
        rel = os.path.relpath(dest, repo_root())
        existed = os.path.isdir(dest) and os.path.isfile(os.path.join(dest, "statement.md"))
        prefix = f"[{i}/{total}] {rel}"

        if args.dry_run:
            action = "refresh" if existed else "create"
            print(f"{prefix}  ({action})  {task['url']}")
            continue

        try:
            os.makedirs(os.path.join(dest, "tests"), exist_ok=True)
            ensure_sol_cpp(dest)
            title, n = fetch_problem(task["url"], dest)
            by_id[task["id"]] = dest
            kind = "refresh" if existed else "create"
            if existed:
                refreshed += 1
            else:
                created += 1
            tests = f"{n} sample(s)" if n else "no samples"
            print(f"{prefix}  {kind}  {title}  ({tests})", flush=True)
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"{prefix}  ERROR  {e}", file=sys.stderr, flush=True)

        if i < total and args.delay > 0:
            time.sleep(args.delay)

    if args.dry_run:
        return 0
    print()
    print(f"created {created}, refreshed {refreshed}, failed {failed}")
    return 1 if failed else 0


def cmd_login(_args: argparse.Namespace) -> int:
    nick, password = env_credentials()
    if not nick:
        nick = input("CSES username: ").strip()
    if not password:
        password = getpass.getpass("CSES password: ")
    if not nick or not password:
        print("error: set CSES_NICK and CSES_PASS in .env, or type them at the prompt", file=sys.stderr)
        return 2
    try:
        name = do_login(nick, password)
    except Exception as e:  # noqa: BLE001
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"logged in as {name}")
    print("session stored in .cses/cookies.txt  (gitignored)")
    return 0


def cmd_whoami(_args: argparse.Namespace) -> int:
    name = whoami()
    if not name:
        print("not logged in — set CSES_NICK and CSES_PASS in .env, or run scripts/login.sh")
        return 1
    print(name)
    return 0


def cmd_submit(args: argparse.Namespace) -> int:
    path = args.dir
    if os.path.isfile(path) and path.endswith(".cpp"):
        path = os.path.dirname(path)
    if not os.path.isdir(path):
        print(f"error: not a problem directory: {args.dir}", file=sys.stderr)
        return 2
    try:
        return submit_solution(path, lang=args.lang, option=args.option)
    except CurlError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


def cmd_celebrate(args: argparse.Namespace) -> int:
    do_celebrate(args.title, args.score)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cses.py",
        description="Sync CSES problems locally, log in, and submit solutions.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch", help="fetch one problem's statement + sample tests")
    f.add_argument("url")
    f.add_argument("dir")
    f.set_defaults(func=cmd_fetch)

    s = sub.add_parser("sync", help="scaffold every CSES problem into problems/")
    s.add_argument(
        "--category",
        help="only this folder slug, e.g. introductory or sorting_and_searching",
    )
    s.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="seconds to wait between problem fetches (default 0.2)",
    )
    s.add_argument("--dry-run", action="store_true", help="print paths, don't write")
    s.set_defaults(func=cmd_sync)

    l = sub.add_parser("login", help="save a CSES session cookie (gitignored)")
    l.set_defaults(func=cmd_login)

    w = sub.add_parser("whoami", help="show the saved CSES username")
    w.set_defaults(func=cmd_whoami)

    u = sub.add_parser("submit", help="submit sol.cpp for a problem and poll the verdict")
    u.add_argument("dir", help="problem folder (or path to sol.cpp)")
    u.add_argument("--lang", default="C++")
    u.add_argument("--option", default="C++17", help="CSES compiler option (default C++17)")
    u.set_defaults(func=cmd_submit)

    c = sub.add_parser("celebrate", help="preview the ACCEPTED confetti animation")
    c.add_argument("--title", default="Trailing Zeros")
    c.add_argument("--score", default="13/13")
    c.set_defaults(func=cmd_celebrate)
    return p


def main() -> int:
    load_dotenv()
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
