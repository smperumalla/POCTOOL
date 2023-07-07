document.addEventListener("DOMContentLoaded", function() {
    const sectionsDiv = document.getElementById("sections");
    const saveDraftButton = document.getElementById("save-draft");

    saveDraftButton.addEventListener("click", function(e) {
        e.preventDefault();
        saveDraft();
    });

    //function that fetches the current form data
    fetchFormData().then(formData => {
        formData.sections.forEach(sectionData => {
            const sectionDiv = addSection(sectionsDiv, sectionData.title);
            sectionData.subsections.forEach(subsectionData => {
                const subsectionDiv = addSubsection(sectionDiv, subsectionData.title);
                subsectionData.questions.forEach(questionData => {
                    addQuestion(subsectionDiv, questionData.text);
                });
            });
        });
    });
});

function addSection(sectionsDiv, title = "") {
    const newSectionDiv = document.createElement("div");
    newSectionDiv.classList.add("section-div");

    const sectionTitleInput = document.createElement("input");
    sectionTitleInput.setAttribute("type", "text");
    sectionTitleInput.setAttribute("placeholder", "Section title");
    sectionTitleInput.classList.add("section-title");
    sectionTitleInput.value = title;
    newSectionDiv.appendChild(sectionTitleInput);

    const addSubsectionButton = document.createElement("button");
    addSubsectionButton.textContent = "Add Subsection";
    addSubsectionButton.addEventListener("click", function(e) {
        e.preventDefault();
        addSubsection(newSectionDiv);
    });
    newSectionDiv.appendChild(addSubsectionButton);

    sectionsDiv.appendChild(newSectionDiv);
    return newSectionDiv;
}

function addSubsection(sectionDiv, title = "") {
    const newSubsectionDiv = document.createElement("div");
    newSubsectionDiv.classList.add("subsection-div");

    const subsectionTitleInput = document.createElement("input");
    subsectionTitleInput.setAttribute("type", "text");
    subsectionTitleInput.setAttribute("placeholder", "Subsection title");
    subsectionTitleInput.classList.add("subsection-title");
    subsectionTitleInput.value = title;
    newSubsectionDiv.appendChild(subsectionTitleInput);

    const addQuestionButton = document.createElement("button");
    addQuestionButton.textContent = "Add Question";
    addQuestionButton.addEventListener("click", function(e) {
        e.preventDefault();
        addQuestion(newSubsectionDiv);
    });
    newSubsectionDiv.appendChild(addQuestionButton);

    sectionDiv.appendChild(newSubsectionDiv);
    return newSubsectionDiv;
}

function addQuestion(subsectionDiv, text = "") {
    const newQuestionInput = document.createElement("input");
    newQuestionInput.setAttribute("type", "text");
    newQuestionInput.setAttribute("placeholder", "Question text");
    newQuestionInput.classList.add("question-text");
    newQuestionInput.value = text;
    subsectionDiv.appendChild(newQuestionInput);
}

function saveDraft() {
    const sections = Array.from(document.getElementsByClassName("section-div")).map(sectionDiv => {
        const title = sectionDiv.querySelector(".section-title").value;
        const subsections = Array.from(sectionDiv.getElementsByClassName("subsection-div")).map(subsectionDiv => {
            const title = subsectionDiv.querySelector(".subsection-title").value;
            const questions = Array.from(subsectionDiv.getElementsByClassName("question-text")).map(questionInput => {
                return { text: questionInput.value };
            });
            return { title, questions };
        });
        return { title, subsections };
    });

    // Assuming you have a function to save the form data
    saveFormData({ sections });
}
