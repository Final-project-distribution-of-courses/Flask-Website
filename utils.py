
def get_number_of_courses(form_data):
    return int(form_data.get('numberOfCourses'))


def get_courses_capacities(form_data, number_of_courses):
    return {f'c{i}': int(form_data.get(f'c{i}Capacity')) for i in range(1, number_of_courses + 1)}


def get_number_of_students(form_data):
    return int(form_data.get('numberOfStudents'))


def get_student_preferences(form_data, number_of_students, courses_capacities):
    valuations = {}
    for i in range(1, number_of_students + 1):
        student_name = f's{i}'
        student_preferences = {}
        for course_name in courses_capacities.keys():
            student_preferences[course_name] = int(form_data.get(f'{student_name}{course_name}Rating'))
        valuations[student_name] = student_preferences
    return valuations


def get_agent_capacity(form_data, number_of_students):
    return {f's{i}': int(form_data.get(f's{i}CoursesToTake')) for i in range(1, number_of_students + 1)}

def get_initial_budgets(form_data, number_of_students):
    return {f's{i}': int(form_data.get(f's{i}Budget')) for i in range(1, number_of_students + 1)}


def get_aceei_other_parameters(form_data):
    epsilon = float(form_data.get('epsilon'))
    delta = float(form_data.get('delta'))
    eftb = str(form_data.get('ef-tb'))
    return epsilon, delta, eftb


def get_manipulation_other_parameters(form_data):
    epsilon = float(form_data.get('epsilon'))

    delta = float(form_data.get('delta'))

    beta = int(form_data.get('beta'))

    eta = float(form_data.get('eta'))

    eftb = str(form_data.get('ef-tb'))

    student = str(form_data.get('studentSelection'))

    criteria = str(form_data.get('criteria_for_profitable_manipulation'))

    return epsilon, delta, beta, eta, eftb, student, criteria


def get_tabusaerch_other_parameters(form_data):
    beta = int(form_data.get('beta'))
    delta_list = form_data.getlist('delta[]')
    delta = {float(delta) for delta in delta_list}

    return beta, delta
