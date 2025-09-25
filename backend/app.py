import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import joblib
import numpy as np
from feature_extractor import FeatureExtractor
from model_trainer import load_model

app = Flask(__name__)
# Configure CORS for production
CORS(app, origins=[
    "http://localhost:3000",  # Local development
    "https://*.vercel.app",   # Vercel deployments
    "https://your-frontend-domain.vercel.app"  # Replace with your actual domain
])

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'exe', 'zip', 'txt', 'bin', 'dll'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the trained model on startup
model = None
try:
    model = load_model()
    print("Model loaded successfully!")
except Exception as e:
    print(f"Warning: Could not load model - {e}")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ThreatSleuth API',
        'version': '1.0.0',
        'model_loaded': model is not None
    })

@app.route('/api/predict', methods=['POST'])
def predict_malware():
    """Main prediction endpoint for malware detection"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        try:
            # Extract features
            extractor = FeatureExtractor()
            features = extractor.extract_features(temp_path)
            
            if model is None:
                # Fallback prediction based on simple heuristics
                prediction, confidence = fallback_prediction(features)
            else:
                # Use trained model
                features_array = np.array(features).reshape(1, -1)
                prediction_proba = model.predict_proba(features_array)[0]
                prediction = model.predict(features_array)[0]
                confidence = max(prediction_proba)
            
            # Generate explanation
            explanation = generate_explanation(features, prediction, confidence)
            
            # Clean up temporary file
            os.remove(temp_path)
            
            return jsonify({
                'filename': filename,
                'prediction': 'malicious' if prediction == 1 else 'benign',
                'confidence': float(confidence),
                'explanation': explanation,
                'features': {
                    'file_size': features[0],
                    'entropy': features[1],
                    'imports_count': features[2]
                }
            })
            
        except Exception as e:
            # Clean up temporary file on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def fallback_prediction(features):
    """Simple heuristic-based prediction when model is not available"""
    file_size, entropy, imports_count = features
    
    # Simple scoring based on suspicious characteristics
    score = 0
    
    # Small files with very low entropy are likely benign text files
    if file_size < 10000 and entropy < 4.0:
        score -= 0.4  # Strong benign signal
    
    # Large files are slightly more suspicious
    if file_size > 5 * 1024 * 1024:  # > 5MB
        score += 0.15
    
    # High entropy suggests encryption/packing (suspicious)
    if entropy > 7.5:
        score += 0.5
    elif entropy > 7.0:
        score += 0.3
    elif entropy > 6.0:
        score += 0.1
    
    # Very low entropy indicates simple/text files (benign)
    if entropy < 3.0:
        score -= 0.3
    elif entropy < 4.0:
        score -= 0.15
    
    # Import analysis
    if imports_count > 100:
        score += 0.3  # Many imports can be suspicious
    elif imports_count == 0 and file_size > 10000:
        score += 0.2  # No imports in large files (possibly packed)
    elif imports_count == 0 and file_size < 10000:
        score -= 0.1  # No imports in small files is normal (text files)
    
    # Convert to binary prediction with more conservative threshold
    prediction = 1 if score > 0.2 else 0
    confidence = min(max(abs(score) + 0.5, 0.5), 0.95)
    
    return prediction, confidence

def generate_explanation(features, prediction, confidence):
    """Generate human-readable explanation for the prediction"""
    file_size, entropy, imports_count = features
    
    explanations = []
    
    if prediction == 1:  # Malicious
        explanations.append("File classified as MALICIOUS based on:")
        
        if entropy > 7.5:
            explanations.append(f"• Very high entropy ({entropy:.2f}) suggests encryption or packing")
        elif entropy > 7.0:
            explanations.append(f"• High entropy ({entropy:.2f}) indicates potential obfuscation")
        
        if imports_count > 100:
            explanations.append(f"• Large number of imports ({imports_count}) may indicate complex functionality")
        elif imports_count == 0:
            explanations.append("• No imports detected - could be packed or obfuscated")
        
        if file_size > 5 * 1024 * 1024:
            explanations.append(f"• Large file size ({file_size / 1024 / 1024:.1f} MB)")
    
    else:  # Benign
        explanations.append("File classified as BENIGN based on:")
        
        if entropy < 6.0:
            explanations.append(f"• Normal entropy level ({entropy:.2f})")
        
        if 1 <= imports_count <= 50:
            explanations.append(f"• Reasonable number of imports ({imports_count})")
        
        if file_size < 1024 * 1024:
            explanations.append(f"• Small file size ({file_size} bytes)")
    
    explanations.append(f"• Confidence: {confidence:.1%}")
    
    return " ".join(explanations)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get API statistics"""
    return jsonify({
        'allowed_extensions': list(ALLOWED_EXTENSIONS),
        'max_file_size_mb': MAX_CONTENT_LENGTH // (1024 * 1024),
        'model_status': 'loaded' if model else 'fallback_mode'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)
