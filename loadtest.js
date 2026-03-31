import http from "k6/http";
import { check, sleep } from "k6";
import {
  randomIntBetween,
  randomItem,
} from "https://jslib.k6.io/k6-utils/1.4.0/index.js";

export const options = {
  stages: [
    { duration: "2m", target: 5 }, // Ramp up to 5 VUs
    { duration: "3m", target: 10 }, // Ramp up to 10 VUs
    { duration: "4m", target: 20 }, // Ramp up to 20 VUs
    { duration: "2m", target: 40 }, // Ramp up to 40 VUs
    { duration: "2m", target: 80 }, // Spike to 80 VUs
    { duration: "2m", target: 10 }, // Ramp down
  ],
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";

const TASK_TITLES = [
  "Fix login bug in auth module",
  "Update API documentation",
  "Review and merge PR #{{num}}",
  "Implement user dashboard",
  "Add unit tests for payment service",
  "Optimize database queries",
  "Design new landing page",
  "Migrate legacy code to new framework",
  "Set up CI/CD pipeline",
  "Write integration tests",
  "Refactor user authentication",
  "Update dependencies to latest versions",
  "Fix memory leak in worker process",
  "Implement rate limiting",
  "Add logging for critical operations",
  "Create backup system",
  "Improve error handling",
  "Add missing API endpoints",
  "Code review for feature X",
  "Performance optimization for reports",
];

const TASK_DESCRIPTIONS = [
  "This task requires attention to detail and thorough testing.",
  "Need to coordinate with the team before starting.",
  "High priority task for this sprint.",
  "Technical debt that needs to be addressed.",
  "Customer reported issue - needs immediate attention.",
  "Part of Q{{num}} roadmap.",
  "Blocked by infrastructure team.",
  "Requires API changes and database migration.",
  "Low priority but good to have.",
  "Simple fix that should take about {{num}} hours.",
];

const PRIORITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];
const PRIORITIY_WEIGHTS = [40, 35, 20, 5]; // Most tasks are low/medium priority

const STATUSES = ["OPEN", "IN_PROGRESS", "BLOCKED", "DONE", "CLOSED"];

function generateRandomEmail() {
  const timestamp = Date.now();
  const randomNum = randomIntBetween(1000, 9999);
  const domains = ["example.com", "test.io", "sample.org", "demo.net"];
  const usernames = [
    "user",
    "dev",
    "qa",
    "tester",
    "engineer",
    "devops",
    "backend",
    "frontend",
  ];
  return `${randomItem(usernames)}_${timestamp}_${randomNum}@${randomItem(domains)}`;
}

function generateRandomUsername() {
  const timestamp = Date.now();
  const randomNum = randomIntBetween(100, 999);
  const names = [
    "john",
    "jane",
    "dev",
    "engineer",
    "tester",
    "analyst",
    "admin",
    "user",
    "qa",
    "lead",
  ];
  return `${randomItem(names)}_${timestamp}_${randomNum}`;
}

function generateRandomPassword() {
  const chars =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!";
  let password = "";
  for (let i = 0; i < 12; i++) {
    password += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return `Pass_${password}`;
}

function generateRandomTaskTitle() {
  let title = randomItem(TASK_TITLES);
  title = title.replace("{{num}}", randomIntBetween(1, 999));
  return title;
}

function generateRandomTaskDescription() {
  let desc = randomItem(TASK_DESCRIPTIONS);
  desc = desc.replace("{{num}}", randomIntBetween(1, 8));
  return desc;
}

function getWeightedPriority() {
  const rand = Math.random() * 100;
  let cumulative = 0;
  for (let i = 0; i < PRIORITIES.length; i++) {
    cumulative += PRIORITIY_WEIGHTS[i];
    if (rand < cumulative) {
      return PRIORITIES[i];
    }
  }
  return "MEDIUM";
}

function signup(email, password, username) {
  const payload = JSON.stringify({
    email: email,
    password: password,
    username: username,
  });

  const res = http.post(`${BASE_URL}/api/v1/auth/signup`, payload, {
    headers: { "Content-Type": "application/json" },
  });

  check(res, {
    "signup successful": (r) => r.status === 201,
  });

  return res;
}

function signin(email, password) {
  const payload = JSON.stringify({
    email: email,
    password: password,
  });

  const res = http.post(`${BASE_URL}/api/v1/auth/signin`, payload, {
    headers: { "Content-Type": "application/json" },
  });

  check(res, {
    "signin successful": (r) => r.status === 200,
  });

  return res;
}

function signout(cookies) {
  const res = http.post(`${BASE_URL}/api/v1/auth/signout`, null, {
    headers: { "Content-Type": "application/json" },
    cookies: cookies,
  });

  check(res, {
    "signout successful": (r) => r.status === 200,
  });
}

function getCurrentUser(cookies) {
  const res = http.get(`${BASE_URL}/api/v1/auth/me`, {
    cookies: cookies,
  });

  check(res, {
    "get current user successful": (r) => r.status === 200,
  });

  return res;
}

function createTask(cookies, taskData) {
  const payload = JSON.stringify(taskData);

  const res = http.post(`${BASE_URL}/api/v1/tasks/`, payload, {
    headers: { "Content-Type": "application/json" },
    cookies: cookies,
  });

  check(res, {
    "task created": (r) => r.status === 201,
  });

  if (res.status === 201) {
    return JSON.parse(res.body);
  }
  return null;
}

function listTasks(cookies) {
  const res = http.get(`${BASE_URL}/api/v1/tasks/`, {
    cookies: cookies,
  });

  check(res, {
    "list tasks successful": (r) => r.status === 200,
  });

  if (res.status === 200) {
    return JSON.parse(res.body);
  }
  return [];
}

function getTask(cookies, taskId) {
  const res = http.get(`${BASE_URL}/api/v1/tasks/${taskId}`, {
    cookies: cookies,
  });

  check(res, {
    "get task successful": (r) => r.status === 200 || r.status === 404,
  });

  if (res.status === 200) {
    return JSON.parse(res.body);
  }
  return null;
}

function updateTask(cookies, taskId, taskData) {
  const payload = JSON.stringify(taskData);

  const res = http.put(`${BASE_URL}/api/v1/tasks/${taskId}`, payload, {
    headers: { "Content-Type": "application/json" },
    cookies: cookies,
  });

  check(res, {
    "task updated": (r) => r.status === 200 || r.status === 404,
  });

  if (res.status === 200) {
    return JSON.parse(res.body);
  }
  return null;
}

function deleteTask(cookies, taskId) {
  const res = http.del(`${BASE_URL}/api/v1/tasks/${taskId}`, null, {
    cookies: cookies,
  });

  check(res, {
    "task deleted": (r) => r.status === 204 || r.status === 404,
  });
}

function triggerAlwaysBreak() {
  const res = http.get(`${BASE_URL}/api/v1/tasks/always-break`);
  check(res, {
    "always-break returned error": (r) => r.status === 500,
  });
}

function triggerBreak50Percent() {
  const res = http.get(`${BASE_URL}/api/v1/tasks/break-50-percent`);
  check(res, {
    "break-50-percent endpoint called": (r) =>
      r.status === 500 || r.status === 200,
  });
}

function triggerBreakRandomly() {
  const res = http.get(`${BASE_URL}/api/v1/tasks/break-randomly`);
  check(res, {
    "break-randomly endpoint called": (r) =>
      r.status === 500 || r.status === 200,
  });
}

function updateTask(cookies, taskId, taskData) {
  const payload = JSON.stringify(taskData);

  const res = http.put(`${BASE_URL}/api/v1/tasks/${taskId}`, payload, {
    headers: { "Content-Type": "application/json" },
    cookies: cookies,
  });

  check(res, {
    "task updated": (r) => r.status === 200 || r.status === 404,
  });

  if (res.status === 200) {
    return JSON.parse(res.body);
  }
  return null;
}

function deleteTask(cookies, taskId) {
  const res = http.del(`${BASE_URL}/api/v1/tasks/${taskId}/`, null, {
    cookies: cookies,
  });

  check(res, {
    "task deleted": (r) => r.status === 204 || r.status === 404,
  });
}

function triggerAlwaysBreak() {
  const res = http.get(`${BASE_URL}/api/v1/tasks/always-break/`);
  check(res, {
    "always-break returned error": (r) => r.status === 500,
  });
}

function triggerBreak50Percent() {
  const res = http.get(`${BASE_URL}/api/v1/tasks/break-50-percent/`);
  check(res, {
    "break-50-percent endpoint called": (r) =>
      r.status === 500 || r.status === 200,
  });
}

function triggerBreakRandomly() {
  const res = http.get(`${BASE_URL}/api/v1/tasks/break-randomly/`);
  check(res, {
    "break-randomly endpoint called": (r) =>
      r.status === 500 || r.status === 200,
  });
}

function newUserScenario() {
  const email = generateRandomEmail();
  const password = generateRandomPassword();
  const username = generateRandomUsername();

  signup(email, password, username);
  sleep(randomIntBetween(3, 6));

  const signinRes = signin(email, password);
  sleep(randomIntBetween(2, 5));

  if (signinRes.status !== 200) {
    return;
  }

  const cookies = signinRes.cookies;

  getCurrentUser(cookies);
  sleep(randomIntBetween(1, 3));

  const taskData = {
    title: generateRandomTaskTitle(),
    description: generateRandomTaskDescription(),
    priority: getWeightedPriority(),
    status: "OPEN",
  };

  const createdTask = createTask(cookies, taskData);
  sleep(randomIntBetween(2, 4));

  if (createdTask) {
    getTask(cookies, createdTask.id);
    sleep(randomIntBetween(1, 3));

    const updateData = {
      status: randomItem(STATUSES),
      priority: getWeightedPriority(),
    };

    updateTask(cookies, createdTask.id, updateData);
    sleep(randomIntBetween(1, 2));
  }

  const tasks = listTasks(cookies);
  sleep(randomIntBetween(1, 3));

  if (tasks.length > 0 && Math.random() < 0.3) {
    const randomTask = randomItem(tasks);
    deleteTask(cookies, randomTask.id);
    sleep(randomIntBetween(1, 2));
  }

  signout(cookies);
}

function returningUserScenario() {
  const email = generateRandomEmail();
  const password = generateRandomPassword();
  const username = generateRandomUsername();

  signup(email, password, username);
  sleep(randomIntBetween(1, 2));

  const signinRes = signin(email, password);
  sleep(randomIntBetween(2, 5));

  if (signinRes.status !== 200) {
    return;
  }

  const cookies = signinRes.cookies;

  getCurrentUser(cookies);
  sleep(randomIntBetween(1, 3));

  const tasks = listTasks(cookies);
  sleep(randomIntBetween(1, 3));

  const numberOfTasks = randomIntBetween(1, 3);

  for (let i = 0; i < numberOfTasks; i++) {
    const taskData = {
      title: generateRandomTaskTitle(),
      description: generateRandomTaskDescription(),
      priority: getWeightedPriority(),
      status: "OPEN",
    };

    const createdTask = createTask(cookies, taskData);
    sleep(randomIntBetween(2, 4));

    if (createdTask) {
      getTask(cookies, createdTask.id);
      sleep(randomIntBetween(1, 2));

      const updateData = {
        status: randomItem(STATUSES),
        priority: getWeightedPriority(),
      };

      updateTask(cookies, createdTask.id, updateData);
      sleep(randomIntBetween(1, 2));
    }
  }

  if (Math.random() < 0.4) {
    const tasks = listTasks(cookies);
    sleep(randomIntBetween(1, 3));

    if (tasks.length > 0 && Math.random() < 0.3) {
      const randomTask = randomItem(tasks);
      deleteTask(cookies, randomTask.id);
      sleep(randomIntBetween(1, 2));
    }
  }

  signout(cookies);
}

function casualUserScenario() {
  const email = generateRandomEmail();
  const password = generateRandomPassword();
  const username = generateRandomUsername();

  signup(email, password, username);
  sleep(randomIntBetween(1, 2));

  const signinRes = signin(email, password);
  sleep(randomIntBetween(1, 2));

  if (signinRes.status !== 200) {
    return;
  }

  const cookies = signinRes.cookies;

  getCurrentUser(cookies);
  sleep(randomIntBetween(1, 2));

  listTasks(cookies);
  sleep(randomIntBetween(1, 3));

  signout(cookies);
}

function errorScenarioUser() {
  const email = generateRandomEmail();
  const password = generateRandomPassword();
  const username = generateRandomUsername();

  signup(email, password, username);
  sleep(randomIntBetween(1, 2));

  const signinRes = signin(email, password);
  sleep(randomIntBetween(1, 2));

  if (signinRes.status !== 200) {
    return;
  }

  const cookies = signinRes.cookies;

  triggerAlwaysBreak();
  sleep(randomIntBetween(1, 2));

  for (let i = 0; i < randomIntBetween(1, 3); i++) {
    triggerBreak50Percent();
    sleep(randomIntBetween(1, 2));
  }

  for (let i = 0; i < randomIntBetween(1, 3); i++) {
    triggerBreakRandomly();
    sleep(randomIntBetween(1, 2));
  }

  listTasks(cookies);
  sleep(randomIntBetween(1, 2));

  signout(cookies);
}

export default function () {
  const rand = Math.random();
  let scenario;

  if (rand < 0.5) {
    scenario = "returning";
  } else if (rand < 0.75) {
    scenario = "new";
  } else if (rand < 0.9) {
    scenario = "casual";
  } else {
    scenario = "error";
  }

  switch (scenario) {
    case "returning":
      returningUserScenario();
      break;
    case "new":
      newUserScenario();
      break;
    case "casual":
      casualUserScenario();
      break;
    case "error":
      errorScenarioUser();
      break;
  }
}
