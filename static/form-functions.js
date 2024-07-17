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
        capacityInput.required = true;
        capacityInput.addEventListener('input', checkAllCapacitiesFilled);
        courseField.appendChild(capacityInput);

        courseFieldsDiv.appendChild(courseField);
    }

    // Enable the number of students input field
    document.getElementById('numberOfStudents').disabled = true;
}

// Function to add student input fields dynamically
function addStudentFields() {
    var numberOfStudents = parseInt(document.getElementById('numberOfStudents').value);
    var studentFieldsDiv = document.getElementById('studentFields');
    studentFieldsDiv.innerHTML = ''; // Clear previous fields
    var numberOfCourses = parseInt(document.getElementById('numberOfCourses').value);

    for (var i = 1; i <= numberOfStudents; i++) {
        var studentField = document.createElement('div');
        studentField.className = 'studentField';

        var studentLabel = document.createElement('div');
        studentLabel.className = 'studentLabel';
        studentLabel.textContent = 'Student ' + i;
        studentField.appendChild(studentLabel);

        var budgetGroup = document.createElement('div');
        budgetGroup.className = 'fieldGroup';
        var budgetLabel = document.createElement('label');
        budgetLabel.className = 'inputLabel';
        budgetLabel.textContent = 'Budget: ';
        budgetGroup.appendChild(budgetLabel);
        var budgetInput = document.createElement('input');
        budgetInput.type = 'number';
        budgetInput.name = 's' + i + 'Budget';
        budgetInput.min = 1;
        budgetInput.required = true;
        budgetGroup.appendChild(budgetInput);
        studentField.appendChild(budgetGroup);

        var coursesGroup = document.createElement('div');
        coursesGroup.className = 'fieldGroup';
        var coursesLabel = document.createElement('label');
        budgetLabel.className = 'inputLabel';
        coursesLabel.textContent = 'Courses to Take: ';
        coursesGroup.appendChild(coursesLabel);
        var coursesInput = document.createElement('input');
        coursesInput.type = 'number';
        coursesInput.min = 1;
        coursesInput.name = 's' + i + 'CoursesToTake';
        coursesInput.required = true;
        coursesGroup.appendChild(coursesInput);
        studentField.appendChild(coursesGroup);

        var ratingsLabel = document.createElement('label');
        ratingsLabel.className = 'inputLabel';
        ratingsLabel.textContent = 'Ratings for Courses: ';
        studentField.appendChild(ratingsLabel);

        var ratingsGroup = document.createElement('div');
        ratingsGroup.className = 'ratingsGroup';
        for (var j = 1; j <= numberOfCourses; j++) {
            var ratingRow = document.createElement('div');
            ratingRow.className = 'ratingRow';
            var ratingLabel = document.createElement('label');
            ratingsLabel.className = 'inputLabel';
            ratingLabel.textContent = 'c' + j + ': ';
            ratingRow.appendChild(ratingLabel);
            var ratingInput = document.createElement('input');
            ratingInput.type = 'number';
            ratingInput.name = 's' + i + 'c' + j + 'Rating';
            ratingInput.min = 1;
            ratingInput.step = 1;
            ratingInput.required = true;
            ratingRow.appendChild(ratingInput);
            ratingsGroup.appendChild(ratingRow);
        }
        studentField.appendChild(ratingsGroup);

        studentFieldsDiv.appendChild(studentField);

    }
}

// Function to check if all capacity fields are filled
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

function addDeltaInput() {
    // Create a new div element to contain the delta input field and remove button
    const newDiv = document.createElement('div');
    newDiv.classList.add('delta-input-container');

    // Create the label element
    const newLabel = document.createElement('label');
    newLabel.innerText = 'Delta (δ):';
    newDiv.appendChild(newLabel);

    // Create the input element
    const newInput = document.createElement('input');
    newInput.type = 'number';
    newInput.name = 'delta[]';
    newInput.step = '0.01';
    newInput.min = '0';
    newInput.required = true;
    newDiv.appendChild(newInput);

    // Create the remove button
    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.innerText = 'Remove';
    removeButton.onclick = function() {
        newDiv.remove();
    };
    newDiv.appendChild(removeButton);

    // Append the new div to the delta fields container
    document.getElementById('deltaFieldsContainer').appendChild(newDiv);
}

// Enable the number of students input field when number of courses is selected
document.getElementById('numberOfCourses').addEventListener('input', function () {
    var numberOfCourses = parseInt(document.getElementById('numberOfCourses').value);
    if (numberOfCourses > 0) {
        document.getElementById('numberOfStudents').disabled = true;
    } else {
        document.getElementById('numberOfStudents').disabled = true;
    }
})