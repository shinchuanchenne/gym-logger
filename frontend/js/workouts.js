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
      li.className = "card";
  
      li.innerHTML = `
        <p><strong>${workout.title}</strong></p>
        <p>${workout.workout_date}</p>
        <p>${workout.notes ?? "-"}</p>
        <div class="inline-actions">
          <a href="/workout-detail.html?id=${workout.id}">View Detail</a>
          <button type="button" data-action="edit" data-id="${workout.id}">Edit</button>
          <button type="button" data-action="delete" data-id="${workout.id}">Delete</button>
        </div>
      `;
  
      workoutList.appendChild(li);
    });
  
    workoutList.querySelectorAll('button[data-action="delete"]').forEach((button) => {
      button.addEventListener("click", () => {
        const workoutId = button.dataset.id;
        deleteWorkout(workoutId);
      });
    });
  
    workoutList.querySelectorAll('button[data-action="edit"]').forEach((button) => {
      button.addEventListener("click", () => {
        const workoutId = button.dataset.id;
        const currentWorkout = workouts.find((item) => String(item.id) === String(workoutId));
        editWorkout(currentWorkout);
      });
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

async function deleteWorkout(workoutId) {
    const token = getToken();
  
    if (!token) {
      redirectToLogin();
      return;
    }
  
    const confirmed = confirm("Are you sure you want to delete this workout?");
    if (!confirmed) {
      return;
    }
  
    try {
      const response = await fetch(`${API_BASE_URL}/workouts/${workoutId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });
  
      if (response.status === 401) {
        clearToken();
        redirectToLogin();
        return;
      }
  
      if (!response.ok) {
        let errorMessage = "Failed to delete workout.";
        try {
          const data = await response.json();
          errorMessage = data.detail || errorMessage;
        } catch (_) {}
        showMessage(errorMessage, "error");
        return;
      }
  
      showMessage("Workout deleted successfully!", "success");
      loadWorkouts();
    } catch (error) {
      showMessage("Cannot connect to server.", "error");
    }
  }

  async function editWorkout(workout) {
    const token = getToken();
  
    if (!token) {
      redirectToLogin();
      return;
    }
  
    const title = prompt("Workout title:", workout.title);
    if (title === null) return;
  
    const workoutDate = prompt("Workout date (YYYY-MM-DD):", workout.workout_date);
    if (workoutDate === null) return;
  
    const notes = prompt("Notes:", workout.notes ?? "");
    if (notes === null) return;
  
    const payload = {
      title: title.trim(),
      workout_date: workoutDate.trim(),
      notes: notes.trim() || null,
    };
  
    try {
      const response = await fetch(`${API_BASE_URL}/workouts/${workout.id}`, {
        method: "PUT",
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
        showMessage(data.detail || "Failed to update workout.", "error");
        return;
      }
  
      showMessage("Workout updated successfully!", "success");
      loadWorkouts();
    } catch (error) {
      showMessage("Cannot connect to server.", "error");
    }
  }

loadWorkouts();