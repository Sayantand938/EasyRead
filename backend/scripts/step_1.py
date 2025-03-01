import os
import zipfile
import html2text
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.ERROR)  # Or level=logging.DEBUG for more detail


def clean_markdown(file_path):
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Strip leading and trailing blank lines
    while lines and lines[0].strip() == "":
        lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()

    # Replace multiple blank lines with a single blank line
    cleaned_lines = []
    blank_line = False

    for line in lines:
        if line.strip() == "":
            if not blank_line:
                cleaned_lines.append("\n")  # Keep a single blank line
            blank_line = True
        else:
            cleaned_lines.append(line)
            blank_line = False

    # Write back to file
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)

def epub_to_markdown(epub_file):
    try:
        with zipfile.ZipFile(epub_file, 'r') as epub:
            opf_file = None
            for name in epub.namelist():
                if name.endswith('.opf'):
                    opf_file = name
                    break

            if not opf_file:
                logging.error("No .opf file found in EPUB.")
                return

            opf_base_dir = os.path.dirname(opf_file) + '/' if os.path.dirname(opf_file) else ""
            opf_content = epub.read(opf_file).decode('utf-8')
            soup = BeautifulSoup(opf_content, 'xml')

            spine = soup.find('spine')
            if not spine:
                logging.error("No <spine> element found in OPF file.")
                return

            itemrefs = spine.find_all('itemref')
            reading_order = [itemref['idref'] for itemref in itemrefs]

            manifest = soup.find('manifest')
            if not manifest:
                logging.error("No <manifest> element found in OPF file.")
                return

            items = {item['id']: item['href'] for item in manifest.find_all('item')}
            base_output_dir = os.path.splitext(epub_file)[0]
            output_dir = os.path.join(project_root, "books", "og", os.path.basename(base_output_dir))
            os.makedirs(output_dir, exist_ok=True)

            markdown_counter = 1

            for item_id in reading_order:
                html_file = items.get(item_id)
                if not html_file:
                    continue

                full_html_path = opf_base_dir + html_file
                try:
                    html_content = epub.read(full_html_path).decode('utf-8')
                except KeyError:
                    logging.error(f"KeyError: Could not find HTML file: {full_html_path}")
                    continue
                except Exception as e:
                    logging.error(f"Error reading HTML file {full_html_path}: {e}")
                    continue


                h = html2text.HTML2Text()
                h.ignore_links = False
                h.body_width = 0
                markdown_content = h.handle(html_content)

                markdown_file = os.path.join(output_dir, f"{markdown_counter}.md")
                try:
                    with open(markdown_file, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                    markdown_counter += 1
                except Exception as e:
                    logging.error(f"Error writing Markdown file {markdown_file}: {e}")
                    continue

            print(f"Markdown files created for {os.path.basename(output_dir)} ✅")

            # Clean all markdown files
            for md_file in os.listdir(output_dir):
                if md_file.endswith(".md"):
                    clean_markdown(os.path.join(output_dir, md_file))

    except FileNotFoundError:
        logging.error(f"Error: EPUB file not found at {epub_file}")
        return
    except zipfile.BadZipFile:
        logging.error(f"Error: Invalid or corrupted EPUB file: {epub_file}")
        return
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return

if __name__ == "__main__":
    book_name = input("Enter the EPUB file name (without the .epub extension): ")
    # Construct absolute path to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Construct the absolute path to the epub file
    epub_file_path = os.path.join(project_root, "books", "epub", book_name + ".epub")
    print(f"Attempting to open EPUB at: {epub_file_path}") # Keep for debugging
    epub_to_markdown(epub_file_path)