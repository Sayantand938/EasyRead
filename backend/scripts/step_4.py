# #!filepath step_4.py
# import os
# import markdown2

# HTML5_BOILERPLATE = """<!DOCTYPE html>
# <html lang="en">
#   <head>
#     <meta charset="UTF-8" />
#     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#     <link rel="stylesheet" href="../../assets/style/style.css" />
#     <title>{title}</title>
#   </head>
#   <body>
#     {content}
#   </body>
# </html>
# """

# TOC_HTML_BOILERPLATE = """<!DOCTYPE html>
# <html lang="en">
#   <head>
#     <meta charset="UTF-8" />
#     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#     <link rel="stylesheet" href="../../assets/style/style.css" />
#     <title>{title}</title>
#   </head>
#   <body>
#     <h1>Table of Contents</h1>
#     <ul>
#       {toc_entries}
#     </ul>
#   </body>
# </html>
# """


# def convert_markdown_to_html(base_directory: str) -> None:
#     """
#     Converts Markdown files to HTML, saves them inside the frontend/pages directory,
#     and generates a table of contents (TOC) in a <foldername>.html file inside that folder.
#     TOC entries are formatted as "Chapter X" instead of just "X".

#     Args:
#         base_directory (str): The root directory containing the "books" folder.
#     """
#     books_directory = os.path.join(base_directory, "books")
#     frontend_base_directory = os.path.join(os.path.dirname(base_directory), "frontend", "pages")  # Changed to "pages"

#     for book_folder in os.listdir(books_directory):
#         if book_folder.endswith("_EasyRead"):
#             easyread_path = os.path.join(books_directory, book_folder)
#             book_name = book_folder.replace("_EasyRead", "")
#             frontend_book_path = os.path.join(frontend_base_directory, book_name) #removed _EasyRead

#             # Change: Place the index.html inside the frontend_book_path
#             final_html_file_path = os.path.join(frontend_book_path, f"{book_name}.html")


#             # Create frontend book directory if it doesn't exist
#             os.makedirs(frontend_book_path, exist_ok=True)

#             toc_entries = ""

#             for md_file in sorted(os.listdir(easyread_path)):
#                 if md_file.endswith(".md"):
#                     md_file_path = os.path.join(easyread_path, md_file)
#                     html_file_name = md_file.replace(".md", ".html")
#                     chapter_number = md_file.replace(".md", "") # Get chapter number
#                     html_file_path = os.path.join(frontend_book_path, html_file_name)

#                     try:
#                         with open(md_file_path, 'r', encoding='utf-8') as md_file_obj:
#                             markdown_content = md_file_obj.read()

#                         html_content = markdown2.markdown(markdown_content)

#                         # Embed the HTML content within the boilerplate
#                         # Write to individual HTML files.
#                         with open(html_file_path, 'w', encoding='utf-8') as html_file_obj:
#                            final_html = HTML5_BOILERPLATE.format(title=md_file.replace(".md", ""), content=html_content)
#                            html_file_obj.write(final_html)

#                         # Create TOC entries
#                         toc_entries += f'<li><a href="{html_file_name}">Chapter {chapter_number}</a></li>\n'


#                     except Exception as e:
#                         print(f"Error converting '{md_file}': {e}")


#             # Create the TOC HTML

#             final_html = TOC_HTML_BOILERPLATE.format(title=book_name, toc_entries=toc_entries)

#             # Write the final HTML to the <foldername>.html file
#             with open(final_html_file_path, 'w', encoding='utf-8') as html_file_obj:
#                 html_file_obj.write(final_html)

#             print(f"Created combined HTML file '{book_name}.html'")


# if __name__ == "__main__":
#     # Get the base directory (two levels up from the current file)
#     base_directory = os.path.dirname(os.path.dirname(__file__))  # Corrected path

#     convert_markdown_to_html(base_directory)

#!filepath step_4.py
import os
import markdown2
import json

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
    to the library.json file in the frontend.

    Args:
        base_directory (str): The root directory containing the "books" folder.
    """
    books_directory = os.path.join(base_directory, "books")
    frontend_base_directory = os.path.join(os.path.dirname(base_directory), "frontend")
    pages_directory = os.path.join(frontend_base_directory, "pages")  # Changed to "pages"
    library_json_path = os.path.join(frontend_base_directory, "library", "library.json")


    for book_folder in os.listdir(books_directory):
        if book_folder.endswith("_EasyRead"):
            easyread_path = os.path.join(books_directory, book_folder)
            book_name = book_folder.replace("_EasyRead", "")
            frontend_book_path = os.path.join(pages_directory, book_name)  # removed _EasyRead

            # Change: Place the index.html inside the frontend_book_path
            final_html_file_path = os.path.join(frontend_book_path, f"{book_name}.html")


            # Create frontend book directory if it doesn't exist
            os.makedirs(frontend_book_path, exist_ok=True)

            toc_entries = ""

            for md_file in sorted(os.listdir(easyread_path)):
                if md_file.endswith(".md"):
                    md_file_path = os.path.join(easyread_path, md_file)
                    html_file_name = md_file.replace(".md", ".html")
                    chapter_number = md_file.replace(".md", "")  # Get chapter number
                    html_file_path = os.path.join(frontend_book_path, html_file_name)

                    try:
                        with open(md_file_path, 'r', encoding='utf-8') as md_file_obj:
                            markdown_content = md_file_obj.read()

                        html_content = markdown2.markdown(markdown_content)

                        # Embed the HTML content within the boilerplate
                        # Write to individual HTML files.
                        with open(html_file_path, 'w', encoding='utf-8') as html_file_obj:
                            final_html = HTML5_BOILERPLATE.format(title=md_file.replace(".md", ""), content=html_content)
                            html_file_obj.write(final_html)

                        # Create TOC entries
                        toc_entries += f'<li><a href="{html_file_name}">Chapter {chapter_number}</a></li>\n'


                    except Exception as e:
                        print(f"Error converting '{md_file}': {e}")


            # Create the TOC HTML

            final_html = TOC_HTML_BOILERPLATE.format(title=book_name, toc_entries=toc_entries)

            # Write the final HTML to the <foldername>.html file
            with open(final_html_file_path, 'w', encoding='utf-8') as html_file_obj:
                html_file_obj.write(final_html)

            print(f"Created combined HTML file '{book_name}.html'")

            # Update library.json
            try:
                with open(library_json_path, 'r', encoding='utf-8') as f:
                    library_data = json.load(f)

                new_entry = {
                    "title": book_name,
                    "link": f"pages/{book_name}/{book_name}.html",
                    "cover": f"assets/covers/{book_name}.png"
                }

                library_data.append(new_entry)

                with open(library_json_path, 'w', encoding='utf-8') as f:
                    json.dump(library_data, f, indent=2)

                print(f"Added entry for '{book_name}' to library.json")

            except Exception as e:
                print(f"Error updating library.json: {e}")


if __name__ == "__main__":
    # Get the base directory (two levels up from the current file)
    base_directory = os.path.dirname(os.path.dirname(__file__))  # Corrected path

    convert_markdown_to_html(base_directory)