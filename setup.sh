#!/usr/bin/env bash

# A.I.M. Operator Terminal Overlay
# Dynamically installs the `aim` alias interface into the local operator's user .bashrc.

if ! grep -q "aim()" ~/.bashrc; then
  cat << 'EOF' >> ~/.bashrc

# A.I.M. Antigravity Global Environment Hook
# Provides dynamic multi-project database interactions from arbitrary filesystem nodes.
aim() {
  if [ "$1" = "search" ]; then
    shift
    python3 "$HOME/aim-antigravity/src/retriever.py" "$@"
  else
    echo "Unknown command. Available commands: aim search \"query\""
  fi
}
EOF
  echo "[SUCCESS] A.I.M. terminal alias installed successfully into ~/.bashrc."
  echo "Please run: 'source ~/.bashrc' or restart your terminal."
else
  echo "[INFO] The 'aim()' function is already mapped in your ~/.bashrc."
fi
