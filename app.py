# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    input_data = data['inputData']

    # Pass the input_data to your Python file or perform desired operations
    # Example: Save to a file
    with open('output.txt', 'w') as file:
        file.write(input_data)

    return 'Data submitted successfully'

if __name__ == '__main__':
    app.run(debug=True)
