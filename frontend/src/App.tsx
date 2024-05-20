import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [summary, setSummary] = useState<string>('');
  const fileInput = useRef<HTMLInputElement>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const file = fileInput.current?.files?.[0];
    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:5000/summarize', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    setSummary(data.summary);
  };

  const handleDelete = () => {
    setSummary('');
  };

  return (
    <>
      <h1>Zusammenfassen</h1>
      <div>
        <form onSubmit={handleSubmit}>
          <input type='file' id='fileInput' ref={fileInput} />
          <button type='submit'>Summarize</button>
        </form>
        <div id='summary'>
          <h2>Summary</h2>
          <p id='summaryText'>{summary}</p>
        </div>
        <button id='deleteButton' onClick={handleDelete}>Delete Summary</button>
      </div>
    </>
  );
}

export default App;