# import os
# import google.generativeai as genai

# # Load environment variables from .env file
# from dotenv import load_dotenv
# load_dotenv()

# # Configure Gemini API
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Create the model with a specific configuration
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.5,
#     "top_k": 40,
#     "max_output_tokens": 8192,
#     "response_mime_type": "text/plain",
# }

# # Initialize the Gemini model
# model = genai.GenerativeModel(
#     model_name="gemini-2.0-flash-exp",
#     generation_config=generation_config,
# )

# def process_chunk_with_gemini(chunk):
#     """
#     Receive a chunk, send it to Gemini for refinement,
#     and return the refined content.
#     """
#     # Join the paragraphs in the chunk into a single string
#     chunk_text = "\n\n".join(chunk)

#     try:
#         # Send the chunk to Gemini for refinement using the same prompt as OpenAI
#         response = model.generate_content(
#             f"You are a text refinement assistant. Improve clarity while preserving structure. Use simpler vocabulary, keep markdown, and respond only with the refined text.:\n\n{chunk_text}"
#         )
        
#         # Extract the refined content from the response
#         refined_content = response.text.strip()
#         return [refined_content]  # Return as a list to maintain compatibility with chunks
#     except Exception as e:
#         print(f"Error processing chunk with Gemini: {e}")
#         return chunk  # Return the original chunk if an error occurs



import os
import google.generativeai as genai
from dotenv import load_dotenv
from itertools import cycle

# Load environment variables from .env file
load_dotenv()

# Retrieve the comma-separated API keys and create a round-robin iterator
api_keys = os.getenv("GEMINI_API_KEYS", "").split(",")
api_key_cycle = cycle(api_keys)  # Create an infinite cycle of API keys

# Initialize the Gemini model with the first API key
current_api_key = next(api_key_cycle)
genai.configure(api_key=current_api_key)

# Create the model with a specific configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.5,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

def process_chunk_with_gemini(chunk):
    """
    Receive a chunk, send it to Gemini for refinement,
    and return the refined content. If an error occurs, switch to the next API key
    and retry the request.
    """
    global current_api_key  # Use the global variable to track the current API key
    
    # Join the paragraphs in the chunk into a single string
    chunk_text = "\n\n".join(chunk)
    
    while True:  # Keep retrying until a successful response is received
        try:
            # Send the chunk to Gemini for refinement using the same prompt as OpenAI
            response = model.generate_content(
                f"You are a text refinement assistant. Replace the advanced vocabulary with simpler alternatives. Preserve the original structure. Stick to the original source as much as possible while simplifying complex sentences into easier to understand sentences. Just reply with the refined text.:\n\n{chunk_text}"
            )
            
            # Extract the refined content from the response
            refined_content = response.text.strip()
            return [refined_content]  # Return as a list to maintain compatibility with chunks
        
        except Exception:
            # If an error occurs, switch to the next API key and retry
            current_api_key = next(api_key_cycle)
            genai.configure(api_key=current_api_key)            