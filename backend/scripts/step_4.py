#!filepath step_4.py
import os
import markdown2
import json
import htmlmin  # Added for HTML minification

HTML5_BOILERPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="../../assets/style/style.css" />
    <title>{title}</title>
  </head>
  <body>
    {content}
  </body>
</html>
"""

TOC_HTML_BOILERPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="../../assets/style/style.css" />
    <title>{title}</title>
  </head>
  <body>
    <h1>Table of Contents</h1>
    <ul>
      {toc_entries}
    </ul>
  </body>
</html>
"""

def convert_markdown_to_html(base_directory: str) -> None:
    """
    Converts Markdown files to HTML, saves them inside the frontend/pages directory,
    and generates a table of contents (TOC) in a <foldername>.html file inside that folder.
    TOC entries are formatted as "Chapter X" instead of just "X". Also, it adds a new entry
    to the library.json file in the frontend. HTML output is minified using htmlmin.

    Args:
        base_directory (str): The root directory containing the "books" folder.
    """
    books_directory = os.path.join(base_directory, "books")
    frontend_base_directory = os.path.join(os.path.dirname(base_directory), "frontend")
    pages_directory = os.path.join(frontend_base_directory, "pages")
    library_json_path = os.path.join(frontend_base_directory, "library", "library.json")

    # Check if easyread directory exists
    easyread_directory = os.path.join(books_directory, "easyread")
    if not os.path.exists(easyread_directory):
        print(f"Error: Directory '{easyread_directory}' not found")
        return

    for book_folder in os.listdir(easyread_directory):
        easyread_path = os.path.join(easyread_directory, book_folder)
        # Skip if not a directory
        if not os.path.isdir(easyread_path):
            continue
            
        book_name = book_folder
        frontend_book_path = os.path.join(pages_directory, book_name)
        final_html_file_path = os.path.join(frontend_book_path, f"{book_name}.html")

        # Create frontend book directory if it doesn't exist
        os.makedirs(frontend_book_path, exist_ok=True)

        toc_entries = ""

        for md_file in sorted(os.listdir(easyread_path)):
            if md_file.endswith(".md"):
                md_file_path = os.path.join(easyread_path, md_file)
                html_file_name = md_file.replace(".md", ".html")
                chapter_number = md_file.replace(".md", "")
                html_file_path = os.path.join(frontend_book_path, html_file_name)

                try:
                    with open(md_file_path, 'r', encoding='utf-8') as md_file_obj:
                        markdown_content = md_file_obj.read()

                    html_content = markdown2.markdown(markdown_content)

                    # Create HTML and minify it
                    final_html = HTML5_BOILERPLATE.format(
                        title=f"{book_name} - Chapter {chapter_number}",
                        content=html_content
                    )
                    minified_html = htmlmin.minify(final_html, remove_empty_space=True)

                    # Write individual chapter HTML files
                    with open(html_file_path, 'w', encoding='utf-8') as html_file_obj:
                        html_file_obj.write(minified_html)

                    # Create TOC entries with relative path
                    toc_entries += f'<li><a href="{html_file_name}">Chapter {chapter_number}</a></li>\n'

                except Exception as e:
                    print(f"Error converting '{md_file}': {e}")
                    continue

        # Create and minify the TOC HTML
        final_toc_html = TOC_HTML_BOILERPLATE.format(
            title=f"{book_name} - Table of Contents",
            toc_entries=toc_entries
        )
        minified_toc_html = htmlmin.minify(final_toc_html, remove_empty_space=True)

        # Write the minified TOC HTML file
        try:
            with open(final_html_file_path, 'w', encoding='utf-8') as html_file_obj:
                html_file_obj.write(minified_toc_html)
            print(f"Created minified TOC HTML file '{final_html_file_path}'")
        except Exception as e:
            print(f"Error creating TOC file '{final_html_file_path}': {e}")

        # Update library.json
        try:
            # Initialize empty list if library.json doesn't exist
            if not os.path.exists(library_json_path):
                library_data = []
            else:
                with open(library_json_path, 'r', encoding='utf-8') as f:
                    library_data = json.load(f)

            # Check if entry already exists to avoid duplicates
            new_entry = {
                "title": book_name,
                "link": f"pages/{book_name}/{book_name}.html",
                "cover": f"assets/covers/{book_name}.png"
            }
            
            if not any(entry["title"] == book_name for entry in library_data):
                library_data.append(new_entry)
                
                with open(library_json_path, 'w', encoding='utf-8') as f:
                    json.dump(library_data, f, indent=2)
                print(f"Added entry for '{book_name}' to library.json")
            else:
                print(f"Entry for '{book_name}' already exists in library.json")

        except Exception as e:
            print(f"Error updating library.json: {e}")

if __name__ == "__main__":
    # Get the base directory (two levels up from the current file)
    base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    convert_markdown_to_html(base_directory)