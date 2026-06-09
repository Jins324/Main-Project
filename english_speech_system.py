"""
English Speech Recognition and Audio Generation System
Specialized for English language processing
"""
import os
import logging
import speech_recognition as sr
from gtts import gTTS
import tempfile
import io
from pydub import AudioSegment
import numpy as np
from difflib import SequenceMatcher

# Optional imports with fallbacks
try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    logging.warning("librosa not available - fluency analysis will be limited")

try:
    import Levenshtein
    LEVENSHTEIN_AVAILABLE = True
except ImportError:
    LEVENSHTEIN_AVAILABLE = False
    logging.warning("Levenshtein not available - using alternative distance calculation")

logger = logging.getLogger(__name__)

class EnglishSpeechSystem:
    """Specialized English speech recognition and audio generation"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.language = 'en-US'
        self.tts_lang = 'en'
        
        # English-specific settings
        self.confidence_threshold = 0.7
        self.max_recording_duration = 30
        self.sample_rate = 16000
        
        # Initialize recognizer settings for English
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        logger.info("English Speech System initialized")
    
    def recognize_speech(self, audio_file_path):
        """Recognize English speech from audio file"""
        
        try:
            logger.info(f"Starting English speech recognition for: {audio_file_path}")
            
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio_data = self.recognizer.record(source)
            
            # Try multiple recognition engines
            text = None
            confidence = 0.0
            
            # 1. Google Speech Recognition (primary)
            try:
                result = self.recognizer.recognize_google(
                    audio_data, 
                    language=self.language,
                    show_all=True
                )
                
                if result and 'alternative' in result:
                    text = result['alternative'][0]['transcript']
                    confidence = result['alternative'][0].get('confidence', 0.0)
                    logger.info(f"Google recognition: '{text}' (confidence: {confidence})")
                    
            except sr.UnknownValueError:
                logger.warning("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                logger.error(f"Google Speech Recognition error: {e}")
            
            # 2. Whisper as fallback (if available)
            if not text or confidence < self.confidence_threshold:
                try:
                    import whisper
                    model = whisper.load_model("base")
                    result = model.transcribe(audio_file_path, language="en")
                    
                    whisper_text = result["text"].strip()
                    whisper_confidence = result.get("avg_logprob", -10) / 10  # Convert to confidence
                    
                    if whisper_confidence > confidence:
                        text = whisper_text
                        confidence = max(whisper_confidence, 0.0)
                        logger.info(f"Whisper recognition: '{text}' (confidence: {confidence})")
                        
                except ImportError:
                    logger.warning("Whisper not available for English fallback")
                except Exception as e:
                    logger.error(f"Whisper recognition error: {e}")
            
            # 3. Sphinx as final fallback
            if not text:
                try:
                    sphinx_text = self.recognizer.recognize_sphinx(audio_data)
                    text = sphinx_text
                    confidence = 0.3  # Low confidence for Sphinx
                    logger.info(f"Sphinx recognition: '{text}' (confidence: {confidence})")
                    
                except sr.UnknownValueError:
                    logger.warning("Sphinx could not understand audio")
                except sr.RequestError as e:
                    logger.error(f"Sphinx error: {e}")
            
            # Clean and validate text
            if text:
                text = self._clean_english_text(text)
                logger.info(f"Final English recognition: '{text}' (confidence: {confidence})")
                return {
                    'text': text,
                    'confidence': confidence,
                    'language': 'en',
                    'engine': 'google' if confidence > 0.7 else 'whisper' if confidence > 0.5 else 'sphinx'
                }
            else:
                logger.warning("No English speech recognized")
                return {
                    'text': '',
                    'confidence': 0.0,
                    'language': 'en',
                    'engine': 'none'
                }
                
        except Exception as e:
            logger.error(f"English speech recognition error: {e}")
            return {
                'text': '',
                'confidence': 0.0,
                'language': 'en',
                'engine': 'error',
                'error': str(e)
            }
    
    def generate_audio(self, text, output_path=None, voice_type='default'):
        """Generate English audio from text"""
        
        try:
            logger.info(f"Generating English audio for: '{text[:50]}...'")
            
            # Clean and validate text
            clean_text = self._clean_english_text(text)
            if not clean_text:
                logger.warning("No valid English text for audio generation")
                return None
            
            # Configure TTS based on voice type
            tts_config = self._get_tts_config(voice_type)
            
            # Generate audio using gTTS
            tts = gTTS(
                text=clean_text,
                lang=self.tts_lang,
                slow=tts_config['slow'],
                tld=tts_config['tld']
            )
            
            # Save to file or return bytes
            if output_path:
                tts.save(output_path)
                logger.info(f"English audio saved to: {output_path}")
                return output_path
            else:
                # Return as bytes
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                return audio_bytes.getvalue()
                
        except Exception as e:
            logger.error(f"English audio generation error: {e}")
            return None
    
    def calculate_pronunciation_score(self, recognized_text, expected_text):
        """Calculate English pronunciation score"""
        
        try:
            if not recognized_text or not expected_text:
                return 0.0
            
            # Clean texts
            recognized = self._clean_english_text(recognized_text.lower())
            expected = self._clean_english_text(expected_text.lower())
            
            # Multiple scoring methods
            scores = []
            
            # 1. SequenceMatcher (text similarity)
            seq_score = SequenceMatcher(None, recognized, expected).ratio()
            scores.append(seq_score * 100)
            
            # 2. Levenshtein distance (edit distance)
            if recognized and expected and LEVENSHTEIN_AVAILABLE:
                distance = Levenshtein.distance(recognized, expected)
                max_len = max(len(recognized), len(expected))
                lev_score = (1 - distance / max_len) * 100 if max_len > 0 else 0
                scores.append(lev_score)
            elif recognized and expected:
                # Alternative distance calculation using SequenceMatcher
                lev_score = SequenceMatcher(None, recognized, expected).ratio() * 100
                scores.append(lev_score)
            
            # 3. Word-level accuracy
            recognized_words = recognized.split()
            expected_words = expected.split()
            
            if expected_words:
                word_matches = sum(1 for word in recognized_words if word in expected_words)
                word_score = (word_matches / len(expected_words)) * 100
                scores.append(word_score)
            
            # 4. Character-level accuracy
            if expected:
                char_matches = sum(1 for char in recognized if char in expected)
                char_score = (char_matches / len(expected)) * 100
                scores.append(char_score)
            
            # Weighted average
            weights = [0.3, 0.3, 0.25, 0.15]  # Sequence, Levenshtein, Word, Character
            final_score = sum(score * weight for score, weight in zip(scores, weights))
            
            logger.info(f"English pronunciation score: {final_score:.1f}")
            return min(100.0, max(0.0, final_score))
            
        except Exception as e:
            logger.error(f"English pronunciation scoring error: {e}")
            return 50.0
    
    def analyze_fluency(self, audio_file_path, recognized_text, expected_text):
        """Analyze English speech fluency"""
        
        try:
            logger.info(f"Analyzing English fluency for: {audio_file_path}")
            
            if not LIBROSA_AVAILABLE:
                # Fallback fluency analysis without librosa
                return self._fallback_fluency_analysis(recognized_text, expected_text)
            
            # Load audio
            y, sr = librosa.load(audio_file_path, sr=self.sample_rate)
            
            # 1. Speaking rate analysis
            duration = librosa.get_duration(y=y, sr=sr)
            word_count = len(recognized_text.split()) if recognized_text else 0
            words_per_minute = (word_count / duration) * 60 if duration > 0 else 0
            
            # English speaking rates
            ideal_wpm = 150  # Average English speaking rate
            wpm_score = 100 - abs(words_per_minute - ideal_wpm)
            wpm_score = max(0, min(100, wpm_score))
            
            # 2. Pause analysis
            speech_segments = librosa.effects.split(y, top_db=20)
            pause_count = len(speech_segments) - 1
            total_pause_time = self._calculate_pause_time(speech_segments, sr)
            
            # Ideal pause ratio for English
            ideal_pause_ratio = 0.15  # 15% of speech should be pauses
            actual_pause_ratio = total_pause_time / duration if duration > 0 else 0
            pause_score = 100 - abs(actual_pause_ratio - ideal_pause_ratio) * 200
            pause_score = max(0, min(100, pause_score))
            
            # 3. Rhythm and intonation
            rhythm_score = self._analyze_rhythm(y, sr)
            
            # 4. Filler word detection
            filler_score = self._detect_filler_words(recognized_text)
            
            # Weighted fluency score
            fluency_score = (
                wpm_score * 0.3 +      # Speaking rate
                pause_score * 0.25 +   # Pauses
                rhythm_score * 0.25 +   # Rhythm
                filler_score * 0.2       # Filler words
            )
            
            logger.info(f"English fluency score: {fluency_score:.1f}")
            return {
                'score': fluency_score,
                'wpm': words_per_minute,
                'wpm_score': wpm_score,
                'pause_score': pause_score,
                'rhythm_score': rhythm_score,
                'filler_score': filler_score,
                'duration': duration
            }
            
        except Exception as e:
            logger.error(f"English fluency analysis error: {e}")
            return self._fallback_fluency_analysis(recognized_text, expected_text)
    
    def _fallback_fluency_analysis(self, recognized_text, expected_text):
        """Fallback fluency analysis without audio processing"""
        
        try:
            # Text-based fluency analysis
            word_count = len(recognized_text.split()) if recognized_text else 0
            expected_word_count = len(expected_text.split()) if expected_text else 0
            
            # Word completion ratio
            completion_ratio = word_count / expected_word_count if expected_word_count > 0 else 0
            
            # Filler word detection
            filler_score = self._detect_filler_words(recognized_text)
            
            # Text complexity score
            complexity_score = min(100, word_count * 5)  # Simple complexity metric
            
            # Weighted score
            fluency_score = (
                completion_ratio * 40 +    # Completion
                filler_score * 30 +        # Fewer fillers
                complexity_score * 30      # Complexity
            )
            
            return {
                'score': min(100, max(0, fluency_score)),
                'wpm': word_count * 10,  # Estimated
                'wpm_score': completion_ratio * 100,
                'pause_score': 50,  # Neutral
                'rhythm_score': 50,  # Neutral
                'filler_score': filler_score,
                'duration': 5.0,  # Estimated
                'fallback': True
            }
            
        except Exception as e:
            logger.error(f"Fallback fluency analysis error: {e}")
            return {'score': 50.0, 'fallback': True}
    
    def _clean_english_text(self, text):
        """Clean and normalize English text"""
        
        if not text:
            return ""
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common recognition artifacts
        artifacts = ['um', 'uh', 'er', 'ah', 'like', 'you know']
        words = text.lower().split()
        words = [word for word in words if word not in artifacts]
        
        # Reconstruct text
        cleaned = ' '.join(words)
        
        # Remove punctuation for scoring
        import string
        cleaned = cleaned.translate(str.maketrans('', '', string.punctuation))
        
        return cleaned.strip()
    
    def _get_tts_config(self, voice_type):
        """Get TTS configuration for English"""
        
        configs = {
            'default': {'slow': False, 'tld': 'com'},
            'slow': {'slow': True, 'tld': 'com'},
            'uk': {'slow': False, 'tld': 'co.uk'},
            'au': {'slow': False, 'tld': 'com.au'},
            'ca': {'slow': False, 'tld': 'ca'}
        }
        
        return configs.get(voice_type, configs['default'])
    
    def _calculate_pause_time(self, speech_segments, sr):
        """Calculate total pause time from speech segments"""
        
        if len(speech_segments) <= 1:
            return 0.0
        
        pause_time = 0.0
        for i in range(len(speech_segments) - 1):
            pause_duration = (speech_segments[i + 1][0] - speech_segments[i][1]) / sr
            pause_time += max(0, pause_duration)
        
        return pause_time
    
    def _analyze_rhythm(self, audio, sr):
        """Analyze speech rhythm and intonation"""
        
        try:
            if not LIBROSA_AVAILABLE:
                return 50.0  # Neutral score without librosa
            
            # Extract fundamental frequency (pitch)
            f0, voiced_flag, voiced_probs = librosa.pyin(
                audio, 
                sr=sr,
                fmin=50,
                fmax=400,
                frame_length=2048
            )
            
            # Filter voiced frames
            voiced_f0 = f0[voiced_flag]
            
            if len(voiced_f0) == 0:
                return 50.0
            
            # Calculate pitch variation
            f0_std = np.std(voiced_f0)
            f0_mean = np.mean(voiced_f0)
            
            # Rhythm score based on pitch variation
            if f0_mean > 0:
                cv = f0_std / f0_mean  # Coefficient of variation
                # Good English speech has moderate pitch variation
                rhythm_score = 100 - abs(cv - 0.3) * 200
                return max(0, min(100, rhythm_score))
            
            return 50.0
            
        except Exception as e:
            logger.error(f"Rhythm analysis error: {e}")
            return 50.0
    
    def _detect_filler_words(self, text):
        """Detect and score filler word usage"""
        
        if not text:
            return 100.0
        
        # English filler words
        filler_words = ['um', 'uh', 'er', 'ah', 'like', 'you know', 'so', 'well', 'actually', 'basically']
        words = text.lower().split()
        
        filler_count = sum(1 for word in words if word in filler_words)
        total_words = len(words)
        
        if total_words == 0:
            return 100.0
        
        filler_ratio = filler_count / total_words
        
        # Score: fewer fillers = higher score
        filler_score = 100 - (filler_ratio * 200)
        return max(0, min(100, filler_score))
    
    def get_system_info(self):
        """Get English speech system information"""
        
        return {
            'language': 'English',
            'code': 'en',
            'recognition_engines': ['Google Speech Recognition', 'Whisper', 'CMU Sphinx'],
            'tts_engine': 'Google Text-to-Speech (gTTS)',
            'voice_options': ['default', 'slow', 'uk', 'au', 'ca'],
            'confidence_threshold': self.confidence_threshold,
            'sample_rate': self.sample_rate,
            'max_duration': self.max_recording_duration
        }

# Test the system
if __name__ == "__main__":
    system = EnglishSpeechSystem()
    
    print("🇺🇸 ENGLISH SPEECH SYSTEM")
    print("=" * 50)
    
    # Test system info
    info = system.get_system_info()
    print(f"Language: {info['language']}")
    print(f"Recognition Engines: {', '.join(info['recognition_engines'])}")
    print(f"TTS Engine: {info['tts_engine']}")
    print(f"Voice Options: {', '.join(info['voice_options'])}")
    
    # Test pronunciation scoring
    print(f"\n🧪 Testing English Pronunciation Scoring:")
    score = system.calculate_pronunciation_score("hello world", "hello world")
    print(f"Perfect match score: {score:.1f}")
    
    score = system.calculate_pronunciation_score("helo world", "hello world")
    print(f"Close match score: {score:.1f}")
    
    score = system.calculate_pronunciation_score("goodbye", "hello world")
    print(f"Poor match score: {score:.1f}")
    
    print(f"\n✅ English Speech System Ready!")
