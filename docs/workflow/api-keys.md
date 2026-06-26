# API Keys and Security Flow

## Commands

```bash
elric apikey create "Internal Service"
elric apikey list
elric apikey revoke <key-id>
```

## Development defaults

In development, docs are accessible and you can decide whether API key middleware is enabled via `.env`.

Key setting:

```env
API_KEY_ENABLED=false
```

Set to `true` when you want to test protected endpoints.

