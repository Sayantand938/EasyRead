import os
import re
import yaml
import json
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY is not set in the .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def get_valid_book_name():
    while True:
        book_name = input("Enter the book name: ")
        if "(OG)" in book_name:
            return book_name
        print("The book name must include '(OG)' as a subtext. Please try again.")

def get_clean_filename(book_name):
    return book_name.replace("(OG)", "").strip() + ".md"

def extract_yaml_frontmatter(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    match = re.search(r"^---\s*$(.*?)^---\s*$", content, re.DOTALL | re.MULTILINE)
    return yaml.safe_load(match.group(1)) if match else None

def extract_chapter_by_number(file_path, chapter_number):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    pattern = rf"^(##\s+Chapter\s+{chapter_number}.*?)(?=^##|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    if match:
        full_match = match.group(1).strip()
        heading_pattern = r"^(##\s+Chapter\s+\d+.*)"
        heading_match = re.search(heading_pattern, full_match, re.MULTILINE)
        heading = heading_match.group(1).strip() if heading_match else ""
        chapter_content = full_match[len(heading):].strip()
        return heading, chapter_content
    return None, None

def split_into_chunks(chapter_content, chunk_size=10):
    paragraphs = [p.strip() for p in chapter_content.split("\n\n") if p.strip()]
    return ["\n\n".join(paragraphs[i:i + chunk_size]) for i in range(0, len(paragraphs), chunk_size)]

def refine_chunk_with_openai(chunk):
    try:
        request_payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": (
                    "You are a text refinement assistant. Improve clarity while preserving structure. "
                    "Use simpler vocabulary, keep markdown, and respond only with the refined text."
                )},
                {"role": "user", "content": chunk}
            ]
        }
        
        completion = client.chat.completions.create(**request_payload)
        
        return {
            "raw_request": request_payload,
            "raw_response": completion.model_dump()
        }
        
    except Exception as e:
        print(f"Error refining chunk: {e}")
        return {
            "raw_request": None,
            "raw_response": None
        }

def save_response_logs(logs, script_dir):
    log_file_path = os.path.join(script_dir, "../logs/response_logs.json")
    existing_logs = []
    
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8') as file:
            existing_logs = json.load(file)

    existing_logs.extend(logs)

    with open(log_file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_logs, file, indent=4, ensure_ascii=False)

def parse_chapter_input(chapter_input):
    chapters = set()
    parts = chapter_input.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            chapters.update(range(start, end + 1))
        else:
            chapters.add(int(part))
    return sorted(chapters)

def write_to_file(file_path, yaml_frontmatter, chapters):
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml_str = yaml.dump(yaml_frontmatter, allow_unicode=True, sort_keys=False)
        file.write(f"---\n{yaml_str}---\n\n")
        for heading, refined_chunks in chapters:
            file.write(f"{heading}\n\n")
            for chunk in refined_chunks:
                file.write(f"{chunk}\n\n")

def process_chapters(book_file_path, chapter_numbers):
    chapter_contents = []
    for chapter_number in chapter_numbers:
        heading, chapter_content = extract_chapter_by_number(book_file_path, chapter_number)
        if chapter_content:
            chapter_contents.append((chapter_number, heading, chapter_content))
        else:
            print(f"Warning: Chapter {chapter_number} not found.")
    return chapter_contents

def refine_chapters(chapter_contents):
    refined_chapters = []
    logs = []
    
    total_chunks = sum(len(split_into_chunks(content)) for _, _, content in chapter_contents)
    
    with tqdm(total=total_chunks, desc="Refining Chapters", unit="chunk") as pbar:
        for chapter_number, heading, chapter_content in chapter_contents:
            refined_chunks = []
            chunks = split_into_chunks(chapter_content)
            
            for chunk in chunks:
                response_data = refine_chunk_with_openai(chunk)
                refined_chunks.append(response_data["raw_response"]["choices"][0]["message"]["content"] if response_data["raw_response"] else chunk)
                logs.append(response_data)
                
                pbar.update(1)
            
            refined_chapters.append((heading, refined_chunks))
    
    return refined_chapters, logs

if __name__ == "__main__":
    book_name = get_valid_book_name()
    clean_file_name = get_clean_filename(book_name)
    obsidian_notes_dir = os.getenv("OBSIDIAN_NOTES_DIR")
    
    if not obsidian_notes_dir:
        print("Error: Environment variable 'OBSIDIAN_NOTES_DIR' is not set.")
        exit(1)
    
    book_file_path = os.path.join(obsidian_notes_dir, f"{book_name}.md")
    
    if not os.path.exists(book_file_path):
        print(f"Error: The file '{book_file_path}' does not exist.")
        exit(1)
    
    yaml_frontmatter = extract_yaml_frontmatter(book_file_path)
    
    if not yaml_frontmatter:
        print("Error: No YAML frontmatter found.")
        exit(1)
    
    chapter_input = input("Enter chapter numbers: ")
    chapter_numbers = parse_chapter_input(chapter_input)
    chapter_contents = process_chapters(book_file_path, chapter_numbers)
    
    if not chapter_contents:
        print("No valid chapters found. Exiting...")
        exit(1)
    
    refined_chapters, logs = refine_chapters(chapter_contents)
    
    save_response_logs(logs, os.path.dirname(os.path.abspath(__file__)))
    
    target_file_path = os.path.join(obsidian_notes_dir, clean_file_name)
    write_to_file(target_file_path, yaml_frontmatter, refined_chapters)
    
    print(f"Refined content saved to '{target_file_path}'.")
