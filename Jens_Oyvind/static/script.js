// Sjekker om brukernavn er tilgjengelig, oppdaterer tekst og class på element usernameFeedback
async function lookUpUsername(username) {
    const feedbackElement = document.getElementById("usernameFeedback");

    if (username.length === 0) {
        feedbackElement.innerHTML = "";
        feedbackElement.classList.remove("error", "success");
        return;
    }
    try {
        const response = await fetch(`/api/availability?username=${encodeURIComponent(username)}`); // encodeURIComponent sørger for at special characters blir håndtert riktig
        const data = await response.json();

        feedbackElement.innerHTML = data.message;

        // endre class avhengig av situasjon
        if (data.available) {
            feedbackElement.classList.add("success");
            feedbackElement.classList.remove("error");
        } else {
            feedbackElement.classList.add("error");
            feedbackElement.classList.remove("success");
        }
    } catch (error) {
        console.error('Error:', error);
        feedbackElement.innerText = "An error occurred while checking username.";
        feedbackElement.classList.add("error");
        feedbackElement.classList.remove("success");
    }
}


// Bytter tekst på knapp ved registrering av admin
function adminCheckboxChanged(checkbox) {
    var submitButton = document.getElementById("register_user_button");
    if (checkbox.checked) {
        submitButton.value = "Register new admin"
    } else {
        submitButton.value = "Register new user"
    }
}

// Sammenligner passord med retyped passord
function comparePasswords(password, passwordRetype){
    const repasswordFeedback = document.getElementById('repasswordFeedback');
    if (password === passwordRetype) {
        repasswordFeedback.textContent = 'Passwords match';
        repasswordFeedback.className = 'success';
    } else {
        repasswordFeedback.textContent = 'Passwords do not match';
        repasswordFeedback.className = 'error';
    }
}
// Gir tilbakemelding om passordet oppfyller krav
function passwordRequirements(password){
    const passwordFeedback = document.getElementById('passwordFeedback');
    if (password.length < 6){
        passwordFeedback.textContent = 'Password too short';
        passwordFeedback.className = 'error';
    } else {
        passwordFeedback.textContent = 'Password accepted';
        passwordFeedback.className = 'success';
    }
}

// Sletter egen bruker. Admin kan slette andre brukere
async function confirmDelete(button) {
    const username = button.getAttribute("data-username");
    const isAdmin = button.getAttribute("data-is-admin") === "true";

    if (confirm(`Are you sure you want to delete ${username}?`)) {
        try {
            const response = await fetch(`/users/${encodeURIComponent(username)}/delete`, {
                method: 'DELETE'
            });
            const result = await response.json();
            alert(result.message);

            // Redirect based on admin status
            window.location.href = isAdmin ? "/admin/users" : "/";
        } catch (error) {
            alert(`An error occurred: ${error.message}`);
        }
    }
}


// Darkmode på/av
async function darkModeToggle() {
    const toggleButton = document.getElementById('toggle_button');
    let darkmode = JSON.parse(toggleButton.getAttribute('data-preferences'));
    if (darkmode == 1){
        darkmode = 0
    } else {
        darkmode = 1
    }
    const response = await fetch('/api/user/preferences', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ darkmode })
    });
    if (response.ok) {
        console.log('Preferences updated successfully');
        window.location.href = "/user/account"; 
    } else {
        console.error('Failed to update preferences');
    }
}

// Funksjon til å legge til flere spørsmål
function addQuestion() {
    const queryList = document.getElementById('query_list');
    let questionCount = queryList.getElementsByTagName('li').length;    
    let listLine = document.createElement('li');
    let newLabel = document.createElement('label');
    newLabel.setAttribute('for', 'lineQuestion'+ (questionCount+1));
    newLabel.className = 'input_description';
    newLabel.innerText = `${(questionCount + 1)}`;
    let newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.className = 'input_ramme';
    newInput.id = 'lineQuestion'+ (questionCount+1);
    newInput.name = 'lineQuestion'+ (questionCount+1);
    listLine.appendChild(newLabel);
    listLine.append(' ');
    listLine.appendChild(newInput);
    queryList.appendChild(listLine);
}

// Oppretter table med alle undersøkelser
async function listQuestionnaires() {
    const questionnairesDiv = document.getElementById('questionnaires');
    const isLoggedIn = questionnairesDiv.getAttribute('data-logged-in') === 'true';
    const response1 = await fetch('/api/questionnaires');
    const questionnaires = await response1.json();
    let completedIds = [];
    if (isLoggedIn) { // Hvis logget inn, sjekk hvilke undersøkelser brukeren har svart på
        const response2 = await fetch('/api/questionnaire/completed');
        completedIds = await response2.json();
    }
    const questionnairesTable = document.createElement('table');
    
    // Table header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const headerCell1 = document.createElement('th');
    headerCell1.innerText = 'Available questionnaires';
    headerRow.appendChild(headerCell1);
    if (isLoggedIn) { // Knapp for hide/show
        const headerCell2 = document.createElement('th');
        const toggleButton = document.createElement('button');
        toggleButton.id = 'toggleButton';
        toggleButton.innerText = 'Hide/show completed';
        toggleButton.addEventListener('click', toggleCompleted);
        headerCell2.appendChild(toggleButton);
        headerRow.appendChild(headerCell2);
    } 
    thead.appendChild(headerRow);
    questionnairesTable.appendChild(thead);

    // Table innhold
    for (let questionnaire of questionnaires) {
        const tr = document.createElement("tr");
        const nameTd = document.createElement("td");
        nameTd.innerText = questionnaire.id_questionnaire + " " + questionnaire.name_questionnaire;
        tr.appendChild(nameTd);
        if (isLoggedIn) { // Hvis logget inn, opprett knapp for besvarelse av undersøkelsene
            const buttonTd = document.createElement("td");
            const button = document.createElement("button");
            button.classList.add("answer-button")

            button.addEventListener("click", () => {
                window.location.href = `/questionnaire/${questionnaire.id_questionnaire}`;
            });

            if (completedIds.includes(questionnaire.id_questionnaire)) {
                button.innerText = "Change answers";
                tr.classList.add('completed-row')
            } else {
                button.innerText = "Answer";
            }
            buttonTd.appendChild(button);
            tr.appendChild(buttonTd);
        } else {
        nameTd.classList.add("single-column-questionnaires")
        }
        questionnairesTable.appendChild(tr);
    }
    questionnairesDiv.appendChild(questionnairesTable);
}

// Skjuler/viser fullførte undersøkelser
function toggleCompleted() {
    const completedRows = document.querySelectorAll('.completed-row');
    completedRows.forEach(row => {
        row.style.display = row.style.display === 'none' ? '' : 'none';
    });
}


document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('questionnaires')) {
        listQuestionnaires();
    }
});

// hamburger
document.addEventListener("DOMContentLoaded", function () {
    const hamburger = document.querySelector(".hamburger");
    const dropdown = document.querySelector(".dropdown-menu");
    hamburger.addEventListener("click", () => {
        dropdown.classList.toggle("active");
    });
});

// filtrerer bort utførte
function filterUsers() {
  const input = document.getElementById("searchInput").value.toLowerCase();
  const rows = document.querySelectorAll("#userTable tbody tr"); // velger alle rows i tbody med id #userTable
  rows.forEach(row => {
    const name = row.cells[0].textContent.toLowerCase();
    const id = row.cells[1].textContent.toLowerCase();
    const match = name.includes(input) || id.includes(input); // Hvis input matcher id eller navn
    row.style.display = match ? "" : "none"; // Hvis match, sett display til "", hvis ikke, skjul med display "none"
  });
}

