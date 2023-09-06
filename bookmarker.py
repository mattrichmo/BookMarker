import sys
import os

def add_link_to_md(link):
    # Define the path to your documents folder
    documents_folder = os.path.expanduser("~/Documents/bookmarker/")

    # Define the path to the Markdown file
    md_file_path = os.path.join(documents_folder, "bookmarks.md")

    # Check if the Markdown file exists, and create it if it doesn't
    if not os.path.exists(md_file_path):
        with open(md_file_path, "w") as file:
            file.write("# Bookmarks\n\n")

    # Append the link to the Markdown file
    with open(md_file_path, "a") as file:
        file.write(f"- [{link}]({link})\n")

def main():
    # Check if the command-line argument is provided
    if len(sys.argv) != 2:
        print("Usage: bookmarker <link>")
        sys.exit(1)

    link = sys.argv[1]
    add_link_to_md(link)
    print(f"Added {link} to your bookmarks.")

if __name__ == "__main__":
    main()
