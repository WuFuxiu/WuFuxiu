#!/usr/bin/env python3
"""Update public GitHub events inside README markers (no external packages)."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import html
import json
import os
import re
from urllib.request import Request, urlopen

USERNAME = os.getenv("PROFILE_USERNAME", "WuFuxiu")
README = Path("README.md")
START = "<!-- ACTIVITY:START -->"
END = "<!-- ACTIVITY:END -->"


def fetch_events() -> list[dict]:
    req = Request(
        f"https://api.github.com/users/{USERNAME}/events/public?per_page=100",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Fuxiu-Profile-README-Activity",
            **({"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"} if os.getenv("GITHUB_TOKEN") else {}),
        },
    )
    with urlopen(req, timeout=25) as response:
        data = json.load(response)
    if not isinstance(data, list):
        raise RuntimeError("GitHub Events API returned an unexpected result")
    return data


def render_event(ev: dict) -> str | None:
    repo = str(ev.get("repo", {}).get("name", ""))
    if not repo or repo.casefold() == f"{USERNAME}/{USERNAME}".casefold():
        # Hide automatic updates of this profile repo to avoid noisy activity logs.
        return None
    kind = ev.get("type")
    payload = ev.get("payload") or {}
    labels = {
        "PushEvent": "⬆️ Pushed code / 推送代码",
        "CreateEvent": "🌱 Created a branch or repo / 创建分支或仓库",
        "PullRequestEvent": "🔀 Worked on a pull request / 参与拉取请求",
        "IssuesEvent": "📝 Worked on an issue / 参与 Issue",
        "IssueCommentEvent": "💬 Commented on an issue / 参与讨论",
        "WatchEvent": "⭐ Starred a repository / 收藏仓库",
        "ReleaseEvent": "🚀 Published a release / 发布版本",
        "ForkEvent": "🍴 Forked a repository / Fork 仓库",
    }
    label = labels.get(kind)
    if label is None:
        return None
    if kind == "WatchEvent" and payload.get("action") not in (None, "started"):
        return None
    stamp = (ev.get("created_at") or "")[:10]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamp):
        stamp = "recent"
    url = f"https://github.com/{repo}"
    repo_txt = html.escape(repo, quote=False)
    return f"- `{stamp}` · {label} · [{repo_txt}]({url})"


def update(readme: str, events: list[dict]) -> str:
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise RuntimeError("README activity markers missing or repeated")
    rows = []
    seen = set()
    for ev in events:
        line = render_event(ev)
        if line and line not in seen:
            seen.add(line)
            rows.append(line)
        if len(rows) >= 5:
            break
    if not rows:
        rows = ["> 暂无近期公开活动 / No recent public GitHub activity."]
    prefix, tail = readme.split(START, 1)
    _old, suffix = tail.split(END, 1)
    return prefix + START + "\n" + "\n".join(rows) + "\n" + END + suffix


def main() -> None:
    original = README.read_text(encoding="utf-8")
    updated = update(original, fetch_events())
    if original != updated:
        README.write_text(updated, encoding="utf-8")
        print("Updated recent activity in README.md")
    else:
        print("Recent activity unchanged")


if __name__ == "__main__":
    main()
