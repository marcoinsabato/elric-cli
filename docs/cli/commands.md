# CLI Commands

## Root commands

```bash
elric --help
elric new <project_name>
elric serve
elric migrate
elric route list
elric apikey --help
elric make --help
```

## `elric make`

```bash
elric make agent <Name> [--type=simple|chat|tool|react|planner|streaming] [--model=<model>]
elric make chain <Name>
elric make tool <Name>
elric make route <Name>
elric make controller <Name>
elric make schema <Name>
elric make model <Name>
elric make migration "<description>"
elric make job <Name>
elric make exception <Name>
elric make test <Name>
```

## Migrations

```bash
elric migrate
elric migrate status
elric migrate rollback
elric migrate fresh
```

## API keys

```bash
elric apikey create "My Service"
elric apikey list
elric apikey revoke <key-id>
```

