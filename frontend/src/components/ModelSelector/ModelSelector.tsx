import React from 'react';
import { MODELS } from '../../constants';

interface ModelSelectorProps {
  selectedModel: string;
  onModelChange: (model: string) => void;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ selectedModel, onModelChange }) => {
  return (
    <div>
      <h2>Please select a model</h2>
      <div style={{ display: 'flex', justifyContent: 'space-between', margin: '10px 0' }}>
        {Object.entries(MODELS).map(([key, value]) => (
          <button
            key={key}
            onClick={() => onModelChange(value)}
            style={{ flex: 1, margin: '0 25px', backgroundColor: selectedModel === value ? '#646cffaa' : '#333333' }}
          >
            {key}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ModelSelector;