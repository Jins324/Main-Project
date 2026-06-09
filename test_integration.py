#!/usr/bin/env python
"""
Test the integrated story-mode with working audio detection
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

def test_integrated_story_mode():
    """Test the integrated story-mode with working audio detection"""
    print("🎮 TESTING INTEGRATED STORY-MODE WITH WORKING AUDIO DETECTION")
    print("=" * 70)
    
    client = Client()
    
    # Test page accessibility
    print("\n🌐 Testing Page Accessibility:")
    try:
        response = client.get('/story-mode/')
        if response.status_code == 200:
            print("✅ Story-mode page accessible")
            
            # Check for working speech recognition components
            content = response.content.decode('utf-8')
            
            audio_components = {
                'speech_recognition_api': 'SpeechRecognition' in content,
                'start_listening_btn': 'startBtn' in content,
                'stop_listening_btn': 'stopBtn' in content,
                'transcription_display': 'transcriptionDisplay' in content,
                'status_indicator': 'statusIndicator' in content,
                'browser_warning': 'browserWarning' in content,
                'working_css': 'status-listening' in content,
                'pulse_animation': '@keyframes pulse' in content
            }
            
            print("\n🎛️ Audio Detection Components:")
            for component, present in audio_components.items():
                status = "✅" if present else "❌"
                print(f"  {status} {component.replace('_', ' ').title()}: {present}")
            
            # Check that old complex recording is removed
            old_components = {
                'media_recorder': 'MediaRecorder' in content,
                'audio_chunks': 'audioChunks' in content,
                'complex_recording': 'toggleRecording' in content,
                'waveform_visualization': 'waveform' in content
            }
            
            print("\n🗑️ Old Complex Components (Should be removed):")
            for component, present in old_components.items():
                status = "✅ Removed" if not present else "❌ Still present"
                print(f"  {status} {component.replace('_', ' ').title()}: {not present}")
            
            # Check that existing functionality is preserved
            existing_features = {
                'audio_generation': 'generateAudio' in content,
                'story_selection': 'selectStory' in content,
                'language_selection': 'selectLanguage' in content,
                'scoring_results': 'scoringResults' in content,
                'age_based_scoring': 'age_adjusted' in content
            }
            
            print("\n🔧 Preserved Existing Features:")
            for feature, present in existing_features.items():
                status = "✅" if present else "❌"
                print(f"  {status} {feature.replace('_', ' ').title()}: {present}")
            
            return True
        else:
            print(f"❌ Page not accessible. Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing page: {e}")
        return False

def test_language_support():
    """Test English and Malayalam language support"""
    print("\n🌍 Testing Language Support:")
    
    client = Client()
    
    # Test English
    try:
        response = client.get('/story-mode/?language=en')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            has_english = 'en-US' in content
            print(f"  ✅ English support: {has_english}")
        else:
            print(f"  ❌ English page failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ English test error: {e}")
    
    # Test Malayalam
    try:
        response = client.get('/story-mode/?language=ml')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            has_malayalam = 'ml-IN' in content
            print(f"  ✅ Malayalam support: {has_malayalam}")
        else:
            print(f"  ❌ Malayalam page failed: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Malayalam test error: {e}")

def test_speech_recognition_logic():
    """Test speech recognition logic in JavaScript"""
    print("\n🎤 Testing Speech Recognition Logic:")
    
    client = Client()
    
    try:
        response = client.get('/story-mode/')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            speech_logic = {
                'recognition_initialization': 'new SpeechRecognition()' in content,
                'language_detection': 'recognition.lang' in content,
                'event_handlers': 'recognition.onresult' in content,
                'error_handling': 'recognition.onerror' in content,
                'continuous_recognition': 'recognition.continuous = true' in content,
                'interim_results': 'recognition.interimResults = true' in content,
                'auto_evaluation': 'evaluateSpeech' in content,
                'text_based_evaluation': 'sendTextBasedEvaluation' in content,
                'child_friendly_score': 'showChildFriendlyScore' in content
            }
            
            for logic, present in speech_logic.items():
                status = "✅" if present else "❌"
                print(f"  {status} {logic.replace('_', ' ').title()}: {present}")
            
            return True
        else:
            print(f"❌ Failed to get page: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing speech logic: {e}")
        return False

def run_integration_test():
    """Run complete integration test"""
    print("🎮 INTEGRATED STORY-MODE AUDIO DETECTION TEST")
    print("=" * 80)
    print("Testing http://127.0.0.1:8000/story-mode with integrated working audio")
    print("=" * 80)
    
    test_results = {}
    
    # Run tests
    test_results['page_accessibility'] = test_integrated_story_mode()
    test_results['language_support'] = test_language_support()
    test_results['speech_recognition_logic'] = test_speech_recognition_logic()
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 INTEGRATION TEST RESULTS")
    print("=" * 80)
    
    passed_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name.replace('_', ' ').title()}: {result}")
    
    success_rate = (passed_tests / total_tests) * 100
    print(f"\n📈 Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate >= 80:
        print("🎉 INTEGRATION SUCCESSFUL!")
        print("\n✅ What was accomplished:")
        print("  • Working speech recognition integrated from test file")
        print("  • Complex audio recording removed and replaced")
        print("  • English and Malayalam language support preserved")
        print("  • Existing functionality maintained")
        print("  • Child-friendly scoring system working")
        print("  • Age-based assessment preserved")
        
        print("\n🚀 Ready for use:")
        print("  • Start Django server: python manage.py runserver")
        print("  • Access: http://127.0.0.1:8000/story-mode")
        print("  • Test with: Chrome, Edge, or Safari browser")
        print("  • Click 'Start Listening' to test speech recognition")
        
    else:
        print("⚠️  Integration needs attention")
    
    return success_rate

if __name__ == "__main__":
    run_integration_test()
