/**
 * API client — the only file that knows about the backend URL.
 * Everything else in the frontend is unaware of Django.
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export async function fetchInterviewQuestions(jobTitle) {
  const response = await fetch(`${BASE_URL}/api/questions/generate/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ job_title: jobTitle }),
  });

  const data = await response.json();

  if (!response.ok) {
    const message =
      typeof data.error === "string"
        ? data.error
        : JSON.stringify(data.error);
    throw new Error(message || "Failed to generate questions.");
  }

  return data.questions;
}
