#!/bin/bash

# Elric Framework - Uninstallation Script
# This script removes the 'elric' command from your system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Elric Framework - Uninstallation${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check possible installation locations
INSTALL_LOCATIONS=(
    "/usr/local/bin/elric"
    "$HOME/.local/bin/elric"
)

FOUND=false

for location in "${INSTALL_LOCATIONS[@]}"; do
    if [ -f "$location" ]; then
        echo -e "${BLUE}→ Found elric at: ${location}${NC}"
        
        # Check if we have permission to remove
        if [ -w "$location" ]; then
            rm "$location"
            echo -e "${GREEN}✓ Removed: ${location}${NC}"
            FOUND=true
        else
            echo -e "${YELLOW}⚠ Need sudo to remove: ${location}${NC}"
            sudo rm "$location"
            echo -e "${GREEN}✓ Removed: ${location}${NC}"
            FOUND=true
        fi
    fi
done

echo ""

if [ "$FOUND" = true ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  ✓ Uninstallation completed successfully!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}  The 'elric' command has been removed from your system.${NC}"
    echo -e "${BLUE}  You can still use 'uv run elric' from the project directory.${NC}"
    echo ""
else
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  ⚠ No installation found${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}  The 'elric' command was not found in common locations.${NC}"
    echo -e "${BLUE}  It may have already been removed.${NC}"
    echo ""
fi
