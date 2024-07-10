import React from 'react';

export const formatScores = (scores: number[] | undefined): React.ReactNode => {
  if (!scores || scores.length !== 3) {
    console.error('Scores array is undefined, null, or has incorrect length:', scores);
    return <div>Unavailable</div>;
  }

  return (
    <div>
      <div>Precision: {scores[0].toFixed(3)}</div>
      <div>Recall: {scores[1].toFixed(3)}</div>
      <div>F1: {scores[2].toFixed(3)}</div>
    </div>
  );
};