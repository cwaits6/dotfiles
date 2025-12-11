# ---- Homebrew environment ---- #
if [[ -x /opt/homebrew/bin/brew ]]; then
  eval "$(/opt/homebrew/bin/brew shellenv)"
elif command -v brew >/dev/null 2>&1; then
  eval "$(brew shellenv)"
fi

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
  $path
)

# ---- Remove non-existant directories ---- #
path=($^path(N-/))

export PATH

