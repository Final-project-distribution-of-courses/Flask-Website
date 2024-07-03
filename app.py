from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    # קבלת הקלט מהטופס
    name = request.form['name']
    course1 = request.form['course1']
    course2 = request.form['course2']
    course3 = request.form['course3']

    # כאן תוכל להפעיל את האלגוריתם על הקלט וליצור את הפלט
    # לשם הדוגמה, ניצור פלט פשוט
    output = f"{name}, הקורסים שהוקצו לך הם: {course1}, {course2}, {course3}"

    return render_template('result.html', name=name, output=output)


if __name__ == '__main__':
    app.run(debug=True)
