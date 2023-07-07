
document.addEventListener("DOMContentLoaded", function() {
    // Add event listener to "Add Section" button
    const addSectionButton = document.getElementById("add-section-button");
    addSectionButton.addEventListener("click", addSection);

    // Add event listener to "Save Draft" button
    const saveDraftButton = document.getElementById("save-draft-button");
    saveDraftButton.addEventListener("click", saveDraft);

    // Add event listener to form submit
    const form = document.getElementById("form-creation");
    form.addEventListener("submit", submitForm);
});

function submitForm(event) {
    event.preventDefault();  // Prevent the default form submission

    let formData = collectFormData();  // Use the same function to collect the form data

    // Send AJAX request to Django server
    fetch("/form_create/", {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Django requires this header for POST requests
        }
    }).then(response => response.json()).then(data => {
        // Check response from server
        if (data.status == "success") {
            console.log("Form created successfully");
        } else {
            console.log("Error creating form");
        }
    });
}

function addSection() {
    const sectionsDiv = document.getElementById("sections-div");

    const newSectionDiv = document.createElement("div");
    newSectionDiv.classList.add("section-div");

    // Add fields for section title
    const sectionTitleInput = document.createElement("input");
    sectionTitleInput.setAttribute("type", "text");
    sectionTitleInput.setAttribute("placeholder", "Section title");
    sectionTitleInput.classList.add("section-title");
    newSectionDiv.appendChild(sectionTitleInput);

    // Add "Add Subsection" button
    const addSubsectionButton = document.createElement("button");
    addSubsectionButton.textContent = "Add Subsection";
    addSubsectionButton.addEventListener("click", function(e) {
        e.preventDefault();
        addSubsection(newSectionDiv);
    });
    newSectionDiv.appendChild(addSubsectionButton);

    sectionsDiv.appendChild(newSectionDiv);
}

function addSubsection(sectionDiv) {
    const newSubsectionDiv = document.createElement("div");
    newSubsectionDiv.classList.add("subsection-div");

    // Add fields for subsection title
    const subsectionTitleInput = document.createElement("input");
    subsectionTitleInput.setAttribute("type", "text");
    subsectionTitleInput.setAttribute("placeholder", "Subsection title");
    subsectionTitleInput.classList.add("subsection-title");
    newSubsectionDiv.appendChild(subsectionTitleInput);

    // Add "Add Question" button
    const addQuestionButton = document.createElement("button");
    addQuestionButton.textContent = "Add Question";
    addQuestionButton.addEventListener("click", function(e) {
        e.preventDefault();
        addQuestion(newSubsectionDiv);
    });
    newSubsectionDiv.appendChild(addQuestionButton);

    sectionDiv.appendChild(newSubsectionDiv);
}

function addQuestion(subsectionDiv) {
    const questionInput = document.createElement("input");
    questionInput.setAttribute("type", "text");
    questionInput.setAttribute("placeholder", "Question");
    questionInput.classList.add("question-input");
    subsectionDiv.appendChild(questionInput);
}

function collectFormData() {
    const sectionsDiv = document.getElementById("sections-div");
    const sectionDivs = sectionsDiv.getElementsByClassName("section-div");

    let formData = {
        form_title: document.getElementById("form-title").value,
        sections: []
    };

    for (let sectionDiv of sectionDivs) {
        let sectionData = {
            title: sectionDiv.getElementsByClassName("section-title")[0].value,
            subsections: []
        };
        
        const subsectionDivs = sectionDiv.getElementsByClassName("subsection-div");
        for (let subsectionDiv of subsectionDivs) {
            let subsectionData = {
                title: subsectionDiv.getElementsByClassName("subsection-title")[0].value,
                questions: []
            };

            const questionInputs = subsectionDiv.getElementsByClassName("question-input");
            for (let questionInput of questionInputs) {
                subsectionData.questions.push({
                    text: questionInput.value
                });
            }
            sectionData.subsections.push(subsectionData);
        }
        formData.sections.push(sectionData);
    }
    
    return formData;
}
function saveDraft() {
    const sectionsDiv = document.getElementById("sections-div");
    const sectionDivs = sectionsDiv.getElementsByClassName("section-div");

    let formData = {
        form_title: document.getElementById("form-title").value,
        sections: []
    };

    for (let sectionDiv of sectionDivs) {
        let sectionData = {
            title: sectionDiv.getElementsByClassName("section-title")[0].value,
            subsections: []
        };

        const subsectionDivs = sectionDiv.getElementsByClassName("subsection-div");
        for (let subsectionDiv of subsectionDivs) {
            let subsectionData = {
                title: subsectionDiv.getElementsByClassName("subsection-title")[0].value,
                questions: []
            };

            const questionInputs = subsectionDiv.getElementsByClassName("question-input");
            for (let questionInput of questionInputs) {
                subsectionData.questions.push({
                    text: questionInput.value
                });
            }
            sectionData.subsections.push(subsectionData);
        }
        formData.sections.push(sectionData);
    }

    // Send AJAX request to Django server
    fetch("/save_draft/", {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => response.json()).then(data => {
        // Check response from server
        if (data.status == "success" || data.status == "error") {
            console.log(data.error || "Draft saved successfully");
            window.location.href = data.url;
        } 
    }).catch((error) => {
        console.error('Error:', error);
    });
    
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            //Check if this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
