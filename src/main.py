import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file")
    exit(1)
client = OpenAI(api_key=api_key)

def get_chat_response(prompt):
    """Send a prompt to OpenAI's API and return the response."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use gpt-4o or another model if preferred
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,  # Adjust as needed
            temperature=0.7,  # Adjust for creativity
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main function to run the console chat application."""
    print("Welcome to the ChatGPT Console! Type 'exit' to quit.")
    while True:
        prompt = input("\nYou: ")
        if prompt.lower() == "exit":
            print("Goodbye!")
            break
        if not prompt.strip():
            print("Please enter a prompt.")
            continue
        response = get_chat_response(prompt)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()