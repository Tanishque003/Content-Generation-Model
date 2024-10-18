import google.generativeai as genai 
import os 

# Set the API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyCBBU-Z5VTrwTU9bZCcZbilVPLciyOEhMw"

# 1. Configuration 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 5000}

# 2. Initialise Model
model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)

# Function to preprocess user input
def preprocess_input(input_text):
    return [input_text]

# Function to respond to user input
def respond_to_input(input_text):
    response = model.generate_content(preprocess_input(input_text))
    return response.text

# Main function to interact with the user
def main():
    print("Hello! I'm a chatbot powered by the Google Generative AI API.")
    print("You can ask me anything or type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        else:
            response = respond_to_input(user_input)
            print("Bot:", response)

if __name__ == "__main__":
    main()
