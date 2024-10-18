from flask import Flask, request, jsonify
import google.generativeai as genai
import os

# Set the API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyCBBU-Z5VTrwTU9bZCcZbilVPLciyOEhMw"

# Configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}

# Initialize Model
model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)

app = Flask(__name__)

# Placeholder for storing session data
session_data = {}

@app.route('/api/enter-topic', methods=['POST'])
def enter_topic():
    data = request.json
    session_data['topic'] = data.get('topic')
    return jsonify({"message": "Topic received"}), 200

@app.route('/api/enter-days-session', methods=['POST'])
def enter_days_session():
    data = request.json
    session_data['days'] = data.get('days')
    return jsonify({"message": "Days/Sessions received"}), 200

@app.route('/api/generate-outline', methods=['GET'])
def generate_outline():
    topic = session_data.get('topic')
    days = session_data.get('days')
    prompt = f"Create an outline for a course on {topic} to be covered in {days} days."
    response = model.generate_content([prompt])
    outline = response.text
    session_data['outline'] = outline
    return jsonify({"outline": outline}), 200

@app.route('/api/generate-content', methods=['GET'])
def generate_content():
    outline = session_data.get('outline')
    prompt = f"Generate detailed content for the following course outline: {outline}"
    response = model.generate_content([prompt])
    content = response.text
    session_data['content'] = content
    return jsonify({"content": content}), 200

@app.route('/api/generate-questions', methods=['GET'])
def generate_questions():
    content = session_data.get('content')
    prompt = f"Generate questions and quizzes based on the following course content: {content}"
    response = model.generate_content([prompt])
    questions = response.text
    session_data['questions'] = questions
    return jsonify({"questions": questions}), 200

@app.route('/api/upload-material', methods=['POST'])
def upload_material():
    file = request.files['file']
    file_content = file.read().decode('utf-8')
    prompt = f"Integrate the following additional material into the course content: {file_content}"
    response = model.generate_content([prompt])
    uploaded_content = response.text
    session_data['uploaded_content'] = uploaded_content
    return jsonify({"message": "Material uploaded and integrated"}), 200

@app.route('/api/export', methods=['GET'])
def export():
    content = session_data.get('content')
    questions = session_data.get('questions')
    uploaded_content = session_data.get('uploaded_content', '')
    complete_package = {
        "content": content,
        "questions": questions,
        "uploaded_content": uploaded_content
    }
    return jsonify(complete_package), 200

if __name__ == '__main__':
    app.run(debug=True)
