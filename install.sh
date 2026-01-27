#!/bin/bash

REPO_URL="https://github.com/xoodymoon/fgalaxy.git"
INSTALL_DIR="$HOME/.fgalaxy"

if [ -d "$INSTALL_DIR" ]; then
    cd "$INSTALL_DIR" && git pull
else
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

chmod +x "$INSTALL_DIR/fgalaxy"

sudo ln -sf "$INSTALL_DIR/fgalaxy" /usr/local/bin/fgalaxy

echo "✅ fGalaxy installed successfully."
