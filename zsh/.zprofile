# ---- Homebrew environment (Apple Silicon) ---- #
for b in /opt/homebrew/bin/brew "$HOME/.homebrew/bin/brew"; do
  [[ -x "$b" ]] && eval "$("$b" shellenv)" && break
done

export HOMEBREW_CASK_OPTS="--appdir=$HOME/Applications"

# ---- Clean PATH edits with zsh array ---- #
setopt extended_glob null_glob

# ---- Remove duplicate entries ---- #
typeset -U path

# ---- PATH ---- #
path=(
  $HOME/.local/bin
  /usr/local/bin
  /Applications/Wireshark.app/Contents/MacOS
  /Applications/VMware\ Fusion.app/Contents/Public
  /usr/local/zfs/bin
  /Applications/Ghostty.app/Contents/MacOS
  /Applications/Obsidian.app/Contents/MacOS
  $path
)

# ---- Remove non-existant directories ---- #
path=($^path(N-/))

export PATH

