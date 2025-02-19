#!filepath chunk_processor_with_gemini.py
import os
import itertools
import time
from openai import OpenAI
from typing import List

# Load the API keys from an environment variable
api_keys = os.getenv("GEMINI_API_KEYS")
if not api_keys:
    raise ValueError("GEMINI_API_KEYS environment variable not set")

# Split the API keys into a list
api_keys_list = api_keys.split(',')

# Create a round-robin iterator for the API keys
api_key_cycle = itertools.cycle(api_keys_list)


def get_client(api_key: str) -> OpenAI:
    """Initializes and returns an OpenAI client with the given API key."""
    return OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )


# Variable to track the last request time
last_request_time = 0


def process_chunk_with_gemini(chunk: str) -> str:
    """Processes a text chunk with the Gemini API, managing API keys and handling rate limits.
    Switches API key for every new chunk and upon encountering errors.
    Retries infinitely with new API keys until the chunk is processed successfully.
    """
    global last_request_time

    messages = [
        {
            "role": "system",
            "content": "You are a text refinement assistant. Your task is to simplify unnecessarily complex words, phrases, and sentences, making the text more natural and accessible to non-native English readers while preserving its original tone and style. The goal is to ensure clarity and ease of understanding without altering sentence structure, paragraphing, or formatting. Maintain the original flow and mood. Only return the refined text without additional explanations or comments. If the text has any markdown headings, then leave the heading as it is.",
        },
        {
            "role": "user",
            "content": f"Refine this text while maintaining its original paragraph structure. Only reply with the refined text:\n\n{chunk}",
        }
    ]

    while True:
        # Switch to a new API key
        current_api_key = next(api_key_cycle)
        client = get_client(current_api_key)

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
                model="gemini-2.0-flash",
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
            # Retry with a different API key
            continue  # Continue the loop to try with the next API key


if __name__ == "__main__":
    sample_chunk1 = "This is a sample text that needs to be refined."
    refined_text1 = process_chunk_with_gemini(sample_chunk1)
    print(f"Refined text 1: {refined_text1}")

    sample_chunk2 = "Another sample chunk of text. It uses some complex and complicated words, phrases and sentences, but it needs to be refined."
    refined_text2 = process_chunk_with_gemini(sample_chunk2)
    print(f"Refined text 2: {refined_text2}")