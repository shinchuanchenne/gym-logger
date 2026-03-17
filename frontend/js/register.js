const registerForm = document.getElementById("register-form");
const messageBox = document.getElementById("message");

function showMessage(text, type) {
  messageBox.textContent = text;
  messageBox.className = `message ${type}`;
}

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  const payload = {
    username,
    email,
    password,
  };

  try {
    const response = await fetch(`${API_BASE_URL}/users/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      showMessage(data.detail || "Register failed.", "error");
      return;
    }

    showMessage("Register successful! Please go to login.", "success");
    registerForm.reset();
  } catch (error) {
    showMessage("Cannot connect to server.", "error");
  }
});