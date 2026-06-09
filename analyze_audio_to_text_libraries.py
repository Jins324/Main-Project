#!/usr/bin/env python
"""
Audio-to-Text Library Analysis and Upgrade
Analyzes current implementation and upgrades with best libraries
"""

import os
import sys
import subprocess
import importlib

class AudioToTextAnalyzer:
    def __init__(self):
        self.current_libraries = {
            'speech_recognition': 'sr',
            'whisper': 'OpenAI Whisper',
            'gtts': 'Google Text-to-Speech',
            'pydub': 'Audio Processing',
            'librosa': 'Audio Analysis (optional)',
            'Levenshtein': 'Text Comparison (optional)'
        }
        
        self.best_libraries = {
            'speech_recognition': {
                'primary': 'OpenAI Whisper (large-v3)',
                'secondary': 'Google Speech Recognition v2',
                'tertiary': 'Vosk (offline)',
                'backup': 'CMU Sphinx'
            },
            'malayalam_specific': {
                'primary': 'Whisper multilingual (ml)',
                'secondary': 'Google Speech (ml-IN)',
                'tertiary': 'Coqui TTS (custom model)',
                'fallback': 'Vosk with Malayalam model'
            },
            'audio_processing': {
                'primary': 'librosa',
                'secondary': 'pydub',
                'tertiary': 'soundfile'
            },
            'scoring': {
                'primary': 'WER (Word Error Rate)',
                'secondary': 'Levenshtein distance',
                'tertiary': 'BLEU score',
                'custom': 'Phonetic similarity'
            }
        }
    
    def check_current_installation(self):
        """Check what libraries are currently installed"""
        print("🔍 CURRENT AUDIO-TO-TEXT LIBRARY ANALYSIS")
        print("=" * 60)
        
        library_status = {}
        
        # Check main libraries
        libraries_to_check = [
            'speech_recognition',
            'whisper', 
            'gtts',
            'pydub',
            'librosa',
            'Levenshtein',
            'vosk',
            'numpy',
            'scipy'
        ]
        
        for lib in libraries_to_check:
            try:
                module = importlib.import_module(lib)
                version = getattr(module, '__version__', 'Unknown')
                library_status[lib] = {'installed': True, 'version': version}
                print(f"✅ {lib}: {version}")
            except ImportError:
                library_status[lib] = {'installed': False, 'version': None}
                print(f"❌ {lib}: Not installed")
        
        return library_status
    
    def analyze_current_implementation(self):
        """Analyze current audio-to-text implementation"""
        print("\n📊 CURRENT IMPLEMENTATION ANALYSIS")
        print("=" * 60)
        
        # Check current English system
        print("\n🇺🇸 ENGLISH SPEECH SYSTEM:")
        try:
            from english_speech_system import EnglishSpeechSystem
            english_system = EnglishSpeechSystem()
            print("  ✅ EnglishSpeechSystem loaded")
            print(f"  🎯 Language: {english_system.language}")
            print(f"  📊 Confidence Threshold: {english_system.confidence_threshold}")
            print(f"  🎚️ Sample Rate: {english_system.sample_rate}")
            print("  🔧 Engines: Google Speech + Whisper")
        except Exception as e:
            print(f"  ❌ Error loading EnglishSpeechSystem: {e}")
        
        # Check current Malayalam system
        print("\n🇮🇳 MALAYALAM SPEECH SYSTEM:")
        try:
            from malayalam_speech_system import MalayalamSpeechSystem
            malayalam_system = MalayalamSpeechSystem()
            print("  ✅ MalayalamSpeechSystem loaded")
            print(f"  🎯 Language: {malayalam_system.language}")
            print(f"  📊 Confidence Threshold: {malayalam_system.confidence_threshold}")
            print(f"  🎚️ Sample Rate: {malayalam_system.sample_rate}")
            print("  🔧 Engines: Google Speech + Whisper")
        except Exception as e:
            print(f"  ❌ Error loading MalayalamSpeechSystem: {e}")
        
        # Check unified processor
        print("\n🔄 UNIFIED SPEECH PROCESSOR:")
        try:
            from unified_speech_processor import UnifiedSpeechProcessor
            unified_system = UnifiedSpeechProcessor()
            print("  ✅ UnifiedSpeechProcessor loaded")
            print(f"  🌍 Languages: {list(unified_system.language_systems.keys())}")
        except Exception as e:
            print(f"  ❌ Error loading UnifiedSpeechProcessor: {e}")
    
    def recommend_best_libraries(self):
        """Recommend the best libraries for audio-to-text"""
        print("\n🎯 RECOMMENDED BEST LIBRARIES")
        print("=" * 60)
        
        print("\n🇺🇸 ENGLISH SPEECH RECOGNITION:")
        print("  1️⃣ OpenAI Whisper (large-v3) - Best accuracy")
        print("     - State-of-the-art accuracy")
        print("     - Handles various accents well")
        print("     - Good for children's speech")
        print("  2️⃣ Google Speech Recognition v2 - Fast & reliable")
        print("     - Real-time processing")
        print("     - Good for clear audio")
        print("  3️⃣ Vosk (offline) - Privacy-focused")
        print("     - Works without internet")
        print("     - Custom models available")
        
        print("\n🇮🇳 MALAYALAM SPEECH RECOGNITION:")
        print("  1️⃣ Whisper multilingual (ml) - Best for Malayalam")
        print("     - Trained on 100+ languages")
        print("     - Good accuracy for Indian languages")
        print("  2️⃣ Google Speech (ml-IN) - Reliable option")
        print("     - Official Google support")
        print("     - Good for standard Malayalam")
        print("  3️⃣ Coqui TTS with custom model - Advanced option")
        print("     - Can train custom models")
        print("     - Better for regional variations")
        
        print("\n🎚️ AUDIO PROCESSING:")
        print("  1️⃣ librosa - Professional audio analysis")
        print("     - Feature extraction")
        print("     - Audio preprocessing")
        print("     - Fluency analysis")
        print("  2️⃣ pydub - Simple audio manipulation")
        print("     - Format conversion")
        print("     - Basic processing")
        print("  3️⃣ soundfile - Fast I/O operations")
        print("     - Efficient reading/writing")
        
        print("\n📊 SCORING & EVALUATION:")
        print("  1️⃣ Word Error Rate (WER) - Industry standard")
        print("     - Professional evaluation")
        print("     - Accurate comparison")
        print("  2️⃣ Levenshtein distance - Text similarity")
        print("     - Character-level comparison")
        print("     - Good for short texts")
        print("  3️⃣ BLEU score - Translation quality")
        print("     - N-gram matching")
        print("     - Good for fluency")
    
    def install_missing_libraries(self):
        """Install missing best libraries"""
        print("\n🔧 INSTALLING MISSING LIBRARIES")
        print("=" * 60)
        
        libraries_to_install = [
            'openai-whisper',
            'vosk',
            'librosa',
            'pydub',
            'soundfile',
            'Levenshtein',
            'jiwer',  # For WER calculation
            'sacrebleu'  # For BLEU score
        ]
        
        for lib in libraries_to_install:
            try:
                print(f"📦 Installing {lib}...")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', lib
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ {lib} installed successfully")
                else:
                    print(f"❌ Failed to install {lib}: {result.stderr}")
            except Exception as e:
                print(f"❌ Error installing {lib}: {e}")
    
    def create_enhanced_speech_system(self):
        """Create enhanced speech system with best libraries"""
        print("\n🚀 CREATING ENHANCED SPEECH SYSTEM")
        print("=" * 60)
        
        enhanced_code = '''
"""
Enhanced Speech Recognition System with Best Libraries
Implements state-of-the-art audio-to-text conversion
"""

import os
import logging
import tempfile
import numpy as np
from typing import Dict, List, Optional, Tuple

# Best libraries for speech recognition
try:
    import whisper
    WHISPER_AVAILABLE = True
    logging.info("OpenAI Whisper available")
except ImportError:
    WHISPER_AVAILABLE = False
    logging.warning("OpenAI Whisper not available")

try:
    import speech_recognition as sr
    SPEECH_REC_AVAILABLE = True
    logging.info("SpeechRecognition available")
except ImportError:
    SPEECH_REC_AVAILABLE = False
    logging.warning("SpeechRecognition not available")

try:
    import vosk
    VOSK_AVAILABLE = True
    logging.info("Vosk available")
except ImportError:
    VOSK_AVAILABLE = False
    logging.warning("Vosk not available")

# Audio processing libraries
try:
    import librosa
    LIBROSA_AVAILABLE = True
    logging.info("librosa available")
except ImportError:
    LIBROSA_AVAILABLE = False
    logging.warning("librosa not available")

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
    logging.info("pydub available")
except ImportError:
    PYDUB_AVAILABLE = False
    logging.warning("pydub not available")

# Scoring libraries
try:
    import jiwer
    WER_AVAILABLE = True
    logging.info("jiwer (WER) available")
except ImportError:
    WER_AVAILABLE = False
    logging.warning("jiwer not available")

try:
    import Levenshtein
    LEVENSHTEIN_AVAILABLE = True
    logging.info("Levenshtein available")
except ImportError:
    LEVENSHTEIN_AVAILABLE = False
    logging.warning("Levenshtein not available")

class EnhancedSpeechRecognizer:
    """Enhanced speech recognition with best libraries"""
    
    def __init__(self, language='en'):
        self.language = language
        self.confidence_threshold = 0.7
        
        # Load models
        self.whisper_models = {}
        self.vosk_models = {}
        self.speech_recognizer = sr.Recognizer() if SPEECH_REC_AVAILABLE else None
        
        # Initialize models
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize speech recognition models"""
        
        # Load Whisper models (best accuracy)
        if WHISPER_AVAILABLE:
            try:
                # Load different model sizes based on language
                if self.language == 'en':
                    self.whisper_models['base'] = whisper.load_model("base")
                    self.whisper_models['small'] = whisper.load_model("small")
                else:
                    # For other languages, use multilingual models
                    self.whisper_models['base'] = whisper.load_model("base")
                logging.info("Whisper models loaded")
            except Exception as e:
                logging.error(f"Error loading Whisper models: {e}")
        
        # Load Vosk models (offline option)
        if VOSK_AVAILABLE:
            try:
                # Vosk model paths would need to be downloaded
                model_path = f"vosk_models/{self.language}"
                if os.path.exists(model_path):
                    self.vosk_models[self.language] = vosk.Model(model_path)
                    logging.info(f"Vosk model loaded for {self.language}")
            except Exception as e:
                logging.error(f"Error loading Vosk models: {e}")
    
    def recognize_speech(self, audio_file_path: str) -> Dict:
        """
        Recognize speech using the best available engine
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Dict with text, confidence, engine, and metadata
        """
        
        results = []
        
        # 1. Try Whisper (best accuracy)
        if WHISPER_AVAILABLE and 'base' in self.whisper_models:
            try:
                result = self._recognize_with_whisper(audio_file_path)
                if result:
                    results.append(result)
            except Exception as e:
                logging.error(f"Whisper recognition failed: {e}")
        
        # 2. Try Google Speech Recognition
        if SPEECH_REC_AVAILABLE and self.speech_recognizer:
            try:
                result = self._recognize_with_google(audio_file_path)
                if result:
                    results.append(result)
            except Exception as e:
                logging.error(f"Google recognition failed: {e}")
        
        # 3. Try Vosk (offline)
        if VOSK_AVAILABLE and self.language in self.vosk_models:
            try:
                result = self._recognize_with_vosk(audio_file_path)
                if result:
                    results.append(result)
            except Exception as e:
                logging.error(f"Vosk recognition failed: {e}")
        
        # Select best result
        if results:
            best_result = max(results, key=lambda x: x['confidence'])
            return best_result
        
        return {
            'text': '',
            'confidence': 0.0,
            'engine': 'none',
            'error': 'All recognition engines failed'
        }
    
    def _recognize_with_whisper(self, audio_file_path: str) -> Optional[Dict]:
        """Recognize speech using Whisper"""
        
        try:
            # Use appropriate model size
            model = self.whisper_models.get('small', self.whisper_models['base'])
            
            # Transcribe with language specification
            result = model.transcribe(
                audio_file_path,
                language=self.language if self.language != 'ml' else 'malayalam',
                fp16=False,  # Use FP32 for compatibility
                verbose=False
            )
            
            text = result['text'].strip()
            
            # Calculate confidence from average log probability
            avg_logprob = result.get('avg_logprob', -1.0)
            confidence = max(0.0, min(1.0, (avg_logprob + 2.0) / 4.0))  # Normalize to 0-1
            
            return {
                'text': text,
                'confidence': confidence,
                'engine': 'whisper',
                'model': model.__class__.__name__,
                'language': self.language,
                'processing_time': result.get('segments', [{}])[0].get('end', 0)
            }
            
        except Exception as e:
            logging.error(f"Whisper recognition error: {e}")
            return None
    
    def _recognize_with_google(self, audio_file_path: str) -> Optional[Dict]:
        """Recognize speech using Google Speech Recognition"""
        
        try:
            with sr.AudioFile(audio_file_path) as source:
                # Adjust for ambient noise
                self.speech_recognizer.adjust_for_ambient_noise(source, duration=1)
                audio_data = self.speech_recognizer.record(source)
            
            # Use appropriate language code
            lang_code = 'en-US' if self.language == 'en' else 'ml-IN'
            
            # Recognize with confidence
            result = self.speech_recognizer.recognize_google(
                audio_data,
                language=lang_code,
                show_all=True
            )
            
            if result and 'alternative' in result:
                alternative = result['alternative'][0]
                text = alternative['transcript']
                confidence = alternative.get('confidence', 0.0)
                
                return {
                    'text': text,
                    'confidence': confidence / 100.0,  # Convert to 0-1
                    'engine': 'google',
                    'language': self.language
                }
            
        except Exception as e:
            logging.error(f"Google recognition error: {e}")
            return None
    
    def _recognize_with_vosk(self, audio_file_path: str) -> Optional[Dict]:
        """Recognize speech using Vosk (offline)"""
        
        try:
            # Convert audio to format Vosk expects
            if LIBROSA_AVAILABLE:
                audio, sr_rate = librosa.load(audio_file_path, sr=16000)
            else:
                # Fallback to pydub
                audio = AudioSegment.from_file(audio_file_path)
                audio = audio.set_frame_rate(16000).set_channels(1)
                audio = np.array(audio.get_array_of_samples())
                sr_rate = 16000
            
            # Recognize with Vosk
            rec = vosk.KaldiRecognizer(self.vosk_models[self.language], sr_rate)
            
            if rec.AcceptWaveform(audio.tobytes()):
                result = rec.Result()
                import json
                data = json.loads(result)
                
                text = data.get('text', '')
                confidence = 0.8  # Vosk doesn't provide confidence, use default
                
                return {
                    'text': text,
                    'confidence': confidence,
                    'engine': 'vosk',
                    'language': self.language
                }
            
        except Exception as e:
            logging.error(f"Vosk recognition error: {e}")
            return None
    
    def calculate_accuracy_score(self, recognized_text: str, expected_text: str) -> Dict:
        """
        Calculate accuracy using multiple metrics
        
        Args:
            recognized_text: Text from speech recognition
            expected_text: Expected/ground truth text
            
        Returns:
            Dict with accuracy metrics
        """
        
        if not recognized_text or not expected_text:
            return {
                'wer': 1.0,
                'levenshtein': 0.0,
                'bleu': 0.0,
                'overall': 0.0
            }
        
        metrics = {}
        
        # Word Error Rate (WER) - Industry standard
        if WER_AVAILABLE:
            try:
                wer = jiwer.wer(expected_text, recognized_text)
                metrics['wer'] = wer
                metrics['wer_accuracy'] = max(0.0, 1.0 - wer)
            except Exception as e:
                logging.error(f"WER calculation error: {e}")
                metrics['wer'] = 1.0
                metrics['wer_accuracy'] = 0.0
        
        # Levenshtein distance
        if LEVENSHTEIN_AVAILABLE:
            try:
                distance = Levenshtein.distance(expected_text, recognized_text)
                max_len = max(len(expected_text), len(recognized_text))
                levenshtein_similarity = 1.0 - (distance / max_len) if max_len > 0 else 0.0
                metrics['levenshtein'] = levenshtein_similarity
            except Exception as e:
                logging.error(f"Levenshtein calculation error: {e}")
                metrics['levenshtein'] = 0.0
        else:
            # Fallback to sequence matcher
            from difflib import SequenceMatcher
            similarity = SequenceMatcher(None, expected_text, recognized_text).ratio()
            metrics['levenshtein'] = similarity
        
        # Overall accuracy (weighted average)
        weights = {
            'wer_accuracy': 0.5,
            'levenshtein': 0.3,
            'length_penalty': 0.2
        }
        
        # Length penalty for very short/long texts
        length_ratio = len(recognized_text) / max(len(expected_text), 1)
        length_penalty = max(0.0, 1.0 - abs(1.0 - length_ratio))
        metrics['length_penalty'] = length_penalty
        
        overall_accuracy = (
            metrics.get('wer_accuracy', 0.0) * weights['wer_accuracy'] +
            metrics.get('levenshtein', 0.0) * weights['levenshtein'] +
            length_penalty * weights['length_penalty']
        )
        
        metrics['overall'] = min(1.0, max(0.0, overall_accuracy))
        
        return metrics

# Usage example:
# recognizer = EnhancedSpeechRecognizer('en')
# result = recognizer.recognize_speech('audio.wav')
# accuracy = recognizer.calculate_accuracy_score(result['text'], expected_text)
'''
        
        with open('enhanced_speech_recognition.py', 'w') as f:
            f.write(enhanced_code)
        
        print("✅ Enhanced speech recognition system created")
        print("📁 File: enhanced_speech_recognition.py")
    
    def run_complete_analysis(self):
        """Run complete analysis and upgrade process"""
        print("🎮 AUDIO-TO-TEXT SYSTEM ANALYSIS AND UPGRADE")
        print("=" * 80)
        
        # Step 1: Check current installation
        library_status = self.check_current_installation()
        
        # Step 2: Analyze current implementation
        self.analyze_current_implementation()
        
        # Step 3: Recommend best libraries
        self.recommend_best_libraries()
        
        # Step 4: Install missing libraries
        self.install_missing_libraries()
        
        # Step 5: Create enhanced system
        self.create_enhanced_speech_system()
        
        print("\n" + "=" * 80)
        print("✅ AUDIO-TO-TEXT ANALYSIS COMPLETE!")
        print("=" * 80)
        
        print("\n🎯 RECOMMENDATIONS:")
        print("1. Install enhanced_speech_recognition.py in your project")
        print("2. Replace current speech systems with EnhancedSpeechRecognizer")
        print("3. Use Whisper as primary engine for best accuracy")
        print("4. Implement WER scoring for professional evaluation")
        print("5. Add age-based adjustments for children's speech")
        
        print("\n🚀 NEXT STEPS:")
        print("1. Test the enhanced system with sample audio files")
        print("2. Compare accuracy with current implementation")
        print("3. Integrate with story-mode page")
        print("4. Add real-time feedback for children")

if __name__ == "__main__":
    analyzer = AudioToTextAnalyzer()
    analyzer.run_complete_analysis()
