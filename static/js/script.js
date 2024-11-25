document.addEventListener("DOMContentLoaded", function() {
    // Get all the FAQ question buttons
    const faqQuestions = document.querySelectorAll(".faq-question");

    faqQuestions.forEach(function(question) {
        question.addEventListener("click", function() {
            // Toggle the display of the associated answer
            const answer = question.nextElementSibling;

            // Check if the answer is already visible
            if (answer.style.display === "block") {
                // Hide the answer
                answer.style.display = "none";
            } else {
                // Show the answer
                answer.style.display = "block";
            }
        });
    });
});



