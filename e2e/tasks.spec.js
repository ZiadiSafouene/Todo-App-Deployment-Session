
const { test, expect } = require("@playwright/test");

test("user can create and complete a task", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: "Task Tracker" })
  ).toBeVisible();

  await page.getByLabel("New task").fill("Prepare workshop");

  await page.getByRole("button", { name: "Add task" }).click();

  const task = page.locator("li").filter({
    hasText: "Prepare workshop",
  });

  await expect(task).toBeVisible();

  await task.getByRole("button", { name: "Complete" }).click();

  await expect(
    task.getByRole("button", { name: "Completed" })
  ).toBeVisible();
});
