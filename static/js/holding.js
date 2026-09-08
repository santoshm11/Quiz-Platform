document.addEventListener('DOMContentLoaded', function() {
    const animationDiv = document.getElementById('animationDiv');
    // Update path as per your setup
    const answerElement = document.getElementById('answer');

    const websocketUrl = 'ws://' + window.location.host + '/ws/participant/';
    const socket = new WebSocket(websocketUrl);

    function getCSRFToken() {
        const token = document.querySelector('meta[name="csrf-token"]');
        return token ? token.getAttribute('content') : '';
    }    

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'answer') {
            fetch('/status/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.status)
        if (data.status === "correct") {
            document.querySelector('.holding-container h2').style.display = 'none';
            animationDiv.innerHTML = `
                <img src="${likeGif}" class="thumbs-down" 
                style="animation: bounce 0.6s ease-in-out 2; /* box-shadow: 0 0 80px rgba(27, 228, 44, 0.8),inset 0px 0px 1000px rgba(27, 228, 54, 0.6);*/
                width: 200px; height: 200px;">
            `;
        } 
        else if (data.status === "incorrect") {
            document.querySelector('.holding-container h2').style.display = 'none';
            animationDiv.innerHTML = `
                <div class="thumbs-down"><span class="emoji" style="/*box-shadow: 0 0 80px rgba(228, 27, 27, 0.8), /* Outer Glow */inset 0px 0px 1000px rgba(228, 27, 27, 0.6);*/">👎</span></div>
            `;
        }
        else {
            document.querySelector('.holding-container h2').style.display = 'none';
            animationDiv.innerHTML = `
                <div class="thumbs-down"><span class="emoji" style="/*box-shadow: 0 0 80px rgba(228, 27, 27, 0.8), /* Outer Glow */inset 0px 0px 1000px rgba(228, 27, 27, 0.6);*/">👎 Unanswered </span></div>
            `;
        }
    });
}

        if (data.type === 'redirect') {
            setTimeout(function() {
                window.location.href = data.target_url;
            }, 5000); // 5000 milliseconds = 5 seconds
        }

        if (data.action === 'redirect_to_result') {
            window.location.href = data.url;  // Redirect using URL from server
        }    
    };            
});