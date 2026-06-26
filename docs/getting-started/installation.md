# Installation

## Install Elric CLI

Recommended:

```bash
pipx install elric-cli
```

Alternative:

```bash
uv tool install elric-cli
```

Verify installation:

```bash
elric --help
```

---

## Requirements for Project Runtime

A generated Elric project expects:

- Python 3.12+
- Docker (for PostgreSQL and Redis in local development)
- `uv` package manager

