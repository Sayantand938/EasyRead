import os
import re

def rename_markdown_files_in_output_folder(output_folder):
    """
    Reads all markdown files in the specified output folder, extracts the first h2 heading
    from each file, and renames the file to that heading.

    Args:
        output_folder: The folder containing the markdown files.
    """
    # Get all markdown files in the output folder
    markdown_files = [f for f in os.listdir(output_folder) if f.endswith('.md')]
    
    if not markdown_files:
        print(f"No markdown files found in the folder '{output_folder}'")
        return

    # Loop through each markdown file in the output folder
    for file in markdown_files:
        file_path = os.path.join(output_folder, file)

        try:
            # Open the file and read its content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find the first h2 heading (i.e., ## heading)
            match = re.search(r"^##\s*(.*?)\s*$", content, re.MULTILINE)
            
            if match:
                new_heading = match.group(1).strip()
                new_filename = f"{new_heading}.md"

                # Ensure the new filename doesn't conflict with existing files
                new_filename = os.path.join(output_folder, new_filename)
                
                # Avoid renaming to the same name
                if file_path != new_filename:
                    os.rename(file_path, new_filename)
                    print(f"Renamed '{file}' to '{new_filename}'")
                else:
                    print(f"Skipping renaming of '{file}' as it already matches the heading.")
            else:
                print(f"No h2 heading found in '{file}'.")

        except Exception as e:
            print(f"Error processing file '{file}': {e}")

if __name__ == "__main__":
    # Ask the user for the book name
    book_name = input("Enter the book name (without .epub extension): ").strip()

    # Define the path to the book's folder inside the Books directory
    # Since the script is in the "scripts" folder, we need to go one level up to access "Books"
    output_folder = os.path.join("..", "Books", book_name)

    # Check if the folder exists
    if os.path.exists(output_folder):
        rename_markdown_files_in_output_folder(output_folder)
    else:
        print(f"Error: The folder '{output_folder}' does not exist.")