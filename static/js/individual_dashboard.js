function populateTeamTable(teams) {
    teamList.innerHTML = "";

    teams.forEach((team, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${team.serialNo}</td>
            <td class="hover-team">${team.uucms_id}</td>
            <td>${team.name}</td>
        `;

        const teamNameCell = row.querySelector(".hover-team");
        teamNameCell.addEventListener("mouseover", (e) => showTeamDetails(e, team));
        teamNameCell.addEventListener("mousemove", (e) => updateTeamCardPosition(e));
        teamNameCell.addEventListener("mouseout", hideTeamDetails);

        teamList.appendChild(row);
    });
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
setInterval(fetchParticipants, 3000);
fetchParticipants();

const participantSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/participant/'
    );

    participantSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'redirect') {
            window.location.href = data.target_url;
        }
    };

    participantSocket.onclose = function(e) {
        console.error('Participant socket closed unexpectedly');
    };