# import os
# from pathlib import Path
# from dotenv import load_dotenv
# from rewriter_openai import process_chunk_with_openai 
# from rewriter_gemini import process_chunk_with_gemini

# # Load environment variables from .env file
# load_dotenv()

# def parse_file_names(input_str):
#     """
#     Parse the user input to extract individual file numbers.
#     Supports comma-separated values (e.g., "1,2,3") and ranges (e.g., "1-3").
#     """
#     file_numbers = set()  # Use a set to avoid duplicates
#     parts = input_str.split(",")
#     for part in parts:
#         part = part.strip()
#         if "-" in part:  # Handle range (e.g., "1-3")
#             try:
#                 start, end = map(int, part.split("-"))
#                 file_numbers.update(range(start, end + 1))
#             except ValueError:
#                 print(f"Invalid range format: '{part}'. Skipping this part.")
#         else:  # Handle single number (e.g., "1")
#             try:
#                 file_numbers.add(int(part))
#             except ValueError:
#                 print(f"Invalid file number: '{part}'. Skipping this part.")
#     return sorted(file_numbers)  # Return sorted list of file numbers


# def write_chunk_to_file(output_file_path, chunk):
#     """
#     Append a chunk of content to the output file.
#     """
#     with open(output_file_path, "a", encoding="utf-8") as output_file:
#         output_file.write("\n\n".join(chunk))  # Join paragraphs with double newlines
#         output_file.write("\n\n")  # Add spacing after the chunk


# def process_file_in_chunks(md_file_path, output_file_path):
#     """
#     Read the content of a markdown file, split it into chunks of 10 paragraphs,
#     send each chunk to the `process_chunk_with_openai` function, and then write the processed
#     chunk to the output file.
#     """
#     try:
#         with open(md_file_path, "r", encoding="utf-8") as md_file:
#             paragraphs = md_file.read().split("\n\n")  # Split content into paragraphs
#     except FileNotFoundError:
#         print(f"Warning: The file '{md_file_path}' does not exist. Skipping.")
#         return

#     # Process the file in chunks of 10 paragraphs
#     chunk_size = 10
#     for i in range(0, len(paragraphs), chunk_size):
#         chunk = paragraphs[i:i + chunk_size]  # Extract a chunk of 10 paragraphs
        
#         # Send the chunk to the rewriter module for processing
#         # processed_chunk = process_chunk_with_openai(chunk) # USE OPENAI
#         processed_chunk = process_chunk_with_gemini(chunk) # USE OPENAI
        
#         # Write the processed chunk to the output file
#         write_chunk_to_file(output_file_path, processed_chunk)


# def main():
#     # Step 1: Accept folder name from the user
#     folder_name = input("Enter the folder name: ").strip()
    
#     # Construct the path to the folder inside ../books/
#     books_dir = Path("../books/")
#     target_folder = books_dir / folder_name
    
#     # Check if the folder exists
#     if not target_folder.exists() or not target_folder.is_dir():
#         print(f"Error: The folder '{folder_name}' does not exist in '../books/'.")
#         return
    
#     # Step 2: Ask the user for markdown file names (comma-separated or range)
#     input_str = input("Enter markdown file names (comma-separated or range, e.g., '1,2,3' or '1-3'): ").strip()
#     file_numbers = parse_file_names(input_str)
    
#     if not file_numbers:
#         print("No valid file numbers provided. Exiting.")
#         return
    
#     # Step 3: Save the content to a new file in OBSIDIAN_NOTES_DIR
#     obsidian_notes_dir = os.getenv("OBSIDIAN_NOTES_DIR")
#     if not obsidian_notes_dir:
#         print("Error: OBSIDIAN_NOTES_DIR is not set in the .env file.")
#         return
    
#     output_file_path = Path(obsidian_notes_dir) / f"{folder_name}.md"
    
#     # Process each file in chunks
#     for file_number in file_numbers:
#         md_file_path = target_folder / f"{file_number}.md"
        
#         # Check if the markdown file exists
#         if not md_file_path.exists() or not md_file_path.is_file():
#             print(f"Warning: The file '{file_number}.md' does not exist in the folder '{folder_name}'. Skipping.")
#             continue
        
#         print(f"Processing file: {md_file_path}")
#         process_file_in_chunks(md_file_path, output_file_path)
    
#     print(f"All content saved successfully to '{output_file_path}'.")

# if __name__ == "__main__":
#     main()



import os
from pathlib import Path
from dotenv import load_dotenv
from rewriter_gemini import process_chunk_with_gemini
from rewriter_openai import process_chunk_with_openai
from tqdm import tqdm  # Import tqdm for the progress bar

# Load environment variables from .env file
load_dotenv()

def parse_file_names(input_str):
    """
    Parse the user input to extract individual file numbers.
    Supports comma-separated values (e.g., "1,2,3") and ranges (e.g., "1-3").
    """
    file_numbers = set()  # Use a set to avoid duplicates
    parts = input_str.split(",")
    for part in parts:
        part = part.strip()
        if "-" in part:  # Handle range (e.g., "1-3")
            try:
                start, end = map(int, part.split("-"))
                file_numbers.update(range(start, end + 1))
            except ValueError:
                print(f"Invalid range format: '{part}'. Skipping this part.")
        else:  # Handle single number (e.g., "1")
            try:
                file_numbers.add(int(part))
            except ValueError:
                print(f"Invalid file number: '{part}'. Skipping this part.")
    return sorted(file_numbers)  # Return sorted list of file numbers


def write_chunk_to_file(output_file_path, chunk):
    """
    Append a chunk of content to the output file.
    """
    with open(output_file_path, "a", encoding="utf-8") as output_file:
        output_file.write("\n\n".join(chunk))  # Join paragraphs with double newlines
        output_file.write("\n\n")  # Add spacing after the chunk


def process_files_with_progress(target_folder, file_numbers, output_file_path):
    """
    Process all files and their chunks with a unified tqdm progress bar.
    """
    # Step 1: Calculate the total number of chunks across all files
    total_chunks = 0
    chunk_size = 10
    for file_number in file_numbers:
        md_file_path = target_folder / f"{file_number}.md"
        if md_file_path.exists() and md_file_path.is_file():
            with open(md_file_path, "r", encoding="utf-8") as md_file:
                paragraphs = md_file.read().split("\n\n")
                total_chunks += (len(paragraphs) + chunk_size - 1) // chunk_size  # Calculate chunks per file

    # Step 2: Create a unified tqdm progress bar
    with tqdm(total=total_chunks, desc="Total Progress", unit="chunk") as pbar:
        for file_number in file_numbers:
            md_file_path = target_folder / f"{file_number}.md"
            
            # Check if the markdown file exists
            if not md_file_path.exists() or not md_file_path.is_file():
                print(f"Warning: The file '{file_number}.md' does not exist. Skipping.")
                continue
            
            # Process the file in chunks
            try:
                with open(md_file_path, "r", encoding="utf-8") as md_file:
                    paragraphs = md_file.read().split("\n\n")  # Split content into paragraphs
                
                for i in range(0, len(paragraphs), chunk_size):
                    chunk = paragraphs[i:i + chunk_size]  # Extract a chunk of 10 paragraphs
                    
                    # Send the chunk to the rewriter module for processing
                    # processed_chunk = process_chunk_with_openai(chunk)
                    processed_chunk = process_chunk_with_gemini(chunk)
                    
                    # Write the processed chunk to the output file
                    write_chunk_to_file(output_file_path, processed_chunk)
                    
                    # Update the progress bar
                    pbar.update(1)
            except Exception as e:
                print(f"Error processing file {md_file_path}: {e}")


def main():
    # Step 1: Accept folder name from the user
    folder_name = input("Enter the folder name: ").strip()
    
    # Construct the path to the folder inside ../books/
    books_dir = Path("../books/")
    target_folder = books_dir / folder_name
    
    # Check if the folder exists
    if not target_folder.exists() or not target_folder.is_dir():
        print(f"Error: The folder '{folder_name}' does not exist in '../books/'.")
        return
    
    # Step 2: Ask the user for markdown file names (comma-separated or range)
    input_str = input("Enter markdown file names (comma-separated or range, e.g., '1,2,3' or '1-3'): ").strip()
    file_numbers = parse_file_names(input_str)
    
    if not file_numbers:
        print("No valid file numbers provided. Exiting.")
        return
    
    # Step 3: Save the content to a new file in OBSIDIAN_NOTES_DIR
    obsidian_notes_dir = os.getenv("OBSIDIAN_NOTES_DIR")
    if not obsidian_notes_dir:
        print("Error: OBSIDIAN_NOTES_DIR is not set in the .env file.")
        return
    
    output_file_path = Path(obsidian_notes_dir) / f"{folder_name}.md"
    
    # Process all files with a unified progress bar
    process_files_with_progress(target_folder, file_numbers, output_file_path)
    
    print(f"All content saved successfully to '{output_file_path}'.")


if __name__ == "__main__":
    main()