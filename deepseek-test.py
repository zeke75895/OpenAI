from openai import OpenAI
import time
from datetime import datetime
import os
from dotenv import load_dotenv 

# Configuration
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# Function to read question from text file
def read_question_from_file(filename):
    """
    Read the content of a question file from the dsa-questions folder
    """
    filepath = f"dsa-questions/{filename}"
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Function to save conversation to file
def save_conversation_log(model_name, messages, response_content, reasoning_content, processing_time):
    """
    Save conversation details to a text file
    Includes reasoning content separately if available
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"deepseek_conversation_{timestamp}.txt"
    filepath = f"deepSeekConversations/{filename}"
    
    # Create directory if it doesn't exist
    os.makedirs("deepSeekConversations", exist_ok=True)
    
    log_entry = f"""
{'='*60}
CONVERSATION LOG - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
{'='*60}

MODEL: {model_name}
PROCESSING TIME: {processing_time:.2f} seconds

{'='*60}
INPUT MESSAGES:
{'='*60}

"""
    
    # Add all messages from the conversation
    for message in messages:
        log_entry += f"Role: {message['role'].upper()}\n"
        log_entry += f"Content: {message['content']}\n"
        log_entry += "-" * 40 + "\n"
    
    # Add reasoning content if available (for reasoning models)
    if reasoning_content:
        log_entry += f"""
{'='*60}
MODEL REASONING (Chain of Thought):
{'='*60}

{reasoning_content}

"""
    
    log_entry += f"""
{'='*60}
MODEL RESPONSE:
{'='*60}

{response_content}

{'='*60}
ADDITIONAL METADATA:
{'='*60}
- Timestamp: {datetime.now().isoformat()}
- Model: {model_name}
- Processing Time: {processing_time:.2f} seconds
- Total Messages: {len(messages)}
- Reasoning Content Included: {'Yes' if reasoning_content else 'No'}
"""
    
    # Save to file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(log_entry)
    
    print(f"Conversation saved to: {filepath}")
    return filepath

# Specify which question file to read
question_filename = "reorder_list.txt"

# Read the question from file
question_content = read_question_from_file(question_filename)

if question_content is None:
    print("Exiting program due to file read error.")
    exit()

# Conversation outline
model_name = "deepseek-reasoner"  # Change this to test different models

messages = [
    {"role": "system", "content": "You are a computer science college student. Solve the following DSA problem and provide your solution with explanation."},
    {"role": "user", "content": question_content},
]

try:
    # Start timing
    start_time = time.time()
    
    # Make the API call
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.7,
        stream=False
    )
    
    # Calculate processing time
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Extract response content based on model type
    response_message = response.choices[0].message
    
    # Check if this is a reasoning model by looking for reasoning_content attribute
    if hasattr(response_message, 'reasoning_content') and response_message.reasoning_content is not None:
        # This is a reasoning model (like deepseek-reasoner)
        reasoning_content = response_message.reasoning_content
        response_content = response_message.content
        print("=" * 60)
        print("MODEL REASONING (Chain of Thought):")
        print("=" * 60)
        print(reasoning_content)
        print("=" * 60)
        print("MODEL RESPONSE:")
        print("=" * 60)
        print(response_content)
    else:
        # This is a non-reasoning model (like deepseek-chat)
        reasoning_content = None
        response_content = response_message.content
        print("=" * 60)
        print("MODEL RESPONSE:")
        print("=" * 60)
        print(response_content)
    
    print("=" * 60)
    print(f"Processing time: {processing_time:.2f} seconds")
    
    # Save conversation to file
    save_conversation_log(model_name, messages, response_content, reasoning_content, processing_time)
    
except Exception as e:
    print(f"Error occurred: {e}")
    # Log any errors
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    error_filename = f"error_log_{timestamp}.txt"
    error_filepath = f"deepSeekConversations/{error_filename}"
    
    # Create directory if it doesn't exist
    os.makedirs("deepSeekConversations", exist_ok=True)
    
    with open(error_filepath, 'w', encoding='utf-8') as error_file:
        error_file.write(f"{datetime.now().isoformat()}: Error - {str(e)}\n")
        error_file.write(f"Model: {model_name}\n")
        error_file.write(f"Question file: {question_filename}\n")
        error_file.write(f"Messages: {messages}\n")
    
    print(f"Error details saved to: {error_filepath}")
