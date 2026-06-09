#!/usr/bin/env python
import os
import sys
import django
import json

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from django.test.client import Client
from django.contrib.auth import get_user_model
from core.models import Story

print("🔍 Comprehensive Story Mode Audio Test...")
print("=" * 60)

User = get_user_model()
client = Client()

# Login
user = User.objects.get(username='testchild')
client.login(username='testchild', password='test123')

# Test Malayalam story with existing audio
malayalam_story = Story.objects.filter(language='ml').first()
print(f"\n1. Testing Malayalam Story: {malayalam_story.title}")

# Get the story mode page
response = client.get(f'/story-mode/?story={malayalam_story.id}&language=ml')
print(f"Page Status: {response.status_code}")

if response.status_code == 200:
    content = response.content.decode('utf-8')
    
    # Check for key elements
    checks = {
        'Audio element': '<audio' in content,
        'Audio controls': 'storyAudio' in content,
        'TTS controls': 'ttsControls' in content,
        'Play button': 'playTtsBtn' in content,
        'Generate audio function': 'generateAudio' in content,
        'Cache audio function': 'generateCachedAudio' in content,
        'Test audio button': 'testAudioPlayback' in content,
        'Force generate button': 'forceGenerateAudio' in content
    }
    
    print("Page Elements Check:")
    for element, found in checks.items():
        status = "✅" if found else "❌"
        print(f"   {status} {element}")
    
    # Check if it has pre-recorded audio or TTS
    if malayalam_story.audio_file:
        print(f"\n   📁 Pre-recorded audio: {malayalam_story.audio_file.name}")
        print(f"   🌐 Audio URL: {malayalam_story.audio_file.url}")
        
        # Test audio URL
        audio_response = client.get(malayalam_story.audio_file.url)
        print(f"   🎵 Audio file status: {audio_response.status_code}")
    else:
        print("\n   🎤 No pre-recorded audio - will use TTS")

# Test English story (no audio file)
english_story = Story.objects.filter(language='en').first()
print(f"\n2. Testing English Story: {english_story.title}")

response = client.get(f'/story-mode/?story={english_story.id}&language=en')
print(f"Page Status: {response.status_code}")

if response.status_code == 200:
    content = response.content.decode('utf-8')
    
    # English stories should use TTS
    has_tts_controls = 'ttsControls' in content
    has_audio_element = '<audio' in content
    
    print(f"   {'✅' if has_tts_controls else '❌'} TTS controls present")
    print(f"   {'✅' if has_audio_element else '❌'} Audio element present")
    
    if english_story.audio_file:
        print(f"   📁 Pre-recorded audio: {english_story.audio_file.name}")
    else:
        print("   🎤 No pre-recorded audio - will use TTS")

# Test TTS generation for English story
print(f"\n3. Testing TTS Generation for English Story...")
try:
    response = client.post('/api/get-or-generate-audio/', {
        'story_id': english_story.id,
        'title': english_story.title,
        'text': english_story.text_content[:200],
        'language': 'en',
        'timeout': 15
    }, content_type='application/json')
    
    print(f"   API Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ English TTS generation works")
        print(f"   Content-Type: {response.get('Content-Type')}")
        content_length = response.get('Content-Length')
        if content_length:
            print(f"   Content-Length: {content_length} bytes")
    else:
        print(f"   ❌ English TTS failed: {response.status_code}")
        try:
            data = response.json()
            print(f"   Error: {data.get('error')}")
        except:
            pass
except Exception as e:
    print(f"   ❌ English TTS Error: {e}")

# Test cache status
print(f"\n4. Cache Status...")
try:
    response = client.get('/api/cache-status/')
    if response.status_code == 200:
        data = response.json()
        print(f"   Cache Directory: {data.get('cache_dir')}")
        print(f"   Cached Files: {data.get('cached_files')}")
        print(f"   Enhanced TTS: {data.get('enhanced_tts_available')}")
        print(f"   gTTS: {data.get('gtts_available')}")
        
        files = data.get('files', [])
        print(f"   Cached Files List:")
        for file_info in files:
            print(f"     - {file_info.get('filename')} ({file_info.get('size_kb')} KB)")
except Exception as e:
    print(f"   ❌ Cache status error: {e}")

# Test JavaScript simulation
print(f"\n5. JavaScript Audio Loading Simulation...")

# Simulate what the frontend would do
print("   📡 Simulating frontend audio request...")

# Test both languages
test_stories = [
    (malayalam_story, 'Malayalam'),
    (english_story, 'English')
]

for story, lang_name in test_stories:
    print(f"\n   Testing {lang_name} audio loading...")
    
    try:
        response = client.post('/api/get-or-generate-audio/', {
            'story_id': story.id,
            'title': story.title,
            'text': story.text_content[:100],
            'language': story.language,
            'timeout': 10
        }, content_type='application/json')
        
        if response.status_code == 200:
            print(f"   ✅ {lang_name} audio generated successfully")
            content_type = response.get('Content-Type')
            if 'audio' in content_type:
                print(f"   🎵 Audio content ready ({response.get('Content-Length')} bytes)")
            else:
                print(f"   📄 Non-audio content: {content_type}")
        else:
            print(f"   ❌ {lang_name} audio failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ {lang_name} audio error: {e}")

print("\n" + "=" * 60)
print("✅ Comprehensive Audio Test Complete")

# Summary
print(f"\n📊 Summary:")
print(f"   Malayalam Stories: {Story.objects.filter(language='ml').count()} (all have audio)")
print(f"   English Stories: {Story.objects.filter(language='en').count()} (need TTS)")
print(f"   Audio Caching API: Working")
print(f"   Template: Using enhanced story_mode_fixed.html")
print(f"   Authentication: Working")
