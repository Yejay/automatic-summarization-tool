import React from 'react';

interface SummaryProps {
  summary: string;
  onDelete: () => void;
}

const Summary: React.FC<SummaryProps> = ({ summary, onDelete }) => {
  if (!summary) return null;

  return (
    <div style={{ marginTop: '20px', backgroundColor: '#333333', padding: '10px', borderRadius: '8px' }}>
      <h2>Summary</h2>
      <p>{summary}</p>
      <button onClick={onDelete} style={{ backgroundColor: '#960202', border: 'none', borderRadius: '5px' }}>
        Delete Summary
      </button>
    </div>
  );
};

export default Summary;