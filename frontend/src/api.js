/**
 * API client — the only file that knows about the backend URL.
 * Everything else in the frontend is unaware of Django.
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export async function fetchInterviewQuestions(jobTitle) {
  // Separate try/catch for the fetch itself — covers offline and DNS failures.
  // Without this, a network error throws a raw TypeError: "Failed to fetch"
  // which is never shown to the user in a friendly way.
  let response;
  try {
    response = await fetch(`${BASE_URL}/api/questions/generate/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_title: jobTitle }),
    });
  } catch {
    throw new Error("Cannot reach the server. Check your connection and try again.");
  }

  const data = await response.json();

  if (!response.ok) {
    // Backend already writes user-friendly error messages — surface them directly.
    // If the error is an object (e.g. DRF field errors), stringify it as a fallback.
    const message =
      typeof data.error === "string"
        ? data.error
        : JSON.stringify(data.error);
    throw new Error(message || "Failed to generate questions.");
  }

  return data.questions;
}