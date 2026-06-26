# Building Features with the CLI

Use generators to keep structure consistent and avoid manual scaffolding mistakes.

## Typical feature flow

```bash
# 1) create route + controller + schema
elric make route Chat
elric make controller ChatController
elric make schema CreateChatRequest

# 2) if data is needed
elric make model Message
elric make migration "add_messages_table"

# 3) apply migration
elric migrate

# 4) inspect routes
elric route list
```

## AI feature flow

```bash
elric make agent ResearchAssistant --type=tool --model=gpt-4o
elric make tool WebSearchTool
elric make chain SummarizeChain
```

