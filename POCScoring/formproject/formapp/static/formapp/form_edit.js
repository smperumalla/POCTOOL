document.addEventListener('click', function(e) {
    // Handle add section
    if(e.target && e.target.matches('.add-section')) {
        const newSectionId = Date.now();
        const newSectionHTML = `
            <div class="section">
                <label for="new_section_${newSectionId}">Section Title:</label>
                <input id="new_section_${newSectionId}" type="text" name="new_section_${newSectionId}">
                <div class="subsections"></div>
                <button type="button" class="add-subsection">Add Subsection</button>
            </div>`;
        document.querySelector('#sections').insertAdjacentHTML('beforeend', newSectionHTML);
    }
    
    // Handle add subsection
    else if(e.target && e.target.matches('.add-subsection')) {
        const newSubsectionId = Date.now();
        const newSubsectionHTML = `
            <div class="subsection">
                <label for="new_subsection_${newSubsectionId}">Subsection Title:</label>
                <input id="new_subsection_${newSubsectionId}" type="text" name="new_subsection_${newSubsectionId}">
                <div class="questions"></div>
                <button type="button" class="add-question">Add Question</button>
            </div>`;
        e.target.parentElement.querySelector('.subsections').insertAdjacentHTML('beforeend', newSubsectionHTML);
    }

    // Handle add question
    else if(e.target && e.target.matches('.add-question')) {
        const newQuestionId = Date.now();
        const newQuestionHTML = `
            <div class="question">
                <label for="new_question_${newQuestionId}">Question:</label>
                <input id="new_question_${newQuestionId}" type="text" name="new_question_${newQuestionId}">
            </div>`;
        e.target.parentElement.querySelector('.questions').insertAdjacentHTML('beforeend', newQuestionHTML);
    }
});
