# Data Persistence Repositories — Design

## Goal
Extend the existing MVC `Item` CRUD app with concrete `Repository` implementations
that persist to CSV, JSON, and SQLite, alongside the existing `InMemoryRepository`.

## Scope
- `model/repository.py`: add `CsvRepository`, `JsonRepository`, `SqliteRepository`,
  each implementing the existing `Repository` ABC (`add`, `get`, `list_all`,
  `update`, `delete`). `InMemoryRepository` stays as-is.
- `main.py` (new, project root): wires one repository (hardcoded, swappable via
  comment) + `controller/item_controller.py` + `view/console_view` module.
- `tests/test_repositories.py` (new): pytest, parametrized across all four
  repository implementations, using `tmp_path` for file-backed ones.

## Repository details

| Class | Backing file (default) | id strategy | stdlib module |
|---|---|---|---|
| `CsvRepository` | `data/items.csv` | in-memory `next_id = max(ids)+1`, full rewrite per mutation | `csv` |
| `JsonRepository` | `data/items.json` | in-memory `next_id = max(ids)+1`, full rewrite per mutation | `json` |
| `SqliteRepository` | `data/items.db` | DB-native `INTEGER PRIMARY KEY AUTOINCREMENT` | `sqlite3` |

Common behavior:
- Constructor takes an optional `path` (defaults to `data/items.<ext>`), creates
  the parent directory if missing.
- CSV/JSON: load full contents into an in-memory `dict[int, Item]` on init;
  every `add`/`update`/`delete` rewrites the whole file. No partial-write
  optimization — data set is small, simplicity wins.
- SQLite: no in-memory cache; every operation is a direct query against the DB
  file, relying on SQLite's own consistency guarantees.
- `update`/`delete` raise `KeyError` for an unknown id, matching
  `InMemoryRepository`'s existing contract.

## main.py
```python
from controller.item_controller import ItemController
from model.repository import CsvRepository  # swap for JsonRepository / SqliteRepository / InMemoryRepository
from view import console_view

if __name__ == "__main__":
    ItemController(CsvRepository(), console_view).run()
```

## Testing
`tests/test_repositories.py` — pytest, `@pytest.mark.parametrize` over factory
functions for the three file-backed repos (using `tmp_path`) plus
`InMemoryRepository`. Shared scenario per repo: add → get → list_all → update →
delete, plus a reload-from-disk check for the file-backed ones (new instance
pointed at the same path sees persisted data).

## Out of scope
- No CLI flag / env var to choose backend (hardcoded in `main.py` per user
  choice).
- No connection pooling, migrations, or schema versioning for SQLite.
- No pickle-based storage (explicitly declined).
