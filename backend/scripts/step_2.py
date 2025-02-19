#! /usr/bin/python3
import os
import re


def clean_and_renumber_markdown_files(base_directory: str, book_name: str):
    """
    Deletes empty markdown files (files containing no content or only blank lines)
    in the specified book's directory and renumbers the remaining files sequentially,
    starting from 1.md.

    Args:
        base_directory (str): The root directory where "books" folder exists.
        book_name (str): The name of the book (used to construct the markdown directory path).
    """

    book_directory = os.path.join(base_directory, "books", book_name)

    files_to_delete = []
    for filename in os.listdir(book_directory):
        if filename.endswith(".md"):
            filepath = os.path.join(book_directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check if the file is empty or contains only whitespace
                if not content.strip():
                    files_to_delete.append(filepath)
                else:
                    #Check if the file contains only blank lines
                    lines = content.splitlines()
                    non_empty_lines = [line for line in lines if line.strip()]

                    if not non_empty_lines:
                        files_to_delete.append(filepath)
            except Exception as e:
                print(f"Error reading file {filepath}: {e}")

    # Delete empty files
    for filepath in files_to_delete:
        try:
            os.remove(filepath)
            print(f"Deleted empty file: {os.path.basename(filepath)}")
        except Exception as e:
            print(f"Error deleting file {filepath}: {e}")

    # Renumber remaining files
    remaining_files = sorted([f for f in os.listdir(book_directory) if f.endswith(".md")],
                             key=lambda x: int(re.match(r'(\d+)\.md', x).group(1)))  # Sort numerically
    
    for i, filename in enumerate(remaining_files):
        old_filepath = os.path.join(book_directory, filename)
        new_filename = f"{i + 1}.md"
        new_filepath = os.path.join(book_directory, new_filename)

        try:
            os.rename(old_filepath, new_filepath)
            print(f"Renamed '{filename}' to '{new_filename}'")
        except Exception as e:
            print(f"Error renaming file {old_filepath} to {new_filepath}: {e}")


if __name__ == "__main__":
    book_name = input("Enter the book name (directory name without .epub): ")

    # Get the base directory (two levels up from the current file)
    base_directory = os.path.dirname(os.path.dirname(__file__))

    clean_and_renumber_markdown_files(base_directory, book_name)