import React, { useState, useRef } from 'react';

interface FileUploadProps {
  onFileSelected: (file: File) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileSelected }) => {
  const [dragActive, setDragActive] = useState<boolean>(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file: File) => {
    setFileName(file.name);
    onFileSelected(file);
  };

  const handleFileInputClick = () => {
    fileInput.current?.click();
  };

  return (
    <div
      className={`file-upload ${dragActive ? 'drag-active' : ''}`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      onClick={handleFileInputClick}
    >
      <input
        type="file"
        ref={fileInput}
        onChange={handleFileInputChange}
        style={{ display: 'none' }}
      />
      {fileName ? <p>{fileName}</p> : <p>Drag & Drop your file here or click to upload</p>}
    </div>
  );
};

export default FileUpload;