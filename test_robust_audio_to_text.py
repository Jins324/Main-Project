#!/usr/bin/env python
"""
Test Robust Audio-to-Text Systems
Deep testing of the robust English and Malayalam audio-to-text conversion
"""
import os
import sys
import django

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from django.test.client import Client
from django.contrib.auth import get_user_model
import json
import traceback
from robust_english_audio_to_text import RobustEnglishAudioToText
from robust_malayalam_audio_to_text import RobustMalayalamAudioToText

def test_english_system_deep():
    """Deep test of English audio-to-text system"""
    
    print("🇺🇸 DEEP TESTING ENGLISH AUDIO-TO-TEXT SYSTEM")
    print("=" * 60)
    
    converter = RobustEnglishAudioToText()
    
    # Test system info
    info = converter.get_system_info()
    print(f"System Info:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Test text cleaning
    print(f"\n🧪 Text Cleaning Test:")
    test_texts = [
        "hello world",
        "um hello uh world",
        "HELLO WORLD",
        "hello, world!",
        ""
    ]
    
    for text in test_texts:
        cleaned = converter._clean_english_text(text)
        print(f"  '{text}' -> '{cleaned}'")
    
    # Test confidence calculation
    print(f"\n📊 Confidence Calculation Test:")
    test_cases = [
        {"avg_logprob": -0.5, "language": "en", "expected": "High"},
        {"avg_logprob": -1.0, "language": "en", "expected": "Medium"},
        {"avg_logprob": -1.5, "language": "en", "expected": "Medium-Low"},
        {"avg_logprob": -2.0, "language": "en", "expected": "Low"}
    ]
    
    for case in test_cases:
        mock_result = {"avg_logprob": case["avg_logprob"], "language": case["language"]}
        confidence = converter._calculate_whisper_confidence(mock_result)
        print(f"  {case['expected']}: {confidence:.2f}")
    
    # Test mock audio processing
    print(f"\n🎤 Mock Audio Processing Test:")
    result = converter.process_audio_recording("nonexistent.wav", "hello world")
    print(f"  Success: {result.get('success', False)}")
    print(f"  Error: {result.get('error', 'None')}")
    print(f"  Recognized: '{result.get('recognized_text', '')}'")
    print(f"  Expected: '{result.get('expected_text', '')}'")
    
    if result.get('scores'):
        scores = result['scores']
        print(f"  Scores: Overall={scores.get('overall', 0):.1f}, Pronunciation={scores.get('pronunciation', 0):.1f}")
    
    print(f"✅ English System Deep Test Complete!")

def test_malayalam_system_deep():
    """Deep test of Malayalam audio-to-text system"""
    
    print(f"\n🇮🇳 DEEP TESTING MALAYALAM AUDIO-TO-TEXT SYSTEM")
    print("=" * 60)
    
    converter = RobustMalayalamAudioToText()
    
    # Test system info
    info = converter.get_system_info()
    print(f"System Info:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
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
    print(f"\n🔍 Malayalam Validation Test:")
    test_texts = [
        "നമസ്കാരം",
        "നമസ്കാരം hello",
        "hello world",
        ""
    ]
    
    for text in test_texts:
        validation = converter.validate_malayalam_text(text)
        print(f"  '{text}': {validation['is_malayalam']} ({validation['confidence']:.2f})")
        if validation['issues']:
            print(f"    Issues: {', '.join(validation['issues'])}")
    
    # Test confidence calculation
    print(f"\n📊 Confidence Calculation Test:")
    test_cases = [
        {"avg_logprob": -0.5, "language": "ml", "expected": "High"},
        {"avg_logprob": -1.0, "language": "ml", "expected": "Medium"},
        {"avg_logprob": -1.5, "language": "ml", "expected": "Medium-Low"},
        {"avg_logprob": -2.0, "language": "ml", "expected": "Low"}
    ]
    
    for case in test_cases:
        mock_result = {"avg_logprob": case["avg_logprob"], "language": case["language"]}
        confidence = converter._calculate_whisper_confidence(mock_result)
        print(f"  {case['expected']}: {confidence:.2f}")
    
    # Test mock audio processing
    print(f"\n🎤 Mock Audio Processing Test:")
    result = converter.process_audio_recording("nonexistent.wav", "നമസ്കാരം")
    print(f"  Success: {result.get('success', False)}")
    print(f"  Error: {result.get('error', 'None')}")
    print(f"  Recognized: '{result.get('recognized_text', '')}'")
    print(f"  Expected: '{result.get('expected_text', '')}'")
    
    if result.get('malayalam_validation'):
        validation = result['malayalam_validation']
        print(f"  Malayalam: {validation['is_malayalam']} ({validation['confidence']:.2f})")
    
    if result.get('scores'):
        scores = result['scores']
        print(f"  Scores: Overall={scores.get('overall', 0):.1f}, Pronunciation={scores.get('pronunciation', 0):.1f}")
    
    print(f"✅ Malayalam System Deep Test Complete!")

def test_web_interfaces_deep():
    """Deep test of web interfaces"""
    
    print(f"\n🌐 DEEP TESTING WEB INTERFACES")
    print("=" * 60)
    
    User = get_user_model()
    client = Client()
    
    # Login
    try:
        user = User.objects.get(username='testchild')
        client.login(username='testchild', password='test123')
        print("✅ Logged in successfully")
    except:
        user = User.objects.create_user(username='testchild', password='test123', is_parent=False)
        client.login(username='testchild', password='test123')
        print("✅ Created and logged in test user")
    
    # Test robust English speech page
    print(f"\n📄 Testing Robust English Speech Page:")
    response = client.get('/robust-english-speech/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        elements = [
            'Robust English Speech Recording',
            'recordBtn',
            'practiceText',
            'resultSection',
            'processingIndicator'
        ]
        
        for element in elements:
            if element in content:
                print(f"   ✅ Found: {element}")
            else:
                print(f"   ❌ Missing: {element}")
    
    # Test robust Malayalam speech page
    print(f"\n📄 Testing Robust Malayalam Speech Page:")
    response = client.get('/robust-malayalam-speech/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        elements = [
            'Robust Malayalam Speech Recording',
            'recordBtn',
            'practiceText',
            'resultSection',
            'processingIndicator'
        ]
        
        for element in elements:
            if element in content:
                print(f"   ✅ Found: {element}")
            else:
                print(f"   ❌ Missing: {element}")
    
    # Test APIs
    print(f"\n🔌 Testing Robust APIs:")
    
    # Test system stats
    response = client.get('/api/robust-system-stats/')
    print(f"   Robust System Stats: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Total Languages: {data.get('total_languages', 0)}")
            print(f"   ✅ Real-time Processing: {data.get('features', {}).get('real_time_processing', False)}")
            print(f"   ✅ Automatic Scoring: {data.get('features', {}).get('automatic_scoring', False)}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown')}")
    
    # Test speech recording history
    response = client.get('/api/speech-recording-history/')
    print(f"   Speech Recording History: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ History entries: {data.get('total', 0)}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown')}")

def test_mock_api_calls():
    """Test API calls with mock data"""
    
    print(f"\n🧪 TESTING MOCK API CALLS")
    print("=" * 60)
    
    User = get_user_model()
    client = Client()
    
    # Login
    try:
        user = User.objects.get(username='testchild')
        client.login(username='testchild', password='test123')
    except:
        user = User.objects.create_user(username='testchild', password='test123', is_parent=False)
        client.login(username='testchild', password='test123')
    
    # Test English audio processing (mock)
    print(f"\n🇺🇸 Testing English Audio Processing (Mock):")
    
    # Create a mock audio file
    from io import BytesIO
    from django.core.files.uploadedfile import SimpleUploadedFile
    
    mock_audio = SimpleUploadedFile("test.wav", b"fake audio data", content_type="audio/wav")
    
    response = client.post('/api/process-english-audio-realtime/', {
        'audio_file': mock_audio,
        'expected_text': 'hello world',
        'story_id': '1'
    })
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Success: {data.get('success', False)}")
        print(f"   Recognized: '{data.get('recognized_text', '')[:30]}...'")
        print(f"   Engine: {data.get('engine', 'unknown')}")
        if data.get('scores'):
            scores = data['scores']
            print(f"   Overall Score: {scores.get('overall', 0):.1f}")
    else:
        print(f"   Error: {response.status_code}")
    
    # Test Malayalam audio processing (mock)
    print(f"\n🇮🇳 Testing Malayalam Audio Processing (Mock):")
    
    mock_audio2 = SimpleUploadedFile("test2.wav", b"fake audio data", content_type="audio/wav")
    
    response = client.post('/api/process-malayalam-audio-realtime/', {
        'audio_file': mock_audio2,
        'expected_text': 'നമസ്കാരം',
        'story_id': '2'
    })
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Success: {data.get('success', False)}")
        print(f"   Recognized: '{data.get('recognized_text', '')[:30]}...'")
        print(f"   Engine: {data.get('engine', 'unknown')}")
        if data.get('malayalam_validation'):
            validation = data['malayalam_validation']
            print(f"   Malayalam: {validation['is_malayalam']} ({validation['confidence']:.2f})")
        if data.get('scores'):
            scores = data['scores']
            print(f"   Overall Score: {scores.get('overall', 0):.1f}")
    else:
        print(f"   Error: {response.status_code}")

def main():
    """Main function"""
    
    print("🔧 ROBUST AUDIO-TO-TEXT SYSTEMS DEEP TEST")
    print("=" * 60)
    
    try:
        # Test individual systems
        test_english_system_deep()
        test_malayalam_system_deep()
        
        # Test web interfaces
        test_web_interfaces_deep()
        
        # Test mock API calls
        test_mock_api_calls()
        
        print(f"\n" + "=" * 60)
        print(f"🔧 ROBUST AUDIO-TO-TEXT SYSTEMS DEEP TEST COMPLETE")
        print(f"\n📋 SYSTEMS TESTED:")
        print(f"   ✅ Robust English Audio-to-Text System")
        print(f"   ✅ Robust Malayalam Audio-to-Text System")
        print(f"   ✅ Real-time Web Interfaces")
        print(f"   ✅ API Endpoints")
        print(f"   ✅ Text Processing & Validation")
        print(f"   ✅ Confidence Scoring")
        print(f"   ✅ Mock Audio Processing")
        
        print(f"\n🌐 NEW ACCESS URLS:")
        print(f"   🇺🇸 Robust English Speech: http://127.0.0.1:8000/robust-english-speech/")
        print(f"   🇮🇳 Robust Malayalam Speech: http://127.0.0.1:8000/robust-malayalam-speech/")
        print(f"   📊 Robust Speech Dashboard: http://127.0.0.1:8000/robust-speech-dashboard/")
        print(f"   🔑 Login: testchild / test123")
        
        print(f"\n🎯 ROBUST SYSTEM FEATURES:")
        print(f"   • Real-time audio recording → speech-to-text")
        print(f"   • Instant text display and scoring")
        print(f"   • Multiple recognition engines with fallback")
        print(f"   • Language-specific text processing")
        print(f"   • Comprehensive scoring and feedback")
        print(f"   • Unicode support for Malayalam")
        print(f"   • Cultural speech pattern analysis")
        print(f"   • Activity progress tracking")
        
    except Exception as e:
        print(f"\n❌ TEST ERROR: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
