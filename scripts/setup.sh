#!/bin/bash

# Config Search Tool Project Setup
# This script creates the project directory structure and empty files

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Project directory
PROJECT_DIR="$HOME/config-search-tool"

echo -e "${BLUE}Config Search Tool Project Setup${NC}"
echo "This script will create the project structure for Config Search Tool."
echo

# Create project directory
echo -e "${BLUE}Creating project directory at ${YELLOW}$PROJECT_DIR${NC}"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR" || { 
    echo -e "${RED}Failed to create or access project directory${NC}"
    exit 1
}

# Create empty files
echo -e "${BLUE}Creating project files...${NC}"

# Create empty files with placeholder comments
cat > "$PROJECT_DIR/configSearchTool.sh" << EOF
#!/bin/bash
# Config Search Tool
# Placeholder - Replace with your bash script code
EOF

cat > "$PROJECT_DIR/config_search_ui.py" << EOF
#!/usr/bin/env python3
# Config Search Tool UI
# Placeholder - Replace with the Python UI code
EOF

cat > "$PROJECT_DIR/install.sh" << EOF
#!/bin/bash
# Config Search Tool Installer
# Placeholder - Replace with the installer code
EOF

cat > "$PROJECT_DIR/README.md" << EOF
# Config Search Tool
# Placeholder - Replace with the README content
EOF

# Make scripts executable
echo -e "${BLUE}Setting executable permissions...${NC}"
chmod +x "$PROJECT_DIR/configSearchTool.sh"
chmod +x "$PROJECT_DIR/config_search_ui.py"
chmod +x "$PROJECT_DIR/install.sh"

# Create scripts directory to hold original bash script
mkdir -p "$PROJECT_DIR/scripts"

echo -e "${GREEN}Project setup complete!${NC}"
echo
echo -e "Project created at: ${YELLOW}$PROJECT_DIR${NC}"
echo
echo -e "${BLUE}Next steps:${NC}"
echo "1. Copy your bash script code into: configSearchTool.sh"
echo "2. Copy the Python UI code into: config_search_ui.py"
echo "3. Copy the installer code into: install.sh"
echo "4. Copy the README content into: README.md"
echo "5. Run the installer: sudo ./install.sh"
echo
echo -e "${YELLOW}NOTE: You will need to copy the code provided in the separate artifacts into these files.${NC}"
