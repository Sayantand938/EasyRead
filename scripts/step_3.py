import os
import json
from tqdm import tqdm
from utils.chunk_processor_with_gemini import process_chunk_with_gemini
from utils.chunk_processor_with_openai import process_chunk_with_openai

# Function to get user input for book name and file range
def get_user_input():
    book_name = input("Enter the book name: ")
    file_range = input("Enter the file range (e.g., 1-3 or a single number like 3): ")
    return book_name, file_range

# Function to construct the file path
def construct_file_path(books_directory, book_name, file_name):
    book_folder_path = os.path.join(books_directory, book_name)
    file_path = os.path.join(book_folder_path, f"{file_name}.md")
    return book_folder_path, file_path

# Function to read file content
def read_file_content(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to split paragraphs into chunks
def create_chunks(paragraphs, chunk_size):
    return [paragraphs[i:i + chunk_size] for i in range(0, len(paragraphs), chunk_size)]

# Function to save processed chunks to a file
def save_chunks_to_file(output_directory, book_name, processed_chunks):
    output_file_path = os.path.join(output_directory, f"{book_name}.md")
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        for chunk in processed_chunks:
            output_file.write(chunk + '\n\n')
    return output_file_path

# Main function to orchestrate the workflow
def main():
    # Constants
    books_directory = "../books"
    chunk_size = 10

    # Get the output directory from the environment variable
    output_directory = os.getenv("OBSIDIAN_NOTES_DIR")
    if not output_directory:
        raise ValueError("OBSIDIAN_NOTES_DIR environment variable not set")

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Step 1: Get user input
    book_name, file_range = get_user_input()

    # Step 2: Parse the file range
    try:
        if '-' in file_range:
            start, end = map(int, file_range.split('-'))
            file_names = [str(i) for i in range(start, end + 1)]
        else:
            file_names = [file_range]
    except ValueError:
        print("Invalid file range format. Please use the format 'start-end' or a single number.")
        return

    # Step 3: Process each file in the range
    for file_name in file_names:
        # Construct file paths
        book_folder_path, file_path = construct_file_path(books_directory, book_name, file_name)

        # Check if the folder and file exist
        if not os.path.exists(book_folder_path):
            print(f"The folder for the book '{book_name}' does not exist.")
            continue
        if not os.path.exists(file_path):
            print(f"The file '{file_name}.md' does not exist in the '{book_name}' folder.")
            continue

        # Read file content
        content = read_file_content(file_path)
        if content is None:
            print(f"Unable to read the file '{file_name}.md'.")
            continue

        # Split content into paragraphs (assuming content is already split into paragraphs)
        paragraphs = content.split('\n\n')

        # Create chunks of paragraphs
        chunks = create_chunks(paragraphs, chunk_size)

        # Process each chunk and save to file
        processed_chunks = []
        for chunk in tqdm(chunks, desc=f"Processing and writing chunks for {file_name}.md", unit="chunk"):
            processed_chunk = process_chunk_with_gemini('\n\n'.join(chunk)) # Switch this
            # processed_chunk = process_chunk_with_openai('\n\n'.join(chunk))
            if processed_chunk is None or processed_chunk.strip() == "":
                processed_chunk = ""
            processed_chunks.append(processed_chunk)
            with open(os.path.join(output_directory, f"{book_name}.md"), 'a', encoding='utf-8') as output_file:
                output_file.write(processed_chunk + '\n\n')

    print(f"✅ The refined texts have been saved")

# Run the main function
if __name__ == "__main__":
    main()
