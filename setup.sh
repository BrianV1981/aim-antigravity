#!/bin/bash

# Dynamically grab the absolute folder path and its basename (e.g., aim-antigravity, aim-claude)
PROJECT_DIR="$PWD"
ALIAS_NAME=$(basename "$PROJECT_DIR")

echo "Installing '$ALIAS_NAME' bash function to ~/.bashrc"

# We use EOF to dynamically inject the $ALIAS_NAME and $PROJECT_DIR path, 
# while escaping \$1 and \$@ so they stay intact for the alias itself!
cat << EOF >> ~/.bashrc

# $ALIAS_NAME - Dynamic Forensic Retrieval and TUI Alias
$ALIAS_NAME() {
  if [ "\$1" = "search" ]; then
    shift
    python3 "$PROJECT_DIR/src/retriever.py" "\$@"
  else
    python3 "$PROJECT_DIR/scripts/aim_cli.py" "\$@"
  fi
}
EOF

echo "Installation complete!"
echo "Please run: source ~/.bashrc"
echo "You can now use '$ALIAS_NAME search' and '$ALIAS_NAME tui' directly from your terminal!"
