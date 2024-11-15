from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flash messages
UPLOAD_FOLDER = 'uploads'
PASSWORD = "delete123"  # Replace with your desired password
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'files' not in request.files:
        return 'No file part', 400

    files = request.files.getlist('files')
    for file in files:
        if file.filename:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    password = request.form.get("password")
    if password != PASSWORD:
        flash("Incorrect password. File not deleted.")
        return redirect(url_for('index'))
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f"File '{filename}' deleted successfully.")
    else:
        flash("File not found.")
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
