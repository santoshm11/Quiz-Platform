document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.querySelector("#resultsTable tbody");
    const quizOverCard = document.getElementById("quizOverCard");
    const resultSection = document.getElementById("resultSection");
    const resultsData = JSON.parse(document.getElementById('results-data').textContent);

    // Hide loading card and show result section immediately
    quizOverCard.style.display = "none";
    resultSection.style.display = "block";

    // Function to display results
    function displayResults(resultsData) {
        tableBody.innerHTML = "";

        resultsData.forEach(answer => {
            const row = document.createElement("tr");
            row.classList.add(answer.status); // green, red, yellow
            console.log(answer.selected_answer)
            row.innerHTML = `
                <td>${answer.sl_no}</td>
                <td>${answer.question_text}</td>
                <td>${answer.correct_answer}</td>
                <td>${answer.selected_answer || "<span style='color: gray;'>UnAnswered</span>"}</td>
            `;

            tableBody.appendChild(row);
        });
    }

    // Call display immediately
    displayResults(resultsData);
});
