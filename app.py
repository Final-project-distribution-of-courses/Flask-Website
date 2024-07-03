import os
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    # Get the input from the form
    name = request.form.get('name')
    course1 = request.form.get('course1')
    course2 = request.form.get('course2')
    course3 = request.form.get('course3')

    # Example output for demonstration
    output = f"{name}, the courses allocated to you are: {course1}, {course2}, {course3}"

    return render_template('result.html', name=name, output=output)


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True)
