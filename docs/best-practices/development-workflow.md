# Development Workflow

## Recommended loop

1. Generate component with CLI
2. Implement logic
3. Run migrations if schema changed
4. Run app locally
5. Verify endpoint behavior

## Suggested command sequence

```bash
elric make route Chat
elric make controller ChatController
elric make schema CreateChatRequest
elric route list
elric migrate
elric serve
```

