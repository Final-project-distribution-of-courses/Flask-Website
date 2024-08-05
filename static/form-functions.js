// Function to add course input fields dynamically
function addCourseFields() {
    var numberOfCourses = parseInt(document.getElementById('numberOfCourses').value);
    var courseFieldsDiv = document.getElementById('courseFields');
    courseFieldsDiv.innerHTML = ''; // Clear previous fields

    for (var i = 1; i <= numberOfCourses; i++) {
        var courseField = document.createElement('div');
        courseField.className = 'courseField';

        var courseLabel = document.createElement('label');
        courseLabel.textContent = 'Course ' + i + ' Capacity: ';
        courseField.appendChild(courseLabel);

        var capacityInput = document.createElement('input');
        capacityInput.type = 'number';
        capacityInput.min = 1;
        capacityInput.name = 'c' + i + 'Capacity';
        capacityInput.className = 'capacityInput';
        capacityInput.required = true;
        capacityInput.addEventListener('input', checkAllCapacitiesFilled);
        courseField.appendChild(capacityInput);

        courseFieldsDiv.appendChild(courseField);
    }

    // Enable the number of students input field
    document.getElementById('numberOfStudents').disabled = true;
}

// Function to handle adding student fields
function addStudentFields() {
    var numberOfStudents = parseInt(document.getElementById('numberOfStudents').value);
    console.log("numberOfStudents: ", numberOfStudents);
    var studentFieldsDiv = document.getElementById('studentFields');
    studentFieldsDiv.innerHTML = ''; // Clear previous fields
    var numberOfCourses = parseInt(document.getElementById('numberOfCourses').value);

    for (var i = 1; i <= numberOfStudents; i++) {
        var studentField = createStudentField(i, numberOfCourses);
        studentFieldsDiv.appendChild(studentField);
    }

    updateStudentSelectionDropdown();
}

// Function to create a student field
function createStudentField(studentIndex, numberOfCourses) {
    var studentField = document.createElement('div');
    studentField.className = 'studentField';

    studentField.appendChild(createStudentLabel(studentIndex));
    studentField.appendChild(createBudgetGroup(studentIndex));
    studentField.appendChild(createCoursesGroup(studentIndex));
    studentField.appendChild(createRatingsGroup(studentIndex, numberOfCourses));

    return studentField;
}

// Function to create the student label
function createStudentLabel(studentIndex) {
    var studentLabel = document.createElement('div');
    studentLabel.className = 'studentLabel';
    studentLabel.textContent = 'Student ' + studentIndex;
    return studentLabel;
}

// Function to create the budget input group
function createBudgetGroup(studentIndex) {
    var budgetGroup = document.createElement('div');
    budgetGroup.className = 'fieldGroup';

    var budgetLabel = document.createElement('label');
    budgetLabel.className = 'inputLabel';
    budgetLabel.textContent = 'Budget: ';
    budgetGroup.appendChild(budgetLabel);

    var budgetInput = document.createElement('input');
    budgetInput.type = 'number';
    budgetInput.name = 's' + studentIndex + 'Budget';
    budgetInput.min = 1;
    budgetInput.required = true;
    budgetGroup.appendChild(budgetInput);

    return budgetGroup;
}

// Function to create the courses input group
function createCoursesGroup(studentIndex) {
    var coursesGroup = document.createElement('div');
    coursesGroup.className = 'fieldGroup';

    var coursesLabel = document.createElement('label');
    coursesLabel.className = 'inputLabel';
    coursesLabel.textContent = 'Courses to Take: ';
    coursesGroup.appendChild(coursesLabel);

    var coursesInput = document.createElement('input');
    coursesInput.type = 'number';
    coursesInput.min = 1;
    coursesInput.name = 's' + studentIndex + 'CoursesToTake';
    coursesInput.required = true;
    coursesGroup.appendChild(coursesInput);

    return coursesGroup;
}

// Function to create the ratings input group
function createRatingsGroup(studentIndex, numberOfCourses) {
    var ratingsGroup = document.createElement('div');
    ratingsGroup.className = 'ratingsGroup';

    var ratingsLabel = document.createElement('label');
    ratingsLabel.className = 'inputLabel';
    ratingsLabel.textContent = 'Ratings for Courses: ';
    ratingsGroup.appendChild(ratingsLabel);

    for (var j = 1; j <= numberOfCourses; j++) {
        if ((j - 1) % 3 === 0) {
            var ratingRow = document.createElement('div');
            ratingRow.className = 'ratingRow';
            ratingsGroup.appendChild(ratingRow);
        }

        var ratingLabel = document.createElement('label');
        ratingLabel.className = 'inputLabel';
        ratingLabel.textContent = 'c' + j + ': ';
        ratingRow.appendChild(ratingLabel);

        var ratingInput = document.createElement('input');
        ratingInput.type = 'number';
        ratingInput.name = 's' + studentIndex + 'c' + j + 'Rating';
        ratingInput.min = 1;
        ratingInput.step = 1;
        ratingInput.required = true;
        ratingRow.appendChild(ratingInput);
    }

    return ratingsGroup;
}

// Function to update the student selection dropdown
function updateStudentSelectionDropdown() {
    var form = document.getElementById('manipulationForm');
    if (form) {
        var algorithm = form.querySelector('input[name="algorithm"]').value;
        console.log("algorithm is:", algorithm);
        if (algorithm === 'manipulation') {
            var studentSelection = document.getElementById('studentSelection');
            studentSelection.innerHTML = '<option value="" disabled selected>Select a student</option>';

            var numberOfStudents = parseInt(document.getElementById('numberOfStudents').value);
            for (var i = 1; i <= numberOfStudents; i++) {
                var studentOption = document.createElement('option');
                studentOption.value = 's' + i;
                studentOption.textContent = 'Student ' + i;
                studentSelection.appendChild(studentOption);
            }

            // Enable the student selection dropdown
            studentSelection.disabled = false;
        }
    }
}

// Function to check if all capacity fields are filled in order to enable the student fields
function checkAllCapacitiesFilled() {
    var numberOfCourses = parseInt(document.getElementById('numberOfCourses').value);
    var allFilled = true;

    for (var i = 1; i <= numberOfCourses; i++) {
        var capacityInput = document.querySelector('input[name="c' + i + 'Capacity"]');
        if (!capacityInput || capacityInput.value === '') {
            allFilled = false;
            break;
        }
    }

    document.getElementById('numberOfStudents').disabled = !allFilled;
}

// Function to add more delta to tabu search
function addDeltaInput() {
    var deltaFieldsDiv = document.getElementById('deltaFields');
    var newDeltaContainer = document.createElement('div');
    newDeltaContainer.className = 'fieldsContainer';

    var newLabel = document.createElement('label');
    newLabel.setAttribute('for', 'delta');
    newLabel.textContent = 'Delta (δ):';

    var newInput = document.createElement('input');
    newInput.setAttribute('type', 'number');
    newInput.setAttribute('name', 'delta[]');
    newInput.setAttribute('step', '0.001');
    newInput.setAttribute('min', '0.001');
    newInput.setAttribute('required', 'required');

    newDeltaContainer.appendChild(newLabel);
    newDeltaContainer.appendChild(newInput);

    var removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.textContent = 'Remove';
    removeButton.className = "removeDeltaBtn"
    removeButton.onclick = function() {
        deltaFieldsDiv.removeChild(newDeltaContainer);
    };

    newDeltaContainer.appendChild(removeButton);

    deltaFieldsDiv.appendChild(newDeltaContainer);
}


function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}


function getRandomFloat(min, max) {
    return (Math.random() * (max - min)) + min;
}

// Function to add random data
function addRandomDataForStudentsAndCourses() {
    var numberOfCourses = getRandomInt(1, 11); // Random number of courses between 1 and 10
    document.getElementById('numberOfCourses').value = numberOfCourses;
    addCourseFields(); // Add course fields dynamically based on the random number

    for (var i = 1; i <= numberOfCourses; i++) {
        document.querySelector(`input[name='c${i}Capacity']`).value = getRandomInt(1, 11); // Random capacity between 1 and 10
    }

    var numberOfStudents = getRandomInt(1, 16); // Random number of students between 1 and 15
    // console.log("number of studetns: ", numberOfStudents)
    document.getElementById('numberOfStudents').value = numberOfStudents;
    addStudentFields(); // Add student fields dynamically based on the random number

    for (var i = 1; i <= numberOfStudents; i++) {
        document.querySelector(`input[name='s${i}Budget']`).value = getRandomInt(1, 101); // Random budget between 1 and 100
        document.querySelector(`input[name='s${i}CoursesToTake']`).value = getRandomInt(1, numberOfCourses); // Random number of courses to take

        for (var j = 1; j <= numberOfCourses; j++) {
            document.querySelector(`input[name='s${i}c${j}Rating']`).value = getRandomInt(1, 101); // Random rating between 1 and 100
        }
    }


}

function addRandomDataInTabuSearch() {

    addRandomDataForStudentsAndCourses()

    document.getElementById('beta').value = getRandomInt(1, 10); // Random beta value between 1 and 10

    document.getElementById('delta').value = getRandomFloat(0.01, 3).toFixed(2);  // Random delta value between 0.01 and 3

    // Handle delta fields
    var deltaFieldsContainer = document.getElementById('deltaFields');
    var numberOfDeltas = getRandomInt(1, 5); // Assuming you want to generate a random number of delta fields between 1 and 4

    // Clear previous delta fields and add new ones
    deltaFieldsContainer.innerHTML = ''; // Clear previous delta fields

    for (var i = 0; i < numberOfDeltas; i++) {
        addDeltaInput(); // Function to add new delta input fields
    }

    // After adding delta fields, set random values
    var deltaInputs = deltaFieldsContainer.querySelectorAll('input[name="delta[]"]');

    deltaInputs.forEach((input) => {
        input.value = getRandomFloat(0.01, 3).toFixed(2); // Random float value for each delta field between 0.01 and 100 with 2 decimal places
    });


    document.getElementById('numberOfStudents').disabled = false;
    console.log(document.getElementById('numberOfStudents').value)

}

function getRandomEFTBStatus() {
    const options = [
        'EFTBStatus.NO_EF_TB',
        'EFTBStatus.EF_TB',
        'EFTBStatus.CONTESTED_EF_TB'
    ];
    const randomIndex = Math.floor(Math.random() * options.length);
    return options[randomIndex];
}

function addRandomDataInAceei() {

    // TODO: PROBLEM - there is a random inputs that return an error.

    addRandomDataForStudentsAndCourses()

    document.getElementById('epsilon').value = getRandomFloat(0.01, 3).toFixed(2);  // Random epsilon value between 0.01 and 3

    document.getElementById('delta').value = getRandomFloat(0.01, 3).toFixed(2);  // Random delta value between 0.01 and 3

    document.getElementById('ef-tb').value = getRandomEFTBStatus();

    document.getElementById('numberOfStudents').disabled = false;
    console.log(document.getElementById('numberOfStudents').value)

}

function selectRandomStudent() {
    // Get the dropdown element
    var select = document.getElementById('studentSelection');

    // Get the number of options in the dropdown
    var options = select.options;
    var numOptions = options.length;

    // Generate a random index between 1 and numOptions - 1 (excluding the first option)
    var randomIndex = Math.floor(Math.random() * (numOptions - 1)) + 1;

    // Set the value of the dropdown to the randomly selected option
    select.selectedIndex = randomIndex;
}

function addRandomDataInManipulation() {

    // TODO: PROBLEM - there is a random inputs that return an error.

    addRandomDataForStudentsAndCourses()

    document.getElementById('epsilon').value = getRandomFloat(0.01, 3).toFixed(2);  // Random epsilon value between 0.01 and 3

    document.getElementById('delta').value = getRandomFloat(0.01, 3).toFixed(2);  // Random delta value between 0.01 and 3

    document.getElementById('eta').value = getRandomInt(1, 5);  // Random eta value between 1 and 5

    document.getElementById('beta').value = getRandomInt(1, 10); // Random beta value between 1 and 10

    document.getElementById('ef-tb').value = getRandomEFTBStatus();

    function getRandomCriteria() {
        const options = [
        'criteria_for_profitable_manipulation.randomness',
        'criteria_for_profitable_manipulation.population'
        ];
        const randomIndex = Math.floor(Math.random() * options.length);
        return options[randomIndex];
    }

    document.getElementById('criteria_for_profitable_manipulation').value = getRandomCriteria();

    selectRandomStudent();

    document.getElementById('numberOfStudents').disabled = false;
    console.log(document.getElementById('numberOfStudents').value)

}


function goToHomePage() {

    window.location.href = "/";
}

function goBackToAlgorithmPage() {
    window.history.back();
}


document.getElementById('epsilonLearnMore').onclick = function() {
    document.getElementById('popup-epsilon').style.display = 'block';
}

document.querySelector('.popup-parameter-close').onclick = function() {
    document.getElementById('popup-epsilon').style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == document.getElementById('popup-epsilon')) {
        document.getElementById('popup-epsilon').style.display = 'none';
    }
}



