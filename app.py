import fairpyx
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from fairpyx import Instance, AllocationBuilder
from fairpyx.algorithms import find_ACEEI_with_EFTB, tabu_search
from fairpyx.algorithms.ACEEI_algorithms.find_profitable_manipulation import find_profitable_manipulation
from fairpyx.adaptors import divide
from utils import *
from LogCaptureHandler import *
import logging

# Create and configure the logger
log_capture_handler = LogCaptureHandler()
log_capture_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
log_capture_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(log_capture_handler)
logger.setLevel(logging.INFO)

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
        print("response: ", response)  # Print the response to the console
        return render_template('results_tabu_search.html', response=response)
    elif algorithm == 'aceei':
        response.update(handle_aceei_form(request.form))
        print("response: ", response)  # Print the response to the console
        return render_template('results_aceei.html', response=response)
    elif algorithm == 'manipulation':
        response.update(handle_manipulation_form(request.form))
        print("response: ", response)  # Print the response to the console
        return render_template('results_manipulation.html', response=response)
    else:
        response["Unknown algorithm"] = []
        return response


def handle_aceei_form(form_data):
    number_of_courses = get_number_of_courses(form_data)
    print("Number of courses is: ", number_of_courses)

    courses_capacities = get_courses_capacities(form_data, number_of_courses)
    print("courses_capacities  is: ", courses_capacities)

    number_of_students = get_number_of_students(form_data)
    print("Number of students is: ", number_of_students)

    valuations = get_student_preferences(form_data, number_of_students, courses_capacities)
    print(f"valuations {valuations}")

    # 's' + i + 'CoursesToTake'
    agent_capacity = get_agent_capacity(form_data, number_of_students)
    print(f"CoursesToTake {agent_capacity}")

    # 's' + i + 'Budget'
    initial_budgets = get_initial_budgets(form_data, number_of_students)
    print(f"initial budgets {initial_budgets}")

    instance = Instance(valuations, agent_capacity, item_capacities=courses_capacities)
    print("Instance is: ", instance)
    epsilon, delta, eftb = get_aceei_other_parameters(form_data)
    print("Epsilon is: ", epsilon)
    print("Delta is: ", delta)
    print("EF-TB is: ", eftb)
    # logger.info("Debug message")
    # logging.getLogger('your_module_name').addHandler(log_capture_handler)

    answer = divide(find_ACEEI_with_EFTB, instance=instance, initial_budgets=initial_budgets, delta=delta,
                    epsilon=epsilon, t=eftb)

    logs, filtered_logs = log_capture_handler.extract_ACEEI_data()
    print("The answer of the ACEEI is: ", answer)

    return {"answer": answer, "filtered_logs": filtered_logs, "logs": logs}


def handle_manipulation_form(form_data):
    number_of_courses = get_number_of_courses(form_data)
    print("Number of courses is: ", number_of_courses)

    courses_capacities = get_courses_capacities(form_data, number_of_courses)
    print("courses_capacities  is: ", courses_capacities)

    number_of_students = get_number_of_students(form_data)
    print("Number of students is: ", number_of_students)

    valuations = get_student_preferences(form_data, number_of_students, courses_capacities)
    print(f"Valuations are: {valuations}")

    # 's' + i + 'CoursesToTake'
    agent_capacity = get_agent_capacity(form_data, number_of_students)
    print(f"CoursesToTake: {agent_capacity}")

    initial_budgets = get_initial_budgets(form_data, number_of_students)
    print(f"Initial Budgets: {initial_budgets}")

    epsilon, delta, beta, eta, eftb, student, criteria = get_manipulation_other_parameters(form_data)
    print("beta is: ", beta)
    print("delta is: ", delta)
    print("beta is: ", beta)
    print("eta is: ", eta)
    print("eftb is: ", eftb)
    print("student is: ", student)
    print("criteria is: ", criteria)

    algorithm = find_ACEEI_with_EFTB
    instance = Instance(valuations, agent_capacity, item_capacities=courses_capacities)

    answer = find_profitable_manipulation(mechanism=algorithm, student=student,
                                          true_student_utility=valuations[student],
                                          criteria=criteria, eta=eta, instance=instance,
                                          initial_budgets=initial_budgets, beta=beta, delta=delta, epsilon=epsilon,
                                          t=eftb)
    log_messages, status = log_capture_handler.extract_manipulation_status()

    print("Answer is:", answer)
    print("Log messages:\n", log_messages)

    return {"answer": answer, "logs": log_messages, "status": status}


def handle_tabusearch_form(form_data):
    try:
        number_of_courses = get_number_of_courses(form_data)
        print("Number of courses is: ", number_of_courses)

        courses_capacities = get_courses_capacities(form_data, number_of_courses)
        print("courses_capacities  is: ", courses_capacities)

        number_of_students = get_number_of_students(form_data)
        print("Number of students is: ", number_of_students)

        valuations = get_student_preferences(form_data, number_of_students, courses_capacities)
        print(f"Valuations are: {valuations}")

        # 's' + i + 'CoursesToTake'
        agent_capacity = get_agent_capacity(form_data, number_of_students)
        print(f"CoursesToTake: {agent_capacity}")

        # 's' + i + 'Budget'
        initial_budgets = get_initial_budgets(form_data, number_of_students)
        print(f"Initial Budgets: {initial_budgets}")

        beta, delta = get_tabusaerch_other_parameters(form_data)
        print("beta is: ", beta)
        print("delta is: ", delta)

        instance = Instance(valuations, agent_capacity, item_capacities=courses_capacities)
        print("Instance is: ", instance)

        answer = divide(tabu_search, instance=instance, initial_budgets=initial_budgets, beta=beta, delta=delta)
        if answer is None:
            raise ValueError("Tabu Search returned None instead of a valid answer.")
        print("answer is ", answer)
        logs, filtered_logs = log_capture_handler.extract_tabu_search_data()
        return {"answer": answer, "logs": logs, "filtered_logs": filtered_logs}
    except Exception as e:
        logger.error(f"Error during Tabu Search execution: {str(e)}")
        return {"error": str(e)}


if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(debug=True, port=8080)
