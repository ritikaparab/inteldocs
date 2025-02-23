import google.generativeai as genai
import os

# Function to initialize the GenAI model with the API key
def initialize_genai(api_key):
    """
    Initializes the Google GenAI API client with the provided API key.
    """
    # Set the environment variable for the API key (ensure you set it as per Google Generative AI's documentation)
    os.environ["GOOGLE_API_KEY"] = api_key

# Function to generate a response based on input context
def generate_response(prompt, conversation_history):
    """
    Generates a response from the Google GenAI model while keeping track of the conversation history.
    Args:
    - prompt (str): The user query.
    - conversation_history (list): A list containing previous conversation turns (questions and answers).
    """
    # Add the new prompt to the conversation history
    conversation_history.append({"role": "user", "content": prompt})
    
    # Combine the entire conversation history to provide context
    context = "\n".join([f"{entry['role']}: {entry['content']}" for entry in conversation_history])

    # Generate the response using Google's Generative AI Chat method
    response = genai.Chat(
        model="chat-bison-001",  # Replace with your desired model name
        messages=[{"role": "user", "content": context}],
        temperature=0.7,  # Adjust the temperature as needed (higher values = more creativity)
        max_output_tokens=150
    )
    
    # Get the model's response
    reply = response['candidates'][0]['message']['content']
    
    # Add the assistant's reply to the conversation history for context
    conversation_history.append({"role": "assistant", "content": reply})
    
    return reply, conversation_history

# Example use case
def main():
    # Initialize the system with your Google GenAI API key
    api_key = "AIzaSyCpnmX6ZuZkZuB26Xejk8x3SGfmdvxzvfY"  # Your Google API key
    initialize_genai(api_key)

    # Store the conversation history
    conversation_history = []
    
    # Example multi-layered questions
    queries = [
        "Compare the risk factors in these three financial reports over the last two years.",
        "What were the main differences in profit margins between the first and second quarter?",
        "Did the risk of inflation increase in the second quarter compared to the first quarter?"
    ]
    
    for query in queries:
        answer, conversation_history = generate_response(query, conversation_history)
        print(f"Q: {query}\nA: {answer}\n")

if __name__ == "__main__":
    main()
