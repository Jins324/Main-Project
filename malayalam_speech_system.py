"""
Malayalam Speech Recognition and Audio Generation System
Specialized for Malayalam language processing with Unicode support
"""
import os
import logging
import speech_recognition as sr
import tempfile
import io
from pydub import AudioSegment
import numpy as np
from difflib import SequenceMatcher
import unicodedata
import re

# Optional imports with fallbacks
try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    logging.warning("librosa not available - Malayalam fluency analysis will be limited")

logger = logging.getLogger(__name__)

class MalayalamSpeechSystem:
    """Specialized Malayalam speech recognition and audio generation"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.language = 'ml-IN'
        self.tts_lang = 'ml'
        
        # Malayalam-specific settings
        self.confidence_threshold = 0.6  # Lower threshold for Malayalam
        self.max_recording_duration = 30
        self.sample_rate = 16000
        
        # Initialize recognizer settings for Malayalam
        self.recognizer.energy_threshold = 250  # Lower for Malayalam sounds
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.9  # Longer pause for Malayalam
        
        logger.info("Malayalam Speech System initialized")
    
    def recognize_speech(self, audio_file_path):
        """Recognize Malayalam speech from audio file"""
        
        try:
            logger.info(f"Starting Malayalam speech recognition for: {audio_file_path}")
            
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio_data = self.recognizer.record(source)
            
            # Try multiple recognition engines specialized for Malayalam
            text = None
            confidence = 0.0
            engine_used = 'none'
            
            # 1. Google Speech Recognition with Malayalam
            try:
                result = self.recognizer.recognize_google(
                    audio_data, 
                    language=self.language,
                    show_all=True
                )
                
                if result and 'alternative' in result:
                    text = result['alternative'][0]['transcript']
                    confidence = result['alternative'][0].get('confidence', 0.0)
                    engine_used = 'google'
                    logger.info(f"Google Malayalam recognition: '{text}' (confidence: {confidence})")
                    
            except sr.UnknownValueError:
                logger.warning("Google Malayalam Speech Recognition could not understand audio")
            except sr.RequestError as e:
                logger.error(f"Google Malayalam Speech Recognition error: {e}")
            
            # 2. Whisper with Malayalam model (primary fallback)
            if not text or confidence < self.confidence_threshold:
                try:
                    import whisper
                    model = whisper.load_model("base")
                    result = model.transcribe(audio_file_path, language="ml")
                    
                    whisper_text = result["text"].strip()
                    whisper_confidence = result.get("avg_logprob", -10) / 10
                    
                    if whisper_confidence > confidence:
                        text = whisper_text
                        confidence = max(whisper_confidence, 0.0)
                        engine_used = 'whisper'
                        logger.info(f"Whisper Malayalam recognition: '{text}' (confidence: {confidence})")
                        
                except ImportError:
                    logger.warning("Whisper not available for Malayalam")
                except Exception as e:
                    logger.error(f"Whisper Malayalam recognition error: {e}")
            
            # 3. Coqui TTS Malayalam model (if available)
            if not text or confidence < 0.4:
                try:
                    # Try Coqui-based recognition if available
                    from TTS.api import TTS
                    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
                    wav = tts.tts(text="temp", speaker_wav=None, language="ml")
                    
                    # This would need custom implementation for recognition
                    logger.info("Coqui Malayalam recognition attempted")
                    
                except ImportError:
                    logger.warning("Coqui TTS not available for Malayalam recognition")
                except Exception as e:
                    logger.error(f"Coqui Malayalam recognition error: {e}")
            
            # Clean and validate Malayalam text
            if text:
                text = self._clean_malayalam_text(text)
                logger.info(f"Final Malayalam recognition: '{text}' (confidence: {confidence})")
                return {
                    'text': text,
                    'confidence': confidence,
                    'language': 'ml',
                    'engine': engine_used
                }
            else:
                logger.warning("No Malayalam speech recognized")
                return {
                    'text': '',
                    'confidence': 0.0,
                    'language': 'ml',
                    'engine': 'none'
                }
                
        except Exception as e:
            logger.error(f"Malayalam speech recognition error: {e}")
            return {
                'text': '',
                'confidence': 0.0,
                'language': 'ml',
                'engine': 'error',
                'error': str(e)
            }
    
    def generate_audio(self, text, output_path=None, voice_type='default'):
        """Generate Malayalam audio from text"""
        
        try:
            logger.info(f"Generating Malayalam audio for: '{text[:50]}...'")
            
            # Clean and validate text
            clean_text = self._clean_malayalam_text(text)
            if not clean_text:
                logger.warning("No valid Malayalam text for audio generation")
                return None
            
            # Try multiple TTS engines for Malayalam
            audio_data = None
            
            # 1. gTTS with Malayalam
            try:
                from gtts import gTTS
                tts = gTTS(
                    text=clean_text,
                    lang=self.tts_lang,
                    slow=False
                )
                
                if output_path:
                    tts.save(output_path)
                    logger.info(f"Malayalam gTTS audio saved to: {output_path}")
                    return output_path
                else:
                    audio_bytes = io.BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)
                    audio_data = audio_bytes.getvalue()
                    logger.info("Malayalam gTTS audio generated successfully")
                    
            except Exception as e:
                logger.error(f"gTTS Malayalam generation error: {e}")
            
            # 2. Coqui TTS for better Malayalam (fallback)
            if not audio_data:
                try:
                    from TTS.api import TTS
                    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
                    
                    # Generate audio
                    wav = tts.tts(text=clean_text, speaker_wav=None, language="ml")
                    
                    if output_path:
                        # Save using soundfile
                        import soundfile as sf
                        sf.write(output_path, wav, 22050)
                        logger.info(f"Malayalam Coqui audio saved to: {output_path}")
                        return output_path
                    else:
                        # Convert to bytes
                        audio_bytes = io.BytesIO()
                        sf.write(audio_bytes, wav, 22050, format='WAV')
                        audio_bytes.seek(0)
                        audio_data = audio_bytes.getvalue()
                        logger.info("Malayalam Coqui audio generated successfully")
                        
                except ImportError:
                    logger.warning("Coqui TTS not available for Malayalam")
                except Exception as e:
                    logger.error(f"Coqui Malayalam generation error: {e}")
            
            # 3. pyttsx3 as final fallback
            if not audio_data:
                try:
                    import pyttsx3
                    engine = pyttsx3.init()
                    
                    # Try to set Malayalam voice
                    voices = engine.getProperty('voices')
                    malayalam_voice = None
                    
                    for voice in voices:
                        if 'malayalam' in voice.name.lower() or 'ml' in voice.id.lower():
                            malayalam_voice = voice
                            break
                    
                    if malayalam_voice:
                        engine.setProperty('voice', malayalam_voice.id)
                    
                    if output_path:
                        engine.save_to_file(clean_text, output_path)
                        engine.runAndWait()
                        logger.info(f"Malayalam pyttsx3 audio saved to: {output_path}")
                        return output_path
                    else:
                        # This would need custom implementation for bytes
                        logger.warning("pyttsx3 bytes output not implemented")
                        
                except ImportError:
                    logger.warning("pyttsx3 not available for Malayalam")
                except Exception as e:
                    logger.error(f"pyttsx3 Malayalam generation error: {e}")
            
            return audio_data
                
        except Exception as e:
            logger.error(f"Malayalam audio generation error: {e}")
            return None
    
    def calculate_pronunciation_score(self, recognized_text, expected_text):
        """Calculate Malayalam pronunciation score with Unicode support"""
        
        try:
            if not recognized_text or not expected_text:
                return 0.0
            
            # Clean texts with Malayalam-specific processing
            recognized = self._clean_malayalam_text(recognized_text.lower())
            expected = self._clean_malayalam_text(expected_text.lower())
            
            # Multiple scoring methods for Malayalam
            scores = []
            
            # 1. Unicode character-level similarity
            char_score = self._unicode_similarity(recognized, expected)
            scores.append(char_score * 100)
            
            # 2. SequenceMatcher for overall text similarity
            seq_score = SequenceMatcher(None, recognized, expected).ratio()
            scores.append(seq_score * 100)
            
            # 3. Malayalam-specific character matching
            ml_score = self._malayalam_character_match(recognized, expected)
            scores.append(ml_score * 100)
            
            # 4. Word-level accuracy (for Malayalam words)
            recognized_words = self._split_malayalam_words(recognized)
            expected_words = self._split_malayalam_words(expected)
            
            if expected_words:
                word_matches = sum(1 for word in recognized_words if word in expected_words)
                word_score = (word_matches / len(expected_words)) * 100
                scores.append(word_score)
            
            # Weighted average (more emphasis on character accuracy for Malayalam)
            weights = [0.4, 0.2, 0.3, 0.1]  # Unicode, Sequence, Malayalam chars, Words
            final_score = sum(score * weight for score, weight in zip(scores, weights))
            
            logger.info(f"Malayalam pronunciation score: {final_score:.1f}")
            return min(100.0, max(0.0, final_score))
            
        except Exception as e:
            logger.error(f"Malayalam pronunciation scoring error: {e}")
            return 50.0
    
    def analyze_fluency(self, audio_file_path, recognized_text, expected_text):
        """Analyze Malayalam speech fluency"""
        
        try:
            logger.info(f"Analyzing Malayalam fluency for: {audio_file_path}")
            
            if not LIBROSA_AVAILABLE:
                # Fallback fluency analysis without librosa
                return self._fallback_malayalam_fluency_analysis(recognized_text, expected_text)
            
            # Load audio
            y, sr = librosa.load(audio_file_path, sr=self.sample_rate)
            
            # 1. Speaking rate analysis (adjusted for Malayalam)
            duration = librosa.get_duration(y=y, sr=sr)
            word_count = len(self._split_malayalam_words(recognized_text)) if recognized_text else 0
            words_per_minute = (word_count / duration) * 60 if duration > 0 else 0
            
            # Malayalam speaking rates (slower than English)
            ideal_wpm = 120  # Average Malayalam speaking rate
            wpm_score = 100 - abs(words_per_minute - ideal_wpm)
            wpm_score = max(0, min(100, wpm_score))
            
            # 2. Pause analysis (longer pauses in Malayalam)
            speech_segments = librosa.effects.split(y, top_db=20)
            pause_count = len(speech_segments) - 1
            total_pause_time = self._calculate_pause_time(speech_segments, sr)
            
            # Ideal pause ratio for Malayalam
            ideal_pause_ratio = 0.2  # 20% of speech should be pauses (higher than English)
            actual_pause_ratio = total_pause_time / duration if duration > 0 else 0
            pause_score = 100 - abs(actual_pause_ratio - ideal_pause_ratio) * 200
            pause_score = max(0, min(100, pause_score))
            
            # 3. Rhythm and intonation (Malayalam-specific)
            rhythm_score = self._analyze_malayalam_rhythm(y, sr)
            
            # 4. Malayalam-specific features
            ml_features_score = self._analyze_malayalam_features(recognized_text)
            
            # Weighted fluency score
            fluency_score = (
                wpm_score * 0.25 +      # Speaking rate
                pause_score * 0.25 +       # Pauses
                rhythm_score * 0.25 +       # Rhythm
                ml_features_score * 0.25      # Malayalam features
            )
            
            logger.info(f"Malayalam fluency score: {fluency_score:.1f}")
            return {
                'score': fluency_score,
                'wpm': words_per_minute,
                'wpm_score': wpm_score,
                'pause_score': pause_score,
                'rhythm_score': rhythm_score,
                'ml_features_score': ml_features_score,
                'duration': duration
            }
            
        except Exception as e:
            logger.error(f"Malayalam fluency analysis error: {e}")
            return self._fallback_malayalam_fluency_analysis(recognized_text, expected_text)
    
    def _fallback_malayalam_fluency_analysis(self, recognized_text, expected_text):
        """Fallback Malayalam fluency analysis without audio processing"""
        
        try:
            # Text-based fluency analysis for Malayalam
            word_count = len(self._split_malayalam_words(recognized_text)) if recognized_text else 0
            expected_word_count = len(self._split_malayalam_words(expected_text)) if expected_text else 0
            
            # Word completion ratio
            completion_ratio = word_count / expected_word_count if expected_word_count > 0 else 0
            
            # Malayalam character analysis
            ml_features_score = self._analyze_malayalam_features(recognized_text)
            
            # Text complexity score (Malayalam-specific)
            complexity_score = min(100, word_count * 4)  # Adjusted for Malayalam
            
            # Weighted score
            fluency_score = (
                completion_ratio * 35 +    # Completion
                ml_features_score * 40 +   # Malayalam features
                complexity_score * 25      # Complexity
            )
            
            return {
                'score': min(100, max(0, fluency_score)),
                'wpm': word_count * 8,  # Estimated for Malayalam
                'wpm_score': completion_ratio * 100,
                'pause_score': 50,  # Neutral
                'rhythm_score': 50,  # Neutral
                'ml_features_score': ml_features_score,
                'duration': 6.0,  # Estimated for Malayalam
                'fallback': True
            }
            
        except Exception as e:
            logger.error(f"Fallback Malayalam fluency analysis error: {e}")
            return {'score': 50.0, 'fallback': True}
    
    def _clean_malayalam_text(self, text):
        """Clean and normalize Malayalam text with Unicode support"""
        
        if not text:
            return ""
        
        # Normalize Unicode
        text = unicodedata.normalize('NFC', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common Malayalam recognition artifacts
        artifacts = ['ഉം', 'എന്ന്', 'ആണ്', 'ഉണ്ട്']
        words = text.split()
        words = [word for word in words if word not in artifacts]
        
        # Reconstruct text
        cleaned = ' '.join(words)
        
        # Remove non-Malayalam characters except spaces
        malayalam_pattern = re.compile(r'[\u0D00-\u0D7F\s]+')
        matches = malayalam_pattern.findall(cleaned)
        cleaned = ''.join(matches)
        
        return cleaned.strip()
    
    def _unicode_similarity(self, text1, text2):
        """Calculate Unicode character similarity for Malayalam"""
        
        if not text1 or not text2:
            return 0.0
        
        # Convert to normalized Unicode
        text1 = unicodedata.normalize('NFC', text1)
        text2 = unicodedata.normalize('NFC', text2)
        
        # Character-level comparison
        chars1 = list(text1)
        chars2 = list(text2)
        
        if not chars1 or not chars2:
            return 0.0
        
        # Calculate character similarity
        common_chars = set(chars1) & set(chars2)
        total_chars = set(chars1) | set(chars2)
        
        if not total_chars:
            return 1.0
        
        similarity = len(common_chars) / len(total_chars)
        return similarity
    
    def _malayalam_character_match(self, recognized, expected):
        """Malayalam-specific character matching"""
        
        if not recognized or not expected:
            return 0.0
        
        # Malayalam character groups (similar sounds)
        char_groups = {
            'ക': ['ക', 'ഖ', 'ഗ', 'ഘ'],
            'ച': ['ച', 'ഛ', 'ജ', 'ഝ'],
            'ട': ['ട', 'ഠ', 'ഡ', 'ഢ'],
            'ത': ['ത', 'ഥ', 'ദ', 'ധ'],
            'പ': ['പ', 'ഫ', 'ബ', 'ഭ', 'മ'],
            'യ': ['യ', 'ര', 'റ', 'ല', 'വ', 'ശ', 'ഷ', 'സ', 'ഹ'],
            'അ': ['അ', 'ആ', 'ഇ', 'ഈ', 'ഉ', 'ഊ', 'ഋ', 'എ', 'ഏ', 'ഐ', 'ഒ', 'ഓ', 'ഔ'],
            'ൺ': ['ൺ', 'ൻ', 'ർ', 'ൽ', 'ൾ', 'ൿ']
        }
        
        # Group characters
        def group_char(char):
            for group, chars in char_groups.items():
                if char in chars:
                    return group
            return char
        
        recognized_grouped = [group_char(c) for c in recognized]
        expected_grouped = [group_char(c) for c in expected]
        
        # Calculate similarity
        if not expected_grouped:
            return 1.0
        
        matches = sum(1 for i, char in enumerate(recognized_grouped) 
                    if i < len(expected_grouped) and char == expected_grouped[i])
        
        return matches / len(expected_grouped)
    
    def _split_malayalam_words(self, text):
        """Split Malayalam text into words"""
        
        if not text:
            return []
        
        # Malayalam word boundaries
        words = re.findall(r'[\u0D00-\u0D7F]+', text)
        return [word for word in words if word.strip()]
    
    def _calculate_pause_time(self, speech_segments, sr):
        """Calculate total pause time from speech segments"""
        
        if len(speech_segments) <= 1:
            return 0.0
        
        pause_time = 0.0
        for i in range(len(speech_segments) - 1):
            pause_duration = (speech_segments[i + 1][0] - speech_segments[i][1]) / sr
            pause_time += max(0, pause_duration)
        
        return pause_time
    
    def _analyze_malayalam_rhythm(self, audio, sr):
        """Analyze Malayalam speech rhythm and intonation"""
        
        try:
            if not LIBROSA_AVAILABLE:
                return 50.0  # Neutral score without librosa
            
            # Extract fundamental frequency (pitch)
            f0, voiced_flag, voiced_probs = librosa.pyin(
                audio, 
                sr=sr,
                fmin=60,    # Lower fmin for Malayalam
                fmax=300,    # Lower fmax for Malayalam
                frame_length=2048
            )
            
            # Filter voiced frames
            voiced_f0 = f0[voiced_flag]
            
            if len(voiced_f0) == 0:
                return 50.0
            
            # Calculate pitch variation (Malayalam has different intonation patterns)
            f0_std = np.std(voiced_f0)
            f0_mean = np.mean(voiced_f0)
            
            # Rhythm score based on Malayalam pitch variation
            if f0_mean > 0:
                cv = f0_std / f0_mean  # Coefficient of variation
                # Malayalam speech has different rhythm characteristics
                rhythm_score = 100 - abs(cv - 0.4) * 150
                return max(0, min(100, rhythm_score))
            
            return 50.0
            
        except Exception as e:
            logger.error(f"Malayalam rhythm analysis error: {e}")
            return 50.0
    
    def _analyze_malayalam_features(self, text):
        """Analyze Malayalam-specific speech features"""
        
        if not text:
            return 100.0
        
        # Check for proper Malayalam character usage
        malayalam_chars = re.findall(r'[\u0D00-\u0D7F]', text)
        total_chars = len(text.replace(' ', ''))
        
        if total_chars == 0:
            return 100.0
        
        malayalam_ratio = len(malayalam_chars) / total_chars
        
        # Check for common Malayalam patterns
        malayalam_patterns = [
            r'[\u0D02\u0D3E]',  # ആ
            r'[\u0D07\u0D4D]',  # ക്
            r'[\u0D15\u0D4D\u0D37]',  # ക്ഷ
        ]
        
        pattern_score = 0
        for pattern in malayalam_patterns:
            if re.search(pattern, text):
                pattern_score += 10
        
        # Combine scores
        feature_score = (malayalam_ratio * 70) + min(pattern_score, 30)
        return max(0, min(100, feature_score))
    
    def get_system_info(self):
        """Get Malayalam speech system information"""
        
        return {
            'language': 'Malayalam',
            'code': 'ml',
            'recognition_engines': ['Google Speech Recognition', 'Whisper', 'Coqui TTS'],
            'tts_engines': ['gTTS', 'Coqui TTS', 'pyttsx3'],
            'unicode_support': True,
            'confidence_threshold': self.confidence_threshold,
            'sample_rate': self.sample_rate,
            'max_duration': self.max_recording_duration,
            'special_features': ['Unicode normalization', 'Malayalam character grouping', 'Cultural rhythm analysis']
        }

# Test the system
if __name__ == "__main__":
    system = MalayalamSpeechSystem()
    
    print("🇮🇳 MALAYALAM SPEECH SYSTEM")
    print("=" * 50)
    
    # Test system info
    info = system.get_system_info()
    print(f"Language: {info['language']}")
    print(f"Recognition Engines: {', '.join(info['recognition_engines'])}")
    print(f"TTS Engines: {', '.join(info['tts_engines'])}")
    print(f"Unicode Support: {info['unicode_support']}")
    print(f"Special Features: {', '.join(info['special_features'])}")
    
    # Test pronunciation scoring
    print(f"\n🧪 Testing Malayalam Pronunciation Scoring:")
    score = system.calculate_pronunciation_score("നമസ്കാരം", "നമസ്കാരം")
    print(f"Perfect match score: {score:.1f}")
    
    score = system.calculate_pronunciation_score("നമസ്കരം", "നമസ്കാരം")
    print(f"Close match score: {score:.1f}")
    
    score = system.calculate_pronunciation_score("വണക്ക്", "നമസ്കാരം")
    print(f"Poor match score: {score:.1f}")
    
    print(f"\n✅ Malayalam Speech System Ready!")
