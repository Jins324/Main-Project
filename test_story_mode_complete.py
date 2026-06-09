#!/usr/bin/env python
"""
Story Mode Audio-to-Text Integration Test
Tests the complete story-mode page with enhanced audio-to-text
"""

import os
import sys
import django

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from core.models import Story, CustomUser
from unified_speech_processor import UnifiedSpeechProcessor
import json

class StoryModeAudioTest:
    def __init__(self):
        self.client = Client()
        self.speech_processor = UnifiedSpeechProcessor()
        
    def test_story_mode_page(self):
        """Test the story-mode page accessibility and audio features"""
        print("📚 TESTING STORY-MODE PAGE WITH AUDIO-TO-TEXT")
        print("=" * 60)
        
        # Test page accessibility
        print("\n🌐 PAGE ACCESSIBILITY TEST:")
        try:
            response = self.client.get('/story-mode/')
            if response.status_code == 200:
                print("✅ Story-mode page accessible")
                print(f"📊 Status Code: {response.status_code}")
                
                # Check for robust audio features
                content = response.content.decode('utf-8')
                
                audio_features = {
                    'robust_audio_enabled': 'robust_audio_enabled' in content,
                    'recording_controls': 'toggleRecording' in content,
                    'audio_processing': 'processRecording' in content,
                    'scoring_system': 'displayScoringResults' in content,
                    'age_based_scoring': 'age_adjusted' in content
                }
                
                print("\n🎛️ AUDIO FEATURES DETECTED:")
                for feature, present in audio_features.items():
                    status = "✅" if present else "❌"
                    print(f"  {status} {feature.replace('_', ' ').title()}: {present}")
                
                return True
            else:
                print(f"❌ Page not accessible. Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error accessing page: {e}")
            return False
    
    def test_audio_libraries(self):
        """Test audio-to-text libraries and functionality"""
        print("\n🔧 AUDIO-TO-TEXT LIBRARIES TEST:")
        print("=" * 40)
        
        libraries_status = {}
        
        # Test speech recognition
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            libraries_status['speech_recognition'] = True
            print("✅ SpeechRecognition library available")
        except ImportError:
            libraries_status['speech_recognition'] = False
            print("❌ SpeechRecognition library not available")
        
        # Test Whisper
        try:
            import whisper
            model = whisper.load_model("base")
            libraries_status['whisper'] = True
            print("✅ Whisper library available (base model loaded)")
        except ImportError:
            libraries_status['whisper'] = False
            print("❌ Whisper library not available")
        except Exception as e:
            libraries_status['whisper'] = False
            print(f"❌ Whisper model loading failed: {e}")
        
        # Test audio processing
        try:
            from pydub import AudioSegment
            libraries_status['pydub'] = True
            print("✅ pydub library available")
        except ImportError:
            libraries_status['pydub'] = False
            print("❌ pydub library not available")
        
        # Test librosa
        try:
            import librosa
            libraries_status['librosa'] = True
            print("✅ librosa library available")
        except ImportError:
            libraries_status['librosa'] = False
            print("❌ librosa library not available")
        
        # Test scoring libraries
        try:
            import jiwer
            libraries_status['jiwer'] = True
            print("✅ jiwer (WER) library available")
        except ImportError:
            libraries_status['jiwer'] = False
            print("❌ jiwer library not available")
        
        try:
            import Levenshtein
            libraries_status['levenshtein'] = True
            print("✅ Levenshtein library available")
        except ImportError:
            libraries_status['levenshtein'] = False
            print("❌ Levenshtein library not available")
        
        return libraries_status
    
    def test_speech_systems(self):
        """Test English and Malayalam speech systems"""
        print("\n🎤 SPEECH SYSTEMS TEST:")
        print("=" * 40)
        
        systems_status = {}
        
        # Test unified speech processor
        try:
            # Test English system
            english_result = self.speech_processor.recognize_speech('test_audio.wav', 'en')
            systems_status['english_system'] = True
            print("✅ English speech system available")
        except Exception as e:
            systems_status['english_system'] = False
            print(f"❌ English speech system error: {e}")
        
        # Test Malayalam system
        try:
            malayalam_result = self.speech_processor.recognize_speech('test_audio.wav', 'ml')
            systems_status['malayalam_system'] = True
            print("✅ Malayalam speech system available")
        except Exception as e:
            systems_status['malayalam_system'] = False
            print(f"❌ Malayalam speech system error: {e}")
        
        # Test audio generation
        try:
            audio_result = self.speech_processor.generate_audio("Hello world", 'en')
            systems_status['audio_generation'] = True
            print("✅ Audio generation available")
        except Exception as e:
            systems_status['audio_generation'] = False
            print(f"❌ Audio generation error: {e}")
        
        return systems_status
    
    def test_story_data(self):
        """Test story data availability"""
        print("\n📖 STORY DATA TEST:")
        print("=" * 40)
        
        try:
            # Check English stories
            english_stories = Story.objects.filter(language='en')
            print(f"📚 English Stories: {english_stories.count()} available")
            
            if english_stories.exists():
                story = english_stories.first()
                print(f"   Sample: '{story.title[:30]}...' ({story.language})")
                print(f"   Audio File: {'Yes' if story.audio_file else 'No'}")
            
            # Check Malayalam stories
            malayalam_stories = Story.objects.filter(language='ml')
            print(f"📚 Malayalam Stories: {malayalam_stories.count()} available")
            
            if malayalam_stories.exists():
                story = malayalam_stories.first()
                print(f"   Sample: '{story.title[:30]}...' ({story.language})")
                print(f"   Audio File: {'Yes' if story.audio_file else 'No'}")
            
            total_stories = english_stories.count() + malayalam_stories.count()
            print(f"📊 Total Stories: {total_stories}")
            
            return total_stories > 0
            
        except Exception as e:
            print(f"❌ Error accessing story data: {e}")
            return False
    
    def test_age_based_scoring(self):
        """Test age-based scoring integration"""
        print("\n🎯 AGE-BASED SCORING TEST:")
        print("=" * 40)
        
        try:
            from core.enhanced_scoring import EnhancedScoringSystem
            scoring_system = EnhancedScoringSystem()
            
            # Test age-based scoring for speech
            reading_data = {
                'reading_fluency_score': 75,
                'pronunciation_score': 80,
                'completion_score': 70,
                'words_read': 20,
                'total_words': 25,
                'reading_time': 2.0
            }
            
            test_ages = [4, 7, 10, 13]
            for age in test_ages:
                result = scoring_system.calculate_story_score(reading_data, age)
                print(f"  👤 Age {age}: {result['final_score']:.1f} points (age_adjusted: {result['metrics']['age_adjusted']})")
            
            print("✅ Age-based scoring working")
            return True
            
        except Exception as e:
            print(f"❌ Age-based scoring error: {e}")
            return False
    
    def test_registration_age_field(self):
        """Test that age field is properly integrated in registration"""
        print("\n📝 REGISTRATION AGE FIELD TEST:")
        print("=" * 40)
        
        try:
            # Test child registration form
            response = self.client.get('/register/child/')
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                # Check for age field
                has_age_field = 'name="age"' in content
                has_age_validation = 'min="3"' in content and 'max="18"' in content
                has_age_help = 'Enter your age' in content
                
                print(f"  ✅ Age field present: {has_age_field}")
                print(f"  ✅ Age validation: {has_age_validation}")
                print(f"  ✅ Age help text: {has_age_help}")
                
                return has_age_field and has_age_validation
            else:
                print(f"  ❌ Registration page not accessible: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Registration test error: {e}")
            return False
    
    def create_test_audio_sample(self):
        """Create a test audio sample for testing"""
        print("\n🎵 CREATING TEST AUDIO SAMPLE:")
        print("=" * 40)
        
        try:
            # Generate a simple test audio using gTTS
            from gtts import gTTS
            import tempfile
            
            # Create test audio
            tts = gTTS("Hello world, this is a test for speech recognition", lang='en')
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                tts.save(f.name)
                test_audio_path = f.name
                print(f"✅ Test audio created: {test_audio_path}")
                
                # Test speech recognition on the sample
                try:
                    result = self.speech_processor.recognize_speech(test_audio_path, 'en')
                    print(f"🎤 Recognition result: '{result.get('text', '')[:50]}...'")
                    print(f"📊 Confidence: {result.get('confidence', 0.0):.2f}")
                    print(f"🔧 Engine: {result.get('engine', 'unknown')}")
                    
                    # Clean up
                    os.unlink(test_audio_path)
                    return True
                    
                except Exception as e:
                    print(f"❌ Speech recognition test failed: {e}")
                    os.unlink(test_audio_path)
                    return False
                    
        except Exception as e:
            print(f"❌ Test audio creation failed: {e}")
            return False
    
    def run_complete_test(self):
        """Run complete story-mode audio-to-text test"""
        print("🎮 STORY-MODE AUDIO-TO-TEXT COMPLETE TEST")
        print("=" * 80)
        print("Testing http://127.0.0.1:8000/story-mode with enhanced audio-to-text")
        print("=" * 80)
        
        test_results = {}
        
        # Run all tests
        test_results['page_accessibility'] = self.test_story_mode_page()
        test_results['audio_libraries'] = self.test_audio_libraries()
        test_results['speech_systems'] = self.test_speech_systems()
        test_results['story_data'] = self.test_story_data()
        test_results['age_based_scoring'] = self.test_age_based_scoring()
        test_results['registration_age'] = self.test_registration_age_field()
        test_results['test_audio'] = self.create_test_audio_sample()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 80)
        
        passed_tests = 0
        total_tests = len(test_results)
        
        for test_name, result in test_results.items():
            if isinstance(result, dict):
                # For library tests, show individual results
                print(f"\n🔍 {test_name.replace('_', ' ').title()}:")
                for lib, available in result.items():
                    status = "✅" if available else "❌"
                    print(f"  {status} {lib}: {available}")
                    if available:
                        passed_tests += 1
            else:
                status = "✅" if result else "❌"
                print(f"{status} {test_name.replace('_', ' ').title()}: {result}")
                if result:
                    passed_tests += 1
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"\n📈 Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
        
        if success_rate >= 80:
            print("🎉 STORY-MODE AUDIO-TO-TEXT SYSTEM READY!")
        elif success_rate >= 60:
            print("⚠️  STORY-MODE SYSTEM PARTIALLY READY")
        else:
            print("❌ STORY-MODE SYSTEM NEEDS WORK")
        
        print("\n🎯 RECOMMENDATIONS:")
        if not test_results.get('page_accessibility', False):
            print("  - Fix story-mode page accessibility")
        if not test_results.get('audio_libraries', {}).get('whisper', False):
            print("  - Install Whisper for best accuracy")
        if not test_results.get('speech_systems', {}).get('english_system', False):
            print("  - Fix English speech system")
        if not test_results.get('speech_systems', {}).get('malayalam_system', False):
            print("  - Fix Malayalam speech system")
        if not test_results.get('age_based_scoring', False):
            print("  - Fix age-based scoring integration")
        if not test_results.get('registration_age', False):
            print("  - Fix age field in registration")
        
        return success_rate

if __name__ == "__main__":
    tester = StoryModeAudioTest()
    tester.run_complete_test()
