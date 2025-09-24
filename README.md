# 🛡️ ThreatSleuth

**AI-Powered Malware Detection Tool - Minimum Viable Product**

ThreatSleuth is a full-stack malware detection application that combines static file analysis with machine learning to identify potentially malicious files. This MVP demonstrates the core functionality of modern malware detection systems using Flask for the backend API and React for the frontend interface.

![ThreatSleuth Demo](https://img.shields.io/badge/Status-MVP%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![React](https://img.shields.io/badge/React-18.2.0-blue)
![License](https://img.shields.io/badge/License-Educational-yellow)

## ✨ Features

### 🔍 **Static Analysis Engine**
- **File Size Analysis**: Examines file size patterns typical of malware
- **Entropy Calculation**: Detects encryption/packing using Shannon entropy
- **PE Import Analysis**: Counts imported functions in executable files
- **Archive Inspection**: Analyzes ZIP files for suspicious content

### 🤖 **Machine Learning Detection**
- **Random Forest Classifier**: Trained on synthetic data mimicking EMBER dataset
- **Feature Engineering**: Combines multiple static features for robust detection
- **Confidence Scoring**: Provides prediction confidence levels
- **Fallback Analysis**: Heuristic-based detection when ML model unavailable

### 🖥️ **Modern Web Interface**
- **Drag & Drop Upload**: Intuitive file upload with progress indicators
- **Real-time Analysis**: Instant feedback during file processing
- **Color-coded Results**: Visual distinction between benign/malicious classifications
- **Detailed Explanations**: Human-readable analysis explanations
- **Responsive Design**: Works on desktop and mobile devices

### 📊 **Supported File Types**
- **Executables**: `.exe`, `.dll`, `.bin`
- **Archives**: `.zip`
- **Text Files**: `.txt`
- **Maximum Size**: 50MB per file

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** (for cloning)

### Installation

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd ThreatSleuth
   ```

2. **Backend Setup**
   ```bash
   cd backend
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Train the ML model (first time only)
   python model_trainer.py
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   
   # Install dependencies
   npm install
   ```

### Running the Application

1. **Start the Backend API**
   ```bash
   cd backend
   # Ensure virtual environment is activated
   python app.py
   ```
   Backend will run on `http://localhost:5000`

2. **Start the Frontend** (in a new terminal)
   ```bash
   cd frontend
   npm start
   ```
   Frontend will run on `http://localhost:3000`

3. **Access ThreatSleuth**
   - Open your browser to `http://localhost:3000`
   - Upload a file for analysis
   - View the detailed results!

## 📁 Project Structure

```
ThreatSleuth/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── feature_extractor.py # File analysis engine
│   ├── model_trainer.py     # ML model training
│   ├── requirements.txt     # Python dependencies
│   └── uploads/            # Temporary file storage
├── frontend/               # React web application
│   ├── public/            # Static assets
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── FileUpload.js     # File upload interface
│   │   │   ├── FileUpload.css
│   │   │   ├── ResultDisplay.js  # Results visualization
│   │   │   └── ResultDisplay.css
│   │   ├── App.js         # Main React component
│   │   ├── App.css        # Global styles
│   │   └── index.js       # React entry point
│   └── package.json       # Node.js dependencies
├── models/                # ML model storage
│   └── malware_detector.joblib  # Trained model file
├── data/                  # Training data (empty in MVP)
├── docs/                  # Documentation
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### `GET /`
**Health Check**
- Returns API status and model availability
- Response: `200 OK`
```json
{
  "status": "healthy",
  "service": "ThreatSleuth API",
  "version": "1.0.0",
  "model_loaded": true
}
```

#### `POST /api/predict`
**Malware Detection**
- Upload a file for analysis
- Content-Type: `multipart/form-data`
- Max file size: 50MB

**Request:**
```bash
curl -X POST -F "file=@sample.exe" http://localhost:5000/api/predict
```

**Response:** `200 OK`
```json
{
  "filename": "sample.exe",
  "prediction": "malicious",
  "confidence": 0.94,
  "explanation": "File classified as MALICIOUS based on: • Very high entropy (7.85) suggests encryption or packing • Large number of imports (156) may indicate complex functionality • Confidence: 94.0%",
  "features": {
    "file_size": 2048576,
    "entropy": 7.85,
    "imports_count": 156
  }
}
```

#### `GET /api/stats`
**API Statistics**
- Returns supported file types and configuration
- Response: `200 OK`
```json
{
  "allowed_extensions": ["exe", "zip", "txt", "bin", "dll"],
  "max_file_size_mb": 50,
  "model_status": "loaded"
}
```

## 🧠 Machine Learning Model

### Architecture
- **Algorithm**: Random Forest Classifier
- **Features**: File size, entropy, import count
- **Training Data**: 5,000 synthetic samples
- **Accuracy**: ~89.6% on test set

### Feature Importance
1. **Import Count** (43.7%): Most significant predictor
2. **Entropy** (35.3%): Second most important
3. **File Size** (20.9%): Supporting feature

### Model Training
The model is automatically trained on first run, but you can retrain:

```bash
cd backend
python model_trainer.py
```

## 🎯 Demo Usage

### Testing with Sample Files

1. **Create a test text file**:
   ```bash
   echo "This is a benign test file" > test.txt
   ```

2. **Upload through the web interface**:
   - Drag and drop `test.txt` onto the upload area
   - Wait for analysis (usually < 5 seconds)
   - View the detailed results

3. **Expected Result**: 
   - Classification: **BENIGN**
   - Confidence: ~85-95%
   - Low entropy, small size, no imports

### Example Analysis Results

**Benign File (test.txt)**:
- ✅ **BENIGN** with 89% confidence
- Features: 25 bytes, entropy 2.1, 0 imports
- Explanation: Normal entropy level, small file size

**Suspicious File (large, high entropy)**:
- 🚨 **MALICIOUS** with 97% confidence  
- Features: 5MB, entropy 7.8, 150 imports
- Explanation: High entropy suggests packing, many imports

## ⚠️ Important Disclaimers

### Educational Purpose Only
This MVP is designed for **educational and demonstration purposes**. It should **NOT** be used for:
- Production security decisions
- Real malware detection in enterprise environments
- Critical security assessments

### Limitations
- **Synthetic Training Data**: Model trained on generated data, not real malware
- **Limited Features**: Only basic static analysis (file size, entropy, imports)
- **False Positives/Negatives**: Expected due to simplified feature set
- **No Dynamic Analysis**: Does not execute or monitor file behavior
- **No Signature Detection**: Does not use malware signatures or hashes

### Security Considerations
- Files are temporarily stored on server during analysis
- Uploaded files are automatically deleted after processing
- Run in isolated environment when testing with real malware samples

## 🔮 Future Enhancements

### Planned Features
- [ ] **Dynamic Analysis**: Sandbox execution and behavior monitoring
- [ ] **YARA Rules Integration**: Signature-based detection
- [ ] **Multi-model Ensemble**: Combine multiple ML approaches
- [ ] **Real EMBER Dataset**: Train on actual malware dataset
- [ ] **API Authentication**: Secure API access with JWT tokens
- [ ] **Batch Processing**: Upload and analyze multiple files
- [ ] **Historical Analytics**: Track detection statistics over time
- [ ] **Export Reports**: PDF/JSON report generation

### Technical Improvements
- [ ] **Database Integration**: PostgreSQL for persistence
- [ ] **Async Processing**: Background job queue for large files
- [ ] **Caching Layer**: Redis for improved performance
- [ ] **Docker Deployment**: Containerized deployment
- [ ] **Cloud Integration**: AWS/Azure deployment options

## 🛠️ Development

### Code Quality
```bash
# Format Python code
black backend/

# Format JavaScript code
cd frontend && npm run format

# Run tests (when available)
pytest backend/
cd frontend && npm test
```

### Environment Variables
Create `.env` file in backend directory:
```env
FLASK_ENV=development
FLASK_DEBUG=True
MAX_CONTENT_LENGTH=52428800
UPLOAD_FOLDER=uploads
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **EMBER Dataset**: Inspiration for feature engineering approach
- **Flask Community**: Excellent web framework for Python APIs
- **React Team**: Amazing frontend library for modern UIs
- **Scikit-learn**: Robust machine learning library

---

**Built with ❤️ for cybersecurity education**

For questions or support, please open an issue on GitHub.