from flask import Flask, render_template, request, redirect, url_for
from fairpyx import Instance, AllocationBuilder
from fairpyx.algorithms import find_ACEEI_with_EFTB, tabu_search, find_profitable_manipulation
from fairpyx.adaptors import divide

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
    delta = float(request.form.get('delta'))
    eftb = str(request.form.get('ef-tb'))
    print("epsilon is: ", epsilon)
    print("delta is: ", delta)
    print("ef-tb is: ", eftb)

    # 's' + i + 'Budget'
    initial_budgets = {}
    for i in range(1, number_of_students + 1):
        # student_name = request.form.get(f'studentName_{i}')
        student_name = f's{i}'
        initial_budgets[student_name] = float(request.form.get(f'{student_name}Budget'))
    print(f"initial budgets {initial_budgets}")

    answer = divide(find_ACEEI_with_EFTB, instance=instance, initial_budgets=initial_budgets, delta=delta,
                    epsilon=epsilon, t=eftb)
    print("answer is ", answer)
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
        agent_capacity[student_name] = float(request.form.get(f'{student_name}CoursesToTake'))
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

    criteria_for_profitable_manipulation = str(request.form.get('criteria_for_profitable_manipulation'))
    print("criteria is: ", criteria_for_profitable_manipulation)

    # 's' + i + 'Budget'
    initial_budget = {}
    for i in range(1, number_of_students + 1):
        # student_name = request.form.get(f'studentName_{i}')
        student_name = f's{i}'
        initial_budget[student_name] = float(request.form.get(f'{student_name}Budget'))
    print(f"initial budgets {initial_budget}")

    # todo: handle student
    answer = divide(find_profitable_manipulation, mechanism=find_ACEEI_with_EFTB, student="s1",
                    true_student_utility=valuations["s1"], criteria=criteria_for_profitable_manipulation, eta=eta,
                    instance=instance, initial_budgets=initial_budget, beta=beta, delta=delta, epsilon=epsilon, t=eftb)
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

@app.route('/process', methods=['POST'])
def process_form():
    algorithm = request.form.get('algorithm')  # Get the algorithm name from the form data

    if algorithm == 'tabusearch':
        response = handle_tabusearch_form(request.form)
    elif algorithm == 'aceei':
        response = handle_aceei_form(request.form)
    elif algorithm == 'manipulation':
        response = handle_manipulation_form(request.form)
        # todo: check how to display if there manipulation or not and final budget b* and  final prices p*
    else:
        response = {"Unknown algorithm": []}

    print(response)  # Print the response to the console
    return render_template('result.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
