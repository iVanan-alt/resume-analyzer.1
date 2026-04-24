from flask import Flask, render_template, request
import fitz

app = Flask(__name__)

skills_db = ["python","java","sql","html","css","machine learning","data structures","communication","problem solving"]

def extract_text(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text.lower()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']
    text = extract_text(file)

    found = []
    missing = []

    for skill in skills_db:
        if skill in text:
            found.append(skill)
        else:
            missing.append(skill)

    score = int((len(found)/len(skills_db))*100)

    return render_template("result.html",
                           score=score,
                           skills=found,
                           missing=missing)

@app.route('/improve')
def improve():
    return render_template("improve.html")

@app.route('/builder')
def builder():
    return render_template("builder.html")

if __name__ == "__main__":
    app.run(debug=True)