# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Development Commands

### Backend Setup and Development
```bash
# Initial setup (run once)
cd backend
python -m venv venv

# Windows activation
venv\Scripts\activate
# Linux/macOS activation  
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train ML model (required on first run)
python model_trainer.py

# Start development server
python app.py
```

### Frontend Setup and Development
```bash
cd frontend

# Install dependencies
npm install

# Start development server (runs on http://localhost:3000)
npm start

# Build for production
npm run build

# Run tests (when available)
npm test
```

### Full Application Startup
```bash
# Terminal 1 - Backend (from project root)
cd backend && python app.py

# Terminal 2 - Frontend (from project root) 
cd frontend && npm start
```

### Model Management
```bash
# Retrain the ML model
cd backend
python model_trainer.py

# The model will be saved to ../models/malware_detector.joblib
```

## Architecture Overview

ThreatSleuth is a full-stack malware detection application with clean separation between frontend, backend, and ML components.

### High-Level Architecture
- **Frontend**: React SPA with drag-and-drop file upload
- **Backend**: Flask REST API with file processing and ML inference  
- **ML Pipeline**: Feature extraction → Random Forest classification
- **Data Flow**: File upload → Feature extraction → ML prediction → Results display

### Core Components

#### Backend (`backend/`)
- **`app.py`**: Main Flask application with API endpoints
  - `/api/predict`: Primary malware detection endpoint
  - `/`: Health check with model status
  - `/api/stats`: Configuration and supported file types
- **`feature_extractor.py`**: Static file analysis engine
  - Shannon entropy calculation
  - PE import counting (for .exe/.dll files)
  - ZIP archive analysis
  - File size analysis
- **`model_trainer.py`**: ML model training and management
  - Random Forest classifier with synthetic data
  - Model persistence with joblib
  - Feature importance analysis

#### Frontend (`frontend/src/`)
- **`App.js`**: Main React component managing application state
- **`components/FileUpload.js`**: Drag-and-drop interface using react-dropzone
- **`components/ResultDisplay.js`**: Analysis results visualization
- **Axios integration**: HTTP client for API communication with proxy configuration

#### ML Model Architecture
- **Algorithm**: Random Forest Classifier (100 trees, max_depth=10)
- **Features**: [file_size, entropy, imports_count] 
- **Training**: Synthetic data (5000 samples) mimicking EMBER dataset patterns
- **Feature Importance**: Import count (43.7%), Entropy (35.3%), File size (20.9%)
- **Fallback Logic**: Heuristic-based classification when model unavailable

### File Processing Pipeline
1. **Upload Validation**: File type and size checks (50MB limit)
2. **Temporary Storage**: Secure filename handling in `uploads/` directory
3. **Feature Extraction**: File-type specific analysis (PE, ZIP, generic)
4. **ML Inference**: Random Forest prediction with confidence scoring
5. **Result Generation**: Human-readable explanations based on features
6. **Cleanup**: Automatic temporary file deletion

### API Design Patterns
- RESTful endpoints with consistent JSON responses
- Multipart form-data for file uploads
- Error handling with appropriate HTTP status codes
- CORS enabled for frontend-backend communication
- Timeout handling (60s) for large file processing

## Development Guidelines

### File Type Support
- **Executables**: `.exe`, `.dll`, `.bin` (PE analysis with pefile library)
- **Archives**: `.zip` (content analysis and suspicious file detection)
- **Text Files**: `.txt` (entropy and size analysis only)
- **Size Limit**: 50MB per file

### Environment Configuration
Create `.env` file in `backend/` directory for configuration:
```env
FLASK_ENV=development
FLASK_DEBUG=True
MAX_CONTENT_LENGTH=52428800
UPLOAD_FOLDER=uploads
```

### Model Training Data
The current model uses synthetic data for educational purposes. Key characteristics:
- **Benign files**: Lower entropy (5.5±1.5), smaller size, moderate imports (25±5)
- **Malicious files**: Higher entropy (7.2±1.0), larger size, varied imports (5-80)
- Training generates realistic feature distributions for demonstration

### Error Handling Patterns
- **Frontend**: User-friendly error messages with retry options
- **Backend**: Detailed logging with safe error responses
- **File Processing**: Graceful fallback on feature extraction failures
- **Model Loading**: Automatic fallback to heuristic classification

### Security Considerations
- Files are stored temporarily and automatically deleted after analysis
- Secure filename handling prevents path traversal attacks
- No execution or dynamic analysis of uploaded files
- Educational disclaimer prominently displayed

## Technical Debt and Limitations

### Current Limitations
- **Synthetic Training Data**: Not trained on real malware samples
- **Limited Feature Set**: Only basic static analysis features
- **No Persistence**: No database for analysis history
- **No Authentication**: Open API without user management
- **Single File Processing**: No batch analysis capability

### Known Issues
- PE analysis depends on `pefile` library availability
- Model path resolution uses multiple fallback locations
- No comprehensive test coverage
- Windows path separators in some file operations