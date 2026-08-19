import { useState } from "react";
import axios from "axios";

function AIAssistant({ apiUrl, onResults }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);

  const askAssistant = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    try {
      const res = await axios.post(`${apiUrl}/assistant/ask`, { question });
      setAnswer(res.data.results);
      onResults(res.data.results.map((p) => p.id));
    } catch (err) {
      console.error("Assistant request failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-assistant">
      <form onSubmit={askAssistant}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. something light for daily office use"
        />
        <button type="submit" disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </form>

      {answer && (
        <div className="ai-answer">
          {answer.length === 0 ? (
            <p>No matching products found — try rephrasing your question.</p>
          ) : (
            <p>
              Found {answer.length} matching product(s), highlighted below.
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default AIAssistant;
