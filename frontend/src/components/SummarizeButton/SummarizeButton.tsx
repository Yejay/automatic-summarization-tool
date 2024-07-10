import React from 'react';

interface SummarizeButtonProps {
  onSummarize: () => void;
  isLoading: boolean;
  isDisabled: boolean;
}

const SummarizeButton: React.FC<SummarizeButtonProps> = ({ onSummarize, isLoading, isDisabled }) => {
  return (
    <button 
      onClick={onSummarize} 
      style={{ width: '25%', padding: '10px', backgroundColor: '#646cffaa', border: 'none', borderRadius: '5px' }}
      disabled={isDisabled || isLoading}
    >
      {isLoading ? 'Summarizing...' : 'Summarize'}
    </button>
  );
};

export default SummarizeButton;