import sys
import os
import re

def add_link_to_md(link, foldername=None, description=None, tags=None):
    # Define the path to your documents folder
    documents_folder = os.path.expanduser("~/Documents/Bookmarker/")

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

        # Remove trailing slash if present
        foldername = foldername.rstrip("/")

        folder_parts = foldername.split("/")
        with open(md_file_path, "a") as file:
            for i, part in enumerate(folder_parts):
                indent = "    " * i
                if i == 0:
                    file.write(f"- {'#' * 2} {part}\n")
                else:
                    file.write(f"{indent}- {'#' * 3} {part}\n")
        link_line = f"{'    ' * len(folder_parts)}- [{description or link}]({link})"
        if tags:
            link_line += f" - Tags: {tags}\n"
        else:
            link_line += "\n"
        with open(md_file_path, "a") as file:
            file.write(link_line)
    else:
        # Append the link to the Markdown file without a folder
        with open(md_file_path, "a") as file:
            link_line = f"- [ {description or link}]({link})"
            if tags:
                link_line += f" - Tags: {tags}\n"
            else:
                link_line += "\n"
            file.write(link_line)
                
def import_data_from_html(html_file_path):
    # Check if the HTML file exists
    if not os.path.exists(html_file_path):
        print(f"HTML file '{html_file_path}' not found.")
        return

    # Open the HTML file and read its contents
    with open(html_file_path, "r") as html_file:
        html_content = html_file.read()

    # Split the HTML content by lines
    lines = html_content.splitlines()

    # Initialize variables to track folder and tags
    current_folder = None
    current_tags = ""

    # Iterate through the lines and process the content
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace

        # Check if the line starts with '<DT><H3>' indicating a folder
        if line.startswith("<DT><H3>"):
            current_folder = re.search(r'<DT><H3>(.*?)</H3>', line).group(1)
        # Check if the line contains a link
        elif line.startswith("<DT><A HREF="):
            link_match = re.search(r'<A HREF="(.*?)".*?TAGS="(.*?)">(.*?)</A>', line)
            if link_match:
                link, tags, description = link_match.groups()
                # Check if a folder is defined, and if so, add it to the Markdown
                if current_folder:
                    add_link_to_md(link, foldername=current_folder, description=description, tags=tags)
                else:
                    add_link_to_md(link, description=description, tags=tags)

    print(f"Data imported from '{html_file_path}' to Markdown file.")


## Function to create Netscape bookmarks in HTML format from the Markdown file
def create_netscape_bookmarks():
    # Define the path to the Netscape bookmark file (HTML format)
    documents_folder = os.path.expanduser("~/Documents/Bookmarker/")
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
    documents_folder = os.path.expanduser("~/Documents/Bookmarker/")
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
    documents_folder = os.path.expanduser("~/Documents/Bookmarker/")
    md_file_path = os.path.join(documents_folder, "bookmarks.md")

    # Read the Markdown file and print folders
    with open(md_file_path, "r") as md_file:
        lines = md_file.readlines()

    folder_stack = []  # To keep track of the folder hierarchy

    for line in lines:
        # Check if the line starts with "- ##" or "- ###" followed by a word or group of words
        match_folder = re.match(r'^(\s*)- (##|###) (.+)', line)
        if match_folder:
            folder_name = match_folder.group(3).strip()
            folder_depth = len(match_folder.group(1)) // 4  # Four spaces represent one level of depth

            # Pop folders from the stack until the correct depth is reached
            while len(folder_stack) > folder_depth:
                folder_stack.pop()

            # Append the current folder to the stack
            folder_stack.append(folder_name)

            # Print the folder hierarchy with proper formatting
            folder_structure = ""
            for i in range(len(folder_stack)):
                folder_structure += "| - " * i + folder_stack[i] + "\n"
            print(folder_structure)




def list_all_links_from_folder(foldername):
    # Define the path to the Markdown file
    documents_folder = os.path.expanduser("~/Documents/Bookmarker/")
    md_file_path = os.path.join(documents_folder, "bookmarks.md")

    # Read the Markdown file and print all links
    with open(md_file_path, "r") as md_file:
        lines = md_file.readlines()

    foldername = foldername.rstrip("/")
    folder_parts = foldername.split("/")
    last_folder_part = folder_parts[-1]
    folder_depth = len(folder_parts)

    folder_found = False
    for line in lines:
        # Check if the line starts with "- ##" or "- ###" followed by a word or group of words
        match_folder = re.match(r'^(\s*)- (##|###) ' + last_folder_part, line)
        if match_folder:
            current_folder_depth = len(match_folder.group(1)) // 4
            if current_folder_depth == folder_depth - 1:
                folder_found = True
                continue

        # Start matching links only after the folder line is found
        if folder_found:
            # Check if the line is a subfolder line
            match_subfolder = re.match(r'^(\s*)- (##|###) ', line)
            if match_subfolder:
                current_subfolder_depth = len(match_subfolder.group(1)) // 4
                if current_subfolder_depth >= folder_depth:
                    break  # Stop matching links if a subfolder line is found

            # Use regular expression to match valid links
            match_link = re.search(r'- \[([^]]+)\]\(([^)]+)\)', line)
            if match_link:
                description = match_link.group(1)
                link = match_link.group(2)
                print(f"[{description}]({link})")

def list_all_links_with_tag(tag):
    # Define the path to the Markdown file
    documents_folder = os.path.expanduser("~/Documents/Bookmarker/")
    md_file_path = os.path.join(documents_folder, "bookmarks.md")

    # Read the Markdown file and print all links
    with open(md_file_path, "r") as md_file:
        lines = md_file.readlines()

    for line in lines:
        # Use regular expression to match valid links with tags
        match_link_with_tags = re.search(r'- \[([^]]+)\]\(([^)]+)\) - Tags: ([^\n]+)', line)
        if match_link_with_tags:
            description = match_link_with_tags.group(1)
            link = match_link_with_tags.group(2)
            tags = match_link_with_tags.group(3).split(", ")
            if tag in tags:
                print(f"[{description}]({link})")



def main():
    # Check if the command-line argument is provided
    if len(sys.argv) < 2:
        print("Usage: bookmarker (bk) [--export] [--import <html_file_path>] <link> [-f <foldername>] [-d <description>] [-t <tags>] [--list --all] [--folders] [--list --f <foldername>] [--list --t <tag>]")
        sys.exit(1)

    if sys.argv[1] == "--list" and sys.argv[2] == "--all":
        list_all_links()
    elif sys.argv[1] == "--list" and sys.argv[2] == "--f" and len(sys.argv) >= 4:
        foldername = sys.argv[3]
        list_all_links_from_folder(foldername)
    elif sys.argv[1] == "--list" and sys.argv[2] == "--t" and len(sys.argv) >= 4:
        tag = sys.argv[3]
        list_all_links_with_tag(tag)
    elif sys.argv[1] == "--folders":
        list_all_folders()
    elif sys.argv[1] == "--export":
        create_netscape_bookmarks()
        print("Bookmarks exported to HTML file.")
    elif sys.argv[1] == "--import" and len(sys.argv) >= 3:
        html_file_path = sys.argv[2]
        import_data_from_html(html_file_path)
    else:
        # Check if the --export argument is present in the arguments
        export_requested = "--export" in sys.argv
        link_index = 1 if not export_requested else 2  # Adjust the index based on --export

        link = sys.argv[link_index]
        foldername = None
        description = None
        tags = None

        # Parse command-line arguments starting from index link_index + 1
        i = link_index + 1
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

        # Only export if --export was requested
        if export_requested:
            create_netscape_bookmarks()
            print("Bookmarks exported to HTML file.")

        if foldername:
            print(f"Added {link} to the '{foldername}' folder in your bookmarks.")
        else:
            print(f"Added {link} to your bookmarks.")

if __name__ == "__main__":
    main()


