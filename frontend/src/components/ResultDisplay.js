import React from 'react';
import './ResultDisplay.css';

const ResultDisplay = ({ result }) => {
  if (!result) return null;

  const { filename, prediction, confidence, explanation, features } = result;
  const isMalicious = prediction === 'malicious';
  
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#28a745'; // High confidence - green
    if (confidence >= 0.6) return '#ffc107'; // Medium confidence - yellow
    return '#dc3545'; // Low confidence - red
  };

  return (
    <div className="result-display">
      <div className="result-header">
        <div className={`result-status ${isMalicious ? 'malicious' : 'benign'}`}>
          <div className="status-icon">
            {isMalicious ? '🚨' : '✅'}
          </div>
          <div className="status-text">
            <h2>{isMalicious ? 'MALICIOUS' : 'BENIGN'}</h2>
            <p className="filename">{filename}</p>
          </div>
        </div>
        
        <div className="confidence-badge">
          <div 
            className="confidence-circle"
            style={{ 
              background: `conic-gradient(${getConfidenceColor(confidence)} ${confidence * 360}deg, #e9ecef 0deg)` 
            }}
          >
            <div className="confidence-inner">
              {Math.round(confidence * 100)}%
            </div>
          </div>
          <span className="confidence-label">Confidence</span>
        </div>
      </div>

      <div className="result-details">
        <div className="explanation-section">
          <h3>Analysis Explanation</h3>
          <div className="explanation-text">
            {explanation}
          </div>
        </div>

        <div className="features-section">
          <h3>File Characteristics</h3>
          <div className="features-grid">
            <div className="feature-item">
              <div className="feature-label">File Size</div>
              <div className="feature-value">{formatFileSize(features.file_size)}</div>
            </div>
            
            <div className="feature-item">
              <div className="feature-label">Entropy</div>
              <div className="feature-value">
                {features.entropy.toFixed(2)}
                <div className="entropy-bar">
                  <div 
                    className="entropy-fill" 
                    style={{ width: `${(features.entropy / 8) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
            
            <div className="feature-item">
              <div className="feature-label">Import Count</div>
              <div className="feature-value">{features.imports_count}</div>
            </div>
          </div>
        </div>

        <div className="risk-assessment">
          <h3>Risk Assessment</h3>
          <div className={`risk-level ${isMalicious ? 'high-risk' : 'low-risk'}`}>
            <div className="risk-indicator">
              <span className="risk-icon">{isMalicious ? '⚠️' : '🛡️'}</span>
              <span className="risk-text">
                {isMalicious ? 'HIGH RISK' : 'LOW RISK'}
              </span>
            </div>
            <div className="risk-description">
              {isMalicious 
                ? 'This file shows characteristics commonly associated with malicious software. Exercise caution.'
                : 'This file appears to be safe based on the analyzed characteristics.'
              }
            </div>
          </div>
        </div>

        <div className="technical-info">
          <h3>Technical Details</h3>
          <div className="tech-grid">
            <div className="tech-item">
              <span className="tech-label">Analysis Method:</span>
              <span className="tech-value">Static Feature Analysis + ML</span>
            </div>
            <div className="tech-item">
              <span className="tech-label">Model:</span>
              <span className="tech-value">Random Forest Classifier</span>
            </div>
            <div className="tech-item">
              <span className="tech-label">Features Used:</span>
              <span className="tech-value">File Size, Entropy, Import Count</span>
            </div>
          </div>
        </div>
      </div>

      <div className="disclaimer">
        <p>⚠️ <strong>Disclaimer:</strong> This analysis is for educational purposes only. Results should not be considered definitive for production security decisions.</p>
      </div>
    </div>
  );
};

export default ResultDisplay;