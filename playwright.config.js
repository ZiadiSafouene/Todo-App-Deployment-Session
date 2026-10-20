
const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./e2e",
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:5500",
    browserName: "chromium",
  },
  webServer: [
    {
      command:
        "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000",
      cwd: "./backend",
      url: "http://127.0.0.1:8000/health",
      reuseExistingServer: !process.env.CI,
      timeout: 30000,
    },
    {
      command:
        "python -m http.server 5500 --directory frontend",
      url: "http://127.0.0.1:5500",
      reuseExistingServer: !process.env.CI,
      timeout: 30000,
    },
  ],
});
