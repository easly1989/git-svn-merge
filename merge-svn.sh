#!/bin/bash
# Git-SVN Merge Automation Script - Linux/macOS Wrapper
# This wrapper makes it easier to run the Python script on Unix-like systems

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Run the Python script with all arguments passed to this shell script
python3 "$SCRIPT_DIR/merge_to_svn.py" "$@"
