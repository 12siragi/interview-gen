import { useState } from "react";
import { fetchInterviewQuestions } from "./api";
import "./App.css";

const LOADING_MESSAGES = [
  "Consulting the hiring committee...",
  "Brewing interview questions...",
  "Thinking like an HR expert...",
  "Crafting the perfect questions...",
];

export default function App() {
  const [jobTitle, setJobTitle] = useState("Customer Success Manager");
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingMsg, setLoadingMsg] = useState("");
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    const trimmed = jobTitle.trim();
    if (!trimmed) return;

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
              Questions for <em>{jobTitle}</em>
            </h2>
            <ol className="question-list">
              {questions.map((q, i) => (
                <li key={i} className="question-item">
                  <span className="question-number">0{i + 1}</span>
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