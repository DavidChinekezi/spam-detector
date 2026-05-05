import { useState } from "react";
import "../styles/home.css"; // import the separate CSS file

// Define the shape of the API response and our result state
interface SpamResult {
  isSpam: boolean;
  score: number;
  keywords: string[];
  message: string;
}

const SpamDetector = () => {
  const [message, setMessage] = useState<string>("");
  const [result, setResult] = useState<SpamResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  // Replace with your actual backend URL (local or production)
  // For local development: "http://127.0.0.1:5000/predict"
  // For production: use your Render or Vercel URL
  const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000/predict";

  const handleAnalyse = async () => {
    if (!message.trim()) {
      setError("Please enter an email message to analyse.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subject: "", body: message }),
      });
      if (!response.ok) throw new Error(`Server error: ${response.status}`);
      const data = await response.json();
      
      // Map backend fields (snake_case) to our frontend interface (camelCase)
      setResult({
        isSpam: data.is_spam,
        score: data.spam_score,
        keywords: data.found_keywords || [],
        message: data.message || (data.is_spam ? "Spam detected!" : "Legitimate email"),
      });
    } catch (err) {
      setError("Failed to connect to spam detection server.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="spam-detector">
      <div className="card">
        <div className="header">
          <div className="icon-wrapper">
            <span className="icon">🛡️</span>
          </div>
          <div>
            <h1>Email Spam Detector</h1>
            <p className="tagline">Stop spam before it stops you</p>
          </div>
        </div>

        <textarea
          placeholder="Paste email content (subject + body) here..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          rows={7}
        />

        <button onClick={handleAnalyse} disabled={loading}>
          {loading ? <span className="loader"></span> : "⚡ Analyse message"}
        </button>

        {error && <div className="error">{error}</div>}

        {result && (
          <div className={`result ${result.isSpam ? "spam" : "ham"}`}>
            <div className="result-badge">{result.isSpam ? "⚠️ SPAM" : "✅ LEGIT"}</div>
            <div className="result-message">{result.message}</div>
            <div className="result-details">
              <span>📊 Spam score: {result.score}</span>
              {result.keywords.length > 0 && (
                <span>🔍 Keywords: {result.keywords.join(", ")}</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SpamDetector;