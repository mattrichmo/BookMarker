import sys
import os
import re

def add_link_to_md(link, foldername=None, description=None, tags=None):
    # Define the path to your documents folder
    documents_folder = os.path.expanduser("~/Documents/bookmarker/")

    # Define the path to the Markdown file
    md_file_path = os.path.join(documents_folder, "bookmarks.md")

    # Check if the Markdown file exists, and create it if it doesn't
    if not os.path.exists(md_file_path):
        with open(md_file_path, "w") as file:
            file.write("# Bookmarks\n\n")

    # If a foldername is provided, check if it exists in the Markdown file
    if foldername:
        with open(md_file_path, "r") as file:
            lines = file.readlines()

        folder_exists = False
        for i, line in enumerate(lines):
            if line.startswith(f"- {foldername}"):
                folder_exists = True
                folder_start = i
                break

        if folder_exists:
            # Append the link under the existing folder
            folder_line = lines[folder_start]
            indent = len(folder_line) - len(folder_line.lstrip())
            link_line = f"\t- [{description or link}]({link})"
            if tags:
                link_line += f" - Tags: {tags}\n"
            else:
                link_line += "\n"
            lines.insert(folder_start + 1, "\t" * indent + link_line)
            with open(md_file_path, "w") as file:
                file.writelines(lines)
        else:
            # Create a new folder and add the link
            with open(md_file_path, "a") as file:
                file.write(f"- {foldername}\n")
                file.write(f"\t- [{description or link}]({link})")
                if tags:
                    file.write(f" - Tags: {tags}\n")
                else:
                    file.write("\n")
    else:
        # Append the link to the Markdown file without a folder
        with open(md_file_path, "a") as file:
            file.write(f"- [{description or link}]({link})")
            if tags:
                file.write(f" - Tags: {tags}\n")
            else:
                file.write("\n")
                

## Function to create Netscape bookmarks in HTML format from the Markdown file
def create_netscape_bookmarks():
    # Define the path to the Netscape bookmark file (HTML format)
    documents_folder = os.path.expanduser("~/Documents/bookmarker/")
    html_file_path = os.path.join(documents_folder, "bookmarks.html")
    md_file_path = os.path.join(documents_folder, "bookmarks.md")

    # Read the Markdown file and generate the Netscape bookmark file
    with open(md_file_path, "r") as md_file:
        lines = md_file.readlines()

    with open(html_file_path, "w") as html_file:
        html_file.write("<!DOCTYPE NETSCAPE-Bookmark-file-1>\n")
        html_file.write("<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\">\n")
        html_file.write("<TITLE>Bookmarks</TITLE>\n")
        html_file.write("<H1>Bookmarks</H1>\n")

        # Initialize a stack to keep track of folder hierarchy
        folder_stack = []

        for line in lines:
            # Use regular expression to match valid links and folders
            match_link = re.search(r'- \[([^]]+)\]\(([^)]+)\)', line)
            match_folder = re.search(r'- (.+)', line)
            match_tags = re.search(r'- Tags: (.+)', line)

            if match_link:
                description = match_link.group(1)
                link = match_link.group(2)
                tags = ""
                if match_tags:
                    tags = match_tags.group(1)
                # Write the link under the current folder hierarchy
                html_file.write(f'<DT><A HREF="{link}" TAGS="{tags}">{description}</A>\n')
            elif match_folder:
                folder_name = match_folder.group(1).strip()
                # Adjust folder hierarchy based on indentation
                while len(folder_stack) > 0 and folder_stack[-1][0] >= len(line) - len(line.lstrip()):
                    folder_stack.pop()

                # Write the folder information to HTML
                html_file.write(f'<DT><H3>{folder_name}</H3>\n')
                html_file.write("<DL>\n")
                folder_stack.append((len(line) - len(line.lstrip()), folder_name))
            

        # Close any remaining folders
        while len(folder_stack) > 0:
            html_file.write("</DL>\n")
            folder_stack.pop()

# Function to list all links in the Markdown file
def list_all_links():
    # Define the path to the Markdown file
    documents_folder = os.path.expanduser("~/Documents/bookmarker/")
    md_file_path = os.path.join(documents_folder, "bookmarks.md")

    # Read the Markdown file and print all links
    with open(md_file_path, "r") as md_file:
        lines = md_file.readlines()

    for line in lines:
        # Use regular expression to match valid links
        match_link = re.search(r'- \[([^]]+)\]\(([^)]+)\)', line)
        if match_link:
            description = match_link.group(1)
            link = match_link.group(2)
            print(f"[{description}]({link})")

def list_all_folders():
    # Define the path to the Markdown file
    documents_folder = os.path.expanduser("~/Documents/bookmarker/")
    md_file_path = os.path.join(documents_folder, "bookmarks.md")

    # Read the Markdown file and print folders
    with open(md_file_path, "r") as md_file:
        lines = md_file.readlines()

    for line in lines:
        # Remove leading and trailing whitespace
        line = line.strip()

        # Check if the line starts with "- " followed by a word or a group of words
        match_folder = re.match(r'- ([\w\s]+)', line)
        if match_folder:
            folder_name = match_folder.group(1).strip()
            print(f"| - {folder_name}")


def main():
    # Define the path to the documents folder here as well
    documents_folder = os.path.expanduser("~/Documents/bookmarker/")

    # Check if the command-line argument is provided
    if len(sys.argv) < 2:
        print("Usage: bookmarker (bk) <link> [-f <foldername>] [-d <description>] [-t <tags>] [--list --all] [--folders]")
        sys.exit(1)

    if sys.argv[1] == "--list" and sys.argv[2] == "--all":
        list_all_links()
    elif sys.argv[1] == "--folders":
        list_all_folders()
    else:
        link = sys.argv[1]
        foldername = None
        description = None
        tags = None

        # Parse command-line arguments
        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == "-f" and i + 1 < len(sys.argv):
                foldername = sys.argv[i + 1]
                i += 1
            elif arg == "-d" and i + 1 < len(sys.argv):
                description = sys.argv[i + 1]
                i += 1
            elif arg == "-t" and i + 1 < len(sys.argv):
                tags = sys.argv[i + 1]
                i += 1
            i += 1

        add_link_to_md(link, foldername, description, tags)
        create_netscape_bookmarks()

        if foldername:
            print(f"Added {link} to the '{foldername}' folder in your bookmarks.")
        else:
            print(f"Added {link} to your bookmarks.")

if __name__ == "__main__":
    main()
