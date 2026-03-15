# dotfiles

![macOS](https://img.shields.io/badge/platform-macOS-lightgrey?logo=apple)
![Neovim](https://img.shields.io/badge/Neovim-0.11+-green?logo=neovim)
![Managed with Stow](https://img.shields.io/badge/managed_with-GNU_Stow-blue)

My dotfiles I utilize as a Platform Engineer

Managed with [GNU Stow](https://www.gnu.org/software/stow/).

## Contents

- **nvim** — Neovim config built on LazyVim
- **ghostty** — Ghostty terminal config
- **claude** — Claude Code custom agents and skills
- **zsh** — zsh with oh-my-zsh and Powerlevel10k

## Prerequisites

- [GNU Stow](https://www.gnu.org/software/stow/) — `brew install stow`
- [Neovim](https://neovim.io/) v0.11+ — `brew install neovim`
- [Ghostty](https://ghostty.org/) — terminal emulator
- [oh-my-zsh](https://ohmyz.sh/) — `sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`
- [Powerlevel10k](https://github.com/romkatv/powerlevel10k) — `brew install powerlevel10k`
- [Claude Code](https://claude.ai/code) — `curl -fsSL https://claude.ai/install.sh | bash` or `brew install --cask claude-code`

## Quick Start

```sh
git clone https://github.com/cwaits6/dotfiles ~/.dotfiles
cd ~/.dotfiles

# Apply all configs
stow nvim ghostty claude zsh

# Or pick individual ones
stow nvim
stow zsh
stow ghostty
stow claude
```
