import fairpyx
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from fairpyx import Instance, AllocationBuilder
from fairpyx.algorithms import find_ACEEI_with_EFTB, tabu_search
from fairpyx.algorithms.ACEEI_algorithms.find_profitable_manipulation import find_profitable_manipulation
from fairpyx.adaptors import divide

app = Flask(__name__)


# Route for the root URL '/
@app.route('/')
def index():
    # Render and return the 'index.html' template from the 'templates' directory
    return render_template('index.html')


# Route to serve files from the 'templates' directory
@app.route('/templates/<filename>')
def serve_templates(filename):
    # Sends the file located in the 'templates' directory with the name 'filename'
    return send_from_directory('templates', filename)


# Route to handle GET requests for the '/form' URL
@app.route('/form', methods=['GET'])
def algorithm_form():
    # Retrieve the 'algorithm' parameter from the URL query string
    algorithm = request.args.get('algorithm')

    # Check the value of the 'algorithm' parameter and render the corresponding form template
    if algorithm == 'aceei':
        return render_template('aceeiForm.html')
    elif algorithm == 'manipulation':
        return render_template('manipulationForm.html')
    elif algorithm == 'tabusearch':
        return render_template('tabusearchForm.html')
    else:
        return "Invalid algorithm selection"


# Route to handle POST requests for the '/process' URL
@app.route('/process', methods=['POST'])
def process_form():
    # Get the 'algorithm' name from the form data submitted via POST request
    algorithm = request.form.get('algorithm')

    # Dictionary mapping algorithm short names to their full names
    algorithms_full_names = {
        "aceei": "ACEEI",
        "manipulation": "Find Profitable Manipulation",
        "tabusearch": "Tabu Search"
    }

    response = {"algorithm": algorithms_full_names.get(algorithm)}

    # Handle form processing based on the selected algorithm
    if algorithm == 'tabusearch':
        response.update(handle_tabusearch_form(request.form))
    elif algorithm == 'aceei':
        response.update(handle_aceei_form(request.form))
    elif algorithm == 'manipulation':
        response.update(handle_manipulation_form(request.form))
        # TODO: check how to display if there manipulation or not and final budget b* and  final prices p*
    else:
        response["Unknown algorithm"] = []

    print("response: ", response)  # Print the response to the console
    return render_template('results.html', response=response)


def handle_aceei_form(form_data):
    number_of_courses = int(form_data.get('numberOfCourses'))
    print("Number of courses is: ", number_of_courses)

    courses_capacities = {f'c{i}': int(form_data.get(f'c{i}Capacity')) for i in range(1, number_of_courses + 1)}
    print("courses_capacities  is: ", courses_capacities)

    number_of_students = int(form_data.get('numberOfStudents'))
    print("Number of students is: ", number_of_students)

    valuations = {}
    for i in range(1, number_of_students + 1):
        student_name = f's{i}'
        student_preferences = {}
        for course_name in courses_capacities.keys():
            student_preferences[course_name] = int(form_data.get(f'{student_name}{course_name}Rating'))
        valuations[student_name] = student_preferences
    print(f"valuations {valuations}")

    # 's' + i + 'CoursesToTake'
    agent_capacity = {f's{i}': int(form_data.get(f's{i}CoursesToTake')) for i in range(1, number_of_students + 1)}
    print(f"CoursesToTake {agent_capacity}")

    instance = Instance(valuations, agent_capacity, courses_capacities)
    print("Instance is: ", instance)
    epsilon = float(form_data.get('epsilon'))
    delta = float(form_data.get('delta'))
    eftb = str(form_data.get('ef-tb'))
    print("Epsilon is: ", epsilon)
    print("Delta is: ", delta)
    print("EF-TB is: ", eftb)

    # 's' + i + 'Budget'
    initial_budgets = {f's{i}': int(form_data.get(f's{i}Budget')) for i in range(1, number_of_students + 1)}
    print(f"initial budgets {initial_budgets}")

    answer = divide(find_ACEEI_with_EFTB, instance=instance, initial_budgets=initial_budgets, delta=delta,
                    epsilon=epsilon, t=eftb)
    print("The answer of the ACEEI is: ", answer)
    return answer


def handle_manipulation_form(form_data):
    number_of_courses = int(request.form.get('numberOfCourses'))
    print("Number of courses is: ", number_of_courses)
    courses_capacites = {}
    for i in range(1, number_of_courses + 1):
        course_capacity = int(request.form.get(f'c{i}Capacity'))
        courses_capacites[f'c{i}'] = course_capacity
    print("courses_capacites is: ", courses_capacites)

    number_of_students = int(request.form.get('numberOfStudents'))
    print("Number of students is: ", number_of_students)
    valuations = {}
    for i in range(1, number_of_students + 1):
        # student_name = request.form.get(f'studentName_{i}')
        student_name = f's{i}'
        student_preferences = {}
        for course_name in courses_capacites.keys():
            student_preferences[course_name] = int(request.form.get(f'{student_name}{course_name}Rating'))
        valuations[student_name] = student_preferences
    print(f"valuations {valuations}")

    # 's' + i + 'CoursesToTake'
    agent_capacity = {}
    for i in range(1, number_of_students + 1):
        # student_name = request.form.get(f'studentName_{i}')
        student_name = f's{i}'
        agent_capacity[student_name] = int(request.form.get(f'{student_name}CoursesToTake'))
    print(f"CoursesToTake {agent_capacity}")

    instance = Instance(valuations, agent_capacity, courses_capacites)
    print("instance is ", instance)

    epsilon = float(request.form.get('epsilon'))
    print("epsilon is: ", epsilon)

    delta = float(request.form.get('delta'))
    print("delta is: ", delta)

    beta = int(request.form.get('beta'))
    print("beta is: ", beta)

    eta = float(request.form.get('eta'))
    print("eta is: ", eta)

    eftb = str(request.form.get('ef-tb'))
    print("ef-tb is: ", eftb)

    student = str(request.form.get('studentSelection'))
    print("student is: ", student)

    criteria = str(request.form.get('criteria_for_profitable_manipulation'))
    print("criteria is: ", criteria)

    algorithm = find_ACEEI_with_EFTB

    # 's' + i + 'Budget'
    initial_budget = {}
    for i in range(1, number_of_students + 1):
        # student_name = request.form.get(f'studentName_{i}')
        student_name = f's{i}'
        initial_budget[student_name] = float(request.form.get(f'{student_name}Budget'))
    print(f"initial budgets {initial_budget}")

    answer = find_profitable_manipulation(mechanism=algorithm, student=student,
                                          true_student_utility=valuations[student],
                                          criteria=criteria, eta=eta, instance=instance,
                                          initial_budgets=initial_budget, beta=beta, delta=delta, epsilon=epsilon,
                                          t=eftb)
    print("answer is ", answer)
    return answer


def handle_tabusearch_form(form_data):
    print("Form data received:", request.form)
    number_of_courses = int(request.form.get('numberOfCourses'))
    print("Number of courses is: ", number_of_courses)
    courses_capacites = {}
    for i in range(1, number_of_courses + 1):
        course_capacity = int(request.form.get(f'c{i}Capacity'))
        courses_capacites[f'c{i}'] = course_capacity
    print("courses_capacites is: ", courses_capacites)

    number_of_students = int(request.form.get('numberOfStudents'))
    print("Number of students is: ", number_of_students)
    valuations = {}
    for i in range(1, number_of_students + 1):
        # student_name = request.form.get(f'studentName_{i}')
        student_name = f's{i}'
        student_preferences = {}
        for course_name in courses_capacites.keys():
            student_preferences[course_name] = int(request.form.get(f'{student_name}{course_name}Rating'))
        valuations[student_name] = student_preferences
    print(f"valuations {valuations}")

    # 's' + i + 'CoursesToTake'
    agent_capacity = {}
    for i in range(1, number_of_students + 1):
        # student_name = request.form.get(f'studentName_{i}')
        student_name = f's{i}'
        agent_capacity[student_name] = int(request.form.get(f'{student_name}CoursesToTake'))

    instance = Instance(valuations, agent_capacity, courses_capacites)
    print("instance is ", instance)
    beta = int(request.form.get('beta'))
    print("beta is: ", beta)

    delta_list = request.form.getlist('delta[]')
    delta = {float(delta) for delta in delta_list}
    print("delta is: ", delta)

    # 's' + i + 'Budget'
    initial_budgets = {}
    for i in range(1, number_of_students + 1):
        # student_name = request.form.get(f'studentName_{i}')
        student_name = f's{i}'
        initial_budgets[student_name] = float(request.form.get(f'{student_name}Budget'))
    print(f"initial budgets {initial_budgets}")

    answer = divide(tabu_search, instance=instance, initial_budgets=initial_budgets, beta=beta, delta=delta)
    print("answer is ", answer)
    return answer


if __name__ == '__main__':
    app.run(debug=True)
