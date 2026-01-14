#!/usr/bin/env python3
"""DevPulse MCP Server - Activity Intelligence for Claude Code"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("devpulse")

def get_devpulse_dir() -> Path:
    return Path.cwd() / ".devpulse"

def ensure_dirs():
    d = get_devpulse_dir()
    (d / "sessions").mkdir(parents=True, exist_ok=True)
    (d / "reports" / "daily").mkdir(parents=True, exist_ok=True)

@mcp.tool()
def log_session(project: str, problem: str, cause: str, done: list[str], result: str, remaining: Optional[str] = None, team_tasks: Optional[str] = None, topic: Optional[str] = None) -> str:
    """Сохранить итоги сессии. project: название, problem: что сломано, cause: почему, done: список изменений, result: было->стало"""
    ensure_dirs()
    now = datetime.now()
    filename = f"{project}_{now.strftime('%Y-%m-%d_%H-%M')}_{topic or 'session'}.md"
    filepath = get_devpulse_dir() / "sessions" / filename
    content = f"## ПРОЕКТ: {project}\n\n### БЫЛО\n{problem}\n\n### ПРИЧИНА\n{cause}\n\n### СДЕЛАНО\n"
    for item in done:
        content += f"- {item}\n"
    content += f"\n### РЕЗУЛЬТАТ\n{result}\n"
    if remaining:
        content += f"\n### ОСТАЛОСЬ\n{remaining}\n"
    if team_tasks:
        content += f"\n### ЗАДАЧИ ДРУГИМ\n{team_tasks}\n"
    filepath.write_text(content, encoding="utf-8")
    return f"✅ {filepath}"

@mcp.tool()
def get_sessions(date: Optional[str] = None, project: Optional[str] = None, days: int = 1) -> str:
    """Получить логи. date: YYYY-MM-DD, project: фильтр, days: дней назад"""
    sessions_dir = get_devpulse_dir() / "sessions"
    if not sessions_dir.exists():
        return "Нет сессий"
    dates = [date] if date else [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    results = []
    for f in sorted(sessions_dir.glob("*.md"), reverse=True):
        if not any(d in f.name for d in dates):
            continue
        if project and not f.name.startswith(project):
            continue
        results.append(f"### {f.name}\n{f.read_text(encoding='utf-8')}")
    return "\n---\n".join(results) if results else "Нет сессий за период"

@mcp.tool()
def daily_report(date: Optional[str] = None) -> str:
    """Дневной отчёт. date: YYYY-MM-DD"""
    ensure_dirs()
    target = date or datetime.now().strftime("%Y-%m-%d")
    sessions_dir = get_devpulse_dir() / "sessions"
    if not sessions_dir.exists():
        return "Нет сессий"
    projects, count = {}, 0
    for f in sessions_dir.glob(f"*{target}*.md"):
        count += 1
        proj = f.name.split("_")[0]
        projects.setdefault(proj, []).append(f.read_text(encoding="utf-8"))
    if not projects:
        return f"Нет сессий за {target}"
    report = f"# Отчёт за {target}\n\nСессий: {count}, Проектов: {len(projects)}\n"
    for p, s in projects.items():
        report += f"\n## {p}\n" + "\n".join(s)
    (get_devpulse_dir() / "reports" / "daily" / f"{target}.md").write_text(report)
    return report

@mcp.tool()
def what_i_did(period: str = "today") -> str:
    """Что делал. period: today/yesterday/week/PROJECT"""
    if period in ("yesterday", "вчера"):
        return get_sessions(date=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))
    if period in ("week", "неделя"):
        return get_sessions(days=7)
    if period not in ("today", "сегодня"):
        return get_sessions(days=30, project=period.upper())
    return get_sessions(days=1)

if __name__ == "__main__":
    mcp.run()
