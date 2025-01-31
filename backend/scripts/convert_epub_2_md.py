import zipfile
import os
import html2text

def list_html_files(epub_path):
    html_files = []
    
    with zipfile.ZipFile(epub_path, 'r') as epub:
        # List all files in the EPUB
        for file in epub.namelist():
            # Check if the file has a .html or .xhtml extension
            if file.endswith('.html') or file.endswith('.xhtml'):
                html_files.append(file)
                
    return html_files

def convert_html_to_md(epub_path, html_files):
    # Extract the book name from the EPUB file path (without .epub extension)
    book_name = os.path.splitext(os.path.basename(epub_path))[0]
    
    # Define the output directory path inside the Books folder
    output_dir = os.path.join("..", "books", book_name)
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize html2text object
    h = html2text.HTML2Text()
    h.body_width = 0  # Set body_width to 0 as requested

    with zipfile.ZipFile(epub_path, 'r') as epub:
        for html_file in html_files:
            # Read the HTML/XHTML file content
            html_content = epub.read(html_file).decode('utf-8')
            
            # Convert HTML/XHTML content to Markdown
            markdown_content = h.handle(html_content)

            # Get the base filename without the .html or .xhtml extension
            base_name = os.path.splitext(os.path.basename(html_file))[0]

            # Define the output file path with .md extension inside the book folder
            md_file_path = os.path.join(output_dir, f"{base_name}.md")
            
            # Save the markdown content to a .md file
            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_content)
            print(f"Converted {html_file} to {md_file_path}")

# Get the book name from the user (without extension)
book_name = input("Enter the book name (without .epub extension): ").strip()

# Construct the full path to the EPUB file in the Books folder
epub_path = os.path.join("..", "Books", f"{book_name}.epub")

# Check if the EPUB file exists
if os.path.exists(epub_path):
    html_files = list_html_files(epub_path)
    if html_files:
        convert_html_to_md(epub_path, html_files)
    else:
        print("No HTML or XHTML files found in the EPUB.")
else:
    print(f"EPUB file '{epub_path}' does not exist.")