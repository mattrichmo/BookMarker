#!/bin/bash

# Remove the 'bookmark' script from the directory in PATH
script_dir="/usr/local/bin"  # Make sure this matches the directory used in setup.sh

if [ -f "$script_dir/bookmark" ]; then
    rm "$script_dir/bookmark"
    echo "The 'bookmark' script has been removed from $script_dir."
fi

# Remove the copied 'bookmarker.py' script
if [ -f "$script_dir/bookmarker.py" ]; then
    rm "$script_dir/bookmarker.py"
    echo "The copied 'bookmarker.py' script has been removed from $script_dir."
fi

# Provide instructions to the user
echo "Uninstallation complete."
