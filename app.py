from flask import Flask, render_template, request, send_file
import fitz  # PyMuPDF
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')


# Resume analyze
@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']
    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()

    skills_list = ["python", "java", "c++", "html", "css", "javascript"]
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    score = len(found_skills) * 20

    return render_template('result.html', score=score, skills=found_skills)


# Resume Builder Page
@app.route('/builder')
def builder():
    return render_template('builder.html')


# Generate PDF Resume
@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    skills = request.form['skills']
    education = request.form['education']
    experience = request.form['experience']

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica", 14)

    c.drawString(100, 750, f"Name: {name}")
    c.drawString(100, 720, f"Skills: {skills}")
    c.drawString(100, 690, f"Education: {education}")
    c.drawString(100, 660, f"Experience: {experience}")

    c.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="resume.pdf", mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)