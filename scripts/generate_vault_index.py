#!/usr/bin/env python3
"""Generate _vault_index.md and _stakeholder_map.md from Obsidian vault frontmatter."""

import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import frontmatter
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

VAULT_PATH = Path(os.environ.get("SA_KNOWLEDGE_PATH", "~/notes")).expanduser()
SA_KNOWLEDGE = VAULT_PATH / "SA_Knowledge"
ACCOUNTS_DIR = SA_KNOWLEDGE / "Accounts"
MEETINGS_DIR = SA_KNOWLEDGE / "Meetings"
TASKS_DIR = SA_KNOWLEDGE / "Tasks"

CANONICAL_ACCOUNTS = set()
VALID_MEETING_TYPES = {
    "sync", "workshop", "discovery", "qbr", "review",
    "escalation", "prep", "internal", "demo",
}
VALID_TASK_STATUSES = {"open", "in-progress", "blocked", "done", "cancelled"}

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

warnings = []


def warn(msg: str):
    warnings.append(msg)
    print(f"WARNING: {msg}", file=sys.stderr)


def extract_wikilink(value: str) -> str:
    if not value:
        return ""
    m = WIKILINK_RE.search(str(value))
    return m.group(1) if m else str(value).strip('"').strip("'")


def parse_date(value) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m"):
        try:
            return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return s


def load_accounts() -> dict:
    accounts = {}
    if not ACCOUNTS_DIR.is_dir():
        warn(f"Accounts directory not found: {ACCOUNTS_DIR}")
        return accounts

    for f in sorted(ACCOUNTS_DIR.glob("*.md")):
        CANONICAL_ACCOUNTS.add(f.stem)
        try:
            post = frontmatter.load(f)
        except Exception as e:
            warn(f"Failed to parse {f.name}: {e}")
            continue
        accounts[f.stem] = {
            "industry": post.get("Industry", ""),
            "tier": post.get("Account Tier", ""),
            "status": post.get("Status", ""),
            "primary_sa": post.get("Primary SA", ""),
            "last_updated": parse_date(post.get("Last Updated")),
            "region": post.get("region", ""),
            "segment": post.get("segment", ""),
        }
    return accounts


def load_meetings() -> list[dict]:
    meetings = []
    if not MEETINGS_DIR.is_dir():
        warn(f"Meetings directory not found: {MEETINGS_DIR}")
        return meetings

    for f in sorted(MEETINGS_DIR.glob("*.md")):
        try:
            post = frontmatter.load(f)
        except Exception as e:
            warn(f"Failed to parse {f.name}: {e}")
            continue

        company_raw = post.get("company", "")
        company = extract_wikilink(company_raw)

        if company and CANONICAL_ACCOUNTS and company not in CANONICAL_ACCOUNTS:
            warn(f"{f.name}: company '{company}' does not match any Account Blueprint")

        date = parse_date(post.get("date"))
        if not date:
            warn(f"{f.name}: missing 'date' field")

        meeting_type = post.get("type", "")
        if meeting_type and str(meeting_type).lower() not in VALID_MEETING_TYPES:
            warn(f"{f.name}: unknown type '{meeting_type}'")

        participants_raw = post.get("participants", [])
        participants = [extract_wikilink(p) for p in participants_raw if p]

        meetings.append({
            "filename": f.stem,
            "company": company,
            "date": date or "unknown",
            "type": str(meeting_type).lower() if meeting_type else "",
            "summary": post.get("summary", ""),
            "participants": participants,
        })
    return meetings


def load_tasks() -> list[dict]:
    tasks = []
    if not TASKS_DIR.is_dir():
        return tasks

    for f in sorted(TASKS_DIR.glob("*.md")):
        try:
            post = frontmatter.load(f)
        except Exception as e:
            warn(f"Failed to parse {f.name}: {e}")
            continue

        status = str(post.get("status", "open")).lower()
        if status not in VALID_TASK_STATUSES:
            warn(f"{f.name}: unknown status '{status}'")

        customer = extract_wikilink(post.get("customer", ""))
        if customer in ("Customer Name", ""):
            warn(f"{f.name}: placeholder or missing customer field")

        tasks.append({
            "filename": f.stem,
            "customer": customer,
            "project": extract_wikilink(post.get("project", "")),
            "status": status,
            "priority": post.get("priority", ""),
            "due_date": parse_date(post.get("due_date")),
        })
    return tasks


def build_stakeholder_map(meetings: list[dict]) -> dict:
    people = defaultdict(lambda: {"accounts": set(), "last_seen": "", "meeting_count": 0})

    for m in meetings:
        for p in m["participants"]:
            entry = people[p]
            if m["company"]:
                entry["accounts"].add(m["company"])
            entry["meeting_count"] += 1
            if m["date"] > entry["last_seen"]:
                entry["last_seen"] = m["date"]

    return dict(people)


def generate_vault_index(accounts, meetings, tasks) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "---",
        "generated: true",
        f"last_updated: {now}",
        "---",
        "",
        "# Vault Index",
        f"> Auto-generated on {now} by `scripts/generate_vault_index.py`",
        "",
    ]

    # Stats
    lines.append("## Statistics")
    lines.append(f"- **Accounts:** {len(accounts)}")
    lines.append(f"- **Meetings:** {len(meetings)}")
    open_tasks = [t for t in tasks if t["status"] not in ("done", "cancelled")]
    lines.append(f"- **Open Tasks:** {len(open_tasks)}")
    lines.append("")

    # Accounts
    lines.append("## Accounts")
    lines.append("")
    lines.append("| Account | Tier | Industry | SA | Status |")
    lines.append("|---------|------|----------|----|--------|")
    for name, a in sorted(accounts.items()):
        lines.append(f"| [[{name}]] | {a['tier']} | {a['industry']} | {a['primary_sa']} | {a['status']} |")
    lines.append("")

    # Meetings by account
    meetings_by_account = defaultdict(list)
    for m in meetings:
        key = m["company"] or "Unassigned"
        meetings_by_account[key].append(m)

    lines.append("## Meetings by Account")
    for account in sorted(meetings_by_account.keys()):
        lines.append(f"\n### {account}")
        lines.append("| Date | Type | Summary |")
        lines.append("|------|------|---------|")
        for m in sorted(meetings_by_account[account], key=lambda x: x["date"], reverse=True):
            summary = m["summary"] or "—"
            mtype = m["type"] or "—"
            lines.append(f"| {m['date']} | {mtype} | {summary} |")
    lines.append("")

    # Open tasks
    if open_tasks:
        lines.append("## Open Tasks")
        lines.append("")
        lines.append("| Task | Customer | Priority | Due Date | Status |")
        lines.append("|------|----------|----------|----------|--------|")
        for t in sorted(open_tasks, key=lambda x: x.get("due_date") or "9999"):
            lines.append(
                f"| {t['filename']} | {t['customer']} | {t['priority']} | {t['due_date'] or '—'} | {t['status']} |"
            )
        lines.append("")

    # Warnings
    if warnings:
        lines.append("## Consistency Warnings")
        lines.append("")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")

    return "\n".join(lines)


def generate_stakeholder_map(people: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "---",
        "generated: true",
        f"last_updated: {now}",
        "---",
        "",
        "# Stakeholder Map",
        f"> Auto-generated on {now} by `scripts/generate_vault_index.py`",
        "",
        "| Person | Accounts | Meetings | Last Seen |",
        "|--------|----------|----------|-----------|",
    ]

    sorted_people = sorted(people.items(), key=lambda x: x[1]["last_seen"], reverse=True)
    for name, info in sorted_people:
        accounts_str = ", ".join(sorted(info["accounts"]))
        lines.append(f"| [[{name}]] | {accounts_str} | {info['meeting_count']} | {info['last_seen']} |")

    lines.append("")
    return "\n".join(lines)


def main():
    if not SA_KNOWLEDGE.is_dir():
        print(f"ERROR: SA_Knowledge directory not found at {SA_KNOWLEDGE}", file=sys.stderr)
        print("Set SA_KNOWLEDGE_PATH in .env or environment", file=sys.stderr)
        sys.exit(1)

    accounts = load_accounts()
    meetings = load_meetings()
    tasks = load_tasks()
    people = build_stakeholder_map(meetings)

    vault_index = generate_vault_index(accounts, meetings, tasks)
    stakeholder_map = generate_stakeholder_map(people)

    index_path = SA_KNOWLEDGE / "_vault_index.md"
    index_path.write_text(vault_index, encoding="utf-8")
    print(f"Generated {index_path}")

    stakeholder_path = SA_KNOWLEDGE / "_stakeholder_map.md"
    stakeholder_path.write_text(stakeholder_map, encoding="utf-8")
    print(f"Generated {stakeholder_path}")

    if warnings:
        print(f"\n{len(warnings)} warnings found (see above)", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
