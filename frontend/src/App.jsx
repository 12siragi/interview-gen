import { useState } from "react";
import { fetchInterviewQuestions } from "./api";
import "./App.css";

export default function App() {
  const [jobTitle, setJobTitle] = useState("Customer Success Manager");
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    const trimmed = jobTitle.trim();
    if (!trimmed) return;

    setLoading(true);
    setError(null);
    setQuestions([]);

    try {
      const result = await fetchInterviewQuestions(trimmed);
      setQuestions(result);
    } catch (err) {
      setError(err.message);
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
              onChange={(e) => setJobTitle(e.target.value)}
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
              <><span className="spinner" />Generating questions...</>
            ) : (
              "Generate Questions"
            )}
          </button>
        </form>

        {error && (
          <div className="error-box" role="alert">
            <strong>Something went wrong:</strong> {error}
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
