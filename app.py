from flask import Flask, render_template, request, jsonify
import pdfplumber

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

def get_debit(row):
    debit = row[4] if len(row) > 4 else ""
    if debit and debit != "Debit":
        return float(debit.replace(",", ""))
    return 0

def get_credit(row):
    credit = row[5] if len(row) > 5 else ""
    if credit and credit != "Credit":
        return float(credit.replace(",", ""))
    return 0

@app.route('/upload', methods=['POST'])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    total_credit, total_debit = 0, 0

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    total_debit += get_debit(row)
                    total_credit += get_credit(row)

    return jsonify({"total_credit": total_credit, "total_debit": total_debit})

if __name__ == '__main__':
    app.run(debug=True)
