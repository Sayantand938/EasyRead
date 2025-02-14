# chunk_processor_with_gemini.py
import os
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

# Variable to track the last request time
last_request_time = 0

def process_chunk_with_gemini(chunk):
    global current_api_key, last_request_time

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

    while True:
        try:
            # Enforce 1 RPS rate limit
            current_time = time.time()
            time_since_last_request = current_time - last_request_time
            if time_since_last_request < 1:
                time.sleep(1 - time_since_last_request)

            # Update the last request time
            last_request_time = time.time()

            # Send the request to the Gemini model
            response = client.chat.completions.create(
                model="gemini-2.0-flash-exp",
                n=1,
                messages=messages
            )
            # Extract the refined content from the response
            refined_chunk = response.choices[0].message.content

            # Ensure refined_chunk is a string
            if refined_chunk is None:
                refined_chunk = ""

            return refined_chunk

        except Exception:
            # Switch to the next API key and retry
            current_api_key = next(api_key_cycle)
            client.api_key = current_api_key

# Example usage
if __name__ == "__main__":
    sample_chunk = "This is a sample text that needs to be refined."
    refined_text = process_chunk_with_gemini(sample_chunk)