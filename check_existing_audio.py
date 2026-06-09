#!/usr/bin/env python
"""
Check existing generated audio files and update Story model
"""
import os
import sys
import django
import re

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from core.models import Story
from django.core.files.base import ContentFile

def check_existing_audio():
    """Check for existing audio files and update Story model"""
    
    print("🔍 CHECKING EXISTING AUDIO FILES...")
    print("=" * 60)
    
    # Check media directories
    media_root = 'media'
    
    # Check original audio directory
    original_audio_dir = os.path.join(media_root, 'stories', 'audio')
    if os.path.exists(original_audio_dir):
        print(f"📁 Original Audio Directory: {original_audio_dir}")
        for root, dirs, files in os.walk(original_audio_dir):
            for file in files:
                if file.endswith(('.mp3', '.wav', '.ogg')):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, media_root)
                    print(f"   🎵 {rel_path}")
    
    # Check generated audio directory
    generated_audio_dir = os.path.join(media_root, 'generated_audio')
    if os.path.exists(generated_audio_dir):
        print(f"\n📁 Generated Audio Directory: {generated_audio_dir}")
        for root, dirs, files in os.walk(generated_audio_dir):
            for file in files:
                if file.endswith(('.mp3', '.wav', '.ogg')):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, media_root)
                    print(f"   🎵 {rel_path}")
    
    # Check all stories and their audio status
    print(f"\n📚 STORY AUDIO STATUS:")
    all_stories = Story.objects.all()
    
    for story in all_stories:
        status = []
        
        # Check original audio_file
        if story.audio_file and story.audio_file.name:
            status.append(f"📁 Original: {story.audio_file.name}")
        
        # Check generated_audio
        if story.generated_audio and story.generated_audio.name:
            status.append(f"🎤 Generated: {story.generated_audio.name}")
        
        # Check if there's a matching generated audio file
        story_id = story.id
        story_title_safe = re.sub(r'[^\w\s-]', '', story.title)[:30].strip()
        
        # Look for files with story ID in name
        potential_files = []
        if os.path.exists(generated_audio_dir):
            for root, dirs, files in os.walk(generated_audio_dir):
                for file in files:
                    if (str(story_id) in file or 
                        story.title.lower().replace(' ', '_') in file.lower() or
                        story_title_safe.replace(' ', '_') in file):
                        potential_files.append(file)
        
        if potential_files:
            status.append(f"🔍 Found: {', '.join(potential_files)}")
        
        if not status:
            status.append("❌ No audio")
        
        status_str = " | ".join(status)
        print(f"   {story.title[:40]:<40} {story.language:<5} {status_str}")
    
    return all_stories

def update_stories_with_existing_audio():
    """Update stories with existing audio files"""
    
    print(f"\n🔄 UPDATING STORIES WITH EXISTING AUDIO...")
    print("=" * 60)
    
    all_stories = Story.objects.all()
    updated_count = 0
    
    media_root = 'media'
    generated_audio_dir = os.path.join(media_root, 'generated_audio')
    
    for story in all_stories:
        if story.generated_audio and story.generated_audio.name:
            print(f"   ✅ {story.title[:30]} - Already has generated audio")
            continue
        
        # Look for matching audio files
        story_id = story.id
        found_file = None
        
        if os.path.exists(generated_audio_dir):
            for root, dirs, files in os.walk(generated_audio_dir):
                for file in files:
                    if (file.endswith(('.mp3', '.wav', '.ogg')) and 
                        (str(story_id) in file or 
                         story.title.lower().replace(' ', '_') in file.lower())):
                        
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, media_root)
                        found_file = file_path
                        break
                
                if found_file:
                    break
        
        if found_file:
            try:
                # Read the audio file
                with open(found_file, 'rb') as f:
                    audio_data = f.read()
                
                # Create ContentFile for Django
                audio_filename = f"generated_audio_{story.id}_{story.language}.mp3"
                audio_file = ContentFile(audio_data, name=audio_filename)
                
                # Update story
                story.generated_audio = audio_file
                story.audio_generation_method = "existing_file"
                story.save()
                
                print(f"   ✅ {story.title[:30]} - Updated with existing audio")
                updated_count += 1
                
            except Exception as e:
                print(f"   ❌ {story.title[:30]} - Error: {e}")
        else:
            print(f"   ⚠️  {story.title[:30]} - No existing audio found")
    
    print(f"\n📊 UPDATE SUMMARY:")
    print(f"   Stories Updated: {updated_count}")
    print(f"   Total Stories: {all_stories.count()}")
    
    return updated_count

def main():
    """Main function"""
    
    # Check existing audio
    all_stories = check_existing_audio()
    
    # Update stories with existing audio
    updated_count = update_stories_with_existing_audio()
    
    # Final status
    print(f"\n🎯 FINAL STATUS:")
    stories_with_audio = Story.objects.filter(
        models.Q(audio_file__isnull=False) | models.Q(generated_audio__isnull=False)
    ).count()
    
    print(f"   Stories with Audio: {stories_with_audio}/{all_stories.count()}")
    print(f"   Stories Updated: {updated_count}")
    
    if stories_with_audio == all_stories.count():
        print(f"   🎉 All stories now have audio!")
    else:
        print(f"   📝 Some stories still need audio generation")

if __name__ == "__main__":
    from django.db import models
    main()
