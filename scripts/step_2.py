import os
import shutil

def delete_empty_md_files(folder_path):
    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file is a markdown (.md) file and if it's empty
        if filename.endswith('.md') and os.path.isfile(file_path):
            if os.path.getsize(file_path) == 0:
                print(f"Deleting empty file: {file_path}")
                os.remove(file_path)

def rename_files_sequentially(folder_path):
    # Get a list of all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Sort files by creation time
    files.sort(key=lambda f: os.path.getctime(os.path.join(folder_path, f)))

    # Create a temporary folder to avoid conflicts
    temp_folder = os.path.join(folder_path, "temp")
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # Move all files to the temporary folder
    for file_name in files:
        shutil.move(os.path.join(folder_path, file_name), os.path.join(temp_folder, file_name))

    # Rename the files to 1.md, 2.md, etc., and move them back
    for index, file_name in enumerate(os.listdir(temp_folder), start=1):
        new_file_name = f"{index}.md"
        shutil.move(os.path.join(temp_folder, file_name), os.path.join(folder_path, new_file_name))
        print(f"Renamed {file_name} to {new_file_name}")

    # Remove the temporary folder
    os.rmdir(temp_folder)

def main():
    # Base directory
    books_folder = os.path.join('..', 'books')
    if not os.path.exists(books_folder):
        print(f"The folder {books_folder} does not exist.")
        exit()

    # Ask the user to enter a name
    book_name = input("Enter the name of the book: ")

    # Create a folder with the entered name
    book_folder_path = os.path.join(books_folder, book_name)
    if not os.path.exists(book_folder_path):
        os.makedirs(book_folder_path)
        print(f"Created folder: {book_folder_path}")
    else:
        print(f"Folder already exists: {book_folder_path}")

    # Delete empty .md files in the folder
    delete_empty_md_files(book_folder_path)
    print("All empty .md files have been deleted.")

    # Rename the remaining files sequentially
    rename_files_sequentially(book_folder_path)
    print("File renaming completed.")

if __name__ == "__main__":
    main()
