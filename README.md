# Elric CLI

Official CLI for bootstrapping and managing Elric projects.

## Installation

After publishing on PyPI:

```bash
pipx install elric-cli
# or
uv tool install elric-cli
```

Upgrade:

```bash
pipx upgrade elric-cli
# or
uv tool upgrade elric-cli
```

## Quick Start

```bash
elric --help
elric new my_app
cd my_app
uv sync
```

`elric new` always uses the official template repository:

- `https://github.com/marcoinsabato/elric-template.git`

## Main Commands

```bash
elric new my_app
elric make agent ResearchAssistant --type=tool --model=gpt-4o
elric make route Chat
elric migrate
elric route list
elric apikey create "My App"
elric serve
```

## Release to PyPI

Automatic publishing is configured via GitHub Actions on tags matching `v*`.

Typical release flow:

```bash
# update version in pyproject.toml
# commit and push main

git tag v1.0.1
git push origin v1.0.1
```

The workflow publishes to PyPI using the `PYPI_API_TOKEN` repository secret.

## Local Development

```bash
uv sync
uv run elric --help
```
