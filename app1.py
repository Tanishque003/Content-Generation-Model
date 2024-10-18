import google.generativeai as genai
import os
from fpdf import FPDF
import requests

# Set the API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyCBBU-Z5VTrwTU9bZCcZbilVPLciyOEhMw"

# Configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}

# Initialize Model
model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)

# Function to preprocess user input
def preprocess_input(input_text):
    return [input_text]

# Function to respond to user input
def respond_to_input(input_text):
    response = model.generate_content(preprocess_input(input_text))
    return response.text

# Function to generate PDF
def generate_pdf(topic, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Topic: {topic}", ln=True, align="C")
    pdf.cell(200, 10, txt=content, ln=True)
    pdf_output = "course_content.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Main function to interact with the user
def main():
    print("Hello! I'm a chatbot powered by the Google Generative AI API.")
    print("You can ask me anything or type 'exit' to quit.")
    topic = None
    content = ""
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            if topic:
                content = generate_pdf(topic, content)
                download_url = f"http://localhost:8888/files/{content}"
                response = requests.get(download_url)
                with open(content, "wb") as f:
                    f.write(response.content)
                print(f"PDF saved as '{content}'")
            break
        elif not topic:
            topic = user_input
            print(f"Great! We'll generate content for the topic: {topic}")
        else:
            response = respond_to_input(user_input)
            content += response + "\n"
            print("Bot:", response)

if __name__ == "__main__":
    main()
