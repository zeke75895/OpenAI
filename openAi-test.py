from openai import OpenAI
import time
from datetime import datetime
import os
from dotenv import load_dotenv 

# Configuration
load_dotenv()

api_key = os.getenv("OPEN_AI_API_KEY")


client = OpenAI(
    api_key=api_key
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
def save_conversation_log(model_name, input_data, output_content, processing_time):
    """
    Save conversation details to a text file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"openai_conversation_{timestamp}.txt"
    filepath = f"OpenAiConversations/{filename}"
    
    # Create directory if it doesn't exist
    os.makedirs("OpenAiConversations", exist_ok=True)
    
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
    
    # Add all messages from the input
    for item in input_data:
        log_entry += f"Role: {item['role'].upper()}\n"
        log_entry += f"Content: {item['content']}\n"
        log_entry += "-" * 40 + "\n"
    
    log_entry += f"""
{'='*60}
MODEL RESPONSE:
{'='*60}

{output_content}

{'='*60}
ADDITIONAL METADATA:
{'='*60}
- Timestamp: {datetime.now().isoformat()}
- Model: {model_name}
- Processing Time: {processing_time:.2f} seconds
- Total Input Items: {len(input_data)}
- Response ID: {response.id if hasattr(response, 'id') else 'N/A'}
- Model Used: {response.model if hasattr(response, 'model') else model_name}
"""
    
    # Save to file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(log_entry)
    
    print(f"\nConversation saved to: {filepath}")
    return filepath

# Specify which question file to read
question_filename = "reorder_list.txt"

# Read the question from file
question_content = read_question_from_file(question_filename)

if question_content is None:
    print("Exiting program due to file read error.")
    exit()

# Prepare input data with the question from file
input_data = [
    {"role": "developer",
     "content": "You are a computer science college student. Solve the following DSA problem and provide your solution with explanation."},
    {"role": "user",
     "content": question_content}
]

try:
    # Start timing
    start_time = time.time()

    # Model choice
    model_choice = "gpt-4.1-nano"
    
    # Make the API call
    response = client.responses.create(
        model=model_choice,
        temperature=0.7,
        input=input_data,
        store=True
    )
    
    # Calculate processing time
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Get response content
    response_content = response.output_text
    
    # Print response
    print("=" * 60)
    print("MODEL RESPONSE:")
    print("=" * 60)
    print(response_content)
    print("=" * 60)
    print(f"\nProcessing time: {processing_time:.2f} seconds")
    
    # Save conversation to file
    save_conversation_log(model_choice, input_data, response_content, processing_time)
    
except Exception as e:
    print(f"Error occurred: {e}")
    # Log any errors
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    error_filename = f"error_log_{timestamp}.txt"
    error_filepath = f"OpenAiConversations/{error_filename}"
    
    # Create directory if it doesn't exist
    os.makedirs("OpenAiConversations", exist_ok=True)
    
    with open(error_filepath, 'w', encoding='utf-8') as error_file:
        error_file.write(f"{datetime.now().isoformat()}: Error - {str(e)}\n")
        error_file.write(f"Model: {model_choice}\n")
        error_file.write(f"Question file: {question_filename}\n")
        error_file.write(f"Input: {input_data}\n")
    
    print(f"Error details saved to: {error_filepath}")
