import { useState } from "react";
import { fetchInterviewQuestions } from "./api";
import "./App.css";

const LOADING_MESSAGES = [
  "Consulting the hiring committee...",
  "Brewing interview questions...",
  "Thinking like an HR expert...",
  "Crafting the perfect questions...",
];

// Must match MAX_JOB_TITLE_LENGTH in constants.py.
// Enforced here so the user gets instant feedback instead of a backend error.
const MAX_TITLE_LENGTH = 120;

export default function App() {
  const [jobTitle, setJobTitle]           = useState("Customer Success Manager");
  const [submittedTitle, setSubmittedTitle] = useState("");  // frozen at submit time
  const [questions, setQuestions]         = useState([]);
  const [loading, setLoading]             = useState(false);
  const [loadingMsg, setLoadingMsg]       = useState("");
  const [error, setError]                 = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    const trimmed = jobTitle.trim();
    if (!trimmed) return;

    // Snapshot the title at submission time so the results heading
    // doesn't update if the user edits the input while results are showing.
    setSubmittedTitle(trimmed);

    // Pick a random loading message each time so it feels alive
    setLoadingMsg(LOADING_MESSAGES[Math.floor(Math.random() * LOADING_MESSAGES.length)]);
    setLoading(true);
    setError(null);
    setQuestions([]);

    try {
      const result = await fetchInterviewQuestions(trimmed);
      setQuestions(result);
    } catch (err) {
      // Show the exact message from the backend (e.g. "Please enter a valid job title")
      // instead of a generic fallback — the backend already writes user-friendly messages
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="badge">AI-Powered</div>
        <h1 className="title">Interview Question Generator</h1>
        <p className="subtitle">
          Enter any job title to get 3 tailored interview questions instantly.
        </p>
      </header>

      <main className="main">
        <form className="form" onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="job-title" className="label">Job Title</label>
            <input
              id="job-title"
              type="text"
              className="input"
              value={jobTitle}
              maxLength={MAX_TITLE_LENGTH}
              onChange={(e) => {
                setJobTitle(e.target.value);
                // Clear error as soon as the user starts correcting their input
                if (error) setError(null);
              }}
              placeholder="e.g. Customer Success Manager"
              disabled={loading}
              required
            />
          </div>
          <button
            type="submit"
            className="btn"
            disabled={loading || !jobTitle.trim()}
          >
            {loading ? (
              <><span className="spinner" />{loadingMsg}</>
            ) : (
              "Generate Questions"
            )}
          </button>
        </form>

        {error && (
          <div className="error-box" role="alert">
            {error}
          </div>
        )}

        {questions.length > 0 && (
          <section className="results" aria-live="polite">
            <h2 className="results-heading">
              {/* submittedTitle is frozen at submit time — won't drift
                  if the user edits the input after seeing results */}
              Questions for <em>{submittedTitle}</em>
            </h2>
            <ol className="question-list">
              {questions.map((q, i) => (
                // q is unique per question — safer key than array index
                <li key={q} className="question-item">
                  {/* padStart handles any count correctly — "01", "02" ... "10", "11" */}
                  <span className="question-number">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <p className="question-text">{q}</p>
                </li>
              ))}
            </ol>
          </section>
        )}
      </main>

      <footer className="footer">
        Built with Django · React · Groq · Llama 3.1
      </footer>
    </div>
  );
}