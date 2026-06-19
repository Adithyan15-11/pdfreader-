from flask import Flask, request, jsonify, render_template
import PyPDF2

app = Flask(__name__)


@app.route('/')
def index():
    # Serves the frontend HTML
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_pdf():
    # Check if a file is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    # Check if a file was selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Process the PDF
    if file and file.filename.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            extracted_text = ""

            # Iterate through all pages and extract text
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

            return jsonify({'text': extracted_text})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file format. Please upload a .pdf file.'}), 400


if __name__ == '__main__':
    app.run(debug=True)