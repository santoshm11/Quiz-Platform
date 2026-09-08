document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("quizOverCard").style.display = "none";
    document.getElementById("resultSection").style.display = "block";
    document.getElementById("resultSection").scrollIntoView({ behavior: "smooth" });

    // Hide quiz over card after 3 seconds and scroll down
    setTimeout(function () {
        // Fetch and display results
        loadQuizResults();
    }, 1000);

    /*/ View graph button behavior
    let graphContainer = document.getElementById("graphContainer");
    let viewGraphBtn = document.getElementById("viewGraphBtn");

    viewGraphBtn.addEventListener("click", function () {
        if (graphContainer.classList.contains("show")) {
            graphContainer.style.opacity = "0";
            setTimeout(() => {
                graphContainer.classList.remove("show");
                graphContainer.style.display = "none"; 
            }, 300);
            viewGraphBtn.textContent = "📈 View Graph";
        } else {
            graphContainer.style.display = "block"; 
            setTimeout(() => {
                graphContainer.classList.add("show");
                graphContainer.style.opacity = "1";
            }, 10);
            viewGraphBtn.textContent = "❌ Hide Graph";
        }
    });*/
});

function loadQuizResults() {
    fetch("/get-quiz-results/")
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const tableBody = document.querySelector("tbody");
                tableBody.innerHTML = ""; // Clear previous content

                data.results.forEach((participant, index) => {
                    let row = `<tr data-uucms="${participant.uucms_id}">
                        <td>${index + 1}</td>
                        <td>${participant.name} (${participant.uucms_id})</td>
                        <td>${participant.score}</td>
                    </tr>`;
                    tableBody.innerHTML += row;
                });
            }
        })
        .catch(error => console.error("Error fetching results:", error));
}

document.querySelector("tbody").addEventListener("click", function(e) {
    let targetRow = e.target.closest("tr");
    if (targetRow) {
        let uucmsID = targetRow.getAttribute("data-uucms");
        window.location.href = `/result-details/${uucmsID}/`;
    }
});