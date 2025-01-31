import os
import markdown
import re
import htmlmin  # For HTML minification
import cssmin  # For CSS minification
import json

# Get the file name from the user
file_name = input("Enter the file name: ")

# Define the folder paths using environment variable for Obsidian notes directory
obsidian_notes_dir = os.getenv("OBSIDIAN_NOTES_DIR", r"D:\OBSIDIAN\NOTES")  # Default fallback
# pages_folder = os.path.join(os.getcwd(), "..", "pages")  # Path to pages folder
pages_folder = os.path.join(os.getcwd(), "..", "..", "frontend", "pages")

# Relative path to the JSON file
json_file_relative_path = os.path.join(pages_folder, "..", "json", "library.json")

# Resolve the relative path to an absolute path
json_file_path = os.path.abspath(json_file_relative_path)

# Construct the full path to the Markdown file
md_file_path = os.path.join(obsidian_notes_dir, file_name + ".md")

# Ensure the pages folder exists
os.makedirs(pages_folder, exist_ok=True)

def generate_toc(md_content):
    toc = []
    headings = re.findall(r"^(#{1,6})\s+(.*)$", md_content, re.MULTILINE)
    for level, heading in headings:
        margin_left = len(level)
        anchor = heading.lower().replace(" ", "-").replace(",", "").replace(".", "")
        toc.append(f'<li style="margin-left: {margin_left}em;"><a href="#{anchor}">{heading}</a></li>')
    
    if toc:
        return f'<ul style="list-style-type: disc; padding-left: 20px;">{"".join(toc)}</ul>'
    return ""

def add_ids_to_headings(md_content):
    def replace_heading(match):
        level, heading = match.groups()
        anchor = heading.lower().replace(" ", "-").replace(",", "").replace(".", "")
        return f'{level} <span id="{anchor}">{heading}</span>'
    
    md_content = re.sub(r"^(#{1,6})\s+(.*)$", replace_heading, md_content, flags=re.MULTILINE)
    return md_content

if os.path.exists(md_file_path):
    with open(md_file_path, "r", encoding="utf-8") as file:
        md_content = file.read()

    md_content = re.sub(r"^---.*?^---\s*", "", md_content, flags=re.DOTALL | re.MULTILINE)

    toc = generate_toc(md_content)
    md_content_with_ids = add_ids_to_headings(md_content)

    html_content = markdown.markdown(md_content_with_ids)

    css_content = """
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Martian+Mono:wght@100..800&family=Source+Code+Pro:ital,wght@0,200..900;1,200..900&display=swap');
        body {
            font-family: "Cascadia Code","JetBrains Mono";
            padding: 20px;
            background-color: #1e1e1e;
            color: #f1f1f1;
            font-size: 1.3rem;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
        }

        h1 {
            color: #dcef4a;
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 1.5rem;
            border-bottom: 2px solid #dcef4a;
            padding-bottom: 0.5rem;
            text-align: center;
            font-family: "Martian Mono";
        }

        h2 {
            color: #dcef4a;
            font-size: 1.75rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }

        h3 {
            color: #dcef4a;
            font-size: 1.5rem;
            margin-top: 1.75rem;
            margin-bottom: 0.75rem;
        }

        h4, h5, h6 {
            color: #dcef4a;
            font-size: 1.25rem;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
        }

        p {
            margin: 1rem 0;
            color: #f1f1f1;
        }

        a {
            color: #dcef4a;
            text-decoration: none;
            transition: color 0.3s ease;
        }

        a:hover {
            color: #81C784;
            text-decoration: underline;
        }

        pre {
            background-color: #2e2e2e;
            padding: 1rem;
            border-radius: 8px;
            color: #d1d1d1;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            overflow-x: auto;
            margin: 1.5rem 0;
        }

        code {
            color: #ffcc00;
            font-family: 'JetBrains Mono', monospace;
            background-color: #2e2e2e;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-size: 0.9rem;
        }

        ul, ol {
            margin: 1.5rem 0;
            padding-left: 1.5rem;
        }

        li {
            margin: 0.75rem 0;
        }

        blockquote {
            border-left: 4px solid #dcef4a;
            padding-left: 1rem;
            margin: 1.5rem 0;
            color: #ccc;
            font-style: italic;
        }

        #toc ul {
            list-style-type: disc;
            padding-left: 20px;
            margin: 0;
        }

        #toc li {
            margin: 0.5rem 0;
        }

        #toc a {
            color: #5ebaee;
            text-decoration: none;
            transition: color 0.3s ease;
        }

        #toc a:hover {
            color: #dcef4a;
        }

        ::-webkit-scrollbar {
            width: 12px;
        }

        ::-webkit-scrollbar-track {
            background: #2e2e2e;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: white;
            border-radius: 10px;
            border: 3px solid #2e2e2e;
        }

        @media (max-width: 768px) {
            body {
                padding: 15px;
                font-size: 0.9rem;
            }

            h1 {
                font-size: 1.75rem;
            }

            h2 {
                font-size: 1.5rem;
            }

            h3 {
                font-size: 1.25rem;
            }

            h4, h5, h6 {
                font-size: 1.1rem;
            }

            pre {
                padding: 0.75rem;
                font-size: 0.85rem;
            }

            code {
                font-size: 0.85rem;
            }

            ul, ol {
                padding-left: 1rem;
            }
        }

        @media (max-width: 480px) {
            body {
                padding: 12px;
                font-size: 1.1rem;
                font-weight: bold;
            }
            p {
                color: #d1d1d1;
            }
            h1 {
                font-size: 1.3rem;
            }

            h2 {
                font-size: 1.25rem;
            }

            h3 {
                font-size: 1.1rem;
            }

            h4, h5, h6 {
                font-size: 1rem;
            }

            pre {
                padding: 0.5rem;
                font-size: 0.8rem;
            }

            code {
                font-size: 0.8rem;
            }

            ul, ol {
                padding-left: 0.75rem;
            }
        }
    """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>{file_name}</title>        
        <style>
        {css_content}
        </style>
    </head>
    <body>
        <h1>{file_name}</h1>
        <div id="toc">{toc}</div>
        {html_content}
    </body>
    </html>
    """

    html_file_name = file_name.replace(" ", "_") + ".html"
    output_html_path = os.path.join(pages_folder, html_file_name)

    # Write HTML to the file
    with open(output_html_path, "w", encoding="utf-8") as output_file:
        output_file.write(html_template)

    # Minify CSS and HTML
    with open(output_html_path, "r", encoding="utf-8") as file:
        unminified_html = file.read()

    def minify_css_in_html(html):
        css_matches = re.findall(r"<style>(.*?)</style>", html, re.DOTALL)
        if css_matches:
            css_content = css_matches[0]
            minified_css = cssmin.cssmin(css_content)
            html = html.replace(css_content, minified_css)
        return html

    html_with_minified_css = minify_css_in_html(unminified_html)
    minified_html = htmlmin.minify(html_with_minified_css, remove_comments=True, remove_empty_space=True)

    with open(output_html_path, "w", encoding="utf-8") as output_file:
        output_file.write(minified_html)

    print(f"✅ Exported: {html_file_name}")

    # Gather all HTML file links from pages folder for the JSON file
    library_data = []
    for filename in os.listdir(pages_folder):
        if filename.endswith(".html"):
            title = filename.replace("_", " ").replace(".html", "")
            library_data.append({
                "title": title,
                "link": f"pages/{filename}"
            })

    # Write the new library data to JSON, overwriting it
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(library_data, json_file, ensure_ascii=False, indent=4)

else:
    print(f"❌ File not found: {md_file_path}")
