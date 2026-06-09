"""
Robust English Audio-to-Text System with Real-time Processing
Handles audio recording, speech-to-text conversion, and scoring
"""
import os
import logging
import speech_recognition as sr
import tempfile
import json
from typing import Dict, Optional
from english_speech_system import EnglishSpeechSystem

logger = logging.getLogger(__name__)

class RobustEnglishAudioToText:
    """Robust English audio-to-text conversion with real-time processing"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speech_system = EnglishSpeechSystem()
        self.language = 'en-US'
        
        # English-specific settings
        self.energy_threshold = 300
        self.dynamic_energy_threshold = True
        self.pause_threshold = 0.8
        self.operation_timeout = 30
        
        # Configure recognizer
        self.recognizer.energy_threshold = self.energy_threshold
        self.recognizer.dynamic_energy_threshold = self.dynamic_energy_threshold
        self.recognizer.pause_threshold = self.pause_threshold
        self.recognizer.operation_timeout = self.operation_timeout
        
        logger.info("Robust English Audio-to-Text System initialized")
    
    def process_audio_recording(self, audio_file_path: str, expected_text: str = "") -> Dict:
        """Complete audio processing pipeline: audio → text → scoring"""
        
        try:
            logger.info(f"Processing English audio recording: {audio_file_path}")
            
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
            
            # Step 2: Score the recognized text against expected text
            if expected_text:
                scoring_result = self.score_speech(recognized_text, expected_text, audio_file_path)
            else:
                scoring_result = {
                    'success': True,
                    'scores': {'overall': 100.0, 'pronunciation': 100.0, 'fluency': 100.0, 'accuracy': 100.0},
                    'feedback': {'overall_message': 'Speech recognized successfully', 'improvement_tips': []}
                }
            
            # Step 3: Combine results
            result = {
                'success': True,
                'recognized_text': recognized_text,
                'expected_text': expected_text,
                'confidence': confidence,
                'engine': engine,
                'scores': scoring_result.get('scores', {}),
                'feedback': scoring_result.get('feedback', {}),
                'processing_time': speech_result.get('processing_time', 0.0)
            }
            
            logger.info(f"English audio processing complete: '{recognized_text[:50]}...'")
            return result
            
        except Exception as e:
            logger.error(f"Error processing English audio recording: {e}")
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
            engines = ['google', 'whisper', 'sphinx']
            
            for engine in engines:
                result = self._try_recognition_engine(audio_data, engine)
                if result.get('success', False) and result.get('confidence', 0.0) > 0.5:
                    logger.info(f"English audio converted using {engine}: '{result.get('text', '')[:50]}...'")
                    return result
            
            # If all engines failed, return best result
            return result
            
        except Exception as e:
            logger.error(f"Error converting English audio to text: {e}")
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
        """Google Speech Recognition"""
        
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
                
                # Clean text
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
        """Whisper recognition"""
        
        try:
            # Save audio to temporary file
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
                
                # Clean text
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
        """CMU Sphinx recognition"""
        
        try:
            text = self.recognizer.recognize_sphinx(audio_data)
            cleaned_text = self._clean_english_text(text)
            confidence = 0.5  # Sphinx doesn't provide confidence
            
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
            avg_logprob = whisper_result.get("avg_logprob", -1.0)
            confidence = max(0.0, min(1.0, (avg_logprob + 2.0) / 2.0))
            
            if whisper_result.get("language") == "en":
                confidence = min(1.0, confidence + 0.1)
            
            return confidence
            
        except Exception:
            return 0.5
    
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
            'language': 'English',
            'code': 'en',
            'engines': ['google', 'whisper', 'sphinx'],
            'energy_threshold': self.energy_threshold,
            'pause_threshold': self.pause_threshold,
            'features': [
                'Real-time speech recognition',
                'Multiple recognition engines',
                'Automatic text cleaning',
                'Comprehensive scoring',
                'Fluency analysis',
                'Pronunciation feedback'
            ]
        }

# Test the system
if __name__ == "__main__":
    converter = RobustEnglishAudioToText()
    
    print("🇺🇸 ROBUST ENGLISH AUDIO-TO-TEXT SYSTEM")
    print("=" * 60)
    
    # Test system info
    info = converter.get_system_info()
    print(f"System Info:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print(f"\n✅ Robust English Audio-to-Text System Ready!")
