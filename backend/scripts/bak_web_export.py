import os
import re
import markdown2
import shutil
import json

def load_env_variable(variable_name):
    """Load environment variable."""
    value = os.getenv(variable_name)
    if not value:
        raise ValueError(f"Environment variable {variable_name} is not set.")
    return value

def clear_books_folder(books_folder):
    """Clear all contents in the books folder."""
    if os.path.exists(books_folder):
        for item in os.listdir(books_folder):
            item_path = os.path.join(books_folder, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove files and symbolic links
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove directories

def clear_library_json(json_file_path):
    """Clear the contents of the library.json file."""
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump([], f)  # Overwrite with an empty list

def extract_yaml_frontmatter(file_content):
    """Extract YAML frontmatter from a markdown file."""
    match = re.match(r'^---\s*$(.*?)^---\s*$', file_content, re.DOTALL | re.MULTILINE)
    if match:
        yaml_frontmatter = match.group(1)
        remaining_content = file_content[match.end():].strip()
        return yaml_frontmatter, remaining_content
    return None, file_content.strip()

def split_into_chunks(content):
    """Split content into chunks based on ## headings."""
    # Split content by '##' headings
    chunks = re.split(r'\n## ', content)
    # Add back the '##' to the headings (except the first chunk)
    chunks = [chunks[0]] + [f"## {chunk}" for chunk in chunks[1:]]
    return chunks

def sanitize_filename(filename):
    """Sanitize the filename by removing invalid characters."""
    return re.sub(r'[\\/*?:"<>|]', '', filename).strip()

def convert_to_html(chunk, file_name_without_extension, heading_title=""):
    """Convert a Markdown chunk to HTML using the provided template."""
    html_content = markdown2.markdown(chunk)

    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{heading_title}</title>
    <link rel="stylesheet" href="../../assets/style/style.css" />
    <script src="https://cdn.jsdelivr.net/npm/tocbot@4.8.1/dist/tocbot.min.js"></script>
</head>
<body>
    <h1>{file_name_without_extension}</h1>
    {html_content}
    <script src="../../assets/script/script.js"></script>
</body>
</html>
"""
    return html_template

def create_index_file(folder_path, file_name_without_extension, chapter_links):
    """Create an index file with links to all chapter files."""
    index_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{file_name_without_extension}</title>
    <link rel="stylesheet" href="../../assets/style/style.css" />
</head>
<body>
    <h1>{file_name_without_extension}</h1>
    <ul>
        {''.join(f'<li><a href="{link}.html">{link}</a></li>' for link in chapter_links)}
    </ul>
</body>
</html>
"""
    # Save the index file
    index_file_path = os.path.join(folder_path, f"{file_name_without_extension}.html")
    with open(index_file_path, 'w', encoding='utf-8') as f:
        f.write(index_template)

def save_html_files(chunks, folder_path, file_name_without_extension):
    """Save chunks as HTML files in the given folder and create an index file."""
    chapter_links = []
    for chunk in chunks:
        # Extract the heading title for the filename
        heading_title_match = re.search(r'^##\s+(.*)', chunk, re.MULTILINE)
        heading_title = heading_title_match.group(1) if heading_title_match else "Untitled"

        # Sanitize the heading title to use as a filename
        sanitized_heading_title = sanitize_filename(heading_title)
        chapter_links.append(sanitized_heading_title)

        # Convert the chunk to HTML
        html_content = convert_to_html(chunk, file_name_without_extension, heading_title)

        # Save the HTML content to a file
        file_name = f"{sanitized_heading_title}.html"
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    # Create the index file
    create_index_file(folder_path, file_name_without_extension, chapter_links)

def update_library_json(file_name_without_extension):
    """Update the library.json file with the new entry."""
    json_dir = os.path.join(os.path.dirname(__file__), '../web/library')
    json_file_path = os.path.join(json_dir, 'library.json')

    # Ensure the library directory exists
    os.makedirs(json_dir, exist_ok=True)

    # Load existing library data or initialize an empty list
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as f:
            try:
                library_data = json.load(f)
            except json.JSONDecodeError:
                library_data = []
    else:
        library_data = []

    # Append the new entry
    library_data.append({
        "title": file_name_without_extension,
        "link": f"books/{file_name_without_extension}/{file_name_without_extension}.html",
        "cover": f"assets/covers/{file_name_without_extension}.png",
    })

    # Save the updated library data back to the JSON file
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(library_data, f, indent=4)

def process_files_with_easyread_tag(directory):
    """Process all .md files with the 'EasyRead' tag."""
    # Clear the library.json file before processing
    json_dir = os.path.join(os.path.dirname(__file__), '../web/library')
    json_file_path = os.path.join(json_dir, 'library.json')
    clear_library_json(json_file_path)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()

                # Extract YAML frontmatter and remaining content
                yaml_frontmatter, remaining_content = extract_yaml_frontmatter(file_content)

                # Skip files without YAML frontmatter
                if not yaml_frontmatter:
                    continue

                # Check if the file has the 'EasyRead' tag
                if 'EasyRead' not in yaml_frontmatter:
                    continue

                # Split the remaining content into chunks
                chunks = split_into_chunks(remaining_content)

                # Create a folder for the file in ../web/books
                base_folder = os.path.join(os.path.dirname(__file__), '../web/books')
                os.makedirs(base_folder, exist_ok=True)
                folder_name = os.path.splitext(file)[0]
                folder_path = os.path.join(base_folder, folder_name)
                os.makedirs(folder_path, exist_ok=True)

                # Save the chunks as HTML files and create the index file
                save_html_files(chunks, folder_path, folder_name)

                # Update the library.json file
                update_library_json(folder_name)

                # Print the processed file name with a checkmark
                print(f"{folder_name} ✅")

if __name__ == "__main__":
    # Load the OBSIDIAN_NOTES_DIR environment variable
    notes_dir = load_env_variable("OBSIDIAN_NOTES_DIR")

    # Clear the books folder before processing
    books_folder = os.path.join(os.path.dirname(__file__), '../web/books')
    clear_books_folder(books_folder)

    # Process files with the 'EasyRead' tag
    process_files_with_easyread_tag(notes_dir)