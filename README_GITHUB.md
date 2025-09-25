# 🛡️ ThreatSleuth

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![React 18](https://img.shields.io/badge/react-18.2.0-blue.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/flask-3.1+-green.svg)](https://flask.palletsprojects.com/)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/ThreatSleuth)

**AI-Powered Malware Detection Tool - Educational Demonstration**

ThreatSleuth is a full-stack malware detection application that combines static file analysis with machine learning to identify potentially malicious files. This educational project demonstrates modern malware detection techniques using Flask for the backend API and React for the frontend interface.

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

## 🚀 Demo

**[Live Demo](https://your-vercel-app.vercel.app)** | **[API Docs](https://your-backend.railway.app)**

## 📊 Supported File Types
- **Executables**: `.exe`, `.dll`, `.bin`
- **Archives**: `.zip`
- **Text Files**: `.txt`
- **Maximum Size**: 50MB per file

## 🛠️ Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** (for cloning)

### Local Development

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ThreatSleuth.git
   cd ThreatSleuth
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   python model_trainer.py  # Train ML model
   python app.py           # Start backend
   ```

3. **Frontend Setup** (new terminal)
   ```bash
   cd frontend
   npm install
   npm start              # Start frontend
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 🌐 Deployment

This project is designed for easy deployment on modern platforms:

- **Frontend**: Vercel (recommended) or Netlify
- **Backend**: Railway, Render, or Heroku

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📁 Project Structure

```
ThreatSleuth/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── feature_extractor.py # File analysis engine
│   ├── model_trainer.py     # ML model training
│   ├── requirements.txt     # Python dependencies
│   ├── Procfile            # Deployment configuration
│   └── runtime.txt         # Python version
├── frontend/               # React web application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.js         # Main React component
│   │   └── index.js       # React entry point
│   ├── package.json       # Node.js dependencies
│   └── vercel.json        # Vercel deployment config
├── models/                # ML model storage
│   └── malware_detector.joblib  # Trained model (1.24MB)
├── DEPLOYMENT.md          # Deployment instructions
└── WARP.md               # Development guidelines
```

## 🔧 API Documentation

### Base URL
```
Local: http://localhost:5000
Production: https://your-backend.railway.app
```

### Endpoints

#### `GET /`
Health check endpoint
```json
{
  "status": "healthy",
  "service": "ThreatSleuth API",
  "version": "1.0.0",
  "model_loaded": true
}
```

#### `POST /api/predict`
Malware detection endpoint
```bash
curl -X POST -F "file=@sample.exe" http://localhost:5000/api/predict
```

**Response:**
```json
{
  "filename": "sample.exe",
  "prediction": "malicious",
  "confidence": 0.94,
  "explanation": "File classified as MALICIOUS based on...",
  "features": {
    "file_size": 2048576,
    "entropy": 7.85,
    "imports_count": 156
  }
}
```

## 🧠 Machine Learning Model

- **Algorithm**: Random Forest Classifier (100 trees)
- **Features**: File size, entropy, import count  
- **Training Data**: 5,000 synthetic samples
- **Accuracy**: ~98% on test set
- **Model Size**: 1.24 MB

### Feature Importance
1. **Entropy** (45.2%): Primary indicator of encryption/packing
2. **Import Count** (41.3%): Function complexity indicator  
3. **File Size** (13.5%): Supporting feature

## ⚠️ Important Disclaimers

### Educational Purpose Only
This project is designed for **educational and demonstration purposes**. It should **NOT** be used for:
- Production security decisions
- Real malware detection in enterprise environments
- Critical security assessments

### Limitations
- **Synthetic Training Data**: Not trained on real malware samples
- **Limited Features**: Only basic static analysis
- **No Dynamic Analysis**: Does not execute or monitor file behavior
- **No Signature Detection**: Does not use malware signatures or hashes

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