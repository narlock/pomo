#!/bin/bash

# =================================
# POMO INSTALLATION SCRIPT
# author: narlock
#
# 1. Installs the contents of the application into $HOME/Documents/narlock/pomo
# 2. Ensures that the main.py file is executable
# 3. Creates a wrapper to ensure that the 'pomo' command runs with python3
# 4. Ensures the wrapper is executable
# =================================

# Define install paths
INSTALL_DIR="$HOME/Documents/narlock/pomo"
SCRIPT_PATH="$INSTALL_DIR/pomo/main.py"
BIN_PATH="/usr/local/bin/pomo"

echo "Installing Pomo..."

# Create the install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Copy all files to the install directory
cp -r . "$INSTALL_DIR"

# Make sure the script is executable
chmod +x "$SCRIPT_PATH"

# Create a wrapper script to ensure 'mark' runs with python3
echo "#!/bin/bash" | sudo tee "$BIN_PATH" > /dev/null
echo "python3 \"$SCRIPT_PATH\" \"\$@\"" | sudo tee -a "$BIN_PATH" > /dev/null

# Make the wrapper script executable
sudo chmod +x "$BIN_PATH"

echo "🚀 Installation complete! Use 'pomo' to begin."
