function closePopup() {
    const popup = document.querySelector(".popup");
    if (popup) {
        popup.remove();
    }
} 
document.addEventListener("DOMContentLoaded", () => {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const form = document.getElementById("registrationForm");
    const uucmsInput = document.getElementById("uucms_id");
    const nameInput = document.getElementById("name");
    const uucmsError = document.getElementById("uucmsError");
    const nameError = document.getElementById("nameError");

    // Function to validate UUCMS ID format
    function validateUUCMS(uucms) {
        const uucmsPattern = /^U\d{2}SD\d{2}S\d{4}$/; // Example pattern
        return uucmsPattern.test(uucms);
    }

    // Function to validate Name (only letters allowed)
    function validateName(name) {
        return /^[A-Za-z\s]+$/.test(name);
    }

    // Real-time validation
    uucmsInput.addEventListener("input", () => {
        if (!validateUUCMS(uucmsInput.value)) {
            uucmsError.textContent = "Invalid UUCMS ID format.";
            uucmsError.style.color = "red";
        } else {
            uucmsError.textContent = "";
        }
    });

    nameInput.addEventListener("input", () => {
        if (!validateName(nameInput.value)) {
            nameError.textContent = "Only alphabets are allowed.";
            nameError.style.color = "red";
        } else {
            nameError.textContent = "";
        }
    });

    // Form submission handling
    form.addEventListener("submit", (event) => {
        event.preventDefault();

        let isValid = true;

        if (!validateUUCMS(uucmsInput.value)) {
            uucmsError.textContent = "Invalid UUCMS ID format.";
            isValid = false;
        } else {
            uucmsError.textContent = "";
        }

        if (!validateName(nameInput.value)) {
            nameError.textContent = "Only alphabets are allowed.";
            isValid = false;
        } else {
            nameError.textContent = "";
        }

        if (isValid) {
            submitForm();
        }
    });

    // Function to send data to the backend (AJAX Request)
    function submitForm() {
        const formData = new FormData(form);

        fetch("/register/", {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                //alert("Registration Successful!");
                showLoginPopup(data.uucms_id, data.password);
                form.reset();
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => {
            console.error("Error submitting form:", error);
        });
    }

    function showLoginPopup(UUCMSID, password) {
        const popup = document.createElement("div");
        popup.classList.add("popup");
        popup.innerHTML = `
            <div class="popup-content">
                <h2>Team Registered Successfully!</h2>
                <p><strong>UUCMS ID:</strong> ${UUCMSID}</p>
                <p><strong>Password:</strong> ${password}</p>
                <button onclick="closePopup()">OK</button>
            </div>
        `;
        document.body.appendChild(popup);
    }
    
});
           
