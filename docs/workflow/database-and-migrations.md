# Database and Migrations

## Core commands

```bash
elric migrate             # upgrade to head
elric migrate status      # show current revision
elric migrate rollback    # rollback last migration
elric migrate fresh       # reset database and re-run migrations
```

## Creating migrations

```bash
elric make migration "add_messages_table"
```

Then apply:

```bash
elric migrate
```

## Practical rule

- Modify models first
- Generate migration
- Review migration
- Apply migration

