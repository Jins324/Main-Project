#!/usr/bin/env python
"""
Audio Recording and Scoring System
Supports both English and Malayalam audio recording with comprehensive scoring
"""
import os
import sys
import django

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from django.db import models
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

class AudioRecordingSystem:
    """Comprehensive audio recording and scoring system"""
    
    def __init__(self):
        self.supported_languages = {
            'en': {
                'name': 'English',
                'recognition_engine': 'google',
                'scoring_model': 'english_pronunciation',
                'confidence_threshold': 0.7
            },
            'ml': {
                'name': 'Malayalam',
                'recognition_engine': 'whisper_malayalam',
                'scoring_model': 'malayalam_pronunciation',
                'confidence_threshold': 0.6
            }
        }
    
    def get_recording_config(self, language):
        """Get recording configuration for specific language"""
        return {
            'language': language,
            'sample_rate': 16000,
            'channels': 1,
            'format': 'wav',
            'max_duration': 30,  # seconds
            'min_duration': 1,   # seconds
            'silence_threshold': 0.01,
            **self.supported_languages.get(language, self.supported_languages['en'])
        }
    
    def process_audio_recording(self, audio_file, expected_text, language='en'):
        """Process audio recording and generate comprehensive score"""
        
        config = self.get_recording_config(language)
        
        try:
            # Step 1: Speech Recognition
            recognized_text = self.speech_to_text(audio_file, language)
            
            # Step 2: Pronunciation Scoring
            pronunciation_score = self.calculate_pronunciation_score(
                recognized_text, expected_text, language
            )
            
            # Step 3: Fluency Analysis
            fluency_score = self.analyze_fluency(audio_file, language)
            
            # Step 4: Accuracy Assessment
            accuracy_score = self.calculate_accuracy(
                recognized_text, expected_text, language
            )
            
            # Step 5: Overall Score Calculation
            overall_score = self.calculate_overall_score(
                pronunciation_score, fluency_score, accuracy_score
            )
            
            # Step 6: Generate Feedback
            feedback = self.generate_feedback(
                recognized_text, expected_text, overall_score, language
            )
            
            return {
                'success': True,
                'recognized_text': recognized_text,
                'expected_text': expected_text,
                'language': language,
                'scores': {
                    'pronunciation': pronunciation_score,
                    'fluency': fluency_score,
                    'accuracy': accuracy_score,
                    'overall': overall_score
                },
                'feedback': feedback,
                'audio_analysis': {
                    'duration': self.get_audio_duration(audio_file),
                    'quality': self.assess_audio_quality(audio_file),
                    'confidence': self.get_recognition_confidence(audio_file, language)
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Audio processing failed'
            }
    
    def speech_to_text(self, audio_file, language):
        """Convert speech to text using appropriate recognition engine"""
        
        if language == 'en':
            return self.english_speech_recognition(audio_file)
        elif language == 'ml':
            return self.malayalam_speech_recognition(audio_file)
        else:
            raise ValueError(f"Unsupported language: {language}")
    
    def english_speech_recognition(self, audio_file):
        """English speech recognition using Google Speech API"""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
            
            # Use Google Speech Recognition
            text = recognizer.recognize_google(audio, language='en-US')
            return text.lower().strip()
            
        except Exception as e:
            logger.error(f"English speech recognition error: {e}")
            return ""
    
    def malayalam_speech_recognition(self, audio_file):
        """Malayalam speech recognition using Whisper or local model"""
        try:
            # Try Whisper first (if available)
            try:
                import whisper
                model = whisper.load_model("base")
                result = model.transcribe(audio_file, language="ml")
                return result["text"].strip()
            except ImportError:
                # Fallback to Google Speech with Malayalam
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language="ml-IN")
                return text.strip()
                
        except Exception as e:
            logger.error(f"Malayalam speech recognition error: {e}")
            return ""
    
    def calculate_pronunciation_score(self, recognized_text, expected_text, language):
        """Calculate pronunciation score based on phonetic similarity"""
        
        if not recognized_text or not expected_text:
            return 0
        
        try:
            if language == 'en':
                return self.english_pronunciation_scoring(recognized_text, expected_text)
            elif language == 'ml':
                return self.malayalam_pronunciation_scoring(recognized_text, expected_text)
            else:
                return 50  # Default score
                
        except Exception as e:
            logger.error(f"Pronunciation scoring error: {e}")
            return 50
    
    def english_pronunciation_scoring(self, recognized_text, expected_text):
        """English pronunciation scoring using phonetic analysis"""
        
        try:
            from difflib import SequenceMatcher
            import Levenshtein
            
            # Text similarity
            similarity = SequenceMatcher(None, recognized_text.lower(), expected_text.lower()).ratio()
            
            # Levenshtein distance
            distance = Levenshtein.distance(recognized_text.lower(), expected_text.lower())
            max_len = max(len(recognized_text), len(expected_text))
            levenshtein_score = 1 - (distance / max_len) if max_len > 0 else 0
            
            # Word-level scoring
            recognized_words = recognized_text.lower().split()
            expected_words = expected_text.lower().split()
            
            correct_words = 0
            for word in recognized_words:
                if word in expected_words:
                    correct_words += 1
            
            word_accuracy = correct_words / len(expected_words) if expected_words else 0
            
            # Combined pronunciation score
            pronunciation_score = (similarity * 0.4 + levenshtein_score * 0.3 + word_accuracy * 0.3) * 100
            
            return min(100, max(0, pronunciation_score))
            
        except Exception as e:
            logger.error(f"English pronunciation scoring error: {e}")
            return 50
    
    def malayalam_pronunciation_scoring(self, recognized_text, expected_text):
        """Malayalam pronunciation scoring with Unicode handling"""
        
        try:
            from difflib import SequenceMatcher
            
            # Handle Malayalam Unicode text
            similarity = SequenceMatcher(None, recognized_text, expected_text).ratio()
            
            # Character-level scoring for Malayalam
            recognized_chars = list(recognized_text.replace(' ', ''))
            expected_chars = list(expected_text.replace(' ', ''))
            
            correct_chars = 0
            for char in recognized_chars:
                if char in expected_chars:
                    correct_chars += 1
            
            char_accuracy = correct_chars / len(expected_chars) if expected_chars else 0
            
            # Combined score
            pronunciation_score = (similarity * 0.6 + char_accuracy * 0.4) * 100
            
            return min(100, max(0, pronunciation_score))
            
        except Exception as e:
            logger.error(f"Malayalam pronunciation scoring error: {e}")
            return 50
    
    def analyze_fluency(self, audio_file, language):
        """Analyze speech fluency including pace, rhythm, and pauses"""
        
        try:
            import librosa
            import numpy as np
            
            # Load audio
            y, sr = librosa.load(audio_file, sr=16000)
            
            # Detect speech segments
            speech_segments = librosa.effects.split(y, top_db=20)
            
            # Calculate speaking time
            speaking_time = sum(end - start for start, end in speech_segments) / sr
            total_time = len(y) / sr
            
            # Speech ratio
            speech_ratio = speaking_time / total_time if total_time > 0 else 0
            
            # Pause analysis
            pause_count = len(speech_segments) - 1
            avg_pause_duration = self.calculate_average_pause_duration(speech_segments, sr)
            
            # Pace analysis (words per minute)
            pace_score = self.calculate_pace_score(speaking_time, language)
            
            # Fluency score calculation
            fluency_score = (
                speech_ratio * 40 +           # Speech ratio (40%)
                min(100, pace_score) * 30 +  # Pace (30%)
                min(100, (1 - min(avg_pause_duration, 2)) * 50) * 30  # Pauses (30%)
            )
            
            return min(100, max(0, fluency_score))
            
        except Exception as e:
            logger.error(f"Fluency analysis error: {e}")
            return 50
    
    def calculate_pace_score(self, speaking_time, language):
        """Calculate speaking pace score"""
        
        # Ideal speaking rates (words per minute)
        ideal_rates = {
            'en': 150,  # English
            'ml': 120   # Malayalam (slower due to complex sounds)
        }
        
        ideal_rate = ideal_rates.get(language, 150)
        
        # Estimate word count based on speaking time
        estimated_words = speaking_time * (ideal_rate / 60)
        
        # Simple pace scoring (this could be enhanced with actual word count)
        if 0.8 <= speaking_time <= 2.0:  # Ideal duration range
            return 100
        elif speaking_time < 0.8:
            return 80  # Too fast
        elif speaking_time > 2.0:
            return 70  # Too slow
        else:
            return 85
    
    def calculate_average_pause_duration(self, speech_segments, sr):
        """Calculate average pause duration between speech segments"""
        
        if len(speech_segments) <= 1:
            return 0
        
        pause_durations = []
        for i in range(len(speech_segments) - 1):
            pause_start = speech_segments[i][1]
            pause_end = speech_segments[i + 1][0]
            pause_duration = (pause_end - pause_start) / sr
            pause_durations.append(pause_duration)
        
        return sum(pause_durations) / len(pause_durations) if pause_durations else 0
    
    def calculate_accuracy(self, recognized_text, expected_text, language):
        """Calculate accuracy score based on text matching"""
        
        if not recognized_text or not expected_text:
            return 0
        
        try:
            from difflib import SequenceMatcher
            
            # Overall text similarity
            similarity = SequenceMatcher(None, recognized_text, expected_text).ratio()
            
            # Word accuracy
            recognized_words = recognized_text.split()
            expected_words = expected_text.split()
            
            if not expected_words:
                return 0
            
            correct_words = 0
            for word in recognized_words:
                if word in expected_words:
                    correct_words += 1
            
            word_accuracy = correct_words / len(expected_words)
            
            # Combined accuracy score
            accuracy_score = (similarity * 0.6 + word_accuracy * 0.4) * 100
            
            return min(100, max(0, accuracy_score))
            
        except Exception as e:
            logger.error(f"Accuracy calculation error: {e}")
            return 50
    
    def calculate_overall_score(self, pronunciation, fluency, accuracy):
        """Calculate overall score with weighted components"""
        
        weights = {
            'pronunciation': 0.4,
            'fluency': 0.3,
            'accuracy': 0.3
        }
        
        overall_score = (
            pronunciation * weights['pronunciation'] +
            fluency * weights['fluency'] +
            accuracy * weights['accuracy']
        )
        
        return min(100, max(0, overall_score))
    
    def generate_feedback(self, recognized_text, expected_text, overall_score, language):
        """Generate comprehensive feedback based on performance"""
        
        feedback = {
            'overall_message': '',
            'pronunciation_feedback': '',
            'fluency_feedback': '',
            'accuracy_feedback': '',
            'improvement_tips': [],
            'level': self.get_performance_level(overall_score)
        }
        
        # Overall message
        if overall_score >= 80:
            feedback['overall_message'] = 'Excellent! Your pronunciation is very clear and accurate!'
        elif overall_score >= 60:
            feedback['overall_message'] = 'Good job! Keep practicing to improve further.'
        elif overall_score >= 40:
            feedback['overall_message'] = 'Nice try! Focus on clarity and pace.'
        else:
            feedback['overall_message'] = 'Keep practicing! Listen carefully and try again.'
        
        # Specific feedback based on language
        if language == 'en':
            feedback['pronunciation_feedback'] = self.english_pronunciation_feedback(recognized_text, expected_text)
            feedback['fluency_feedback'] = self.english_fluency_feedback(recognized_text, expected_text)
        elif language == 'ml':
            feedback['pronunciation_feedback'] = self.malayalam_pronunciation_feedback(recognized_text, expected_text)
            feedback['fluency_feedback'] = self.malayalam_fluency_feedback(recognized_text, expected_text)
        
        # Accuracy feedback
        feedback['accuracy_feedback'] = self.accuracy_feedback(recognized_text, expected_text)
        
        # Improvement tips
        feedback['improvement_tips'] = self.get_improvement_tips(overall_score, language)
        
        return feedback
    
    def english_pronunciation_feedback(self, recognized_text, expected_text):
        """Generate English pronunciation feedback"""
        
        if not recognized_text:
            return "No speech detected. Please speak clearly into the microphone."
        
        # Check for common issues
        feedback_messages = []
        
        # Word missing feedback
        expected_words = set(expected_text.lower().split())
        recognized_words = set(recognized_text.lower().split())
        missing_words = expected_words - recognized_words
        
        if missing_words:
            feedback_messages.append(f"Missing words: {', '.join(list(missing_words)[:3])}")
        
        # Extra words feedback
        extra_words = recognized_words - expected_words
        if extra_words:
            feedback_messages.append(f"Extra words detected: {', '.join(list(extra_words)[:3])}")
        
        return " ".join(feedback_messages) if feedback_messages else "Pronunciation is clear and understandable."
    
    def malayalam_pronunciation_feedback(self, recognized_text, expected_text):
        """Generate Malayalam pronunciation feedback"""
        
        if not recognized_text:
            return "സംസാരം കണ്ടെത്തിയില്ല. ദയവായി മൈക്രോഫോണിൽ വ്യക്തമായി സംസാരിക്കുക."
        
        feedback_messages = []
        
        # Character-level feedback for Malayalam
        expected_chars = set(expected_text.replace(' ', ''))
        recognized_chars = set(recognized_text.replace(' ', ''))
        missing_chars = expected_chars - recognized_chars
        
        if missing_chars:
            feedback_messages.append("ചില അക്ഷരങ്ങൾ കാണുന്നില്ല. കൂടുതൽ ശ്രദ്ധയോടെ സംസാരിക്കുക.")
        
        return " ".join(feedback_messages) if feedback_messages else "ഉച്ചാരണം വ്യക്തവും മനസ്സിലാക്കാവുന്നതുമാണ്."
    
    def english_fluency_feedback(self, recognized_text, expected_text):
        """Generate English fluency feedback"""
        
        feedback_messages = []
        
        # Check speaking pace
        if len(recognized_text) < len(expected_text) * 0.5:
            feedback_messages.append("Try to speak at a steady pace without rushing.")
        elif len(recognized_text) > len(expected_text) * 1.5:
            feedback_messages.append("You're speaking too quickly. Slow down for clarity.")
        
        return " ".join(feedback_messages) if feedback_messages else "Good speaking pace and rhythm."
    
    def malayalam_fluency_feedback(self, recognized_text, expected_text):
        """Generate Malayalam fluency feedback"""
        
        feedback_messages = []
        
        if len(recognized_text) < len(expected_text) * 0.5:
            feedback_messages.append("സ്ഥിരമായ വേഗത്തിൽ സംസാരിക്കാൻ ശ്രമിക്കുക.")
        elif len(recognized_text) > len(expected_text) * 1.5:
            feedback_messages.append("വളരെ വേഗം സംസാരിക്കുന്നു. വ്യക്തതയ്ക്കായി പതുക്കെ സംസാരിക്കുക.")
        
        return " ".join(feedback_messages) if feedback_messages else "നല്ല സംസാര വേഗതയും താളവും."
    
    def accuracy_feedback(self, recognized_text, expected_text):
        """Generate accuracy feedback"""
        
        if not recognized_text:
            return "Please speak clearly and try again."
        
        similarity = len(set(recognized_text.split()) & set(expected_text.split())) / len(set(expected_text.split()))
        
        if similarity >= 0.8:
            return "Excellent accuracy! Most words were recognized correctly."
        elif similarity >= 0.6:
            return "Good accuracy with some minor word recognition issues."
        elif similarity >= 0.4:
            return "Moderate accuracy. Focus on clear pronunciation of each word."
        else:
            return "Low accuracy. Please speak more clearly and slowly."
    
    def get_improvement_tips(self, overall_score, language):
        """Get improvement tips based on score and language"""
        
        tips = []
        
        if overall_score < 40:
            tips.extend([
                "Practice speaking slowly and clearly",
                "Listen to native speakers and imitate",
                "Record yourself and listen back"
            ])
        elif overall_score < 60:
            tips.extend([
                "Focus on proper pronunciation of difficult words",
                "Practice speaking in complete sentences",
                "Work on your speaking pace"
            ])
        elif overall_score < 80:
            tips.extend([
                "Refine your accent and intonation",
                "Practice with more complex sentences",
                "Work on fluency and natural speech patterns"
            ])
        
        # Language-specific tips
        if language == 'ml':
            tips.extend([
                "ശ്രദ്ധയോടെ ഓരോ അക്ഷരവും ഉച്ചരിക്കുക",
                "മലയാളം സിനിമകൾ കാണുകയും അനുകരിക്കുകയും ചെയ്യുക"
            ])
        elif language == 'en':
            tips.extend([
                "Watch English movies and series",
                "Practice with English speaking apps",
                "Read English books aloud"
            ])
        
        return tips[:5]  # Return top 5 tips
    
    def get_performance_level(self, overall_score):
        """Get performance level based on score"""
        
        if overall_score >= 90:
            return "Expert"
        elif overall_score >= 80:
            return "Advanced"
        elif overall_score >= 70:
            return "Intermediate"
        elif overall_score >= 60:
            return "Basic"
        else:
            return "Beginner"
    
    def get_audio_duration(self, audio_file):
        """Get audio file duration"""
        
        try:
            import librosa
            duration = librosa.get_duration(filename=audio_file)
            return duration
        except:
            return 0
    
    def assess_audio_quality(self, audio_file):
        """Assess audio quality"""
        
        try:
            import librosa
            import numpy as np
            
            y, sr = librosa.load(audio_file, sr=16000)
            
            # Calculate basic quality metrics
            rms = np.sqrt(np.mean(y**2))
            peak = np.max(np.abs(y))
            
            # Quality assessment
            if rms < 0.01:
                return "Too quiet"
            elif rms > 0.9:
                return "Too loud"
            elif peak > 0.95:
                return "Clipping detected"
            else:
                return "Good"
                
        except:
            return "Unknown"
    
    def get_recognition_confidence(self, audio_file, language):
        """Get speech recognition confidence"""
        
        try:
            if language == 'en':
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    audio = recognizer.record(source)
                
                # Try to get confidence (if available)
                try:
                    result = recognizer.recognize_google(audio, language='en-US', show_all=True)
                    if result and 'alternative' in result:
                        return result['alternative'][0].get('confidence', 0.8)
                except:
                    pass
            
            return 0.8  # Default confidence
            
        except:
            return 0.5

# Test the system
if __name__ == "__main__":
    system = AudioRecordingSystem()
    
    print("🎤 Audio Recording and Scoring System")
    print("=" * 50)
    
    # Test configurations
    for lang in ['en', 'ml']:
        config = system.get_recording_config(lang)
        print(f"\n📋 {config['name']} Configuration:")
        print(f"   Engine: {config['recognition_engine']}")
        print(f"   Scoring Model: {config['scoring_model']}")
        print(f"   Confidence Threshold: {config['confidence_threshold']}")
        print(f"   Sample Rate: {config['sample_rate']} Hz")
        print(f"   Max Duration: {config['max_duration']} seconds")
    
    print(f"\n✅ Audio Recording and Scoring System Ready!")
    print(f"🎯 Features:")
    print(f"   • English and Malayalam speech recognition")
    print(f"   • Comprehensive pronunciation scoring")
    print(f"   • Fluency analysis")
    print(f"   • Accuracy assessment")
    print(f"   • Detailed feedback and improvement tips")
    print(f"   • Audio quality assessment")
