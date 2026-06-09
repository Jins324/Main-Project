"""
English Audio-to-Text Conversion System
Specialized for English speech recognition with multiple engines
"""
import os
import logging
import speech_recognition as sr
import tempfile
import json
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class EnglishAudioToText:
    """Specialized English audio-to-text conversion"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.language = 'en-US'
        
        # English-specific settings
        self.energy_threshold = 300
        self.dynamic_energy_threshold = True
        self.pause_threshold = 0.8
        self.operation_timeout = 30
        
        # Configure recognizer for English
        self.recognizer.energy_threshold = self.energy_threshold
        self.recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold
        self.recognizer.pause_threshold = self.pause_threshold
        self.recognizer.operation_timeout = self.operation_timeout
        
        # Recognition engines priority
        self.engines = [
            'google',      # Primary: Google Speech Recognition
            'whisper',     # Secondary: OpenAI Whisper
            'sphinx'       # Fallback: CMU Sphinx
        ]
        
        logger.info("English Audio-to-Text System initialized")
    
    def convert_audio_to_text(self, audio_file_path: str, engine: str = 'auto') -> Dict:
        """Convert English audio to text using specified or best engine"""
        
        try:
            logger.info(f"Converting English audio to text: {audio_file_path}")
            
            # Validate audio file
            if not os.path.exists(audio_file_path):
                return {
                    'success': False,
                    'text': '',
                    'confidence': 0.0,
                    'engine': 'none',
                    'error': 'Audio file not found'
                }
            
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio_data = self.recognizer.record(source)
            
            # Try engines in order of preference
            if engine == 'auto':
                # Try all engines until one succeeds
                for eng in self.engines:
                    result = self._try_engine(audio_data, eng)
                    if result['success'] and result['confidence'] > 0.5:
                        logger.info(f"English audio converted using {eng}: '{result['text'][:50]}...'")
                        return result
            else:
                # Use specified engine
                result = self._try_engine(audio_data, engine)
                if result['success']:
                    logger.info(f"English audio converted using {engine}: '{result['text'][:50]}...'")
                    return result
            
            # If all engines failed
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'engine': 'none',
                'error': 'All recognition engines failed'
            }
            
        except Exception as e:
            logger.error(f"English audio-to-text conversion error: {e}")
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'engine': 'error',
                'error': str(e)
            }
    
    def _try_engine(self, audio_data, engine: str) -> Dict:
        """Try specific recognition engine"""
        
        try:
            if engine == 'google':
                return self._google_recognition(audio_data)
            elif engine == 'whisper':
                return self._whisper_recognition(audio_data)
            elif engine == 'sphinx':
                return self._sphinx_recognition(audio_data)
            else:
                return {
                    'success': False,
                    'text': '',
                    'confidence': 0.0,
                    'engine': engine,
                    'error': f'Unknown engine: {engine}'
                }
                
        except Exception as e:
            logger.error(f"Error with {engine} engine: {e}")
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'engine': engine,
                'error': str(e)
            }
    
    def _google_recognition(self, audio_data) -> Dict:
        """Google Speech Recognition for English"""
        
        try:
            # Try with confidence scores
            result = self.recognizer.recognize_google(
                audio_data,
                language=self.language,
                show_all=True
            )
            
            if result and 'alternative' in result and len(result['alternative']) > 0:
                best_alternative = result['alternative'][0]
                text = best_alternative.get('transcript', '')
                confidence = best_alternative.get('confidence', 0.0)
                
                # Clean and normalize text
                cleaned_text = self._clean_english_text(text)
                
                return {
                    'success': True,
                    'text': cleaned_text,
                    'confidence': float(confidence),
                    'engine': 'google',
                    'alternatives': len(result['alternative'])
                }
            else:
                return {
                    'success': False,
                    'text': '',
                    'confidence': 0.0,
                    'engine': 'google',
                    'error': 'No speech detected'
                }
                
        except sr.UnknownValueError:
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'engine': 'google',
                'error': 'Google could not understand audio'
            }
        except sr.RequestError as e:
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'engine': 'google',
                'error': f'Google service error: {e}'
            }
    
    def _whisper_recognition(self, audio_data) -> Dict:
        """Whisper recognition for English"""
        
        try:
            # Save audio to temporary file for Whisper
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
                with open(temp_path, 'wb') as f:
                    f.write(audio_data.get_wav_data())
            
            try:
                import whisper
                model = whisper.load_model("base")
                result = model.transcribe(temp_path, language="en")
                
                text = result.get("text", "").strip()
                confidence = self._calculate_whisper_confidence(result)
                
                # Clean and normalize text
                cleaned_text = self._clean_english_text(text)
                
                return {
                    'success': True,
                    'text': cleaned_text,
                    'confidence': confidence,
                    'engine': 'whisper',
                    'language_detected': result.get("language", "en")
                }
                
            except ImportError:
                return {
                    'success': False,
                    'text': '',
                    'confidence': 0.0,
                    'engine': 'whisper',
                    'error': 'Whisper not available'
                }
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_path)
                except:
                    pass
                    
        except Exception as e:
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'engine': 'whisper',
                'error': f'Whisper error: {e}'
            }
    
    def _sphinx_recognition(self, audio_data) -> Dict:
        """CMU Sphinx recognition for English (offline fallback)"""
        
        try:
            text = self.recognizer.recognize_sphinx(audio_data)
            
            # Clean and normalize text
            cleaned_text = self._clean_english_text(text)
            
            # Sphinx doesn't provide confidence, so estimate
            confidence = self._estimate_sphinx_confidence(cleaned_text)
            
            return {
                'success': True,
                'text': cleaned_text,
                'confidence': confidence,
                'engine': 'sphinx',
                'offline': True
            }
            
        except sr.UnknownValueError:
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'engine': 'sphinx',
                'error': 'Sphinx could not understand audio'
            }
        except sr.RequestError as e:
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'engine': 'sphinx',
                'error': f'Sphinx error: {e}'
            }
    
    def _clean_english_text(self, text: str) -> str:
        """Clean and normalize English text"""
        
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common recognition artifacts
        artifacts = ['um', 'uh', 'er', 'ah', 'like', 'you know', 'i mean']
        words = text.lower().split()
        words = [word for word in words if word not in artifacts]
        
        # Reconstruct text
        cleaned = ' '.join(words)
        
        # Remove punctuation but keep basic sentence structure
        import string
        cleaned = cleaned.translate(str.maketrans('', '', string.punctuation))
        
        # Capitalize first letter
        if cleaned:
            cleaned = cleaned[0].upper() + cleaned[1:]
        
        return cleaned.strip()
    
    def _calculate_whisper_confidence(self, whisper_result: Dict) -> float:
        """Calculate confidence from Whisper result"""
        
        try:
            # Use average log probability as confidence indicator
            avg_logprob = whisper_result.get("avg_logprob", -1.0)
            
            # Convert log probability to confidence (rough approximation)
            confidence = max(0.0, min(1.0, (avg_logprob + 2.0) / 2.0))
            
            # Boost confidence if language detection is confident
            if whisper_result.get("language") == "en":
                confidence = min(1.0, confidence + 0.1)
            
            return confidence
            
        except Exception:
            return 0.5  # Default confidence
    
    def _estimate_sphinx_confidence(self, text: str) -> float:
        """Estimate confidence for Sphinx recognition"""
        
        try:
            if not text:
                return 0.0
            
            # Basic confidence estimation based on text characteristics
            word_count = len(text.split())
            
            # Very short or very long text is less reliable
            if word_count < 2:
                return 0.3
            elif word_count > 50:
                return 0.4
            else:
                return 0.5  # Default moderate confidence
                
        except Exception:
            return 0.3  # Low default confidence
    
    def get_supported_engines(self) -> Dict:
        """Get list of supported recognition engines"""
        
        engines = {
            'google': {
                'name': 'Google Speech Recognition',
                'online': True,
                'confidence_scores': True,
                'description': 'Primary engine for English recognition'
            },
            'whisper': {
                'name': 'OpenAI Whisper',
                'online': False,
                'confidence_scores': False,
                'description': 'High accuracy offline recognition'
            },
            'sphinx': {
                'name': 'CMU Sphinx',
                'online': False,
                'confidence_scores': False,
                'description': 'Offline fallback recognition'
            }
        }
        
        return engines
    
    def test_all_engines(self, audio_file_path: str) -> Dict:
        """Test all recognition engines with the same audio"""
        
        results = {}
        
        for engine in self.engines:
            result = self.convert_audio_to_text(audio_file_path, engine)
            results[engine] = result
        
        # Find best result
        best_engine = None
        best_confidence = 0.0
        
        for engine, result in results.items():
            if result['success'] and result['confidence'] > best_confidence:
                best_engine = engine
                best_confidence = result['confidence']
        
        return {
            'all_results': results,
            'best_engine': best_engine,
            'best_confidence': best_confidence,
            'best_text': results[best_engine]['text'] if best_engine else ''
        }

# Test the system
if __name__ == "__main__":
    converter = EnglishAudioToText()
    
    print("🇺🇸 ENGLISH AUDIO-TO-TEXT SYSTEM")
    print("=" * 50)
    
    # Test system info
    engines = converter.get_supported_engines()
    print(f"Supported Engines:")
    for code, info in engines.items():
        print(f"  {code}: {info['name']} ({'Online' if info['online'] else 'Offline'})")
    
    # Test text cleaning
    print(f"\n🧪 Text Cleaning Test:")
    test_texts = [
        "hello world",
        "um hello uh world",
        "HELLO WORLD",
        "hello, world!",
        ""
    ]
    
    for text in test_texts:
        cleaned = converter._clean_english_text(text)
        print(f"  '{text}' -> '{cleaned}'")
    
    print(f"\n✅ English Audio-to-Text System Ready!")
