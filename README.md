# DevPulse MCP Server

Activity Intelligence для Claude Code. Логирование сессий работы.

## Установка

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
| `list_projects` | Список проектов |

## Использование

```
> Залогируй: FINANCE, проблема DPO 526 дней, причина all-time vs год...

> Что я делал вчера?

> Дневной отчёт

> Список проектов
```

## Структура

Все логи в **общей папке** `~/.devpulse/`:

```
~/.devpulse/
├── sessions/
│   ├── FINANCE_2026-01-14_10-30_dpo-fix.md
│   ├── B2C_2026-01-14_12-00_chat.md
│   └── CRM_2026-01-14_15-30_api.md
└── reports/
    └── daily/
        └── 2026-01-14.md
```

Готово для синхронизации с облаком.

---
DevPulse · Activity Intelligence for Tech Leads
