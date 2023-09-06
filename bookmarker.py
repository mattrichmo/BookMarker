import sys
import os

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
            lines.insert(folder_start + 1, f"  - [{description or link}]({link})")
            if tags:
                lines[-1] += f" - Tags: {tags}\n"
            else:
                lines[-1] += "\n"
            with open(md_file_path, "w") as file:
                file.writelines(lines)
        else:
            # Create a new folder and add the link
            with open(md_file_path, "a") as file:
                file.write(f"- {foldername}\n")
                file.write(f"  - [{description or link}]({link})")
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

def main():
    # Check if the command-line argument is provided
    if len(sys.argv) < 2:
        print("Usage: bookmarker (bk) <link> [-f <foldername>] [-d <description>] [-t <tags>]")
        sys.exit(1)

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
    if foldername:
        print(f"Added {link} to the '{foldername}' folder in your bookmarks.")
    else:
        print(f"Added {link} to your bookmarks.")

if __name__ == "__main__":
    main()
