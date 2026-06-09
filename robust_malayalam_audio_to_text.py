"""
Robust Malayalam Audio-to-Text System with Real-time Processing
Handles audio recording, speech-to-text conversion, and scoring
"""
import os
import logging
import speech_recognition as sr
import tempfile
import unicodedata
import re
from typing import Dict, Optional
from malayalam_speech_system import MalayalamSpeechSystem

logger = logging.getLogger(__name__)

class RobustMalayalamAudioToText:
    """Robust Malayalam audio-to-text conversion with real-time processing"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speech_system = MalayalamSpeechSystem()
        self.language = 'ml-IN'
        
        # Malayalam-specific settings
        self.energy_threshold = 250  # Lower for Malayalam sounds
        self.dynamic_energy_threshold = True
        self.pause_threshold = 0.9  # Longer pause for Malayalam
        self.operation_timeout = 30
        
        # Configure recognizer
        self.recognizer.energy_threshold = self.energy_threshold
        self.recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold
        self.recognizer.pause_threshold = self.pause_threshold
        self.recognizer.operation_timeout = self.operation_timeout
        
        logger.info("Robust Malayalam Audio-to-Text System initialized")
    
    def process_audio_recording(self, audio_file_path: str, expected_text: str = "") -> Dict:
        """Complete audio processing pipeline: audio → text → scoring"""
        
        try:
            logger.info(f"Processing Malayalam audio recording: {audio_file_path}")
            
            # Step 1: Convert audio to text
            speech_result = self.convert_audio_to_text(audio_file_path)
            
            if not speech_result.get('success', False):
                return {
                    'success': False,
                    'error': speech_result.get('error', 'Speech recognition failed'),
                    'recognized_text': '',
                    'expected_text': expected_text,
                    'scores': {'overall': 0.0, 'pronunciation': 0.0, 'fluency': 0.0, 'accuracy': 0.0},
                    'feedback': {'overall_message': 'Speech recognition failed', 'improvement_tips': []}
                }
            
            recognized_text = speech_result.get('text', '')
            confidence = speech_result.get('confidence', 0.0)
            engine = speech_result.get('engine', 'unknown')
            
            # Step 2: Validate Malayalam text
            validation_result = self.validate_malayalam_text(recognized_text)
            
            # Step 3: Score the recognized text against expected text
            if expected_text:
                scoring_result = self.score_speech(recognized_text, expected_text, audio_file_path)
            else:
                scoring_result = {
                    'success': True,
                    'scores': {'overall': 100.0, 'pronunciation': 100.0, 'fluency': 100.0, 'accuracy': 100.0},
                    'feedback': {'overall_message': 'Speech recognized successfully', 'improvement_tips': []}
                }
            
            # Step 4: Combine results
            result = {
                'success': True,
                'recognized_text': recognized_text,
                'expected_text': expected_text,
                'confidence': confidence,
                'engine': engine,
                'malayalam_validation': validation_result,
                'scores': scoring_result.get('scores', {}),
                'feedback': scoring_result.get('feedback', {}),
                'processing_time': speech_result.get('processing_time', 0.0)
            }
            
            logger.info(f"Malayalam audio processing complete: '{recognized_text[:50]}...'")
            return result
            
        except Exception as e:
            logger.error(f"Error processing Malayalam audio recording: {e}")
            return {
                'success': False,
                'error': str(e),
                'recognized_text': '',
                'expected_text': expected_text,
                'scores': {'overall': 0.0, 'pronunciation': 0.0, 'fluency': 0.0, 'accuracy': 0.0},
                'feedback': {'overall_message': f'Processing error: {str(e)}', 'improvement_tips': []}
            }
    
    def convert_audio_to_text(self, audio_file_path: str) -> Dict:
        """Convert audio file to text using best available engine"""
        
        try:
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
            engines = ['google', 'whisper', 'coqui']
            
            for engine in engines:
                result = self._try_recognition_engine(audio_data, engine)
                if result.get('success', False) and result.get('confidence', 0.0) > 0.4:  # Lower threshold for Malayalam
                    logger.info(f"Malayalam audio converted using {engine}: '{result.get('text', '')[:50]}...'")
                    return result
            
            # If all engines failed, return best result
            return result
            
        except Exception as e:
            logger.error(f"Error converting Malayalam audio to text: {e}")
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'engine': 'error',
                'error': str(e)
            }
    
    def _try_recognition_engine(self, audio_data, engine: str) -> Dict:
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
            # Save audio to temporary file
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
        """Coqui recognition for Malayalam"""
        
        try:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
                with open(temp_path, 'wb') as f:
                    f.write(audio_data.get_wav_data())
            
            try:
                # This would need custom implementation for Coqui recognition
                # For now, return a placeholder
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
        """Clean and normalize Malayalam text"""
        
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
            avg_logprob = whisper_result.get("avg_logprob", -1.0)
            confidence = max(0.0, min(1.0, (avg_logprob + 2.5) / 2.5))  # More lenient for Malayalam
            
            if whisper_result.get("language") == "ml":
                confidence = min(1.0, confidence + 0.15)
            
            return confidence
            
        except Exception:
            return 0.4  # Default confidence for Malayalam
    
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
    
    def score_speech(self, recognized_text: str, expected_text: str, audio_file_path: str) -> Dict:
        """Score speech using the speech system"""
        
        try:
            # Use the speech system for comprehensive scoring
            scores = self.speech_system.calculate_pronunciation_score(recognized_text, expected_text)
            
            # Get fluency analysis
            fluency_result = self.speech_system.analyze_fluency(audio_file_path, recognized_text, expected_text)
            
            # Get feedback
            feedback = self.speech_system.generate_feedback(scores, fluency_result, recognized_text, expected_text)
            
            return {
                'success': True,
                'scores': scores,
                'fluency': fluency_result,
                'feedback': feedback
            }
            
        except Exception as e:
            logger.error(f"Error scoring speech: {e}")
            return {
                'success': False,
                'scores': {'overall': 0.0, 'pronunciation': 0.0, 'fluency': 0.0, 'accuracy': 0.0},
                'feedback': {'overall_message': f'Scoring error: {str(e)}', 'improvement_tips': []}
            }
    
    def get_system_info(self) -> Dict:
        """Get system information"""
        
        return {
            'language': 'Malayalam',
            'code': 'ml',
            'engines': ['google', 'whisper', 'coqui'],
            'energy_threshold': self.energy_threshold,
            'pause_threshold': self.pause_threshold,
            'features': [
                'Real-time speech recognition',
                'Unicode normalization',
                'Malayalam text validation',
                'Cultural speech patterns',
                'Comprehensive scoring',
                'Fluency analysis',
                'Pronunciation feedback'
            ]
        }

# Test the system
if __name__ == "__main__":
    converter = RobustMalayalamAudioToText()
    
    print("🇮🇳 ROBUST MALAYALAM AUDIO-TO-TEXT SYSTEM")
    print("=" * 60)
    
    # Test system info
    info = converter.get_system_info()
    print(f"System Info:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print(f"\n✅ Robust Malayalam Audio-to-Text System Ready!")
