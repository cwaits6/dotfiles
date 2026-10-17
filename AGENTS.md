# AGENTS.md

Personal dotfiles for macOS (daily driver) and Ubuntu/Debian servers, managed with GNU Stow.
This repo is **public on GitHub**.

## Layout

- Each top-level directory (`zsh/`, `nvim/`, `ghostty/`, `claude/`, `herdr/`) is a stow package that mirrors `$HOME`.
- `install.sh` bootstraps a machine: packages, oh-my-zsh + theme + plugins, stow links, default shell.
- `Brewfile` lists the macOS Homebrew taps, formulae and casks that `install.sh` installs.

## Keep install.sh in sync

Any change that adds or removes a dependency must update `install.sh` in the same change:

- New stow package → add it to `PACKAGES` for the OSes it applies to.
- New oh-my-zsh custom plugin or theme → add a `try ... clone` line.
- New tool referenced from the zsh config → add it to the `Brewfile` (macOS) and, if it's needed on servers, to the apt list or its own install function (Linux).
- Removed tools → remove them from `install.sh` and the `Brewfile` too.

Update `README.md` when the setup steps change.

To refresh the `Brewfile` after installing things with brew:

```sh
brew bundle dump --file=Brewfile --force && grep -vE '^(vscode|go|uv|krew) ' Brewfile > Brewfile.tmp && mv Brewfile.tmp Brewfile
```

## Rules for install.sh

- **Idempotent:** re-running must be safe. Check before acting, and use `clone()` and `stow --restow`.
- **Never block on one tool:** wrap optional steps in `try "<name>" <command>`. Work machines may block some installs; the script should finish and list what it skipped.
- **Bash 3.2 compatible** (macOS `/bin/bash`): no associative arrays, `mapfile`, or `${var,,}`.
- Keep it short and readable. Prefer one clear function over clever one-liners.

## Rules for the zsh config

- It must load cleanly on macOS and Linux, with or without any optional tool installed.
- Guard every external tool: `if command -v foo >/dev/null 2>&1; then ...; fi`.
- Guard every sourced file: `[[ -r file ]] && source file`.
- Secrets live in `~/.zshrc.private`, which is never committed. Never add tokens, keys or hostnames that reveal private infrastructure to this repo.

## Checks before committing

```sh
bash -n install.sh && zsh -n zsh/.zshrc && zsh -n zsh/.zprofile
command -v shellcheck >/dev/null && shellcheck install.sh
```
