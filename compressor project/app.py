import os
import zipfile
from io import BytesIO
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return "No files selected", 400

    # Create a buffer to hold the zip file in memory
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            zf.writestr(file.filename, file.read())
    
    memory_file.seek(0)
    
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='compressed_files.zip'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)