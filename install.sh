#!/usr/bin/env bash
# Bootstrap these dotfiles on macOS or Ubuntu/Debian. Safe to re-run.
# Keep compatible with macOS's /bin/bash 3.2.
set -euo pipefail

DOTFILES="$(cd "$(dirname "$0")" && pwd)"
ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"
SKIPPED=()

log()  { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m!!\033[0m %s\n' "$*" >&2; }

# Run a step, but keep going if it fails (some tools are blocked on work machines).
try() {
  local name="$1"; shift
  "$@" || { warn "$name failed, skipping"; SKIPPED+=("$name"); }
}

# Clone a repo once; later runs fast-forward it.
clone() {
  if [ -d "$2/.git" ]; then git -C "$2" pull --ff-only -q
  else git clone --depth 1 -q "$1" "$2"; fi
}

# Move real files (not symlinks) aside so stow doesn't refuse to link over them.
backup_conflicts() {
  local src target
  for src in "$DOTFILES/$1"/.[!.]* "$DOTFILES/$1"/*; do
    [ -f "$src" ] || continue
    target="$HOME/$(basename "$src")"
    if [ -f "$target" ] && [ ! -L "$target" ]; then
      warn "backing up $target"
      mv "$target" "$target.bak.$(date +%Y%m%d%H%M%S)"
    fi
  done
}

# stow_pkg <package> [extra stow flags]
stow_pkg() {
  backup_conflicts "$1"
  stow --dir "$DOTFILES" --target "$HOME" "${@:2}" --restow "$1"
}

install_fzf() {
  # apt's fzf is too old for `fzf --zsh`
  clone https://github.com/junegunn/fzf.git "$HOME/.fzf" &&
    "$HOME/.fzf/install" --bin >/dev/null 2>&1 &&
    mkdir -p "$HOME/.local/bin" &&
    ln -sf "$HOME/.fzf/bin/fzf" "$HOME/.local/bin/fzf"
}

case "$(uname -s)" in
  Darwin)
    log "Homebrew packages"
    if command -v brew >/dev/null 2>&1; then
      try "brew bundle" brew bundle --file "$DOTFILES/Brewfile"
    else
      warn "Homebrew not found (https://brew.sh), skipping Brewfile"
      SKIPPED+=("brew bundle")
    fi
    PACKAGES="zsh nvim ghostty claude"
    ;;
  Linux)
    log "apt packages"
    if command -v sudo >/dev/null 2>&1 && sudo -v; then
      try "apt packages" sudo sh -c 'apt-get update -qq && apt-get install -y -qq zsh stow git curl zoxide >/dev/null'
    else
      warn "no sudo, skipping apt (zsh and stow must already be installed)"
      SKIPPED+=("apt packages")
    fi
    log "fzf"
    try fzf install_fzf
    PACKAGES="zsh"
    ;;
  *)
    warn "unsupported OS: $(uname -s)"
    exit 1
    ;;
esac

log "oh-my-zsh, theme, plugins"
try oh-my-zsh               clone https://github.com/ohmyzsh/ohmyzsh.git                   "$HOME/.oh-my-zsh"
try powerlevel10k           clone https://github.com/romkatv/powerlevel10k.git             "$ZSH_CUSTOM/themes/powerlevel10k"
try zsh-autosuggestions     clone https://github.com/zsh-users/zsh-autosuggestions.git     "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
try zsh-syntax-highlighting clone https://github.com/zsh-users/zsh-syntax-highlighting.git "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"

log "dotfiles"
if command -v stow >/dev/null 2>&1; then
  for pkg in $PACKAGES; do try "stow $pkg" stow_pkg "$pkg"; done
  [ "$(uname -s)" = Darwin ] && try "stow herdr" stow_pkg herdr --no-folding
else
  warn "stow not found, skipping dotfile links"
  SKIPPED+=(stow)
fi

if command -v zsh >/dev/null 2>&1 && [ "$(basename "${SHELL:-}")" != zsh ]; then
  log "default shell -> zsh"
  try chsh chsh -s "$(command -v zsh)"
fi

if [ "${#SKIPPED[@]}" -gt 0 ]; then
  warn "finished with skipped steps: ${SKIPPED[*]}"
else
  log "done"
fi
log "run: exec zsh"
