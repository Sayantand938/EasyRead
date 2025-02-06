# # # web_export.py
# # import os
# # import re
# # import yaml
# # import markdown2
# # import htmlmin
# # import json

# # # Retrieve the OBSIDIAN_NOTES_DIR from the environment variable
# # OBSIDIAN_NOTES_DIR = os.environ.get('OBSIDIAN_NOTES_DIR')

# # if not OBSIDIAN_NOTES_DIR:
# #     print("Environment variable OBSIDIAN_NOTES_DIR is not set.")
# #     exit(1)

# # # Define the output directory for the HTML files
# # output_dir = os.path.join(os.path.dirname(__file__), '../web/pages')

# # # Ensure the output directory exists
# # os.makedirs(output_dir, exist_ok=True)

# # # Define the directory for the JSON file
# # json_dir = os.path.join(os.path.dirname(__file__), '../web/library')

# # # Ensure the JSON directory exists
# # os.makedirs(json_dir, exist_ok=True)

# # # Function to delete all .html files in the output directory
# # def delete_html_files(directory):
# #     for root, _, files in os.walk(directory):
# #         for file_name in files:
# #             if file_name.endswith('.html'):
# #                 file_path = os.path.join(root, file_name)
# #                 os.remove(file_path)

# # # Function to check if a file has the 'EasyRead' tag in its YAML front matter
# # def has_easyread_tag(file_path):
# #     with open(file_path, 'r', encoding='utf-8') as file:
# #         content = file.read()
# #         yaml_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
# #         if yaml_match:
# #             yaml_content = yaml_match.group(1)
# #             yaml_data = yaml.safe_load(yaml_content)
# #             if 'tags' in yaml_data and 'EasyRead' in yaml_data['tags']:
# #                 return True, yaml_match.group(2)
# #     return False, None

# # # Delete all existing .html files in the output directory
# # delete_html_files(output_dir)

# # # List to hold the library data
# # library_data = []

# # # Iterate through all .md files in the OBSIDIAN_NOTES_DIR
# # for root, _, files in os.walk(OBSIDIAN_NOTES_DIR):
# #     for file_name in files:
# #         if file_name.endswith('.md'):
# #             markdown_file_path = os.path.join(root, file_name)
# #             has_tag, markdown_content = has_easyread_tag(markdown_file_path)
# #             if has_tag:
# #                 # Convert the Markdown content (excluding YAML front matter) to HTML
# #                 html_content = markdown2.markdown(markdown_content, extras=["header-ids"])

# #                 # Define the HTML5 boilerplate template
# #                 file_name_without_extension = os.path.splitext(file_name)[0]
# #                 html_boilerplate = f"""
# #                 <!DOCTYPE html>
# #                 <html lang="en">
# #                 <head>
# #                     <meta charset="UTF-8">
# #                     <meta name="viewport" content="width=device-width, initial-scale=1.0">
# #                     <title>{file_name_without_extension}</title>
# #                     <link rel="stylesheet" href="../assets/style/style.css" />
# #                     <script src="https://cdn.jsdelivr.net/npm/tocbot@4.8.1/dist/tocbot.min.js"></script>
# #                 </head>
# #                 <body>
# #                     <!-- Sidebar -->
# #                     <div id="sidebar" class="sidebar">
# #                         <div id="toc-container"></div>
# #                     </div>

# #                     <h1>{file_name_without_extension}</h1>
# #                     {html_content}
# #                     <div id="sidebar" class="sidebar">
# #                         <div id="toc-container"></div>
# #                     </div>

# #                     <script src="../assets/script/script.js"></script>
# #                 </body>
# #                 </html>
# #                 """

# #                 # Minify the HTML content
# #                 minified_html = htmlmin.minify(html_boilerplate, remove_comments=True, remove_empty_space=True)

# #                 # Define the output HTML file path
# #                 html_file_path = os.path.join(output_dir, file_name_without_extension + '.html')

# #                 # Save the minified HTML content to the file
# #                 with open(html_file_path, 'w', encoding='utf-8') as file:
# #                     file.write(minified_html)

# #                 print(f"{file_name} is Processed ✅")

# #                 # Add the book data to the library list
# #                 library_data.append({
# #                     "title": file_name_without_extension,
# #                     "link": f"pages/{file_name_without_extension}.html",
# #                     "cover": f"pages/covers/{file_name_without_extension}.png",
# #                 })

# # # Define the path to the library.json file
# # library_json_path = os.path.join(json_dir, 'library.json')

# # # Save the library data to the library.json file
# # with open(library_json_path, 'w', encoding='utf-8') as json_file:
# #     json.dump(library_data, json_file, ensure_ascii=False, indent=4)


# import os
# import re
# import yaml
# import markdown2
# import json

# # Retrieve the OBSIDIAN_NOTES_DIR from the environment variable
# OBSIDIAN_NOTES_DIR = os.environ.get('OBSIDIAN_NOTES_DIR')

# if not OBSIDIAN_NOTES_DIR:
#     print("Environment variable OBSIDIAN_NOTES_DIR is not set.")
#     exit(1)

# # Define the output directory for the HTML files
# output_dir = os.path.join(os.path.dirname(__file__), '../web/books')

# # Ensure the output directory exists
# os.makedirs(output_dir, exist_ok=True)

# # Define the directory for the JSON file
# json_dir = os.path.join(os.path.dirname(__file__), '../web/library')

# # Ensure the JSON directory exists
# os.makedirs(json_dir, exist_ok=True)

# # Function to delete all .html files in the output directory
# def delete_html_files(directory):
#     for root, _, files in os.walk(directory):
#         for file_name in files:
#             if file_name.endswith('.html'):
#                 file_path = os.path.join(root, file_name)
#                 os.remove(file_path)

# # Function to check if a file has the 'EasyRead' tag in its YAML front matter
# def has_easyread_tag(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         content = file.read()
#         yaml_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
#         if yaml_match:
#             yaml_content = yaml_match.group(1)
#             yaml_data = yaml.safe_load(yaml_content)
#             if 'tags' in yaml_data and 'EasyRead' in yaml_data['tags']:
#                 return True, yaml_match.group(2)
#     return False, None

# # Delete all existing .html files in the output directory
# delete_html_files(output_dir)

# # List to hold the library data
# library_data = []

# # Iterate through all .md files in the OBSIDIAN_NOTES_DIR
# for root, _, files in os.walk(OBSIDIAN_NOTES_DIR):
#     for file_name in files:
#         if file_name.endswith('.md'):
#             markdown_file_path = os.path.join(root, file_name)
#             has_tag, markdown_content = has_easyread_tag(markdown_file_path)
#             if has_tag:
#                 # Create a directory for the markdown file
#                 file_name_without_extension = os.path.splitext(file_name)[0]
#                 book_output_dir = os.path.join(output_dir, file_name_without_extension)
#                 os.makedirs(book_output_dir, exist_ok=True)

#                 # Split the markdown content by Heading 2
#                 headings = re.split(r'(\n## .+)', markdown_content)
#                 chapter_links = []

#                 for i in range(1, len(headings), 2):
#                     heading_title = headings[i].strip().lstrip('##').strip()
#                     chapter_content = headings[i] + headings[i + 1]

#                     # Convert the Markdown content to HTML
#                     html_content = markdown2.markdown(chapter_content, extras=["header-ids"])

#                     # Define the HTML5 boilerplate template
#                     html_boilerplate = f"""
#                     <!DOCTYPE html>
#                     <html lang="en">
#                     <head>
#                         <meta charset="UTF-8">
#                         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#                         <title>{heading_title}</title>
#                         <link rel="stylesheet" href="../../assets/style/style.css" />
#                         <script src="https://cdn.jsdelivr.net/npm/tocbot@4.8.1/dist/tocbot.min.js"></script>
#                     </head>
#                     <body>
#                         <h1>{heading_title}</h1>
#                         {html_content}
#                         <script src="../../assets/script/script.js"></script>
#                     </body>
#                     </html>
#                     """

#                     # Define the output HTML file path
#                     chapter_file_name = f"{heading_title}.html".replace(" ", "_")
#                     chapter_file_path = os.path.join(book_output_dir, chapter_file_name)

#                     # Save the HTML content to the file
#                     with open(chapter_file_path, 'w', encoding='utf-8') as file:
#                         file.write(html_boilerplate)

#                     print(f"{heading_title} is Processed ✅")

#                     # Add the chapter link to the list
#                     chapter_links.append(f'<a href="{chapter_file_name}">{heading_title}</a>')

#                 # Create an index HTML file for the book
#                 index_content = f"""
#                 <!DOCTYPE html>
#                 <html lang="en">
#                 <head>
#                     <meta charset="UTF-8">
#                     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#                     <title>{file_name_without_extension}</title>
#                     <link rel="stylesheet" href="../../assets/style/style.css" />
#                 </head>
#                 <body>
#                     <h1>{file_name_without_extension}</h1>
#                     <ul>
#                         {''.join(f'<li>{link}</li>' for link in chapter_links)}
#                     </ul>
#                 </body>
#                 </html>
#                 """

#                 # Define the output index HTML file path
#                 index_file_path = os.path.join(book_output_dir, f"{file_name_without_extension}.html")

#                 # Save the index HTML content to the file
#                 with open(index_file_path, 'w', encoding='utf-8') as file:
#                     file.write(index_content)

#                 print(f"Index for {file_name_without_extension} is Processed ✅")

#                 # Add the book data to the library list
#                 library_data.append({
#                     "title": file_name_without_extension,
#                     "link": f"books/{file_name_without_extension}/{file_name_without_extension}.html",
#                     "cover": f"books/covers/{file_name_without_extension}.png",
#                 })

# # Define the path to the library.json file
# library_json_path = os.path.join(json_dir, 'library.json')

# # Save the library data to the library.json file
# with open(library_json_path, 'w', encoding='utf-8') as json_file:
#     json.dump(library_data, json_file, ensure_ascii=False, indent=4)



import os
import re
import yaml
import markdown2
import json

# Retrieve the OBSIDIAN_NOTES_DIR from the environment variable
OBSIDIAN_NOTES_DIR = os.environ.get('OBSIDIAN_NOTES_DIR')

if not OBSIDIAN_NOTES_DIR:
    print("Environment variable OBSIDIAN_NOTES_DIR is not set.")
    exit(1)

# Define the output directory for the HTML files
output_dir = os.path.join(os.path.dirname(__file__), '../web/books')

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define the directory for the JSON file
json_dir = os.path.join(os.path.dirname(__file__), '../web/library')

# Ensure the JSON directory exists
os.makedirs(json_dir, exist_ok=True)

# Function to delete all .html files in the output directory
def delete_html_files(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.html'):
                file_path = os.path.join(root, file_name)
                os.remove(file_path)

# Function to check if a file has the 'EasyRead' tag in its YAML front matter
def has_easyread_tag(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        yaml_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            yaml_data = yaml.safe_load(yaml_content)
            if 'tags' in yaml_data and 'EasyRead' in yaml_data['tags']:
                return True, yaml_match.group(2)
    return False, None

# Delete all existing .html files in the output directory
delete_html_files(output_dir)

# List to hold the library data
library_data = []

# Iterate through all .md files in the OBSIDIAN_NOTES_DIR
for root, _, files in os.walk(OBSIDIAN_NOTES_DIR):
    for file_name in files:
        if file_name.endswith('.md'):
            markdown_file_path = os.path.join(root, file_name)
            has_tag, markdown_content = has_easyread_tag(markdown_file_path)
            if has_tag:
                # Create a directory for the markdown file
                file_name_without_extension = os.path.splitext(file_name)[0]
                book_output_dir = os.path.join(output_dir, file_name_without_extension)
                os.makedirs(book_output_dir, exist_ok=True)

                # Split the markdown content by Heading 2
                headings = re.split(r'(\n## .+)', markdown_content)
                chapter_links = []

                for i in range(1, len(headings), 2):
                    heading_title = headings[i].strip().lstrip('##').strip()
                    chapter_content = headings[i] + headings[i + 1]

                    # Convert the Markdown content to HTML
                    html_content = markdown2.markdown(chapter_content, extras=["header-ids"])

                    # Define the HTML5 boilerplate template
                    html_boilerplate = f"""
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

                    # Define the output HTML file path
                    chapter_file_name = f"{heading_title}.html".replace(" ", "_")
                    chapter_file_path = os.path.join(book_output_dir, chapter_file_name)

                    # Save the HTML content to the file
                    with open(chapter_file_path, 'w', encoding='utf-8') as file:
                        file.write(html_boilerplate)

                    print(f"{heading_title} is Processed ✅")

                    # Add the chapter link to the list
                    chapter_links.append(f'<a href="{chapter_file_name}">{heading_title}</a>')

                # Create an index HTML file for the book
                index_content = f"""
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
                        {''.join(f'<li>{link}</li>' for link in chapter_links)}
                    </ul>
                </body>
                </html>
                """

                # Define the output index HTML file path
                index_file_path = os.path.join(book_output_dir, f"{file_name_without_extension}.html")

                # Save the index HTML content to the file
                with open(index_file_path, 'w', encoding='utf-8') as file:
                    file.write(index_content)

                print(f"Index for {file_name_without_extension} is Processed ✅")

                # Add the book data to the library list
                library_data.append({
                    "title": file_name_without_extension,
                    "link": f"books/{file_name_without_extension}/{file_name_without_extension}.html",
                    "cover": f"assets/covers/{file_name_without_extension}.png",
                })

# Define the path to the library.json file
library_json_path = os.path.join(json_dir, 'library.json')

# Save the library data to the library.json file
with open(library_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(library_data, json_file, ensure_ascii=False, indent=4)
