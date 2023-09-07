#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Define the directory where the 'bookmark' script will be placed
script_dir="/usr/local/bin"  # You can change this to a different directory if needed

# Check if the specified directory exists
if [ ! -d "$script_dir" ]; then
    echo "The directory $script_dir does not exist. Please create it or choose a different directory."
    exit 1
fi

# Copy 'bookmarker.py' to the script directory
cp "bookmarker.py" "$script_dir/"

# Create the 'bookmark' script
echo '#!/bin/bash' > "$script_dir/bookmark"
echo 'python3 "$(dirname "$0")/bookmarker.py" "$@"' >> "$script_dir/bookmark"

# Create an alias for 'bk' to call 'bookmark'
echo 'alias bk="bookmark"' >> "$HOME/.zshrc"  # Add this line for Zsh

# Make the 'bookmark' script executable
chmod +x "$script_dir/bookmark"

# Provide instructions to the user
echo "The 'bookmark' and 'bk' commands have been created in $script_dir and made executable."
echo "You can now use 'bookmark' or 'bk' to add links to your Markdown file."
echo "  bookmark https://www.example.com"
echo "  bk https://www.example.com"
echo " Arguments include description, tags, and folder names."
echo ' Example with arguments: bookmark http://example.com -d "This is the description" -f "This is the folder" -t "tag1, tag2, tag3,"'
