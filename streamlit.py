import streamlit as st
import google.generativeai as genai
import os
from fpdf import FPDF
from io import BytesIO

# Set the API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyCBBU-Z5VTrwTU9bZCcZbilVPLciyOEhMw"

# Configuration
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 4096}

# Initialize Model
model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)

# Placeholder for storing session data
session_data = {}

st.title("Course Content Generator")

# Enter Topic
st.header("Step 1: Enter Topic")
topic = st.text_input("Enter the course topic:")
if st.button("Submit Topic"):
    session_data['topic'] = topic
    st.success("Topic received")

# Enter Days/Session
st.header("Step 2: Enter Days/Session")
days = st.number_input("Enter the number of days/sessions:", min_value=1)
if st.button("Submit Days/Session"):
    session_data['days'] = days
    st.success("Days/Sessions received")

# Generate Outline
if 'topic' in session_data and 'days' in session_data:
    st.header("Step 3: Generate Outline")
    if st.button("Generate Outline"):
        prompt = f"Create an outline for a course on {session_data['topic']} to be covered in {session_data['days']} days."
        response = model.generate_content([prompt])
        outline = response.text
        session_data['outline'] = outline
        st.text_area("Generated Outline:", outline)

# Generate Content
if 'outline' in session_data:
    st.header("Step 4: Generate Content")
    if st.button("Generate Content"):
        prompt = f"Generate detailed content for the following course outline: {session_data['outline']}"
        response = model.generate_content([prompt])
        content = response.text
        session_data['content'] = content
        st.text_area("Generated Content:", content)

# Generate Questions/Quizzes
if 'content' in session_data:
    st.header("Step 5: Generate Questions/Quizzes")
    if st.button("Generate Questions/Quizzes"):
        prompt = f"Generate questions and quizzes based on the following course content: {session_data['content']}"
        response = model.generate_content([prompt])
        questions = response.text
        session_data['questions'] = questions
        st.text_area("Generated Questions/Quizzes:", questions)

# Upload Material
st.header("Step 6: Upload Material")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    file_content = uploaded_file.read().decode('utf-8')
    if st.button("Upload Material"):
        prompt = f"Integrate the following additional material into the course content: {file_content}"
        response = model.generate_content([prompt])
        uploaded_content = response.text
        session_data['uploaded_content'] = uploaded_content
        st.text_area("Uploaded and Integrated Material:", uploaded_content)

# Export and Download as PDF
if 'content' in session_data and 'questions' in session_data:
    st.header("Step 7: Export and Download")
    
    uploaded_content = session_data.get('uploaded_content', '')
    complete_package = {
        "content": session_data['content'],
        "questions": session_data['questions'],
        "uploaded_content": uploaded_content
    }
    
    def create_pdf(content_dict):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 12)
        
        for section, text in content_dict.items():
            pdf.cell(200, 10, txt = section, ln = True, align = 'C')
            pdf.multi_cell(0, 10, txt = text)
            pdf.ln(10)
        
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        return pdf_output
    
    if st.button("Export and Download as PDF"):
        pdf_content = create_pdf(complete_package)
        st.download_button(label="Download PDF", data=pdf_content, file_name="course_content.pdf", mime="application/pdf")
    
    st.text_area("Complete Course Package:", str(complete_package))

if __name__ == '__main__':
    st.set_page_config(page_title="Course Content Generator", layout="centered")
    st.run()
