from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form', methods=['GET', 'POST'])
def algorithm_form():
    algorithm = request.args.get('algorithm')

    if algorithm == 'aceei':
        return render_template('aceei_form.html')
    elif algorithm == 'manipulation':
        return render_template('manipulation_form.html')
    elif algorithm == 'tabusearch':
        return render_template('tabusearch_form.html')
    else:
        # Handle invalid algorithm selection
        return "Invalid algorithm selection"


if __name__ == '__main__':
    app.run(debug=True)
