import os
import shutil

def merge_md_files(book_name, output_path):
    """
    Merges all markdown files in the specified book folder into a single file,
    saves it to the output path, and deletes the original folder.

    Args:
        book_name: The name of the book (folder name inside the Books directory).
        output_path: The path where the merged file will be saved.
    """
    # Construct the folder path using the book name
    # Since the script is in the "scripts" folder, we need to go one level up to access "Books"
    folder_name = os.path.join("..", "books", book_name)
    
    # Store the absolute path of the folder
    absolute_folder_path = os.path.abspath(folder_name)
    
    # Check if the folder exists
    if not os.path.isdir(absolute_folder_path):
        print(f"Folder '{absolute_folder_path}' does not exist.")
        return
    
    # Change to the specified folder
    os.chdir(absolute_folder_path)
    
    # List all files in the folder and filter for .md files
    md_files = sorted([f for f in os.listdir() if f.endswith('.md') and f.startswith('Chapter')])
    
    if not md_files:
        print("No markdown files found in the folder.")
        return
    
    # Sort files numerically based on the chapter number
    md_files.sort(key=lambda x: int(x.split()[1].split('.')[0]))
    
    # Ensure output path exists
    os.makedirs(output_path, exist_ok=True)
    
    # Merge content into a single file
    output_file_name = os.path.join(output_path, f"{book_name} (OG).md")
    with open(output_file_name, 'w', encoding='utf-8') as outfile:
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read() + '\n\n')  # Add some space between chapters
            print(f"Added {md_file} to {output_file_name}")
    
    print(f"All files have been merged into {output_file_name}")
    
    # Move back to the parent directory before deleting the folder
    os.chdir('..')  # Move up one directory
    
    # Delete the folder after merging
    shutil.rmtree(absolute_folder_path)
    print(f"Folder '{absolute_folder_path}' has been deleted.")

# Get the book name from the user
book_name = input("Enter the book name: ")

# Define the output path (e.g., OBSIDIAN notes folder)
output_path = r"D:\OBSIDIAN\NOTES"

# Call the function to merge and clean up
merge_md_files(book_name, output_path)