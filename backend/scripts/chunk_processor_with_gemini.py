# ==============================================================
#                 FOR BENGALI TRANSLATION
# ==============================================================

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
    """Processes a text chunk with the Gemini API, translating it from English to Bengali."""
    global last_request_time

    messages = [
        {
            "role": "system",
            "content": "Simplify the following English text so that it is easier to read and understand. Keep the meaning the same, use simple words, and make it clear for someone whose first language is not English. Avoid complex vocabulary and long sentences. In reply just give me the refined paragraohs"
        },
        {
            "role": "user",
            "content": chunk
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

            # Extract the translated content from the response
            translated_chunk = response.choices[0].message.content

            # Ensure translated_chunk is a string
            if translated_chunk is None:
                translated_chunk = ""

            return translated_chunk

        except Exception:
            # Retry with a different API key
            continue  # Continue the loop to try with the next API key


if __name__ == "__main__":
    sample_chunk1 = "This is a sample text that needs to be translated."
    translated_text1 = process_chunk_with_gemini(sample_chunk1)
    print(f"Translated text 1: {translated_text1}")

    sample_chunk2 = "Another sample chunk of text. It contains idiomatic expressions and cultural nuances that require precise translation."
    translated_text2 = process_chunk_with_gemini(sample_chunk2)
    print(f"Translated text 2: {translated_text2}")