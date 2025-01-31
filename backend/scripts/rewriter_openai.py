import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def process_chunk_with_openai(chunk):
    """
    Receive a chunk, send it to gpt-4o-mini for summarization,
    and return the summarized content.
    """
    # Join the paragraphs in the chunk into a single string
    chunk_text = "\n\n".join(chunk)

    try:
        # Send the chunk to gpt-4o-mini for summarization
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a text refinement assistant. Improve clarity while preserving structure. Use simpler vocabulary, keep markdown, and respond only with the refined text."},
                {
                    "role": "user",
                    "content": f"Refine this text. In reply only give me the refined text in the original format it was given.:\n\n{chunk_text}"
                }
            ]
        )
        # Extract the summarized content from the response
        summarized_content = completion.choices[0].message.content.strip()
        return [summarized_content]  # Return as a list to maintain compatibility with chunks
    except Exception as e:
        print(f"Error processing chunk with gpt-4o-mini: {e}")
        return chunk  # Return the original chunk if an error occurs
    
    
    