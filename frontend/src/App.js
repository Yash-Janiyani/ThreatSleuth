import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ResultDisplay from './components/ResultDisplay';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalysisResult = (analysisResult) => {
    setResult(analysisResult);
    setLoading(false);
    setError(null);
  };

  const handleAnalysisStart = () => {
    setLoading(true);
    setResult(null);
    setError(null);
  };

  const handleAnalysisError = (errorMessage) => {
    setError(errorMessage);
    setLoading(false);
    setResult(null);
  };

  const resetAnalysis = () => {
    setResult(null);
    setError(null);
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <h1>🛡️ ThreatSleuth</h1>
          <p>AI-Powered Malware Detection</p>
        </div>
      </header>

      <main className="App-main">
        <div className="container">
          {!result && !loading && (
            <div className="upload-section">
              <h2>Upload a file for analysis</h2>
              <p className="subtitle">
                Supported formats: .exe, .dll, .zip, .txt, .bin (Max: 50MB)
              </p>
              <FileUpload
                onAnalysisStart={handleAnalysisStart}
                onAnalysisResult={handleAnalysisResult}
                onAnalysisError={handleAnalysisError}
              />
            </div>
          )}

          {loading && (
            <div className="loading-section">
              <div className="spinner"></div>
              <h2>Analyzing file...</h2>
              <p>This may take a few moments</p>
            </div>
          )}

          {error && (
            <div className="error-section">
              <div className="error-message">
                <h2>❌ Analysis Failed</h2>
                <p>{error}</p>
                <button onClick={resetAnalysis} className="retry-button">
                  Try Another File
                </button>
              </div>
            </div>
          )}

          {result && (
            <div className="result-section">
              <ResultDisplay result={result} />
              <button onClick={resetAnalysis} className="new-analysis-button">
                Analyze Another File
              </button>
            </div>
          )}
        </div>
      </main>

      <footer className="App-footer">
        <p>ThreatSleuth v1.0.0 - Educational purposes only</p>
      </footer>
    </div>
  );
}

export default App;