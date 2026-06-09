"""
Simple Malayalam Audio-to-Text Converter
Just converts audio files to text and provides scoring
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

class SimpleMalayalamAudioToText:
    """Simple Malayalam audio-to-text converter"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speech_system = MalayalamSpeechSystem()
        self.language = 'ml-IN'
        
        # Configure recognizer for Malayalam
        self.recognizer.energy_threshold = 250
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.9
        
        logger.info("Simple Malayalam Audio-to-Text Converter initialized")
    
    def convert_audio_to_text(self, audio_file_path: str, expected_text: str = "") -> Dict:
        """Convert audio file to text and score it"""
        
        try:
            logger.info(f"Converting Malayalam audio: {audio_file_path}")
            
            # Validate audio file
            if not os.path.exists(audio_file_path):
                return {
                    'success': False,
                    'text': '',
                    'scores': {'overall': 0.0, 'pronunciation': 0.0, 'fluency': 0.0, 'accuracy': 0.0},
                    'feedback': {'overall_message': 'Audio file not found', 'improvement_tips': []},
                    'error': 'Audio file not found'
                }
            
            # Load and convert audio
            with sr.AudioFile(audio_file_path) as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio_data = self.recognizer.record(source)
            
            # Try speech recognition
            text = self._recognize_speech(audio_data)
            
            if text:
                # Clean Malayalam text
                cleaned_text = self._clean_malayalam_text(text)
                
                # Score the recognized text
                scores = self._score_text(cleaned_text, expected_text)
                feedback = self._generate_feedback(cleaned_text, expected_text, scores)
                
                return {
                    'success': True,
                    'text': cleaned_text,
                    'confidence': 0.7,  # Lower confidence for Malayalam
                    'engine': 'google',
                    'scores': scores,
                    'feedback': feedback,
                    'malayalam_validation': self._validate_malayalam_text(cleaned_text)
                }
            else:
                return {
                    'success': False,
                    'text': '',
                    'scores': {'overall': 0.0, 'pronunciation': 0.0, 'fluency': 0.0, 'accuracy': 0.0},
                    'feedback': {'overall_message': 'No speech detected', 'improvement_tips': ['തെവരിയായ വിലം സംസായായായായ', 'ദയിലം സംസായായായായ'],
                    'error': 'No speech detected'
                }
                
        except Exception as e:
            logger.error(f"Error converting Malayalam audio: {e}")
            return {
                'success': False,
                'text': '',
                'scores': {'overall': 0.0, 'pronunciation': 0.0, 'system_error': str(e)},
                'feedback': {'overall_message': 'Conversion error', 'improvement_tips': []},
                'error': str(e)
            }
    
    def _recognize_speech(self, audio_data) -> str:
        """Recognize speech from audio data"""
        
        try:
            # Try Google Speech Recognition
            text = self.recognizer.recognize_google(audio_data, language=self.language)
            return text
            
        except sr.UnknownValueError:
            try:
                # Try Whisper
                import whisper
                model = whisper.load_model("base")
                result = model.transcribe(audio_data, language="ml")
                return result.get("text", "").strip()
            except:
                return ""
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return ""
    
    def _clean_malayalam_text(self, text: str) -> str:
        """Clean and normalize Malayalam text"""
        
        if not text:
            return ""
        
        # Normalize Unicode
        text = unicodedata.normalize('NFC', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common Malayalam artifacts
        artifacts = ['ഉം', 'എന്ന്', 'ആണ്', 'ഉണ്ട്', 'മാത്രം']
        words = text.split()
        words = [word for word in words if word not in artifacts]
        
        # Reconstruct text
        cleaned = ' '.join(words)
        
        # Remove non-Malayalam characters except spaces and basic punctuation
        malayalam_pattern = re.compile(r'[\u0D00-\u0D7F\s\.\,\!\?\;\;\:]')
        matches = malayalam_pattern.findall(cleaned)
        cleaned = ''.join(matches)
        
        # Remove extra spaces
        cleaned = ' '.join(cleaned.split())
        
        return cleaned.strip()
    
    def _score_text(self, recognized_text: str, expected_text: str) -> Dict:
        """Score recognized text against expected text"""
        
        try:
            if not recognized_text or not expected_text:
                return {'overall': 0.0, 'pronunciation': 0.0, 'fluency': 0.0, 'accuracy': 0.0}
            
            # Use speech system for detailed scoring
            scores = self.speech_system.calculate_pronunciation_score(recognized_text, expected_text)
            
            return scores
            
        except Exception as e:
            logger.error(f"Error scoring text: {e}")
            return {'overall': 0.0, 'pronunciation': 0.0, 'fluency': 0.0, 'accuracy': 0.0}
    
    def _generate_feedback(self, recognized_text: str, expected_text: str, scores: Dict) -> Dict:
        """Generate feedback based on scoring"""
        
        try:
            overall_score = scores.get('overall', 0.0)
            
            if overall_score >= 80:
                message = "അതിചെ! നിന്റെ ഉചിയായായായ."
                tips = ["ഈ നിന്റെ മിലം സംസായായായ.", "പയമാത്രം പയമാത്രം സംസായായായ."]
            elif overall_score >= 60:
                message = "നന്നതം! നിന്റെ ഉചിയായായ."
                tips = ["വായായായ പയമാത്രം സംസായായായ.", "സാവന് പയമാത്രം സംസായായായ."]
            elif overall_score >= 40:
                message = "ശരായായായ. നിന്റെ ഉചിയായായ."
                tips = ["കൂർ വായായായ.", "പടം സംസായായായ.", "തായായായം സംസായായ."]
            else:
                message = "പയമാത്രം സംസായായായ."
                tips = ["ലളിന്റെ ഉചിയായായ.", "പടം സംസായായായ."]
            
            return {
                'overall_message': message,
                'improvement_tips': tips
            }
            
        except Exception as e:
            logger.error(f"Error generating feedback: {e}")
            return {'overall_message': 'No feedback available', 'improvement_tips': []}
    
    def _validate_malayalam_text(self, text: str) -> Dict:
        """Validate if text is proper Malayalam"""
        
        try:
            if not text:
                return {'is_malayalam': False, 'confidence': 0.0, 'issues': ['Empty text']}
            
            # Check Unicode normalization
            normalized = unicodedata.normalize('NFC', text)
            if text != normalized:
                return {'is_malayalam': False, 'confidence': 0.0, 'issues': ['Unicode not normalized']}
            
            # Check for Malayalam characters
            malayalam_chars = re.findall(r'[\u0D00-\u0D7F]', text)
            total_chars = len(text.replace(' ', ''))
            
            if total_chars == 0:
                return {'is_malayalam': False, 'confidence': 0.0, 'issues': ['No characters found']}
            
            malayalam_ratio = len(malayalam_chars) / total_chars
            
            # Calculate overall confidence
            confidence = malayalam_ratio * 0.9
            
            issues = []
            if malayalam_ratio < 0.8:
                issues.append(f'Low Malayalam character ratio: {malayalam_ratio:.2f}')
            
            return {
                'is_malayalam': confidence > 0.6,
                'confidence': confidence,
                'malayalam_ratio': malayalam_ratio,
                'issues': issues if issues else ['Valid Malayalam text']
            }
            
        except Exception as e:
            return {'is_malayalam': False, 'confidence': 0.0, 'issues': [f'Validation error: {e}']}

# Test the system
if __name__ == "__main__":
    converter = SimpleMalayalamAudioToText()
    
    print("🇮🇳 SIMPLE MALAYALAM AUDIO-TO-TEXT CONVERTER")
    print("=" * 50)
    
    print("✅ Simple system ready for audio-to-text conversion and scoring")
