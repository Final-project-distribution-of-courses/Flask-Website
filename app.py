from flask import Flask, render_template, request, redirect, url_for
from fairpyx import Instance

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def algorithm_form():
    algorithm = request.args.get('algorithm')

    if request.method == 'POST':
        form_data = request.form
        if algorithm == 'aceei':
            return handle_aceei_form(form_data)
        elif algorithm == 'manipulation':
            return handle_manipulation_form(form_data)
        elif algorithm == 'tabusearch':
            return handle_tabusearch_form(form_data)
        else:
            return "Invalid algorithm selection"

    if algorithm == 'aceei':
        return render_template('aceei_form.html')
    elif algorithm == 'manipulation':
        return render_template('manipulation_form.html')
    elif algorithm == 'tabusearch':
        return render_template('tabusearch_form.html')
    else:
        return "Invalid algorithm selection"

def handle_aceei_form(form_data):
    pass
    return "ACEEI form processed successfully"

def handle_manipulation_form(form_data):
    pass
    return "Manipulation form processed successfully"

def handle_tabusearch_form(form_data):
    number_of_courses = int(request.form.get('numberOfCourses'))
    print("Number of courses is: ", number_of_courses)
    courses_capacites = {}
    for i in range(1, number_of_courses + 1):
        course_capacity = int(request.form.get(f'c{i}Capacity'))
        courses_capacites[f'c{i}'] = course_capacity
    print("courses_capacites is: ", courses_capacites)

    number_of_students = int(request.form.get('numberOfStudents'))
    print("Number of students is: ", number_of_students)
    # valuations = {}
    # for i in range(1, number_of_students + 1):
    #     # student_name = request.form.get(f'studentName_{i}')
    #     student_name = f's{i}'
    #     student_preferences = {}
    #     for course_name in courses_capacites.keys():
    #         student_preferences[course_name] = int(request.form.get(f'{student_name}[{course_name}]'))
    #     valuations[student_name] = student_preferences

    # todo: handle agent capacity
    # instance = Instance(valuations,2, courses_capacites)

    beta = float(request.form.get('beta'))
    delta = float(request.form.get('delta'))
    print("beta is: ", beta)
    print("delta is: ", delta)
    # Format HTML response with instance, beta, and delta values

    return "Form processed successfully"
@app.route('/process', methods=['POST'])
def process_form():
    response = handle_tabusearch_form(request.form)  # Call handle_tabusearch_form to get the response
    print(response)  # Print the response to the console
    # Handle the form processing logic here
    return "Form processed successfully"

if __name__ == '__main__':
    app.run(debug=True)
