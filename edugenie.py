from boltiotai import openai
import os
import sys
from dotenv import load_dotenv
from flask import Flask, render_template_string, request, jsonify

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')
if not openai.api_key:
    sys.stderr.write("API key hasn't been set up.\n")
    sys.exit(1)

def generate_info(subject):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Give information about {subject} in a neat format: 1) Meaning, 2) Uses, 3) Important info, 4) Related resources, 5) A quote."}
        ]
    )
    return response['choices'][0]['message']['content']

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>EduGenie - Info Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        h1 { text-align: center; color: brown; margin-top: 20px; }
        #output { white-space: pre-wrap; background-color: #f8f9fa; padding: 15px; border-radius: 8px; }
    </style>
    <script>
        async function generateInfo() {
            const output = document.querySelector("#output");
            output.textContent = "Generating...";
            const response = await fetch("/generate", {
                method: "POST",
                body: new FormData(document.querySelector("#info_form"))
            });
            const text = await response.text();
            output.textContent = text;
        }

        function copyToClipboard() {
            const output = document.querySelector("#output");
            const textarea = document.createElement("textarea");
            textarea.value = output.textContent;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand("copy");
            document.body.removeChild(textarea);
            alert("Copied to clipboard");
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>EDUGENIE ✨</h1>
        <form id="info_form" onsubmit="event.preventDefault(); generateInfo();" class="mb-3">
            <div class="mb-3">
                <label for="subject" class="form-label">Enter word/topic:</label>
                <input type="text" name="subject" class="form-control" id="subject" required>
                <div class="form-text">We will provide detailed information.</div>
            </div>
            <button type="submit" class="btn btn-primary">Get Info</button>
        </form>

        <div class="card mt-4">
            <div class="card-header d-flex justify-content-between align-items-center">
                Output:
                <button class="btn btn-secondary btn-sm" onclick="copyToClipboard()">Copy</button>
            </div>
            <div class="card-body">
                <pre id="output"></pre>
            </div>
        </div>
    </div>
</body>
</html>
""")

@app.route('/generate', methods=['POST'])
def generate():
    subject = request.form['subject']
    return generate_info(subject)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
