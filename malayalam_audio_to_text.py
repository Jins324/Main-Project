"""
Malayalam Audio-to-Text Conversion System
Specialized for Malayalam speech recognition with Unicode support
"""
import os
import logging
import speech_recognition as sr
import tempfile
import unicodedata
import re
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class MalayalamAudioToText:
    """Specialized Malayalam audio-to-text conversion"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.language = 'ml-IN'
        
        # Malayalam-specific settings
        self.energy_threshold = 250  # Lower for Malayalam sounds
        self.dynamic_energy_threshold = True
        self.pause_threshold = 0.9  # Longer pause for Malayalam
        self.operation_timeout = 30
        
        # Configure recognizer for Malayalam
        self.recognizer.energy_threshold = self.energy_threshold
        self.recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold
        self.recognizer.pause_threshold = self.pause_threshold
        self.recognizer.operation_timeout = self.operation_timeout
        
        # Recognition engines priority
        self.engines = [
            'google',      # Primary: Google Speech Recognition
            'whisper',     # Secondary: OpenAI Whisper
            'coqui'        # Tertiary: Coqui TTS (if available)
        ]
        
        logger.info("Malayalam Audio-to-Text System initialized")
    
    def convert_audio_to_text(self, audio_file_path: str, engine: str = 'auto') -> Dict:
        """Convert Malayalam audio to text using specified or best engine"""
        
        try:
            logger.info(f"Converting Malayalam audio to text: {audio_file_path}")
            
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
                    if result['success'] and result['confidence'] > 0.4:  # Lower threshold for Malayalam
                        logger.info(f"Malayalam audio converted using {eng}: '{result['text'][:50]}...'")
                        return result
            else:
                # Use specified engine
                result = self._try_engine(audio_data, engine)
                if result['success']:
                    logger.info(f"Malayalam audio converted using {engine}: '{result['text'][:50]}...'")
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
            logger.error(f"Malayalam audio-to-text conversion error: {e}")
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
            elif engine == 'coqui':
                return self._coqui_recognition(audio_data)
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
        """Google Speech Recognition for Malayalam"""
        
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
                
                # Clean and normalize Malayalam text
                cleaned_text = self._clean_malayalam_text(text)
                
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
                'error': 'Google could not understand Malayalam audio'
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
        """Whisper recognition for Malayalam"""
        
        try:
            # Save audio to temporary file for Whisper
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
                with open(temp_path, 'wb') as f:
                    f.write(audio_data.get_wav_data())
            
            try:
                import whisper
                model = whisper.load_model("base")
                result = model.transcribe(temp_path, language="ml")
                
                text = result.get("text", "").strip()
                confidence = self._calculate_whisper_confidence(result)
                
                # Clean and normalize Malayalam text
                cleaned_text = self._clean_malayalam_text(text)
                
                return {
                    'success': True,
                    'text': cleaned_text,
                    'confidence': confidence,
                    'engine': 'whisper',
                    'language_detected': result.get("language", "ml")
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
    
    def _coqui_recognition(self, audio_data) -> Dict:
        """Coqui TTS recognition for Malayalam (if available)"""
        
        try:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
                with open(temp_path, 'wb') as f:
                    f.write(audio_data.get_wav_data())
            
            try:
                from TTS.api import TTS
                # This would need custom implementation for recognition
                # Coqui is primarily TTS, but we can use it for speech processing
                
                # For now, return a placeholder implementation
                return {
                    'success': False,
                    'text': '',
                    'confidence': 0.0,
                    'engine': 'coqui',
                    'error': 'Coqui recognition not implemented yet'
                }
                
            except ImportError:
                return {
                    'success': False,
                    'text': '',
                    'confidence': 0.0,
                    'engine': 'coqui',
                    'error': 'Coqui TTS not available'
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
                'engine': 'coqui',
                'error': f'Coqui error: {e}'
            }
    
    def _clean_malayalam_text(self, text: str) -> str:
        """Clean and normalize Malayalam text with Unicode support"""
        
        if not text:
            return ""
        
        # Normalize Unicode
        text = unicodedata.normalize('NFC', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common Malayalam recognition artifacts
        artifacts = ['ഉം', 'എന്ന്', 'ആണ്', 'ഉണ്ട്', 'മാത്രം']
        words = text.split()
        words = [word for word in words if word not in artifacts]
        
        # Reconstruct text
        cleaned = ' '.join(words)
        
        # Remove non-Malayalam characters except spaces and basic punctuation
        malayalam_pattern = re.compile(r'[\u0D00-\u0D7F\s\.\,\!\?\;\:]')
        matches = malayalam_pattern.findall(cleaned)
        cleaned = ''.join(matches)
        
        # Remove extra spaces
        cleaned = ' '.join(cleaned.split())
        
        return cleaned.strip()
    
    def _calculate_whisper_confidence(self, whisper_result: Dict) -> float:
        """Calculate confidence from Whisper result for Malayalam"""
        
        try:
            # Use average log probability as confidence indicator
            avg_logprob = whisper_result.get("avg_logprob", -1.0)
            
            # Convert log probability to confidence (adjusted for Malayalam)
            confidence = max(0.0, min(1.0, (avg_logprob + 2.5) / 2.5))  # Slightly more lenient
            
            # Boost confidence if language detection is confident
            if whisper_result.get("language") == "ml":
                confidence = min(1.0, confidence + 0.15)
            
            return confidence
            
        except Exception:
            return 0.4  # Default confidence for Malayalam (lower than English)
    
    def validate_malayalam_text(self, text: str) -> Dict:
        """Validate if text is proper Malayalam"""
        
        try:
            if not text:
                return {
                    'is_malayalam': False,
                    'confidence': 0.0,
                    'issues': ['Empty text']
                }
            
            # Check Unicode normalization
            normalized = unicodedata.normalize('NFC', text)
            if text != normalized:
                return {
                    'is_malayalam': False,
                    'confidence': 0.0,
                    'issues': ['Unicode not normalized']
                }
            
            # Check for Malayalam characters
            malayalam_chars = re.findall(r'[\u0D00-\u0D7F]', text)
            total_chars = len(text.replace(' ', ''))
            
            if total_chars == 0:
                return {
                    'is_malayalam': False,
                    'confidence': 0.0,
                    'issues': ['No characters found']
                }
            
            malayalam_ratio = len(malayalam_chars) / total_chars
            
            # Check for common Malayalam patterns
            malayalam_patterns = [
                r'[\u0D02\u0D3E]',  # ആ
                r'[\u0D07\u0D4D]',  # ക്
                r'[\u0D15\u0D4D\u0D37]',  # ക്ഷ
            ]
            
            pattern_matches = 0
            for pattern in malayalam_patterns:
                if re.search(pattern, text):
                    pattern_matches += 1
            
            # Calculate overall confidence
            confidence = malayalam_ratio * 0.7 + (pattern_matches / len(malayalam_patterns)) * 0.3
            
            issues = []
            if malayalam_ratio < 0.8:
                issues.append(f'Low Malayalam character ratio: {malayalam_ratio:.2f}')
            
            if pattern_matches < 2:
                issues.append('Few Malayalam patterns detected')
            
            return {
                'is_malayalam': confidence > 0.6,
                'confidence': confidence,
                'malayalam_ratio': malayalam_ratio,
                'pattern_matches': pattern_matches,
                'issues': issues if issues else ['Valid Malayalam text']
            }
            
        except Exception as e:
            return {
                'is_malayalam': False,
                'confidence': 0.0,
                'issues': [f'Validation error: {e}']
            }
    
    def get_supported_engines(self) -> Dict:
        """Get list of supported recognition engines"""
        
        engines = {
            'google': {
                'name': 'Google Speech Recognition',
                'online': True,
                'confidence_scores': True,
                'description': 'Primary engine for Malayalam recognition'
            },
            'whisper': {
                'name': 'OpenAI Whisper',
                'online': False,
                'confidence_scores': False,
                'description': 'High accuracy offline recognition'
            },
            'coqui': {
                'name': 'Coqui TTS',
                'online': False,
                'confidence_scores': False,
                'description': 'Specialized Malayalam processing'
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
    converter = MalayalamAudioToText()
    
    print("🇮🇳 MALAYALAM AUDIO-TO-TEXT SYSTEM")
    print("=" * 50)
    
    # Test system info
    engines = converter.get_supported_engines()
    print(f"Supported Engines:")
    for code, info in engines.items():
        print(f"  {code}: {info['name']} ({'Online' if info['online'] else 'Offline'})")
    
    # Test text cleaning
    print(f"\n🧪 Text Cleaning Test:")
    test_texts = [
        "നമസ്കാരം",
        "നമസ്കാരം എന്ന്",
        "നമസ്കാരം ആണ്",
        "നമസ്കാരം ഉണ്ട്",
        ""
    ]
    
    for text in test_texts:
        cleaned = converter._clean_malayalam_text(text)
        print(f"  '{text}' -> '{cleaned}'")
    
    # Test Malayalam validation
    print(f"\n🧪 Malayalam Validation Test:")
    test_texts = [
        "നമസ്കാരം",
        "നമസ്കാരം hello",
        "hello world",
        ""
    ]
    
    for text in test_texts:
        validation = converter.validate_malayalam_text(text)
        print(f"  '{text}': {validation['is_malayalam']} ({validation['confidence']:.2f})")
    
    print(f"\n✅ Malayalam Audio-to-Text System Ready!")
