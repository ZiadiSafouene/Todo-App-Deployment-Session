
const API = window.API_BASE;

const form = document.querySelector("#task-form");
const input = document.querySelector("#task-input");
const list = document.querySelector("#task-list");
const message = document.querySelector("#message");

async function request(path, options = {}) {
  const response = await fetch(`${API}${path}`, options);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Request failed");
  }

  return response.json();
}

function renderTasks(tasks) {
  list.replaceChildren();

  for (const task of tasks) {
    const item = document.createElement("li");
    const title = document.createElement("span");
    const button = document.createElement("button");

    title.textContent = task.title;
    button.textContent = task.completed ? "Completed" : "Complete";
    button.disabled = task.completed;

    button.addEventListener("click", async () => {
      try {
        await request(`/api/tasks/${task.id}/complete`, {
          method: "PATCH",
        });
        await loadTasks();
      } catch (error) {
        message.textContent = error.message;
      }
    });

    item.append(title, button);
    list.append(item);
  }
}

async function loadTasks() {
  renderTasks(await request("/api/tasks"));
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "";

  try {
    await request("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: input.value }),
    });

    input.value = "";
    await loadTasks();
  } catch (error) {
    message.textContent = error.message;
  }
});

loadTasks().catch((error) => {
  message.textContent = `Cannot connect to the API: ${error.message}`;
});
