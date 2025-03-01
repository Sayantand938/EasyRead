#! /usr/bin/python3
import os
import re
from typing import List
from chunk_processor_with_gemini import process_chunk_with_gemini
from tqdm import tqdm

def process_and_refine_markdown(project_root: str, book_name: str, file_name: str) -> None:
    """
    Extracts chunks of 10 paragraphs from a Markdown file, sends them to Gemini for refinement,
    reconstructs the Markdown file, and saves it in a new directory with the suffix "_EasyRead".

    Args:
        project_root (str): The root directory of the project.
        book_name (str): The name of the book (directory name under "books").
        file_name (str): The name of the Markdown file to process (without extension).

    Returns:
        None. Creates a new Markdown file in the "_EasyRead" directory.
    """
    book_directory: str = os.path.join(project_root, "books", "og", book_name)
    markdown_file_path: str = os.path.join(book_directory, f"{file_name}.md")
    easyread_directory: str = os.path.join(project_root, "books", "easyread", book_name.replace("_EasyRead", ""))
    new_markdown_file_path: str = os.path.join(easyread_directory, f"{file_name}.md")

    # Create the EasyRead directory if it doesn't exist
    os.makedirs(easyread_directory, exist_ok=True)

    try:
        with open(markdown_file_path, 'r', encoding='utf-8') as f:
            content: str = f.read()

        # Split the content into paragraphs based on two or more newlines.
        paragraphs: List[str] = re.split(r'\n\s*\n', content)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]  # Remove empty strings

        refined_paragraphs: List[str] = []
        num_chunks: int = (len(paragraphs) + 9) // 10  # Calculate total number of chunks
        with tqdm(total=num_chunks, desc="Refining Chunks") as pbar:
            for i in range(0, len(paragraphs), 10):
                chunk: List[str] = paragraphs[i:i + 10]
                chunk_content: str = "\n\n".join(chunk)  # Join paragraphs with double newlines

                # Send the chunk to Gemini for refinement
                try:
                    refined_chunk: str = process_chunk_with_gemini(chunk_content)
                except Exception as e:
                    refined_chunk: str = chunk_content  # Or some other fallback

                # Split the refined chunk back into paragraphs
                refined_paragraphs.extend(re.split(r'\n\s*\n', refined_chunk))

                pbar.update(1)  # Update progress bar

        # Reconstruct the Markdown content from the refined paragraphs, ensuring consistent spacing
        # Join paragraphs with exactly two newlines
        refined_content: str = "\n\n".join(refined_paragraphs)

        # Normalize all paragraph separations to exactly two newlines.
        refined_content = re.sub(r'\n+', '\n\n', refined_content)

        # Save the refined content to the new Markdown file in the EasyRead directory
        with open(new_markdown_file_path, 'w', encoding='utf-8') as f:
            f.write(refined_content)

    except FileNotFoundError:
        print(f"Error: File not found - {markdown_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    book_name: str = input("Enter the folder name (book name): ")
    file_name: str = input("Enter the markdown file name (without extension): ")

    # Get the project root directory (two levels up from the current script)
    project_root: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    process_and_refine_markdown(project_root, book_name, file_name)