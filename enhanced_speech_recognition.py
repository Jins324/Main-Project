
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
