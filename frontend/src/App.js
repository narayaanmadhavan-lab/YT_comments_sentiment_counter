import React, { useState } from 'react';

function App() {
  const [url, setUrl] = useState('');
  const [sentiments, setSentiments] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeSentiment = async () => {
    if (!url) {
      alert("Please enter a YouTube URL.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        'http://127.0.0.1:8000/analyze?youtube_url=' + encodeURIComponent(url)
      );

      if (!response.ok) {
        throw new Error("Failed to analyze sentiment");
      }

      const data = await response.json();

      if (data.error) {
        alert("API Error: " + data.error);
        setLoading(false);
        return;
      }

      setSentiments({
        ...data,
        total: data.positive + data.neutral + data.negative,
      });
    } catch (error) {
      alert('Error: ' + error.message);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>YouTube Comment Sentiment Analyzer</h1>

      <input
        type="text"
        placeholder="Enter YouTube video URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: 400, padding: 8, marginBottom: 10 }}
      />
      <br />

      <button onClick={analyzeSentiment} style={{ padding: 10 }}>
        Analyze
      </button>

      {loading && <p>Loading...</p>}

      {sentiments && (
        <div style={{ marginTop: 30 }}>
          <h3>Results:</h3>
          <p><strong>Total Comments:</strong> {sentiments.total}</p>
          <p><strong>Positive:</strong> {sentiments.positive}</p>
          <p><strong>Neutral:</strong> {sentiments.neutral}</p>
          <p><strong>Negative:</strong> {sentiments.negative}</p>
        </div>
      )}
    </div>
  );
}

export default App;
