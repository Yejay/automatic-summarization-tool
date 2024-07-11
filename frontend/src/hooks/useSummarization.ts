import { useState } from 'react';
import { summarizeText } from '../services/api';

export const useSummarization = () => {
  const [summary, setSummary] = useState<string>('');
  const [model, setModel] = useState<string>('bart');
  const [loadingSummarize, setLoadingSummarize] = useState<boolean>(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelected = (file: File) => {
    setSelectedFile(file);
    setError(null);
  };

  const handleSummarize = async () => {
    if (!selectedFile) {
      setError('Please select a file first.');
      return;
    }
    setLoadingSummarize(true);
    setError(null);
    try {
      const result = await summarizeText(selectedFile, model);
      setSummary(result);
    } catch (error) {
      console.error('Error summarizing text:', error);
      setError('An error occurred while summarizing the text. Please try again.');
    } finally {
      setLoadingSummarize(false);
    }
  };

  const handleDelete = () => {
    setSummary('');
    setSelectedFile(null);
  };

  return { 
    summary, 
    model, 
    loadingSummarize, 
    selectedFile, 
    error,
    setModel, 
    handleFileSelected, 
    handleSummarize, 
    handleDelete 
  };
};