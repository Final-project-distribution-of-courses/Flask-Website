function openPopup(popupId) {
    var popup = document.getElementById(popupId);
    var xhr = new XMLHttpRequest();
    console.log(`${popupId}.html`)
    xhr.open('GET', `/templates/${popupId}.html`, true); // Adjust the path as needed
    xhr.onload = function() {
        if (xhr.status === 200) {
            popup.querySelector('.popup-content').innerHTML += xhr.responseText;
            popup.style.display = "block";
        } else {
            console.error('Failed to load popup content:', xhr.status, xhr.statusText);
        }
    };
    xhr.send();
}

function closePopup(popupId) {
    var popup = document.getElementById(popupId);
    popup.style.display = "none";
    popup.querySelector('.popup-content').innerHTML = '<span class="close" onclick="closePopup(\'' + popupId + '\')">&times;</span>'; // Reset content
}

// Close the popup if the user clicks outside of it
window.onclick = function(event) {
    if (event.target.classList.contains('popup')) {
        closePopup(event.target.id);
    }
}
function showAlgorithmFields() {
    var selectedAlgorithm = document.getElementById("algorithm").value;
    var aceeiFields = document.getElementById("aceei-fields");
    var manipulationFields = document.getElementById("manipulation-fields");
    var tabusearchFields = document.getElementById("tabusearch-fields");

    aceeiFields.style.display = "none";
    manipulationFields.style.display = "none";
    tabusearchFields.style.display = "none";

    if (selectedAlgorithm === "ACEEI") {
        aceeiFields.style.display = "block";
    } else if (selectedAlgorithm === "Find a profitable manipulation for a student") {
        manipulationFields.style.display = "block";
    } else if (selectedAlgorithm === "Tabu Search") {
        tabusearchFields.style.display = "block";
    }
}

// Get the modal
var modal = document.getElementById("errorModal");

// Get the close button
var closeBtn = document.getElementsByClassName("close-btn")[0];

// When the user clicks on the submit button
document.getElementById('algorithmForm').addEventListener('submit', function(event) {
    var selectedAlgorithm = document.getElementById('algorithmSelect').value;

    if (!selectedAlgorithm) {
        event.preventDefault();
        modal.style.display = "block"; // Show the modal
    }
});

// When the user clicks on the close button, close the modal
closeBtn.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}