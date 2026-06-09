"""
Unified Speech Processing System
Coordinates English and Malayalam speech recognition and audio generation
"""
import os
import logging
from english_speech_system import EnglishSpeechSystem
from malayalam_speech_system import MalayalamSpeechSystem

logger = logging.getLogger(__name__)

class UnifiedSpeechProcessor:
    """Main coordinator for language-specific speech processing"""
    
    def __init__(self):
        # Initialize language-specific systems
        self.english_system = EnglishSpeechSystem()
        self.malayalam_system = MalayalamSpeechSystem()
        
        # Language mapping
        self.language_systems = {
            'en': self.english_system,
            'english': self.english_system,
            'ml': self.malayalam_system,
            'malayalam': self.malayalam_system
        }
        
        logger.info("Unified Speech Processor initialized with English and Malayalam systems")
    
    def recognize_speech(self, audio_file_path, language='en'):
        """Recognize speech using language-specific system"""
        
        try:
            # Normalize language code
            lang_code = language.lower()
            if lang_code not in self.language_systems:
                logger.error(f"Unsupported language: {language}")
                return {
                    'text': '',
                    'confidence': 0.0,
                    'language': language,
                    'engine': 'none',
                    'error': f'Unsupported language: {language}'
                }
            
            # Get appropriate system
            speech_system = self.language_systems[lang_code]
            
            # Use language-specific recognition
            result = speech_system.recognize_speech(audio_file_path)
            
            logger.info(f"Speech recognition completed for {language}: '{result.get('text', '')[:50]}...'")
            return result
            
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return {
                'text': '',
                'confidence': 0.0,
                'language': language,
                'engine': 'error',
                'error': str(e)
            }
    
    def generate_audio(self, text, language='en', output_path=None, voice_type='default'):
        """Generate audio using language-specific system"""
        
        try:
            # Normalize language code
            lang_code = language.lower()
            if lang_code not in self.language_systems:
                logger.error(f"Unsupported language: {language}")
                return None
            
            # Get appropriate system
            speech_system = self.language_systems[lang_code]
            
            # Use language-specific audio generation
            result = speech_system.generate_audio(text, output_path, voice_type)
            
            logger.info(f"Audio generation completed for {language}: {len(text) if text else 0} characters")
            return result
            
        except Exception as e:
            logger.error(f"Audio generation error: {e}")
            return None
    
    def calculate_pronunciation_score(self, recognized_text, expected_text, language='en'):
        """Calculate pronunciation score using language-specific system"""
        
        try:
            # Normalize language code
            lang_code = language.lower()
            if lang_code not in self.language_systems:
                logger.error(f"Unsupported language: {language}")
                return 50.0
            
            # Get appropriate system
            speech_system = self.language_systems[lang_code]
            
            # Use language-specific scoring
            score = speech_system.calculate_pronunciation_score(recognized_text, expected_text)
            
            logger.info(f"Pronunciation scoring completed for {language}: {score:.1f}")
            return score
            
        except Exception as e:
            logger.error(f"Pronunciation scoring error: {e}")
            return 50.0
    
    def analyze_fluency(self, audio_file_path, recognized_text, expected_text, language='en'):
        """Analyze fluency using language-specific system"""
        
        try:
            # Normalize language code
            lang_code = language.lower()
            if lang_code not in self.language_systems:
                logger.error(f"Unsupported language: {language}")
                return {'score': 50.0}
            
            # Get appropriate system
            speech_system = self.language_systems[lang_code]
            
            # Use language-specific fluency analysis
            result = speech_system.analyze_fluency(audio_file_path, recognized_text, expected_text)
            
            logger.info(f"Fluency analysis completed for {language}: {result.get('score', 0):.1f}")
            return result
            
        except Exception as e:
            logger.error(f"Fluency analysis error: {e}")
            return {'score': 50.0}
    
    def get_language_system_info(self, language='en'):
        """Get information about a specific language system"""
        
        try:
            # Normalize language code
            lang_code = language.lower()
            if lang_code not in self.language_systems:
                logger.error(f"Unsupported language: {language}")
                return None
            
            # Get appropriate system
            speech_system = self.language_systems[lang_code]
            
            # Return system information
            return speech_system.get_system_info()
            
        except Exception as e:
            logger.error(f"System info error: {e}")
            return None
    
    def get_all_systems_info(self):
        """Get information about all language systems"""
        
        try:
            systems_info = {}
            
            for lang_code, speech_system in self.language_systems.items():
                systems_info[lang_code] = speech_system.get_system_info()
            
            return systems_info
            
        except Exception as e:
            logger.error(f"All systems info error: {e}")
            return {}
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        
        return {
            'en': {
                'name': 'English',
                'code': 'en',
                'system': 'english_system'
            },
            'ml': {
                'name': 'Malayalam',
                'code': 'ml',
                'system': 'malayalam_system'
            }
        }
    
    def process_audio_recording(self, audio_file_path, expected_text, language='en'):
        """Process complete audio recording with scoring"""
        
        try:
            logger.info(f"Processing audio recording for {language}")
            
            # Step 1: Speech recognition
            recognition_result = self.recognize_speech(audio_file_path, language)
            recognized_text = recognition_result.get('text', '')
            confidence = recognition_result.get('confidence', 0.0)
            
            # Step 2: Pronunciation scoring
            pronunciation_score = self.calculate_pronunciation_score(
                recognized_text, expected_text, language
            )
            
            # Step 3: Fluency analysis
            fluency_result = self.analyze_fluency(
                audio_file_path, recognized_text, expected_text, language
            )
            fluency_score = fluency_result.get('score', 50.0)
            
            # Step 4: Accuracy calculation
            accuracy_score = self._calculate_accuracy(
                recognized_text, expected_text, language
            )
            
            # Step 5: Overall score calculation
            overall_score = self._calculate_overall_score(
                pronunciation_score, fluency_score, accuracy_score, language
            )
            
            # Step 6: Generate feedback
            feedback = self._generate_feedback(
                recognized_text, expected_text, overall_score, language
            )
            
            # Return comprehensive result
            return {
                'success': True,
                'language': language,
                'recognized_text': recognized_text,
                'expected_text': expected_text,
                'confidence': confidence,
                'scores': {
                    'pronunciation': pronunciation_score,
                    'fluency': fluency_score,
                    'accuracy': accuracy_score,
                    'overall': overall_score
                },
                'fluency_details': fluency_result,
                'feedback': feedback,
                'recognition_engine': recognition_result.get('engine', 'unknown')
            }
            
        except Exception as e:
            logger.error(f"Audio processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'language': language
            }
    
    def _calculate_accuracy(self, recognized_text, expected_text, language):
        """Calculate accuracy score using language-specific approach"""
        
        try:
            if not recognized_text or not expected_text:
                return 0.0
            
            # Use language-specific system for accuracy
            speech_system = self.language_systems.get(language.lower())
            if not speech_system:
                return 50.0
            
            # For English, use word-level accuracy
            if language.lower() in ['en', 'english']:
                recognized_words = recognized_text.lower().split()
                expected_words = expected_text.lower().split()
                
                if not expected_words:
                    return 0.0
                
                correct_words = sum(1 for word in recognized_words if word in expected_words)
                accuracy = (correct_words / len(expected_words)) * 100
                
            # For Malayalam, use character-level accuracy
            else:
                from difflib import SequenceMatcher
                accuracy = SequenceMatcher(None, recognized_text, expected_text).ratio() * 100
            
            return min(100.0, max(0.0, accuracy))
            
        except Exception as e:
            logger.error(f"Accuracy calculation error: {e}")
            return 50.0
    
    def _calculate_overall_score(self, pronunciation, fluency, accuracy, language):
        """Calculate overall score with language-specific weighting"""
        
        try:
            # Language-specific weights
            if language.lower() in ['en', 'english']:
                # English: more emphasis on pronunciation
                weights = {
                    'pronunciation': 0.4,
                    'fluency': 0.3,
                    'accuracy': 0.3
                }
            else:
                # Malayalam: more emphasis on accuracy (character matching)
                weights = {
                    'pronunciation': 0.3,
                    'fluency': 0.3,
                    'accuracy': 0.4
                }
            
            # Calculate weighted score
            overall_score = (
                pronunciation * weights['pronunciation'] +
                fluency * weights['fluency'] +
                accuracy * weights['accuracy']
            )
            
            return min(100.0, max(0.0, overall_score))
            
        except Exception as e:
            logger.error(f"Overall score calculation error: {e}")
            return 50.0
    
    def _generate_feedback(self, recognized_text, expected_text, overall_score, language):
        """Generate language-specific feedback"""
        
        try:
            feedback = {
                'overall_message': '',
                'pronunciation_feedback': '',
                'fluency_feedback': '',
                'accuracy_feedback': '',
                'improvement_tips': [],
                'level': self._get_performance_level(overall_score)
            }
            
            # Language-specific feedback
            if language.lower() in ['en', 'english']:
                feedback = self._generate_english_feedback(
                    recognized_text, expected_text, overall_score, feedback
                )
            else:
                feedback = self._generate_malayalam_feedback(
                    recognized_text, expected_text, overall_score, feedback
                )
            
            return feedback
            
        except Exception as e:
            logger.error(f"Feedback generation error: {e}")
            return {
                'overall_message': 'Feedback generation failed',
                'level': 'Unknown'
            }
    
    def _generate_english_feedback(self, recognized_text, expected_text, overall_score, feedback):
        """Generate English-specific feedback"""
        
        # Overall message
        if overall_score >= 80:
            feedback['overall_message'] = 'Excellent! Your English pronunciation is very clear and accurate!'
        elif overall_score >= 60:
            feedback['overall_message'] = 'Good job! Your English pronunciation is quite good with room for improvement.'
        elif overall_score >= 40:
            feedback['overall_message'] = 'Nice try! Focus on clear pronunciation of each word.'
        else:
            feedback['overall_message'] = 'Keep practicing! Listen carefully to English pronunciation and try again.'
        
        # Specific feedback
        feedback['pronunciation_feedback'] = self._get_english_pronunciation_feedback(recognized_text, expected_text)
        feedback['fluency_feedback'] = self._get_english_fluency_feedback(recognized_text, expected_text)
        feedback['accuracy_feedback'] = self._get_english_accuracy_feedback(recognized_text, expected_text)
        
        # Improvement tips
        feedback['improvement_tips'] = self._get_english_improvement_tips(overall_score)
        
        return feedback
    
    def _generate_malayalam_feedback(self, recognized_text, expected_text, overall_score, feedback):
        """Generate Malayalam-specific feedback"""
        
        # Overall message
        if overall_score >= 80:
            feedback['overall_message'] = 'അത്യുത്തം! നിങ്ങളുടെ മലയാളം ഉച്ചാരണം വളരെ വ്യക്തവും കൃത്യവുമാണ്!'
        elif overall_score >= 60:
            feedback['overall_message'] = 'നല്ല! നിങ്ങളുടെ മലയാളം ഉച്ചാരണം നല്ലാതെ നല്ലാണ്, മെച്ചപ്പെട്ടാൻ സ്ഥലം ഉണ്ട്.'
        elif overall_score >= 40:
            feedback['overall_message'] = 'നന്ദി! ഓരോ വാക്യത്തിന്റെ വ്യക്തമായ ഉച്ചാരണത്തിൽ ശ്രദ്ധിക്കുക.'
        else:
            feedback['overall_message'] = 'തുടരുക! മലയാളം ഉച്ചാരണം ശ്രദ്ധിച്ച് കേൾക്കുകയും വീണ്ട് ശ്രമിക്കുക.'
        
        # Specific feedback
        feedback['pronunciation_feedback'] = self._get_malayalam_pronunciation_feedback(recognized_text, expected_text)
        feedback['fluency_feedback'] = self._get_malayalam_fluency_feedback(recognized_text, expected_text)
        feedback['accuracy_feedback'] = self._get_malayalam_accuracy_feedback(recognized_text, expected_text)
        
        # Improvement tips
        feedback['improvement_tips'] = self._get_malayalam_improvement_tips(overall_score)
        
        return feedback
    
    def _get_english_pronunciation_feedback(self, recognized_text, expected_text):
        """Get English pronunciation feedback"""
        
        if not recognized_text:
            return "No speech detected. Please speak clearly into the microphone."
        
        # Check for common issues
        issues = []
        
        expected_words = set(expected_text.lower().split())
        recognized_words = set(recognized_text.lower().split())
        
        missing_words = expected_words - recognized_words
        extra_words = recognized_words - expected_words
        
        if missing_words:
            issues.append(f"Missing words: {', '.join(list(missing_words)[:3])}")
        
        if extra_words:
            issues.append(f"Extra words detected: {', '.join(list(extra_words)[:3])}")
        
        return " | ".join(issues) if issues else "Pronunciation is clear and understandable."
    
    def _get_malayalam_pronunciation_feedback(self, recognized_text, expected_text):
        """Get Malayalam pronunciation feedback"""
        
        if not recognized_text:
            return "സംസാരം കണ്ടെത്തിയില്ല. ദയവായി മൈക്രോഫോണിൽ വ്യക്തമായി സംസാരിക്കുക."
        
        # Check for Malayalam-specific issues
        issues = []
        
        expected_chars = set(expected_text.replace(' ', ''))
        recognized_chars = set(recognized_text.replace(' ', ''))
        
        missing_chars = expected_chars - recognized_chars
        
        if missing_chars:
            issues.append("ചില അക്ഷരങ്ങൾ കാണുന്നില്ല. കൂടുതൽ ശ്രദ്ധിച്ച് സംസാരിക്കുക.")
        
        return " | ".join(issues) if issues else "ഉച്ചാരണം വ്യക്തവും മനസ്സിലാക്കാവുന്നു."
    
    def _get_english_fluency_feedback(self, recognized_text, expected_text):
        """Get English fluency feedback"""
        
        if len(recognized_text) < len(expected_text) * 0.5:
            return "Try to speak at a steady pace without rushing."
        elif len(recognized_text) > len(expected_text) * 1.5:
            return "You're speaking too quickly. Slow down for clarity."
        else:
            return "Good speaking pace and rhythm."
    
    def _get_malayalam_fluency_feedback(self, recognized_text, expected_text):
        """Get Malayalam fluency feedback"""
        
        if len(recognized_text) < len(expected_text) * 0.5:
            return "സ്ഥിരമായ വേഗത്തിൽ സംസാരിക്കാൻ ശ്രമിക്കുക."
        elif len(recognized_text) > len(expected_text) * 1.5:
            return "വളരെ വേഗത്തിൽ സംസാരിക്കുന്നു. വ്യക്തതയ്ക്കായി പതുക്കെ സംസാരിക്കുക."
        else:
            return "നല്ലായ സംസാര വേഗതയും താളവും."
    
    def _get_english_accuracy_feedback(self, recognized_text, expected_text):
        """Get English accuracy feedback"""
        
        if not recognized_text:
            return "Please speak clearly and try again."
        
        similarity = self._calculate_text_similarity(recognized_text, expected_text)
        
        if similarity >= 0.8:
            return "Excellent accuracy! Most words were recognized correctly."
        elif similarity >= 0.6:
            return "Good accuracy with some minor word recognition issues."
        elif similarity >= 0.4:
            return "Moderate accuracy. Focus on clear pronunciation of each word."
        else:
            return "Low accuracy. Please speak more clearly and slowly."
    
    def _get_malayalam_accuracy_feedback(self, recognized_text, expected_text):
        """Get Malayalam accuracy feedback"""
        
        if not recognized_text:
            return "ദയവായി വ്യക്തമായി ശ്രമിച്ച് വീണ്ട് ശ്രമിക്കുക."
        
        similarity = self._calculate_text_similarity(recognized_text, expected_text)
        
        if similarity >= 0.8:
            return "അത്യുത്തം! ഭൂരിഭാഗം വാക്യങ്ങൾ ശരിയായി തിരിച്ചു."
        elif similarity >= 0.6:
            return "നല്ല! ചില ചെറിയ വാക്യം തിരിച്ചു പ്രശ്നങ്ങൾ ഉണ്ട്."
        elif similarity >= 0.4:
            return "ഇടത്തും കൃത്യം. ഓരോ വാക്യത്തിന്റെ വ്യക്തമായ ഉച്ചാരണത്തിൽ ശ്രദ്ധിക്കുക."
        else:
            return "കുറഞ്ഞ് കൃത്യം. കൂടുതൽ വ്യക്തമായി സംസാരിക്കുകയും പതുക്കെ സംസാരിക്കുക."
    
    def _get_english_improvement_tips(self, overall_score):
        """Get English improvement tips"""
        
        tips = []
        
        if overall_score < 40:
            tips.extend([
                "Practice speaking slowly and clearly",
                "Listen to native English speakers",
                "Record yourself and listen back"
            ])
        elif overall_score < 60:
            tips.extend([
                "Focus on proper word pronunciation",
                "Practice English rhythm and intonation",
                "Use a mirror to watch mouth movements"
            ])
        elif overall_score < 80:
            tips.extend([
                "Work on reducing filler words",
                "Practice with longer sentences",
                "Improve your speaking pace"
            ])
        else:
            tips.extend([
                "Great job! Keep practicing",
                "Try more complex sentences",
                "Work on accent refinement"
            ])
        
        return tips[:5]
    
    def _get_malayalam_improvement_tips(self, overall_score):
        """Get Malayalam improvement tips"""
        
        tips = []
        
        if overall_score < 40:
            tips.extend([
                "ശ്രദ്ധിച്ച് പതുക്കെ സംസാരിക്കുക",
                "മലയാളം സിനിമകൾ കാണുകയും അനുകരിക്കുക",
                "സ്വന്തം റെക്കോർഡ് ചെയ്ത്ത് കേൾക്കുക"
            ])
        elif overall_score < 60:
            tips.extend([
                "ഓരോ അക്ഷരത്തിന്റെ ശരിയായി ഉച്ചാരണം ശ്രദ്ധിക്കുക",
                "മലയാളം താളവും ലയത്തിൽ ശ്രദ്ധിക്കുക",
                "കണ്ണാടി മുന്നുന്ന് സംസാരിക്കുക"
            ])
        elif overall_score < 80:
            tips.extend([
                "ദീർഘമായ വാക്യങ്ങൾ ഉപയോഗിക്കുക",
                "ദീർഘമായ വാക്യങ്ങൾ ഉച്ചാരണത്തിൽ ശ്രദ്ധിക്കുക",
                "സ്വാഭാവികമായ സംസാരം പരിശീലനം നൽകുക"
            ])
        else:
            tips.extend([
                "അത്യുത്തം! തുടരുക",
                "കൂടുതൽ സങ്കീർഷ്നം പരിശീലനം നൽകുക",
                "മലയാളം സാഹിത്യങ്ങൾ വായിക്കുക"
            ])
        
        return tips[:5]
    
    def _calculate_text_similarity(self, text1, text2):
        """Calculate text similarity"""
        
        if not text1 or not text2:
            return 0.0
        
        from difflib import SequenceMatcher
        return SequenceMatcher(None, text1, text2).ratio()
    
    def _get_performance_level(self, overall_score):
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

# Test the unified system
if __name__ == "__main__":
    processor = UnifiedSpeechProcessor()
    
    print("🌍 UNIFIED SPEECH PROCESSOR")
    print("=" * 50)
    
    # Test system info
    systems_info = processor.get_all_systems_info()
    for lang, info in systems_info.items():
        print(f"\n{info['language']} System:")
        print(f"  Recognition: {', '.join(info['recognition_engines'])}")
        print(f"  TTS: {info['tts_engine']}")
    
    # Test English processing
    print(f"\n🧪 Testing English Processing:")
    result = processor.process_audio_recording(
        "test_audio.wav", "hello world", "en"
    )
    print(f"English result: {result.get('success', False)}")
    if result.get('success'):
        print(f"  Overall score: {result['scores']['overall']:.1f}")
    
    # Test Malayalam processing
    print(f"\n🧪 Testing Malayalam Processing:")
    result = processor.process_audio_recording(
        "test_audio.wav", "നമസ്കാരം", "ml"
    )
    print(f"Malayalam result: {result.get('success', False)}")
    if result.get('success'):
        print(f"  Overall score: {result['scores']['overall']:.1f}")
    
    print(f"\n✅ Unified Speech Processor Ready!")
