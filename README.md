# Elric CLI

CLI ufficiale per creare e gestire progetti Elric.

## Installazione

### Con pipx (consigliato)

```bash
pipx install elric-cli
```

### Con uv tool

```bash
uv tool install elric-cli
```

## Comandi principali

```bash
elric --help
elric new my_app --template https://github.com/marcoinsabato/elric-template.git
```

Dentro un progetto Elric puoi usare anche:

```bash
elric make agent ResearchAssistant --type=tool --model=gpt-4o
elric make route Chat
elric migrate
elric route list
elric apikey create "My App"
elric serve
```

## Template repository

Il comando `elric new` usa:

- `--template <git-url>`
- oppure la variabile ambiente `ELRIC_TEMPLATE_REPO`

Esempio:

```bash
export ELRIC_TEMPLATE_REPO=https://github.com/marcoinsabato/elric-template.git
elric new my_app
```

## Sviluppo locale

```bash
uv sync
uv run elric --help
```
