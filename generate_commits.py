#!/usr/bin/env python3
"""
Daily Random Contribution Generator
Generates a random number of commits (default 20-25) spread naturally across the day.
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
]


def run_command(cmd, env=None):
    result = subprocess.run(cmd, env=env, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error executing {' '.join(cmd)}: {result.stderr}", file=sys.stderr)
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def generate_commits(min_commits=20, max_commits=25, target_date=None):
    if target_date is None:
        target_date = datetime.datetime.now(datetime.timezone.utc).date()

    count = random.randint(min_commits, max_commits)
    print(f"Generating {count} random commits for date: {target_date}")

    # Generate `count` distinct ascending times between 08:30 and 22:30 (in seconds from midnight)
    start_sec = 8 * 3600 + 30 * 60  # 08:30
    end_sec = 22 * 3600 + 30 * 60    # 22:30

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

        # Stage and commit with custom date
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

    print(f"\nSuccessfully generated {count} commits.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate daily git contributions.")
    parser.add_argument("--min", type=int, default=20, help="Minimum commits (default: 20)")
    parser.add_argument("--max", type=int, default=25, help="Maximum commits (default: 25)")
    parser.add_argument("--date", type=str, default=None, help="Target date YYYY-MM-DD (default: today)")

    args = parser.parse_args()

    date_obj = None
    if args.date:
        date_obj = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()

    generate_commits(min_commits=args.min, max_commits=args.max, target_date=date_obj)
