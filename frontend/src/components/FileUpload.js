import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './FileUpload.css';

const FileUpload = ({ onAnalysisStart, onAnalysisResult, onAnalysisError }) => {
  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    
    // Check file size (50MB limit)
    if (file.size > 50 * 1024 * 1024) {
      onAnalysisError('File size exceeds 50MB limit');
      return;
    }

    // Check file type
    const allowedTypes = ['.exe', '.zip', '.txt', '.bin', '.dll'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
      onAnalysisError('Unsupported file type. Please upload .exe, .zip, .txt, .bin, or .dll files');
      return;
    }

    onAnalysisStart();

    const formData = new FormData();
    formData.append('file', file);

    try {
      const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
      const response = await axios.post(`${API_URL}/api/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000, // 60 second timeout
      });

      onAnalysisResult(response.data);
    } catch (error) {
      if (error.response) {
        onAnalysisError(error.response.data.error || 'Server error occurred');
      } else if (error.request) {
        onAnalysisError('Unable to connect to server. Please ensure the backend is running.');
      } else {
        onAnalysisError('An unexpected error occurred');
      }
    }
  }, [onAnalysisStart, onAnalysisResult, onAnalysisError]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/octet-stream': ['.exe', '.dll', '.bin'],
      'application/zip': ['.zip'],
      'text/plain': ['.txt'],
    },
    multiple: false,
    maxSize: 50 * 1024 * 1024, // 50MB
  });

  return (
    <div className="file-upload-container">
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'drag-active' : ''} ${isDragReject ? 'drag-reject' : ''}`}
      >
        <input {...getInputProps()} />
        
        <div className="upload-icon">
          📁
        </div>
        
        {isDragActive ? (
          isDragReject ? (
            <div className="upload-text">
              <h3>❌ File type not supported</h3>
              <p>Please upload .exe, .zip, .txt, .bin, or .dll files</p>
            </div>
          ) : (
            <div className="upload-text">
              <h3>📤 Drop the file here</h3>
              <p>Release to start analysis</p>
            </div>
          )
        ) : (
          <div className="upload-text">
            <h3>Drag & drop a file here</h3>
            <p>or <span className="click-text">click to browse</span></p>
            <div className="file-info">
              <small>Supported: .exe, .zip, .txt, .bin, .dll (max 50MB)</small>
            </div>
          </div>
        )}
      </div>
      
      <div className="upload-features">
        <div className="feature">
          <span className="feature-icon">🔍</span>
          <span>Static Analysis</span>
        </div>
        <div className="feature">
          <span className="feature-icon">🤖</span>
          <span>AI Detection</span>
        </div>
        <div className="feature">
          <span className="feature-icon">⚡</span>
          <span>Fast Results</span>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;