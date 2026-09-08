const teamList = document.getElementById("teamList");
const teamCard = document.getElementById("teamCard");

// Function to populate the team table dynamically
function populateTeamTable(teams) {
    teamList.innerHTML = "";

    teams.forEach((team, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${team.serialNo}</td>
            <td class="hover-team">${team.uucms_id}</td>
            <td>${team.name}</td>
            <td><button onclick="logoutTeam('${team.uucms_id}')" class="logout-btn">Logout</button></td>
        `;

        const teamNameCell = row.querySelector(".hover-team");
        teamNameCell.addEventListener("mouseover", (e) => showTeamDetails(e, team));
        teamNameCell.addEventListener("mousemove", (e) => updateTeamCardPosition(e));
        teamNameCell.addEventListener("mouseout", hideTeamDetails);

        teamList.appendChild(row);
    });
}

// Logout team function
function logoutTeam(teamId) {
    console.log(teamId)
    fetch(`/logout-participant/${teamId}`, { method: "GET" })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => alert("Request failed: " + error));
}

function showTeamDetails(event, team) {
    teamCard.innerHTML = `
        <h3>${team.name}</h3>
        <p><strong>UUCMS ID:</strong> ${team.uucms_id}</p>
    `;
    teamCard.style.display = "block";
    updateTeamCardPosition(event);
}

function updateTeamCardPosition(event) {
    teamCard.style.left = event.pageX + 15 + "px";
    teamCard.style.top = event.pageY + 15 + "px";
}

function hideTeamDetails() {
    teamCard.style.display = "none";
}

// Optional polling (remove later when WebSocket stable)
async function fetchParticipants() {
    try {
        const response = await fetch("/api/get-logged-in-participants/");
        const teams = await response.json();
        populateTeamTable(teams);
    } catch (error) {
        console.error("Error fetching teams:", error);
        teamList.innerHTML = `<tr><td colspan="4">Failed to load teams</td></tr>`;
    }
}
let participantInterval = setInterval(fetchParticipants, 3000);
fetchParticipants();

// WebSocket connection
const adminSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/admin/'
    );

    document.getElementById('startQuizBtn').onclick = function() {
        adminSocket.send(JSON.stringify({
            'type': 'start_quiz'
        }));
        clearInterval(participantInterval);
        alert("Quiz Started")
    };

    adminSocket.onclose = function(e) {
        console.error('Admin socket closed unexpectedly');
    };