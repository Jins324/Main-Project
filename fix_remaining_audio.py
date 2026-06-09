#!/usr/bin/env python
"""
Fix remaining English stories without audio
"""
import os
import sys
import django
import time

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from core.models import Story
from core.audio_cache_views import generate_and_cache_audio
from django.core.files.base import ContentFile
from datetime import datetime

def fix_remaining_stories():
    """Fix remaining stories without audio"""
    
    print("🔧 FIXING REMAINING STORIES WITHOUT AUDIO...")
    print("=" * 60)
    
    # Find English stories without audio
    english_stories = Story.objects.filter(language='en')
    print(f"Total English stories: {english_stories.count()}")
    
    stories_to_fix = []
    for story in english_stories:
        if not story.audio_file and not story.generated_audio:
            stories_to_fix.append(story)
    
    print(f"English stories needing audio: {len(stories_to_fix)}")
    
    success_count = 0
    error_count = 0
    
    for i, story in enumerate(stories_to_fix, 1):
        print(f"\n[{i}/{len(stories_to_fix)}] Fixing: {story.title}")
        print(f"   Language: {story.get_language_display()} ({story.language})")
        print(f"   Story ID: {story.id}")
        
        try:
            start_time = time.time()
            
            # Generate audio using existing cache system
            cache_path, method_used, error = generate_and_cache_audio(
                story.text_content, 
                story.id, 
                story.title, 
                story.language
            )
            
            generation_time = time.time() - start_time
            
            if error:
                print(f"   ❌ Generation failed: {error}")
                error_count += 1
                continue
            
            if not cache_path or not os.path.exists(cache_path):
                print(f"   ❌ No audio file generated")
                error_count += 1
                continue
            
            # Read generated audio file
            with open(cache_path, 'rb') as f:
                audio_data = f.read()
            
            # Create ContentFile for Django
            audio_filename = f"generated_audio_{story.id}_{story.language}.mp3"
            audio_file = ContentFile(audio_data, name=audio_filename)
            
            # Save to Story model
            story.generated_audio = audio_file
            story.audio_generation_method = method_used
            story.audio_generation_date = datetime.now()
            story.audio_generation_time = generation_time
            story.save()
            
            print(f"   ✅ Audio generated successfully!")
            print(f"   📁 Method: {method_used}")
            print(f"   ⏱️  Time: {generation_time:.2f} seconds")
            print(f"   📊 Size: {len(audio_data)} bytes")
            print(f"   💾 Saved as: {audio_filename}")
            
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ Error processing story: {e}")
            error_count += 1
            import traceback
            traceback.print_exc()
    
    print(f"\n" + "=" * 60)
    print(f"📊 FIX SUMMARY:")
    print(f"   Stories Processed: {len(stories_to_fix)}")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {error_count}")
    
    return success_count, error_count

def final_test():
    """Final test of all stories"""
    
    print(f"\n🧪 FINAL AUDIO TEST...")
    print("=" * 60)
    
    all_stories = Story.objects.all()
    
    for story in all_stories:
        status = []
        
        if story.audio_file and story.audio_file.name:
            status.append("📁 Original")
        
        if story.generated_audio and story.generated_audio.name:
            status.append("🎤 Generated")
        
        if not status:
            status.append("❌ None")
        
        status_str = " | ".join(status)
        print(f"   {story.title[:40]:<40} {story.language:<5} {status_str}")
    
    # Check final count
    stories_with_audio = Story.objects.filter(
        models.Q(audio_file__isnull=False) | models.Q(generated_audio__isnull=False)
    )
    
    print(f"\n📊 FINAL COUNT:")
    print(f"   Total Stories: {all_stories.count()}")
    print(f"   Stories with Audio: {stories_with_audio.count()}")
    
    if stories_with_audio.count() == all_stories.count():
        print(f"   🎉 ALL STORIES HAVE AUDIO!")
        return True
    else:
        print(f"   ⚠️  {all_stories.count() - stories_with_audio.count()} stories still need audio")
        return False

def main():
    """Main function"""
    
    # Fix remaining stories
    success_count, error_count = fix_remaining_stories()
    
    # Final test
    all_have_audio = final_test()
    
    if all_have_audio:
        print(f"\n✅ SUCCESS! All stories now have audio!")
        print(f"🎯 Audio playback should work for all stories")
        print(f"🌐 Test URL: http://127.0.0.1:8000/story-mode/")
        print(f"🔑 Login: testchild/test123")
    else:
        print(f"\n⚠️  Some stories still need audio")

if __name__ == "__main__":
    from django.db import models
    main()
