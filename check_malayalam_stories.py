#!/usr/bin/env python
import os
import sys
import django

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from core.models import Story

print("🔍 Analyzing Malayalam Stories...")
print("=" * 50)

malayalam_stories = Story.objects.filter(language='ml')
print(f"Found {malayalam_stories.count()} Malayalam stories")

for story in malayalam_stories:
    print(f"\nStory ID: {story.id}")
    print(f"Title: {story.title}")
    print(f"Language: {story.language}")
    print(f"Audio File: {story.audio_file.name if story.audio_file else 'None'}")
    
    if story.audio_file:
        print(f"Audio Path: {story.audio_file.path}")
        print(f"Audio URL: {story.audio_file.url}")
        print(f"File exists: {os.path.exists(story.audio_file.path) if story.audio_file else 'N/A'}")
        if story.audio_file and os.path.exists(story.audio_file.path):
            file_size = os.path.getsize(story.audio_file.path)
            print(f"File size: {file_size} bytes ({file_size/1024:.1f} KB)")
    else:
        print("⚠️  No audio file - will use TTS generation")

print("\n" + "=" * 50)
print("✅ Analysis complete")
