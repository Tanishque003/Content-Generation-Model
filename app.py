import os
from flask import Flask, request, render_template, send_file
import google.generativeai as genai
from fpdf import FPDF
from io import BytesIO

# Set the API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyCBBU-Z5VTrwTU9bZCcZbilVPLciyOEhMw"

# Configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}

# Initialize Model
model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)

# Initialize Flask app
app = Flask(__name__)

# Chat history to store user inputs and bot responses
chat_history = []

# Function to preprocess user input
def preprocess_input(input_text):
    return [input_text]

# Function to respond to user input
def respond_to_input(input_text):
    response = model.generate(preprocess_input(input_text))
    return response.text

# Function to generate PDF
def generate_pdf(topic, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Topic: {topic}", ln=True, align="C")
    pdf.multi_cell(0, 10, txt=content)
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        if user_input.lower() == 'exit':
            return render_template("index.html", chat_history=chat_history, download_link=True)
        if 'topic' not in chat_history:
            chat_history.append({"role": "user", "text": user_input})
            chat_history.append({"role": "bot", "text": f"Great! We'll generate content for the topic: {user_input}"})
        else:
            chat_history.append({"role": "user", "text": user_input})
            bot_response = respond_to_input(user_input)
            chat_history.append({"role": "bot", "text": bot_response})
        return render_template("index.html", chat_history=chat_history, download_link=False)
    return render_template("index.html", chat_history=chat_history, download_link=False)

@app.route("/download")
def download_pdf():
    if chat_history:
        topic = chat_history[0]["text"]
        content = "\n".join([entry["text"] for entry in chat_history if entry["role"] == "bot"])
        pdf_output = generate_pdf(topic, content)
        return send_file(pdf_output, as_attachment=True, download_name="course_content.pdf", mimetype="application/pdf")
    return "No chat history available to generate PDF."

if __name__ == "__main__":
    app.run(debug=True)
