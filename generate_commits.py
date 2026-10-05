#!/usr/bin/env python3
"""
Daily Contribution Generator
Generates a random number of commits (default 70-75) with past timestamps
so they immediately reflect on today's GitHub contribution graph.
"""

import argparse
import datetime
import os
import random
import subprocess
import sys

MESSAGES = [
    "chore(activity): update daily activity metric",
    "refactor(core): streamline routine logging process",
    "docs(log): record daily performance statistics",
    "perf(tracker): improve daily event indexing",
    "fix(data): normalize activity record formatting",
    "feat(monitor): track daily contribution cadence",
    "style: format activity ledger records",
    "test: verify activity timestamp sequence",
    "chore(deps): maintain routine status healthcheck",
    "build: update routine telemetry bundle",
    "chore(audit): sync daily progress checkpoint",
    "refactor(metric): refine routine snapshot parser",
    "docs: clarify daily workflow documentation",
    "perf: optimize log append throughput",
    "feat(analytics): record daily event stream",
    "chore(cleanup): prune obsolete telemetry buffer",
    "fix(runtime): ensure clean record boundary",
    "style: reformat activity ledger entries",
    "chore(sync): reconcile daily ledger state",
    "feat(telemetry): capture routine heartbeat entry",
    "chore(health): record heartbeat ping status",
    "perf(engine): optimize telemetry flush buffer",
    "docs(ledger): document daily activity cycle",
    "fix(stream): stabilize activity journal sequence",
    "refactor(sync): consolidate telemetry dispatch",
    "test(metric): validate routine record consistency",
    "style(clean): organize activity journal entries",
    "build(ci): refresh routine build artifacts",
    "chore(bench): checkpoint daily activity benchmark",
    "feat(stats): capture aggregated daily activity",
]


def run_command(cmd, env=None):
    result = subprocess.run(cmd, env=env, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error executing {' '.join(cmd)}: {result.stderr}", file=sys.stderr)
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def generate_commits(min_commits=70, max_commits=75, target_date=None):
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    if target_date is None:
        target_date = now_utc.date()

    count = random.randint(min_commits, max_commits)
    print(f"Generating {count} commits for date: {target_date}")

    # Ensure all timestamps are strictly in the PAST so GitHub immediately counts them
    if target_date == now_utc.date():
        current_sec = now_utc.hour * 3600 + now_utc.minute * 60 + now_utc.second
        end_sec = max(count * 15, current_sec - 15)
        start_sec = max(0, min(3600, end_sec - count * 60))
        if end_sec - start_sec <= count:
            start_sec = max(0, end_sec - count * 15)
    else:
        start_sec = 1800  # 00:30 UTC
        end_sec = 23 * 3600  # 23:00 UTC

    if (end_sec - start_sec) < count:
        end_sec = start_sec + count + 20

    # Pick `count` ascending random timestamps strictly before end_sec
    sampled_seconds = sorted(random.sample(range(start_sec, end_sec), count))

    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "activity.log")

    base_env = os.environ.copy()
    user_name = "isreeharim"
    user_email = "isreeharim@gmail.com"

    for idx, sec in enumerate(sampled_seconds, start=1):
        commit_dt = datetime.datetime.combine(
            target_date,
            datetime.time(hour=sec // 3600, minute=(sec % 3600) // 60, second=sec % 60),
            tzinfo=datetime.timezone.utc,
        )
        iso_time = commit_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        readable_time = commit_dt.strftime("%Y-%m-%d %H:%M:%S UTC")

        msg = random.choice(MESSAGES)
        commit_title = f"{msg} [#{idx}/{count}] [skip ci]"

        # Append to activity.log
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(f"[{readable_time}] {commit_title}\n")

        # Stage and commit with custom date in the past
        commit_env = base_env.copy()
        commit_env["GIT_AUTHOR_DATE"] = iso_time
        commit_env["GIT_COMMITTER_DATE"] = iso_time
        commit_env["GIT_AUTHOR_NAME"] = user_name
        commit_env["GIT_AUTHOR_EMAIL"] = user_email
        commit_env["GIT_COMMITTER_NAME"] = user_name
        commit_env["GIT_COMMITTER_EMAIL"] = user_email

        run_command(["git", "add", log_file_path])
        run_command(["git", "commit", "-m", commit_title], env=commit_env)
        print(f"  [{idx}/{count}] Committed at {readable_time}: {commit_title}")

    print(f"\nSuccessfully generated {count} commits (all strictly in the past).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate daily git contributions.")
    parser.add_argument("--min", type=int, default=70, help="Minimum commits (default: 70)")
    parser.add_argument("--max", type=int, default=75, help="Maximum commits (default: 75)")
    parser.add_argument("--count", type=int, default=None, help="Exact commit count (overrides min and max)")
    parser.add_argument("--date", type=str, default=None, help="Target date YYYY-MM-DD (default: today)")

    args = parser.parse_args()

    min_c = args.min
    max_c = args.max
    if args.count is not None:
        min_c = args.count
        max_c = args.count

    date_obj = None
    if args.date:
        date_obj = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()

    generate_commits(min_commits=min_c, max_commits=max_c, target_date=date_obj)
