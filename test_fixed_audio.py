#!/usr/bin/env python
import os
import sys
import django

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from django.test.client import Client
from core.models import Story
from django.contrib.auth import get_user_model

print("🔧 Testing Fixed Audio Generation...")
print("=" * 50)

client = Client()
User = get_user_model()
user = User.objects.get(username='testchild')
client.login(username='testchild', password='test123')

# Test English TTS generation
english_story = Story.objects.filter(language='en').first()
print(f"\nTesting English TTS for: {english_story.title}")

try:
    response = client.post('/api/get-or-generate-audio/', {
        'story_id': english_story.id,
        'title': english_story.title,
        'text': english_story.text_content[:100],
        'language': 'en',
        'timeout': 15
    }, content_type='application/json')
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ English TTS works!")
        content_type = response.get('Content-Type')
        content_length = response.get('Content-Length')
        print(f"Content-Type: {content_type}")
        print(f"Content-Length: {content_length} bytes")
    else:
        print("❌ English TTS failed")
        try:
            data = response.json()
            print(f"Error: {data.get('error')}")
        except:
            print("Response:", response.content[:200])
except Exception as e:
    print(f"❌ Error: {e}")

# Test Malayalam TTS generation (new story)
malayalam_story = Story.objects.filter(language='ml').first()
print(f"\nTesting Malayalam TTS for: {malayalam_story.title}")

try:
    response = client.post('/api/get-or-generate-audio/', {
        'story_id': malayalam_story.id,
        'title': malayalam_story.title,
        'text': malayalam_story.text_content[:100],
        'language': 'ml',
        'timeout': 15
    }, content_type='application/json')
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Malayalam TTS works!")
        content_type = response.get('Content-Type')
        content_length = response.get('Content-Length')
        print(f"Content-Type: {content_type}")
        print(f"Content-Length: {content_length} bytes")
    else:
        print("❌ Malayalam TTS failed")
        try:
            data = response.json()
            print(f"Error: {data.get('error')}")
        except:
            print("Response:", response.content[:200])
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("✅ Audio Generation Test Complete")
