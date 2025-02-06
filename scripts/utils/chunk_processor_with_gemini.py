# chunk_processor_with_gemini.py
import os
import json
import itertools
import time
from openai import OpenAI

# Load the API keys from an environment variable
api_keys = os.getenv("GEMINI_API_KEYS")
if not api_keys:
    raise ValueError("GEMINI_API_KEYS environment variable not set")

# Split the API keys into a list
api_keys_list = api_keys.split(',')

# Create a round-robin iterator for the API keys
api_key_cycle = itertools.cycle(api_keys_list)

# Initialize the OpenAI client with the first API key
current_api_key = next(api_key_cycle)
client = OpenAI(
    api_key=current_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Define the log file path
logs_directory = "../logs"
log_file_path = os.path.join(logs_directory, "chunk_processor_logs.json")

# Ensure the logs directory exists
os.makedirs(logs_directory, exist_ok=True)

# Ensure the log file exists and is initialized
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        json.dump([], log_file, ensure_ascii=False, indent=4)

# Counter to keep track of processed chunks
processed_chunks_count = 0

def process_chunk_with_gemini(chunk):
    global current_api_key, processed_chunks_count  # Ensure current_api_key and processed_chunks_count are accessible within this function

    # Prepare the messages for the API call
    messages = [
        {
            "role": "system",
            "content": "You are a text refinement assistant. Your task is to replace unnecessarily complex words, phrases and sentences with simpler, more natural alternatives, making the text more accessible while preserving the original tone, style, and emotional depth. The goal is to make the writing clear and easy to understand for a broader audience without losing its literary richness, nuance, or emotional impact. Do not alter the sentence structure, paragraphing, or formatting. Maintain the original flow and mood of the text so it feels unchanged when read. Only return the refined text without additional explanations or comments",
        },
        {
            "role": "user",
            "content": f"Refine this text while maintaining its original paragraph structure. Only reply with the refined text:\n\n{chunk}",
        }
    ]

    for _ in range(len(api_keys_list)):
        try:
            # Send the request to the Gemini model
            response = client.chat.completions.create(
                model="gemini-2.0-flash-exp",
                n=1,
                messages=messages
            )

            # Extract the refined content from the response
            refined_chunk = response.choices[0].message.content

            # Log the original and refined chunks
            log_entry = {
                "original_chunk": chunk,
                "refined_chunk": refined_chunk
            }
            log_to_file(log_entry)

            # Ensure refined_chunk is a string
            if refined_chunk is None:
                refined_chunk = ""

            # Increment the processed chunks counter
            processed_chunks_count += 1

            # Take a 30-second break after every 50 chunks
            if processed_chunks_count % 50 == 0:
                time.sleep(30)

            return refined_chunk
        except Exception as e:
            # Switch to the next API key silently
            current_api_key = next(api_key_cycle)
            client.api_key = current_api_key

    # If all API keys fail, log an error message and return the original chunk
    print(f"All API keys failed for chunk: {chunk}")
    return chunk

def log_to_file(log_entry):
    # Read existing logs if the file exists
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            logs = json.load(log_file)
    else:
        logs = []

    # Append the new log entry
    logs.append(log_entry)

    # Write the updated logs back to the file
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        json.dump(logs, log_file, ensure_ascii=False, indent=4)

# Example usage
if __name__ == "__main__":
    sample_chunk = "This is a sample text that needs to be refined."
    refined_text = process_chunk_with_gemini(sample_chunk)
    print("Refined Text:", refined_text)
