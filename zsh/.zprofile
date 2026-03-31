# -------- homebrew -------- #

for b in /opt/homebrew/bin/brew "$HOME/.homebrew/bin/brew"; do
  [[ -x "$b" ]] && eval "$("$b" shellenv)" && break
done

export HOMEBREW_CASK_OPTS="--appdir=$HOME/Applications"

# ---------- path ---------- #

setopt extended_glob null_glob
typeset -U path

path=(
  $HOME/.local/bin
  ${KREW_ROOT:-$HOME/.krew}/bin
  /usr/local/bin
  /Applications/Wireshark.app/Contents/MacOS
  /Applications/VMware\ Fusion.app/Contents/MacOS
  /usr/local/zfs/bin
  /Applications/Ghostty.app/Contents/MacOS
  /Applications/Obsidian.app/Contents/MacOS
  $path
)

# remove non-existent directories
path=($^path(N-/))

export PATH
