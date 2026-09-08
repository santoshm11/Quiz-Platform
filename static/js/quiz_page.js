document.addEventListener('DOMContentLoaded', function() {
    let selectedOption = null;
    let selectedAnswer = null;
    let answerSubmitted = false;
    let autoSubmitTimeout;
    let countdownInterval;

    const questionElement = document.getElementById('question');
    const submitButton = document.getElementById('submitBtn');

    const websocketUrl = 'ws://' + window.location.host + '/ws/participant/';
    const socket = new WebSocket(websocketUrl);

    // Handle option selection
    function selectOption(option, optionText) {
        selectedOption = option;
        selectedAnswer = optionText;  // ✅ Fix applied

        document.querySelectorAll(".option").forEach((btn, index) => {
            btn.style.background = "#0a1f44"; // Reset all buttons
            if (index + 1 === option) {
                btn.style.background = "#00aaff"; // Highlight selected
            }
        });
    }

    // Start countdown timer
    function startTimer(duration) {
        let timer = duration;
        clearInterval(countdownInterval);  // Clear any existing interval
        countdownInterval = setInterval(() => {
            document.getElementById("timer").textContent = timer;
            if (timer === 0) {
                clearInterval(countdownInterval);
                autoSubmit();
            }
            timer--;
        }, 1000);
    }

    // Auto-submit when timer runs out
    function autoSubmit() {
        if (!answerSubmitted) {
            submitAnswer('No Response');
        }
    }

    function getCSRFToken() {
        const token = document.querySelector('meta[name="csrf-token"]');
        return token ? token.getAttribute('content') : '';
    }

    // Send answer to backend
    function submitAnswer(answer) {
            answerSubmitted = true;
        
            // ✅ AJAX POST to save answer
            fetch('/submit-answer/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),  // Django CSRF token
                },
                body: JSON.stringify({
                    'question_id': currentQuestionId,  // You'll need to track this!
                    'selected_option': answer,
                    'uucms_id': "{{ request.user.uucms_id }}" ,
                }),
            })
            .then(response => response.json())
            .then(data => {
                console.log("Answer Saved:", data);
                // ✅ Optional: Additional logic if needed
            })
            .catch(error => console.error('Error:', error));
        
            // ✅ WebSocket for control flow (keep as is)
            socket.send(JSON.stringify({
                'type': 'answer',
                'answer': answer,
                'uucms_id': "{{ request.user.uucms_id }}" ,
            }));
        
            submitButton.disabled = true;  // Disable after submission
        
            // ✅ Redirect (WebSocket also handles redirect if needed)
            window.location.href = '/holding/';            
    }

    // Handle WebSocket incoming messages
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log(event.data);

        if (data.type === 'question') {
            currentQuestionId = data.question_id; 
            document.getElementById("question").textContent = data.question;
            document.getElementById("timer").textContent = data.duration;
            const options = data.options;

            // Update options dynamically
            document.getElementById("option1").textContent = options[0];
            document.getElementById("option2").textContent = options[1];
            document.getElementById("option3").textContent = options[2];
            document.getElementById("option4").textContent = options[3];

            // Set click events
            document.getElementById("option1").onclick = () => selectOption(1, options[0]);
            document.getElementById("option2").onclick = () => selectOption(2, options[1]);
            document.getElementById("option3").onclick = () => selectOption(3, options[2]);
            document.getElementById("option4").onclick = () => selectOption(4, options[3]);

            startTimer(data.duration);

            // Setup auto-submit fallback
            clearTimeout(autoSubmitTimeout);
            autoSubmitTimeout = setTimeout(autoSubmit, data.duration * 1000);
        }

        // Handle redirect
        else if (data.type === 'redirect') {
            window.location.href = data.target_url;
        }
    };

    // Manual submission
    submitButton.onclick = function() {
        if (selectedAnswer) {
            submitAnswer(selectedAnswer);
            clearTimeout(autoSubmitTimeout);
        } else {
            //alert('Please select an option!');
        }
    };

    // Handle WebSocket close
    socket.onclose = function() {
        alert('WebSocket connection closed!');
    };
});