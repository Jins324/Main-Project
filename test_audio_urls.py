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

print("🔍 Testing Malayalam Audio URLs...")
print("=" * 50)

client = Client()
malayalam_stories = Story.objects.filter(language='ml')

for story in malayalam_stories:
    print(f"\nStory ID: {story.id}")
    print(f"Title: {story.title}")
    
    if story.audio_file:
        audio_url = story.audio_file.url
        print(f"Audio URL: {audio_url}")
        
        # Test if URL is accessible
        try:
            response = client.get(audio_url)
            print(f"HTTP Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Content-Type: {response.get('Content-Type', 'Unknown')}")
                print(f"Content-Length: {response.get('Content-Length', 'Unknown')}")
                print("✅ Audio URL is accessible")
            else:
                print(f"❌ Audio URL returned status {response.status_code}")
                print(f"Response content: {response.content[:200]}")
        except Exception as e:
            print(f"❌ Error accessing audio URL: {e}")
    else:
        print("⚠️  No audio file")

print("\n" + "=" * 50)
print("✅ Audio URL testing complete")
