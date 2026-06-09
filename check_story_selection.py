#!/usr/bin/env python
import os
import sys
import django

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from django.test.client import Client
from django.contrib.auth import get_user_model
from core.models import Story

print("🔍 CHECKING STORY SELECTION LOGIC...")
print("=" * 60)

User = get_user_model()
client = Client()
user = User.objects.get(username='testchild')
client.login(username='testchild', password='test123')

# Test 1: Check if story is being passed to template
print("\n1. Testing Story Selection Logic...")

# Get a Malayalam story
malayalam_story = Story.objects.filter(language='ml').first()
print(f"   Testing with Malayalam story: {malayalam_story.title}")
print(f"   Story ID: {malayalam_story.id}")
print(f"   Has audio file: {bool(malayalam_story.audio_file)}")
if malayalam_story.audio_file:
    print(f"   Audio file path: {malayalam_story.audio_file.name}")
    print(f"   Audio file exists: {malayalam_story.audio_file.storage.exists(malayalam_story.audio_file.name)}")

# Test the view directly
response = client.get(f'/story-mode/?story={malayalam_story.id}&language=ml')
print(f"   Response Status: {response.status_code}")

if response.status_code == 200:
    content = response.content.decode('utf-8')
    
    # Check if story object is in the template
    if 'story.audio_file' in content:
        print("   ✅ Template has story.audio_file reference")
    else:
        print("   ❌ Template missing story.audio_file reference")
    
    # Check if the audio element is rendered
    if 'id="storyAudio"' in content:
        print("   ✅ Audio element rendered")
    else:
        print("   ❌ Audio element NOT rendered")
    
    # Check if TTS controls are rendered (for stories without audio)
    if 'id="ttsControls"' in content:
        print("   ✅ TTS controls rendered")
    else:
        print("   ❌ TTS controls NOT rendered")
    
    # Look for the story title
    if malayalam_story.title in content:
        print("   ✅ Story title found in template")
    else:
        print("   ❌ Story title NOT found in template")
    
    # Look for story content
    if malayalam_story.text_content[:50] in content:
        print("   ✅ Story content found in template")
    else:
        print("   ❌ Story content NOT found in template")
    
    # Check for template conditionals
    if '{% if story.audio_file %}' in content:
        print("   ✅ Template conditional found")
    else:
        print("   ❌ Template conditional NOT found")

# Test 2: Check the view logic
print("\n2. Checking View Logic...")

# Import the view function
from core.views import story_mode
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

# Create a mock request
factory = RequestFactory()
request = factory.get(f'/story-mode/?story={malayalam_story.id}&language=ml')
request.user = user

try:
    # Call the view function
    response = story_mode(request)
    print(f"   View Response Status: {response.status_code}")
    
    # Check the context
    if hasattr(response, 'context_data'):
        context = response.context_data
        print(f"   Story in context: {context.get('story') is not None}")
        print(f"   Story ID: {context.get('story').id if context.get('story') else 'None'}")
        print(f"   Story Title: {context.get('story').title if context.get('story') else 'None'}")
        print(f"   Has Audio: {bool(context.get('story').audio_file) if context.get('story') else 'None'}")
    else:
        print("   ❌ No context_data in response")
        
except Exception as e:
    print(f"   ❌ View Error: {e}")

# Test 3: Check English story
print("\n3. Testing English Story...")
english_story = Story.objects.filter(language='en').first()
print(f"   Testing with English story: {english_story.title}")
print(f"   Has audio file: {bool(english_story.audio_file)}")

response = client.get(f'/story-mode/?story={english_story.id}&language=en')
print(f"   Response Status: {response.status_code}")

if response.status_code == 200:
    content = response.content.decode('utf-8')
    
    if 'id="storyAudio"' in content:
        print("   ✅ Audio element rendered (should not be there)")
    else:
        print("   ✅ Audio element correctly NOT rendered")
    
    if 'id="ttsControls"' in content:
        print("   ✅ TTS controls rendered (correct)")
    else:
        print("   ❌ TTS controls NOT rendered (incorrect)")

print("\n" + "=" * 60)
print("🔍 STORY SELECTION ANALYSIS COMPLETE")
