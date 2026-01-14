# DevPulse MCP Server

Activity Intelligence для Claude Code. Логирование сессий работы.

## Установка в Claude Code

Добавь в `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "devpulse": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/ingadev/devpulse-mcp", "devpulse-mcp"]
    }
  }
}
```

Перезапусти Claude Code.

## Tools

| Tool | Описание |
|------|----------|
| `log_session` | Сохранить итоги сессии |
| `get_sessions` | Получить логи за период |
| `daily_report` | Дневной отчёт |
| `what_i_did` | Что делал (today/yesterday/week/PROJECT) |

## Использование

```
> Залогируй: FINANCE, проблема DPO 526 дней, причина all-time vs год, сделал period filter, результат 321 день

> Что я делал вчера?

> Дневной отчёт
```

## Структура логов

```
./project/
├── .devpulse/
│   ├── sessions/
│   │   └── FINANCE_2026-01-14_10-30_dpo-fix.md
│   └── reports/daily/
│       └── 2026-01-14.md
└── ...
```

Добавь `.devpulse/` в `.gitignore`.

---
DevPulse · Activity Intelligence for Tech Leads
