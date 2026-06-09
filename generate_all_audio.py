#!/usr/bin/env python
"""
Audio Pre-generation Script for All Stories
Generates audio files for all stories and saves them to the database
"""
import os
import sys
import django
import time
from datetime import datetime

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from core.models import Story
from core.audio_cache_views import generate_and_cache_audio
from django.core.files.base import ContentFile
from django.conf import settings

def generate_audio_for_all_stories():
    """Generate audio for all stories and save to database"""
    
    print("🎵 GENERATING AUDIO FOR ALL STORIES...")
    print("=" * 60)
    
    # Get all stories
    all_stories = Story.objects.all()
    print(f"Found {all_stories.count()} stories")
    
    success_count = 0
    error_count = 0
    
    for i, story in enumerate(all_stories, 1):
        print(f"\n[{i}/{all_stories.count()}] Processing: {story.title}")
        print(f"   Language: {story.get_language_display()} ({story.language})")
        print(f"   Story ID: {story.id}")
        
        # Generate audio for this story
        try:
            start_time = time.time()
            
            # Generate audio using the existing cache system
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
            
            # Read the generated audio file
            with open(cache_path, 'rb') as f:
                audio_data = f.read()
            
            # Create ContentFile for Django
            audio_filename = f"generated_audio_{story.id}_{story.language}.mp3"
            audio_file = ContentFile(audio_data, name=audio_filename)
            
            # Save to Story model
            if story.generated_audio:
                # Delete old file if exists
                if story.generated_audio.storage.exists(story.generated_audio.name):
                    story.generated_audio.delete(save=False)
            
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
    print(f"   Total Stories: {all_stories.count()}")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {error_count}")
    print(f"   📈 Success Rate: {(success_count/all_stories.count()*100):.1f}%")
    
    return success_count, error_count

def check_audio_status():
    """Check the current status of audio for all stories"""
    
    print("\n🔍 CHECKING AUDIO STATUS...")
    print("=" * 60)
    
    all_stories = Story.objects.all()
    
    malayalam_stories = all_stories.filter(language='ml')
    english_stories = all_stories.filter(language='en')
    
    print(f"📚 Total Stories: {all_stories.count()}")
    print(f"🇮🇳 Malayalam Stories: {malayalam_stories.count()}")
    print(f"🇺🇸 English Stories: {english_stories.count()}")
    
    # Check original audio files
    with_original_audio = all_stories.filter(audio_file__isnull=False).count()
    with_generated_audio = all_stories.filter(generated_audio__isnull=False).count()
    
    print(f"\n📁 Audio Files:")
    print(f"   Original Audio Files: {with_original_audio}")
    print(f"   Generated Audio Files: {with_generated_audio}")
    print(f"   Stories with Audio: {with_original_audio + with_generated_audio}")
    
    # Detailed breakdown
    print(f"\n📋 Detailed Status:")
    for story in all_stories:
        status = []
        
        if story.audio_file:
            status.append("📁 Original")
        if story.generated_audio:
            status.append("🎤 Generated")
        
        if not status:
            status.append("❌ None")
        
        status_str = " | ".join(status)
        print(f"   {story.title[:30]:<30} {story.language:<5} {status_str}")
    
    return with_original_audio + with_generated_audio

def main():
    """Main function"""
    
    # Check current status first
    current_audio_count = check_audio_status()
    
    print(f"\n🤔 Do you want to generate audio for stories without audio? (y/n)")
    
    # For automation, we'll generate for all stories
    print("🚀 Generating audio for all stories...")
    
    success_count, error_count = generate_audio_for_all_stories()
    
    if success_count > 0:
        print(f"\n✅ Successfully generated audio for {success_count} stories!")
        print(f"🎯 Next step: Update story-mode to use generated audio")
        
        # Check final status
        final_audio_count = check_audio_status()
        if final_audio_count > current_audio_count:
            print(f"📈 Audio count increased from {current_audio_count} to {final_audio_count}")
        else:
            print(f"📊 Audio count: {final_audio_count}")
    else:
        print(f"\n❌ No audio was generated successfully")

if __name__ == "__main__":
    main()
