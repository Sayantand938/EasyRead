# chunk_processor_with_openai.py 
import os
import json
from openai import OpenAI


# Initialize the OpenAI client
client = OpenAI()

# Define the log file path
logs_directory = "../logs"
log_file_path = os.path.join(logs_directory, "chunk_processor_logs.json")

# Ensure the logs directory exists
os.makedirs(logs_directory, exist_ok=True)

# Ensure the log file exists and is initialized
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        json.dump([], log_file, ensure_ascii=False, indent=4)

def process_chunk_with_openai(chunk):
    # Prepare the messages for the API call
    messages = [
        {
            "role": "system",
            "content": "You are a text refinement assistant. Your task is to replace unnecessarily complex words with simpler, more natural alternatives while preserving the original tone, style, and emotional depth. Ensure that the refined text retains its literary richness and does not lose nuance or impact. Do not alter sentence structure, paragraphing, or formatting. Maintain the original taste of the writing so that it feels the same when read. Only return the refined text without additional explanations.",
        },
        {
            "role": "user",
            "content": f"Refine this text while maintaining its original paragraph structure. Only reply the refiend text:\n\n{chunk}",
        }
    ]

    try:
        # Send the request to the Gemini model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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

        return refined_chunk
    except Exception as e:
        print(f"Error during API call: {e}")
        return chunk  # Return the original chunk if an error occurs

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
    refined_text = process_chunk(sample_chunk)
    print("Refined Text:", refined_text)
