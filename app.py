from flask import Flask, render_template, request, redirect, url_for, send_file, session
import pandas as pd
import os
from utils.pseudonymization import apply_pseudoanonymization

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    technique = request.form.get('technique')

    if not file or not technique:
        return "Please upload a file and select technique."

    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    df = pd.read_csv(filepath)
    session['filepath'] = filepath
    session['technique'] = technique

    return render_template('select_columns.html', columns=list(df.columns))

@app.route('/process', methods=['POST'])
def process():
    selected_columns = request.form.getlist('columns')

    filepath = session.get('filepath')
    technique = session.get('technique')

    df = pd.read_csv(filepath)
    pseudo_df = df.copy()

    if selected_columns:
        for col in selected_columns:
            pseudo_df[col] = pseudo_df[col].apply(lambda x: apply_pseudoanonymization(x, technique))

    output_path = os.path.join(app.config['PROCESSED_FOLDER'], 'pseudo_' + os.path.basename(filepath))
    pseudo_df.to_csv(output_path, index=False)

    return render_template('result.html', 
                           original=df.to_html(classes='table table-bordered'), 
                           pseudo=pseudo_df.to_html(classes='table table-bordered'),
                           download_link=output_path)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
