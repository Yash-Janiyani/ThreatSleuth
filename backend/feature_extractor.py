import os
import math
import zipfile
import struct
from collections import Counter
try:
    import pefile
    PE_AVAILABLE = True
except ImportError:
    PE_AVAILABLE = False

class FeatureExtractor:
    """Extract static features from uploaded files for malware detection"""
    
    def __init__(self):
        pass
    
    def extract_features(self, file_path):
        """
        Extract features from a file
        Returns: [file_size, entropy, imports_count]
        """
        try:
            # Basic file features
            file_size = os.path.getsize(file_path)
            entropy = self.calculate_entropy(file_path)
            
            # File type specific features
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in ['.exe', '.dll', '.bin']:
                imports_count = self.extract_pe_imports_count(file_path)
            elif file_ext == '.zip':
                imports_count = self.extract_zip_features(file_path)
            else:
                imports_count = 0  # For txt and other files
            
            return [file_size, entropy, imports_count]
            
        except Exception as e:
            print(f"Error extracting features from {file_path}: {e}")
            # Return default safe values on error
            return [0, 0, 0]
    
    def calculate_entropy(self, file_path):
        """Calculate Shannon entropy of a file"""
        try:
            with open(file_path, 'rb') as f:
                # Read file in chunks to handle large files
                byte_counts = Counter()
                chunk_size = 8192
                total_bytes = 0
                
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    byte_counts.update(chunk)
                    total_bytes += len(chunk)
                
                if total_bytes == 0:
                    return 0
                
                # Calculate entropy
                entropy = 0
                for count in byte_counts.values():
                    probability = count / total_bytes
                    if probability > 0:
                        entropy -= probability * math.log2(probability)
                
                return entropy
                
        except Exception as e:
            print(f"Error calculating entropy: {e}")
            return 0
    
    def extract_pe_imports_count(self, file_path):
        """Extract import count from PE files (exe, dll)"""
        if not PE_AVAILABLE:
            return 0
            
        try:
            pe = pefile.PE(file_path)
            imports_count = 0
            
            # Count imported functions
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    if hasattr(entry, 'imports'):
                        imports_count += len(entry.imports)
            
            pe.close()
            return imports_count
            
        except Exception as e:
            print(f"Error extracting PE imports: {e}")
            return 0
    
    def extract_zip_features(self, file_path):
        """Extract features from ZIP files"""
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                # Count number of files in archive
                file_count = len(zip_file.namelist())
                
                # Check for suspicious file extensions
                suspicious_extensions = ['.exe', '.dll', '.bat', '.cmd', '.scr', '.vbs', '.js']
                suspicious_count = 0
                
                for filename in zip_file.namelist():
                    file_ext = os.path.splitext(filename)[1].lower()
                    if file_ext in suspicious_extensions:
                        suspicious_count += 1
                
                # Return composite score: file_count + suspicious_files * 10
                return file_count + (suspicious_count * 10)
                
        except Exception as e:
            print(f"Error extracting ZIP features: {e}")
            return 0
    
    def extract_string_features(self, file_path):
        """Extract string-based features (for future enhancement)"""
        try:
            suspicious_strings = [
                b'CreateProcess', b'WriteProcessMemory', b'VirtualAlloc',
                b'GetProcAddress', b'LoadLibrary', b'RegOpenKey',
                b'InternetOpen', b'HttpSendRequest'
            ]
            
            string_count = 0
            with open(file_path, 'rb') as f:
                content = f.read()
                for sus_str in suspicious_strings:
                    string_count += content.count(sus_str)
            
            return string_count
            
        except Exception as e:
            print(f"Error extracting string features: {e}")
            return 0