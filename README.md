# dotfiles

![macOS](https://img.shields.io/badge/platform-macOS-lightgrey?logo=apple)
![Linux](https://img.shields.io/badge/platform-Ubuntu%20%7C%20Debian-orange?logo=ubuntu)
![Neovim](https://img.shields.io/badge/Neovim-0.11+-green?logo=neovim)
![Managed with Stow](https://img.shields.io/badge/managed_with-GNU_Stow-blue)

My dotfiles I utilize as a Platform Engineer

Managed with [GNU Stow](https://www.gnu.org/software/stow/).

## Contents

- **nvim** — Neovim config built on LazyVim
- **ghostty** — Ghostty terminal config
- **claude** — Claude Code custom agents and skills
- **zsh** — zsh with oh-my-zsh and Powerlevel10k
- **herdr** — Herdr terminal multiplexer config

## Prerequisites

- [GNU Stow](https://www.gnu.org/software/stow/) — `brew install stow`
- [Neovim](https://neovim.io/) v0.11+ — `brew install neovim`
- [Ghostty](https://ghostty.org/) — terminal emulator
- [oh-my-zsh](https://ohmyz.sh/) — `sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`
- [Powerlevel10k](https://github.com/romkatv/powerlevel10k) — `brew install powerlevel10k`
- [Claude Code](https://claude.ai/code) — `curl -fsSL https://claude.ai/install.sh | bash` or `brew install --cask claude-code`
- [Herdr](https://herdr.dev) — terminal agent multiplexer — `brew install herdr`

## Quick Start

```sh
git clone https://github.com/cwaits6/dotfiles ~/.dotfiles
~/.dotfiles/install.sh
exec zsh
```

`install.sh` is safe to re-run. It:

- **macOS:** installs everything in the `Brewfile`, then stows `zsh nvim ghostty claude herdr`.
- **Ubuntu/Debian:** installs `zsh stow git curl zoxide` with apt and a current `fzf`, then stows `zsh`.
- **Both:** installs oh-my-zsh, Powerlevel10k and the zsh plugins, backs up any existing dotfiles it would replace (`*.bak.<timestamp>`), and sets zsh as the default shell.

Steps that fail (for example, a tool blocked on a work machine) are skipped and listed at the end.

## Manual stow

```sh
cd ~/.dotfiles
stow nvim ghostty claude zsh
stow --no-folding herdr
```
