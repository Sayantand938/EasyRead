import os
from natsort import natsorted

def is_file_empty(file_path):
    """
    Check if a file is empty or contains only blank lines or a single line with fewer than 10 words.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # Remove blank lines
            non_blank_lines = [line.strip() for line in lines if line.strip()]
            # If no non-blank lines, the file is empty
            if not non_blank_lines:
                return True
            # If there's only one line and it has fewer than 10 words, consider it empty
            if len(non_blank_lines) == 1 and len(non_blank_lines[0].split()) < 10:
                return True
            return False
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False

def process_files():
    # Step 1: Take input for the folder name from the user
    folder_name = input("Enter the folder name: ").strip()
    
    # Step 2: Construct the path to the folder
    folder_path = os.path.join('..', 'books', folder_name)
    
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return
    
    # Step 3: Collect all .md files
    md_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                md_files.append(file_path)
    
    # Step 4: Sort the files naturally
    md_files = natsorted(md_files, key=lambda x: os.path.basename(x))
    
    # Step 5: Filter out empty files
    non_empty_files = []
    for file_path in md_files:
        if is_file_empty(file_path):
            print(f"Deleting empty file: {file_path}")
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        else:
            non_empty_files.append(file_path)
    
    # Step 6: Rename the remaining files sequentially
    for index, file_path in enumerate(non_empty_files, start=1):
        new_file_name = f"{index}.md"
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        print(f"Renaming '{file_path}' to '{new_file_path}'")
        try:
            os.rename(file_path, new_file_path)
        except Exception as e:
            print(f"Error renaming file {file_path} to {new_file_path}: {e}")

# Run the function
process_files()