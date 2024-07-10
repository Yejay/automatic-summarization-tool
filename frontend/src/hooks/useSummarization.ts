import { useState } from 'react';
import { summarizeText } from '../services/api';

export const useSummarization = () => {
  const [summary, setSummary] = useState<string>('');
  const [model, setModel] = useState<string>('bart');
  const [loadingSummarize, setLoadingSummarize] = useState<boolean>(false);

  const handleSummarize = async (file: File) => {
    setLoadingSummarize(true);
    try {
      const result = await summarizeText(file, model);
      setSummary(result);
    } catch (error) {
      console.error('Error summarizing text:', error);
      // Handle error (e.g., show error message to user)
    } finally {
      setLoadingSummarize(false);
    }
  };

  const handleDelete = () => {
    setSummary('');
  };

  return { summary, model, loadingSummarize, setModel, handleSummarize, handleDelete };
};