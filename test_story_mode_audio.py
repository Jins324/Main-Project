#!/usr/bin/env python
import os
import sys
import django
import requests

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from django.test.client import Client
from core.models import Story

print("🔍 Testing Story Mode Audio Playback...")
print("=" * 60)

client = Client()

# Test 1: Check if story-mode page loads
print("\n1. Testing Story Mode Page Loading...")
try:
    response = client.get('/story-mode/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Story mode page loads successfully")
    else:
        print(f"   ❌ Story mode page failed: {response.status_code}")
        print(f"   Response: {response.content[:200]}")
except Exception as e:
    print(f"   ❌ Error loading story mode: {e}")

# Test 2: Check Malayalam stories
print("\n2. Checking Malayalam Stories...")
malayalam_stories = Story.objects.filter(language='ml')
print(f"   Found {malayalam_stories.count()} Malayalam stories")

for story in malayalam_stories:
    print(f"   Story {story.id}: {story.title}")
    print(f"     Audio file: {story.audio_file.name if story.audio_file else 'None'}")
    if story.audio_file:
        print(f"     Audio URL: {story.audio_file.url}")
        # Test audio URL accessibility
        try:
            audio_response = client.get(story.audio_file.url)
            print(f"     Audio URL Status: {audio_response.status_code}")
        except Exception as e:
            print(f"     Audio URL Error: {e}")

# Test 3: Check English stories  
print("\n3. Checking English Stories...")
english_stories = Story.objects.filter(language='en')
print(f"   Found {english_stories.count()} English stories")

for story in english_stories:
    print(f"   Story {story.id}: {story.title}")
    print(f"     Audio file: {story.audio_file.name if story.audio_file else 'None'}")
    if story.audio_file:
        print(f"     Audio URL: {story.audio_file.url}")
        # Test audio URL accessibility
        try:
            audio_response = client.get(story.audio_file.url)
            print(f"     Audio URL Status: {audio_response.status_code}")
        except Exception as e:
            print(f"     Audio URL Error: {e}")

# Test 4: Test audio caching API
print("\n4. Testing Audio Caching API...")
test_story = malayalam_stories.first() if malayalam_stories.exists() else english_stories.first()

if test_story:
    print(f"   Testing with story: {test_story.title} (ID: {test_story.id})")
    
    try:
        response = client.post('/api/get-or-generate-audio/', {
            'story_id': test_story.id,
            'title': test_story.title,
            'text': test_story.text_content[:200],
            'language': test_story.language,
            'timeout': 10
        }, content_type='application/json')
        
        print(f"   API Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Audio caching API works")
            print(f"   Content-Type: {response.get('Content-Type')}")
            print(f"   Content-Length: {response.get('Content-Length', 'Unknown')}")
        else:
            print(f"   ❌ Audio caching API failed: {response.status_code}")
            print(f"   Response: {response.content[:200]}")
    except Exception as e:
        print(f"   ❌ Audio caching API Error: {e}")

# Test 5: Check cache status
print("\n5. Checking Cache Status...")
try:
    response = client.get('/api/cache-status/')
    print(f"   Cache Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Cache Directory: {data.get('cache_dir')}")
        print(f"   Cache Exists: {data.get('cache_exists')}")
        print(f"   Cached Files: {data.get('cached_files')}")
        print(f"   Enhanced TTS Available: {data.get('enhanced_tts_available')}")
        print(f"   gTTS Available: {data.get('gtts_available')}")
    else:
        print(f"   ❌ Cache status API failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Cache status Error: {e}")

print("\n" + "=" * 60)
print("✅ Audio Analysis Complete")
