#!/bin/bash

# SpecifInput Quick Installer
# This script installs SpecifInput to your system

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons"

echo "Installing SpecifInput..."

# Create directories if they don't exist
mkdir -p "$INSTALL_DIR"
mkdir -p "$DESKTOP_DIR" 
mkdir -p "$ICON_DIR"

# Copy executable
echo "Installing executable..."
cp "$SCRIPT_DIR/SpecifInput" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/SpecifInput"

# Copy icon
echo "Installing icon..."
cp "$SCRIPT_DIR/logo.png" "$ICON_DIR/specifinput.png"

# Create desktop file with proper paths
echo "Creating desktop entry..."
cat > "$DESKTOP_DIR/SpecifInput.desktop" << 'EOF'
[Desktop Entry]
Name=SpecifInput
Comment=Background Input Sender
Exec=SpecifInput
Icon=specifinput
Terminal=false
Type=Application
Categories=Utility;
StartupNotify=true
StartupWMClass=SpecifInput
EOF

chmod +x "$DESKTOP_DIR/SpecifInput.desktop"

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

# Add ~/.local/bin to PATH if not already there
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo ""
    echo "Note: Add ~/.local/bin to your PATH to run 'SpecifInput' from terminal:"
    echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
    echo "   source ~/.bashrc"
fi

echo ""
echo "SpecifInput installed!"
echo ""
echo "You can now:"
echo "• Find it in your application menu (search 'SpecifInput')"
echo "• Run from terminal: SpecifInput (if ~/.local/bin is in PATH)"
echo "• Double-click the executable in file manager"
echo ""
echo "The application will run as a standalone program - no terminal window needed!"