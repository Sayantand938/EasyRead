import os
import re

def process_files():
    # Step 1: Take input for the folder name from the user
    folder_name = input("Enter the folder name: ").strip()
    
    # Step 2: Construct the path to the folder
    folder_path = os.path.join('..', 'books', folder_name)
    
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return
    
    # Step 3: Process all .md files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.md'):
            file_path = os.path.join(folder_path, file_name)
            
            try:
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                # Check if the first line contains an H1 heading
                if lines and lines[0].startswith('# '):
                    # Extract the content of the H1 heading
                    h1_match = re.search(r'#\s*(\*\*|\*\*\*)?(\d+)(\*\*|\*\*\*)?', lines[0])
                    if h1_match:
                        chapter_number = h1_match.group(2)  # Extract the number
                        new_heading = f"## Chapter {chapter_number}\n"
                        
                        # Replace the old H1 with the new heading
                        lines[0] = new_heading
                        
                        # Write the updated content back to the file
                        with open(file_path, 'w', encoding='utf-8') as file:
                            file.writelines(lines)
                        
                        print(f"Updated heading in '{file_name}' to '{new_heading.strip()}'")
                    else:
                        print(f"No valid H1 found in '{file_name}'. Skipping...")
                else:
                    print(f"No H1 heading found in '{file_name}'. Skipping...")
            except Exception as e:
                print(f"Error processing file '{file_name}': {e}")

# Run the function
process_files()