const messageBox = document.getElementById("message");
const workoutDetailBox = document.getElementById("workout-detail");
const exerciseList = document.getElementById("exercise-list");
const createExerciseForm = document.getElementById("create-exercise-form");
const logoutButton = document.getElementById("logout-button");

function showMessage(text, type) {
  messageBox.textContent = text;
  messageBox.className = `message ${type}`;
}

function redirectToLogin() {
  window.location.href = "/login.html";
}

function getWorkoutIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

function renderWorkoutDetail(workout) {
  workoutDetailBox.innerHTML = `
    <div class="card">
      <p><strong>Title:</strong> ${workout.title}</p>
      <p><strong>Date:</strong> ${workout.workout_date}</p>
      <p><strong>Notes:</strong> ${workout.notes ?? "-"}</p>
    </div>
  `;
}

function renderExerciseList(exercises, workoutId) {
  exerciseList.innerHTML = "";

  if (!exercises || exercises.length === 0) {
    exerciseList.innerHTML = "<li>No exercises yet.</li>";
    return;
  }

  exercises.forEach((exercise) => {
    const li = document.createElement("li");
    li.className = "card";

    li.innerHTML = `
      <p><strong>${exercise.exercise_name}</strong></p>
      <p>Sets: ${exercise.sets} | Reps: ${exercise.reps} | Weight: ${exercise.weight}</p>
      <p>Notes: ${exercise.notes ?? "-"}</p>
      <div class="inline-actions">
        <button type="button" data-action="edit" data-id="${exercise.id}">Edit</button>
        <button type="button" data-action="delete" data-id="${exercise.id}">Delete</button>
      </div>
    `;

    exerciseList.appendChild(li);
  });

  exerciseList.querySelectorAll('button[data-action="delete"]').forEach((button) => {
    button.addEventListener("click", () => {
      const exerciseId = button.dataset.id;
      deleteExercise(workoutId, exerciseId);
    });
  });

  exerciseList.querySelectorAll('button[data-action="edit"]').forEach((button) => {
    button.addEventListener("click", () => {
      const exerciseId = button.dataset.id;
      const currentExercise = exercises.find((item) => String(item.id) === String(exerciseId));
      editExercise(workoutId, currentExercise);
    });
  });
}

async function loadWorkoutDetail() {
  const token = getToken();
  const workoutId = getWorkoutIdFromUrl();

  if (!token) {
    redirectToLogin();
    return;
  }

  if (!workoutId) {
    showMessage("Workout id is missing.", "error");
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/workouts/${workoutId}`, {
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
      showMessage(data.detail || "Failed to load workout detail.", "error");
      return;
    }

    renderWorkoutDetail(data);
    renderExerciseList(data.exercise_logs ?? [], workoutId);
  } catch (error) {
    showMessage("Cannot connect to server.", "error");
  }
}

createExerciseForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const token = getToken();
  const workoutId = getWorkoutIdFromUrl();

  if (!token) {
    redirectToLogin();
    return;
  }

  const payload = {
    exercise_name: document.getElementById("exercise_name").value.trim(),
    sets: Number(document.getElementById("sets").value),
    reps: Number(document.getElementById("reps").value),
    weight: Number(document.getElementById("weight").value),
    notes: document.getElementById("exercise_notes").value.trim() || null,
  };

  try {
    const response = await fetch(`${API_BASE_URL}/workouts/${workoutId}/exercise-logs`, {
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
      showMessage(data.detail || "Failed to create exercise.", "error");
      return;
    }

    showMessage("Exercise created successfully!", "success");
    createExerciseForm.reset();
    loadWorkoutDetail();
  } catch (error) {
    showMessage("Cannot connect to server.", "error");
  }
});

async function deleteExercise(workoutId, exerciseId) {
  const token = getToken();

  if (!token) {
    redirectToLogin();
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/workouts/${workoutId}/exercise-logs/${exerciseId}`, {
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
      let errorMessage = "Failed to delete exercise.";
      try {
        const data = await response.json();
        errorMessage = data.detail || errorMessage;
      } catch (_) {}
      showMessage(errorMessage, "error");
      return;
    }

    showMessage("Exercise deleted successfully!", "success");
    loadWorkoutDetail();
  } catch (error) {
    showMessage("Cannot connect to server.", "error");
  }
}

async function editExercise(workoutId, exercise) {
  const token = getToken();

  if (!token) {
    redirectToLogin();
    return;
  }

  const exercise_name = prompt("Exercise name:", exercise.exercise_name);
  if (exercise_name === null) return;

  const sets = prompt("Sets:", exercise.sets);
  if (sets === null) return;

  const reps = prompt("Reps:", exercise.reps);
  if (reps === null) return;

  const weight = prompt("Weight:", exercise.weight);
  if (weight === null) return;

  const notes = prompt("Notes:", exercise.notes ?? "");
  if (notes === null) return;

  const payload = {
    exercise_name: exercise_name.trim(),
    sets: Number(sets),
    reps: Number(reps),
    weight: Number(weight),
    notes: notes.trim() || null,
  };

  try {
    const response = await fetch(`${API_BASE_URL}/workouts/${workoutId}/exercise-logs/${exercise.id}`, {
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
      showMessage(data.detail || "Failed to update exercise.", "error");
      return;
    }

    showMessage("Exercise updated successfully!", "success");
    loadWorkoutDetail();
  } catch (error) {
    showMessage("Cannot connect to server.", "error");
  }
}

logoutButton.addEventListener("click", () => {
  clearToken();
  redirectToLogin();
});

loadWorkoutDetail();