import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings

warnings.filterwarnings('ignore')

class MalwareModelTrainer:
    """Train and manage malware detection models"""
    
    def __init__(self, model_path='../models/malware_detector.joblib'):
        self.model_path = model_path
        self.model = None
        self.feature_names = ['file_size', 'entropy', 'imports_count']
    
    def generate_synthetic_data(self, n_samples=1000):
        """
        Generate synthetic training data that mimics EMBER dataset structure
        In a real scenario, this would load actual EMBER data
        """
        np.random.seed(42)
        
        # Generate features for benign files
        benign_samples = n_samples // 2
        benign_file_sizes = np.random.lognormal(mean=10, sigma=2, size=benign_samples)  # Smaller files
        benign_entropy = np.random.normal(loc=5.5, scale=1.5, size=benign_samples)  # Lower entropy
        benign_imports = np.random.poisson(lam=25, size=benign_samples)  # Reasonable imports
        
        # Clip values to reasonable ranges
        benign_entropy = np.clip(benign_entropy, 0, 8)
        benign_imports = np.clip(benign_imports, 0, 200)
        benign_file_sizes = np.clip(benign_file_sizes, 1024, 50_000_000)
        
        # Generate features for malicious files
        malicious_samples = n_samples - benign_samples
        malicious_file_sizes = np.random.lognormal(mean=12, sigma=2, size=malicious_samples)  # Larger files
        malicious_entropy = np.random.normal(loc=7.2, scale=1.0, size=malicious_samples)  # Higher entropy
        malicious_imports = np.concatenate([
            np.random.poisson(lam=5, size=malicious_samples//3),  # Some with very few imports (packed)
            np.random.poisson(lam=80, size=malicious_samples//3),  # Some with many imports
            np.random.poisson(lam=30, size=malicious_samples - 2*(malicious_samples//3))  # Normal range
        ])
        
        # Clip values to reasonable ranges
        malicious_entropy = np.clip(malicious_entropy, 0, 8)
        malicious_imports = np.clip(malicious_imports, 0, 500)
        malicious_file_sizes = np.clip(malicious_file_sizes, 1024, 100_000_000)
        
        # Combine features
        X = np.vstack([
            np.column_stack([benign_file_sizes, benign_entropy, benign_imports]),
            np.column_stack([malicious_file_sizes, malicious_entropy, malicious_imports])
        ])
        
        # Create labels (0 = benign, 1 = malicious)
        y = np.concatenate([
            np.zeros(benign_samples),
            np.ones(malicious_samples)
        ])
        
        return X, y
    
    def train_model(self, X=None, y=None):
        """Train the malware detection model"""
        if X is None or y is None:
            print("Generating synthetic training data...")
            X, y = self.generate_synthetic_data(n_samples=5000)
        
        print(f"Training on {len(X)} samples...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train Random Forest model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model trained successfully!")
        print(f"Accuracy: {accuracy:.3f}")
        print(f"Feature importance: {dict(zip(self.feature_names, self.model.feature_importances_))}")
        
        return self.model
    
    def save_model(self):
        """Save the trained model to disk"""
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Save model and metadata
        model_data = {
            'model': self.model,
            'feature_names': self.feature_names,
            'model_type': 'RandomForest'
        }
        
        joblib.dump(model_data, self.model_path)
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load a trained model from disk"""
        if not os.path.exists(self.model_path):
            return None
            
        try:
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.feature_names = model_data['feature_names']
            print(f"Model loaded from {self.model_path}")
            return self.model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

def load_model(model_path='../models/malware_detector.joblib'):
    """Utility function to load model for the Flask app"""
    try:
        if not os.path.exists(model_path):
            # Try different possible paths
            possible_paths = [
                'models/malware_detector.joblib',
                '../models/malware_detector.joblib',
                'backend/models/malware_detector.joblib'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            else:
                return None
        
        model_data = joblib.load(model_path)
        return model_data['model']
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def train_and_save_model():
    """Train and save a new model"""
    trainer = MalwareModelTrainer()
    trainer.train_model()
    trainer.save_model()
    return trainer.model

if __name__ == "__main__":
    print("Training ThreatSleuth malware detection model...")
    
    # Train and save the model
    model = train_and_save_model()
    
    # Test the model with some sample data
    print("\nTesting model with sample data:")
    
    test_samples = [
        [50000, 4.2, 15],      # Small, low entropy, few imports -> likely benign
        [5000000, 7.8, 150],   # Large, high entropy, many imports -> likely malicious
        [1000000, 7.9, 2],     # Medium size, high entropy, very few imports -> likely malicious (packed)
        [100000, 5.1, 35]      # Medium size, normal entropy, normal imports -> likely benign
    ]
    
    predictions = model.predict(test_samples)
    probabilities = model.predict_proba(test_samples)
    
    for i, (sample, pred, prob) in enumerate(zip(test_samples, predictions, probabilities)):
        result = "Malicious" if pred == 1 else "Benign"
        confidence = max(prob)
        print(f"Sample {i+1}: {sample} -> {result} (confidence: {confidence:.3f})")
    
    print("\nModel training complete!")