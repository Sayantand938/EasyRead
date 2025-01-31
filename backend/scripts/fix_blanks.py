import os

def get_file_name():
    """Ask the user for a file name and append .md to it."""
    file_name = input("Enter the file name (without extension): ").strip()
    return f"{file_name}.md"

def construct_file_path(file_name):
    """Construct the full file path using the OBSIDIAN_NOTES_DIR environment variable."""
    notes_dir = os.environ.get("OBSIDIAN_NOTES_DIR")
    if not notes_dir:
        raise EnvironmentError("Environment variable 'OBSIDIAN_NOTES_DIR' is not set.")
    return os.path.join(notes_dir, file_name)

def ensure_blank_lines(file_path):
    """Ensure each line in the file is followed by a blank line (except the last line), skipping YAML frontmatter."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Detect YAML frontmatter (between --- lines)
        in_frontmatter = False
        frontmatter_end_index = 0
        
        for i, line in enumerate(lines):
            if line.strip() == "---":
                if in_frontmatter:
                    frontmatter_end_index = i  # End of YAML frontmatter
                    break
                else:
                    in_frontmatter = True  # Start of YAML frontmatter
        
        # Add a blank line after each line (except the last line or if a blank line already exists)
        modified_lines = []
        for i, line in enumerate(lines):
            modified_lines.append(line)
            # Skip adding a blank line if:
            # 1. It's the last line.
            # 2. The line is already empty.
            # 3. The next line is already a blank line.
            # 4. The line is part of the YAML frontmatter.
            if (i < len(lines) - 1 and  # Not the last line
                line.strip() and  # Current line is not empty
                not (i + 1 < len(lines) and lines[i + 1].strip() == "") and  # Next line is not already blank
                i >= frontmatter_end_index  # Skip YAML frontmatter
            ):
                modified_lines.append("\n")
        
        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(modified_lines)
        
        print(f"File '{file_path}' has been updated successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    try:
        # Get the file name from the user
        file_name = get_file_name()
        
        # Construct the full file path
        file_path = construct_file_path(file_name)
        
        # Ensure each line is followed by a blank line
        ensure_blank_lines(file_path)
    except EnvironmentError as e:
        print(e)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully...")

if __name__ == "__main__":
    main()