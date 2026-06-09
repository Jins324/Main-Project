#!/usr/bin/env python
"""
Generate audio for remaining stories without audio
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

def generate_missing_audio():
    """Generate audio for stories that don't have any"""
    
    print("🎵 GENERATING AUDIO FOR MISSING STORIES...")
    print("=" * 60)
    
    # Find stories without audio
    stories_without_audio = Story.objects.filter(
        audio_file__isnull=True,
        generated_audio__isnull=True
    )
    
    print(f"Found {stories_without_audio.count()} stories without audio")
    
    success_count = 0
    error_count = 0
    
    for i, story in enumerate(stories_without_audio, 1):
        print(f"\n[{i}/{stories_without_audio.count()}] Generating: {story.title}")
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
    print(f"📊 GENERATION SUMMARY:")
    print(f"   Stories Processed: {stories_without_audio.count()}")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {error_count}")
    print(f"   📈 Success Rate: {(success_count/stories_without_audio.count()*100):.1f}%" if stories_without_audio.count() > 0 else "N/A")
    
    return success_count, error_count

def final_verification():
    """Final verification of all stories having audio"""
    
    print(f"\n🔍 FINAL VERIFICATION...")
    print("=" * 60)
    
    all_stories = Story.objects.all()
    stories_with_audio = Story.objects.filter(
        models.Q(audio_file__isnull=False) | models.Q(generated_audio__isnull=False)
    )
    
    print(f"   Total Stories: {all_stories.count()}")
    print(f"   Stories with Audio: {stories_with_audio.count()}")
    print(f"   Stories without Audio: {all_stories.count() - stories_with_audio.count()}")
    
    if stories_with_audio.count() == all_stories.count():
        print(f"   🎉 ALL STORIES NOW HAVE AUDIO!")
    else:
        print(f"   ⚠️  Some stories still need audio")
    
    # Show final status
    print(f"\n📋 FINAL AUDIO STATUS:")
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

def main():
    """Main function"""
    
    # Generate missing audio
    success_count, error_count = generate_missing_audio()
    
    # Final verification
    final_verification()
    
    if success_count > 0:
        print(f"\n✅ Successfully generated audio for {success_count} more stories!")
        print(f"🎯 Audio playback should now work for all stories")
        print(f"🌐 Test URL: http://127.0.0.1:8000/story-mode/")
        print(f"🔑 Login: testchild/test123")

if __name__ == "__main__":
    from django.db import models
    main()
