#!/usr/bin/env python
"""
Test separated English and Malayalam speech systems
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
from english_speech_system import EnglishSpeechSystem
from malayalam_speech_system import MalayalamSpeechSystem
from unified_speech_processor import UnifiedSpeechProcessor

def test_english_system():
    """Test English speech system"""
    
    print("🇺🇸 TESTING ENGLISH SPEECH SYSTEM")
    print("=" * 60)
    
    system = EnglishSpeechSystem()
    
    # Test system info
    info = system.get_system_info()
    print(f"Language: {info['language']}")
    print(f"Recognition Engines: {', '.join(info['recognition_engines'])}")
    print(f"TTS Engine: {info['tts_engine']}")
    print(f"Voice Options: {', '.join(info['voice_options'])}")
    
    # Test pronunciation scoring
    print(f"\n🧪 English Pronunciation Scoring:")
    test_cases = [
        ("hello world", "hello world", "Perfect match"),
        ("helo world", "hello world", "Close match"),
        ("goodbye", "hello world", "Poor match"),
        ("", "hello world", "Empty input")
    ]
    
    for recognized, expected, description in test_cases:
        score = system.calculate_pronunciation_score(recognized, expected)
        print(f"   {description}: {score:.1f}")
    
    # Test fluency analysis
    print(f"\n📊 English Fluency Analysis:")
    # Mock audio analysis (would normally use audio file)
    fluency_result = system.analyze_fluency("mock_audio.wav", "hello world", "hello world")
    print(f"   Fluency Score: {fluency_result.get('score', 0):.1f}")
    print(f"   WPM: {fluency_result.get('wpm', 0):.1f}")
    
    # Test audio generation
    print(f"\n🎵 English Audio Generation:")
    audio_data = system.generate_audio("Hello world, this is a test.")
    if audio_data:
        print(f"   ✅ Audio generated: {len(audio_data)} bytes")
    else:
        print(f"   ❌ Audio generation failed")
    
    print(f"✅ English Speech System Test Complete!")

def test_malayalam_system():
    """Test Malayalam speech system"""
    
    print(f"\n🇮🇳 TESTING MALAYALAM SPEECH SYSTEM")
    print("=" * 60)
    
    system = MalayalamSpeechSystem()
    
    # Test system info
    info = system.get_system_info()
    print(f"Language: {info['language']}")
    print(f"Recognition Engines: {', '.join(info['recognition_engines'])}")
    print(f"TTS Engines: {', '.join(info['tts_engines'])}")
    print(f"Unicode Support: {info['unicode_support']}")
    print(f"Special Features: {', '.join(info['special_features'])}")
    
    # Test pronunciation scoring
    print(f"\n🧪 Malayalam Pronunciation Scoring:")
    test_cases = [
        ("നമസ്കാരം", "നമസ്കാരം", "Perfect match"),
        ("നമസ്കരം", "നമസ്കാരം", "Close match"),
        ("വണക്ക്", "നമസ്കാരം", "Poor match"),
        ("", "നമസ്കാരം", "Empty input")
    ]
    
    for recognized, expected, description in test_cases:
        score = system.calculate_pronunciation_score(recognized, expected)
        print(f"   {description}: {score:.1f}")
    
    # Test fluency analysis
    print(f"\n📊 Malayalam Fluency Analysis:")
    fluency_result = system.analyze_fluency("mock_audio.wav", "നമസ്കാരം", "നമസ്കാരം")
    print(f"   Fluency Score: {fluency_result.get('score', 0):.1f}")
    print(f"   WPM: {fluency_result.get('wpm', 0):.1f}")
    
    # Test audio generation
    print(f"\n🎵 Malayalam Audio Generation:")
    audio_data = system.generate_audio("നമസ്കാരം.")
    if audio_data:
        print(f"   ✅ Audio generated: {len(audio_data)} bytes")
    else:
        print(f"   ❌ Audio generation failed")
    
    print(f"✅ Malayalam Speech System Test Complete!")

def test_unified_processor():
    """Test unified speech processor"""
    
    print(f"\n🌍 TESTING UNIFIED SPEECH PROCESSOR")
    print("=" * 60)
    
    processor = UnifiedSpeechProcessor()
    
    # Test supported languages
    languages = processor.get_supported_languages()
    print(f"Supported Languages:")
    for code, info in languages.items():
        print(f"   {code}: {info['name']} ({info['system']})")
    
    # Test English processing
    print(f"\n🧪 Testing English Processing:")
    result = processor.process_audio_recording("test_en.wav", "hello world", "en")
    if result.get('success'):
        scores = result.get('scores', {})
        print(f"   ✅ Success: Overall {scores.get('overall', 0):.1f}")
        print(f"   Pronunciation: {scores.get('pronunciation', 0):.1f}")
        print(f"   Fluency: {scores.get('fluency', 0):.1f}")
        print(f"   Accuracy: {scores.get('accuracy', 0):.1f}")
        print(f"   Engine: {result.get('recognition_engine', 'unknown')}")
    else:
        print(f"   ❌ Failed: {result.get('error', 'Unknown')}")
    
    # Test Malayalam processing
    print(f"\n🧪 Testing Malayalam Processing:")
    result = processor.process_audio_recording("test_ml.wav", "നമസ്കാരം", "ml")
    if result.get('success'):
        scores = result.get('scores', {})
        print(f"   ✅ Success: Overall {scores.get('overall', 0):.1f}")
        print(f"   Pronunciation: {scores.get('pronunciation', 0):.1f}")
        print(f"   Fluency: {scores.get('fluency', 0):.1f}")
        print(f"   Accuracy: {scores.get('accuracy', 0):.1f}")
        print(f"   Engine: {result.get('recognition_engine', 'unknown')}")
    else:
        print(f"   ❌ Failed: {result.get('error', 'Unknown')}")
    
    print(f"✅ Unified Processor Test Complete!")

def test_web_interfaces():
    """Test web interfaces for separated systems"""
    
    print(f"\n🌐 TESTING WEB INTERFACES")
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
    
    # Test English speech page
    print(f"\n📄 Testing English Speech Page:")
    response = client.get('/english-speech/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        elements = [
            'English Speech Recording',
            'language_name',
            'system_info',
            'practice_text'
        ]
        
        for element in elements:
            if element in content:
                print(f"   ✅ Found: {element}")
            else:
                print(f"   ❌ Missing: {element}")
    
    # Test Malayalam speech page
    print(f"\n📄 Testing Malayalam Speech Page:")
    response = client.get('/malayalam-speech/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        elements = [
            'Malayalam Speech Recording',
            'language_name',
            'system_info',
            'practice_text'
        ]
        
        for element in elements:
            if element in content:
                print(f"   ✅ Found: {element}")
            else:
                print(f"   ❌ Missing: {element}")
    
    # Test English APIs
    print(f"\n🔌 Testing English APIs:")
    
    # Start English recording
    response = client.post('/api/start-english-recording/', 
                          json.dumps({'expected_text': 'hello world'}),
                          content_type='application/json')
    print(f"   Start English Recording: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Session ID: {data.get('session_id', 'N/A')}")
            print(f"   ✅ Language: {data.get('language', 'N/A')}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown')}")
    
    # Test Malayalam APIs
    print(f"\n🔌 Testing Malayalam APIs:")
    
    # Start Malayalam recording
    response = client.post('/api/start-malayalam-recording/', 
                          json.dumps({'expected_text': 'നമസ്കാരം'}),
                          content_type='application/json')
    print(f"   Start Malayalam Recording: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Session ID: {data.get('session_id', 'N/A')}")
            print(f"   ✅ Language: {data.get('language', 'N/A')}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown')}")
    
    # Test system stats API
    print(f"\n📊 Testing System Stats API:")
    response = client.get('/api/language-system-stats/')
    print(f"   Language System Stats: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            english_stats = data.get('english_stats', {})
            malayalam_stats = data.get('malayalam_stats', {})
            
            print(f"   ✅ English Recordings: {english_stats.get('total_recordings', 0)}")
            print(f"   ✅ Malayalam Recordings: {malayalam_stats.get('total_recordings', 0)}")
            print(f"   ✅ Total Recordings: {data.get('total_recordings', 0)}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown')}")

def main():
    """Main function"""
    
    print("🔧 SEPARATED SPEECH SYSTEMS TEST")
    print("=" * 60)
    
    # Test individual systems
    test_english_system()
    test_malayalam_system()
    
    # Test unified processor
    test_unified_processor()
    
    # Test web interfaces
    test_web_interfaces()
    
    print(f"\n" + "=" * 60)
    print(f"🔧 SEPARATED SPEECH SYSTEMS TEST COMPLETE")
    print(f"\n📋 SYSTEMS TESTED:")
    print(f"   ✅ English Speech System (Recognition + TTS)")
    print(f"   ✅ Malayalam Speech System (Recognition + TTS)")
    print(f"   ✅ Unified Speech Processor (Coordinator)")
    print(f"   ✅ Separated Web Interfaces")
    print(f"   ✅ Language-Specific APIs")
    print(f"   ✅ Independent Processing Pipelines")
    
    print(f"\n🌐 NEW ACCESS URLS:")
    print(f"   🇺🇸 English Speech: http://127.0.0.1:8000/english-speech/")
    print(f"   🇮🇳 Malayalam Speech: http://127.0.0.1:8000/malayalam-speech/")
    print(f"   📊 System Dashboard: http://127.0.0.1:8000/speech-system-dashboard/")
    print(f"   🔑 Login: testchild / test123")
    
    print(f"\n🎯 SEPARATION BENEFITS:")
    print(f"   • English: Optimized for English phonetics and rhythm")
    print(f"   • Malayalam: Unicode support + cultural speech patterns")
    print(f"   • Independent: Separate engines and processing")
    print(f"   • Specialized: Language-specific scoring algorithms")
    print(f"   • Scalable: Easy to extend with new languages")
    print(f"   • Accurate: Better recognition and TTS quality")

if __name__ == "__main__":
    main()
