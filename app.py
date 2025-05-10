from flask import Flask, render_template, request, session
import pandas as pd
import os
from utils.pseudonymization import apply_pseudoanonymization

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    original_table = None
    pseudo_table = None
    columns = None
    selected_technique = session.get('technique')
    selected_columns = []

    if request.method == 'POST':
        if 'file' in request.files:
            # First form: Upload file + select technique
            file = request.files['file']
            technique = request.form.get('technique')
            if not file or not technique:
                return "Missing file or technique."

            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            session['filepath'] = filepath
            session['technique'] = technique

            df = pd.read_csv(filepath)
            columns = list(df.columns)

        elif 'columns' in request.form:
            # Second form: Process selected columns
            filepath = session.get('filepath')
            technique = session.get('technique')
            selected_columns = request.form.getlist('columns')

            if not filepath or not technique:
                return "Session expired. Please re-upload the file."

            df = pd.read_csv(filepath)
            pseudo_df = df.copy()

            for col in selected_columns:
                pseudo_df[col] = pseudo_df[col].apply(lambda x: apply_pseudoanonymization(x, technique))

            columns = list(df.columns)
            original_table = df.to_html(classes='table table-bordered', index=False)
            pseudo_table = pseudo_df.to_html(classes='table table-bordered', index=False)

    return render_template(
        'index.html',
        columns=columns,
        original_table=original_table,
        pseudo_table=pseudo_table,
        selected_technique=selected_technique,
        selected_columns=selected_columns
    )

if __name__ == '__main__':
    app.run(debug=True)
