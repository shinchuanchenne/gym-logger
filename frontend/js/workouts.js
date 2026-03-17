const messageBox = document.getElementById("message");
const workoutList = document.getElementById("workout-list");
const createWorkoutForm = document.getElementById("create-workout-form");
const logoutButton = document.getElementById("logout-button");

function showMessage(text, type) {
  messageBox.textContent = text;
  messageBox.className = `message ${type}`;
}

function redirectToLogin() {
  window.location.href = "./login.html";
}

function renderWorkouts(workouts) {
  workoutList.innerHTML = "";

  if (workouts.length === 0) {
    workoutList.innerHTML = "<li>No workouts yet.</li>";
    return;
  }

  workouts.forEach((workout) => {
    const li = document.createElement("li");
    li.textContent = `${workout.workout_date} - ${workout.title}${workout.notes ? " - " + workout.notes : ""}`;
    workoutList.appendChild(li);
  });
}

async function loadWorkouts() {
  const token = getToken();

  if (!token) {
    redirectToLogin();
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/workouts`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });

    if (response.status === 401) {
      clearToken();
      redirectToLogin();
      return;
    }

    const data = await response.json();

    if (!response.ok) {
      showMessage(data.detail || "Failed to load workouts.", "error");
      return;
    }

    renderWorkouts(data);
  } catch (error) {
    showMessage("Cannot connect to server.", "error");
  }
}

createWorkoutForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const token = getToken();

  if (!token) {
    redirectToLogin();
    return;
  }

  const title = document.getElementById("title").value.trim();
  const workoutDate = document.getElementById("workout_date").value;
  const notes = document.getElementById("notes").value.trim();

  const payload = {
    title,
    workout_date: workoutDate,
    notes: notes || null,
  };

  try {
    const response = await fetch(`${API_BASE_URL}/workouts`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });

    if (response.status === 401) {
      clearToken();
      redirectToLogin();
      return;
    }

    const data = await response.json();

    if (!response.ok) {
      showMessage(data.detail || "Failed to create workout.", "error");
      return;
    }

    showMessage("Workout created successfully!", "success");
    createWorkoutForm.reset();
    loadWorkouts();
  } catch (error) {
    showMessage("Cannot connect to server.", "error");
  }
});

logoutButton.addEventListener("click", () => {
  clearToken();
  redirectToLogin();
});

loadWorkouts();