const loginForm = document.getElementById("login-form");
const messageBox = document.getElementById("message");

function showMessage(text, type){
    messageBox.textContent = text;
    messageBox.className = `message ${type}`;
}

loginForm.addEventListener("submit", async(event) => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    const formBody = new URLSearchParams();
    formBody.append("username", email);
    formBody.append("password", password);

    try {
        const response = await fetch (`${API_BASE_URL}/auth/token`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: formBody.toString(),
        });

        const data = await response.json();

        if (!response.ok){
            showMessage(data.detail || "Login failed.", "error");
            return;
        }

        saveToken(data.access_token);
        showMessage("Login successful! Redirecting...", "success");

        console.log("login success");


        setTimeout(() => {
            console.log("about to redirect");
            window.location.href = "/workouts.html";
        }, 800);
    } catch (error) {
        showMessage("Cannot connect to server.", "error");
    }
});