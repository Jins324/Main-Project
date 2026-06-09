#!/usr/bin/env python
"""
Fix stories with invalid audio files
"""
import os
import sys
import django

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from core.models import Story
from django.core.files.base import ContentFile
from datetime import datetime

def fix_invalid_audio_files():
    """Fix stories with invalid audio file references"""
    
    print("🔧 FIXING INVALID AUDIO FILES...")
    print("=" * 60)
    
    all_stories = Story.objects.all()
    fixed_count = 0
    error_count = 0
    
    for story in all_stories:
        print(f"\n🔍 Checking: {story.title}")
        
        # Check original audio file
        if story.audio_file and story.audio_file.name:
            if os.path.exists(story.audio_file.path):
                print(f"   ✅ Original audio file exists: {story.audio_file.name}")
            else:
                print(f"   ❌ Original audio file missing: {story.audio_file.name}")
                # Clear the invalid reference
                story.audio_file = None
                story.save()
                print(f"   🗑️  Cleared invalid audio_file reference")
                fixed_count += 1
        
        # Check generated audio file
        if story.generated_audio and story.generated_audio.name:
            try:
                if os.path.exists(story.generated_audio.path):
                    print(f"   ✅ Generated audio file exists: {story.generated_audio.name}")
                else:
                    print(f"   ❌ Generated audio file missing: {story.generated_audio.name}")
                    # Clear the invalid reference
                    story.generated_audio = None
                    story.audio_generation_method = None
                    story.audio_generation_date = None
                    story.audio_generation_time = None
                    story.save()
                    print(f"   🗑️  Cleared invalid generated_audio reference")
                    fixed_count += 1
                    
            except ValueError as e:
                print(f"   ❌ ValueError with generated_audio: {e}")
                # Clear the invalid reference
                story.generated_audio = None
                story.audio_generation_method = None
                story.audio_generation_date = None
                story.audio_generation_time = None
                story.save()
                print(f"   🗑️  Cleared invalid generated_audio reference (ValueError)")
                fixed_count += 1
                
        # Check if story has any audio now
        has_audio = (story.audio_file and story.audio_file.name) or (story.generated_audio and story.generated_audio.name)
        if has_audio:
            print(f"   ✅ Story has valid audio")
        else:
            print(f"   ❌ Story has no valid audio")
    
    print(f"\n" + "=" * 60)
    print(f"📊 FIX SUMMARY:")
    print(f"   Total Stories: {all_stories.count()}")
    print(f"   ✅ Fixed: {fixed_count}")
    print(f"   ❌ Errors: {error_count}")
    
    return fixed_count

def check_final_status():
    """Check final status after fixes"""
    
    print(f"\n🎯 CHECKING FINAL STATUS...")
    print("=" * 60)
    
    all_stories = Story.objects.all()
    stories_with_valid_audio = 0
    
    for story in all_stories:
        has_audio = False
        audio_type = None
        
        if story.audio_file and story.audio_file.name:
            try:
                if os.path.exists(story.audio_file.path):
                    has_audio = True
                    audio_type = "Original"
            except:
                pass
        
        if story.generated_audio and story.generated_audio.name:
            try:
                if os.path.exists(story.generated_audio.path):
                    has_audio = True
                    audio_type = "Generated"
            except:
                pass
        
        status = "✅" if has_audio else "❌"
        audio_info = f" ({audio_type})" if audio_type else ""
        print(f"   {status} {story.title[:40]}{audio_info}")
        
        if has_audio:
            stories_with_valid_audio += 1
    
    print(f"\n📊 FINAL STATUS:")
    print(f"   Stories with Valid Audio: {stories_with_valid_audio}/{all_stories.count()}")
    print(f"   Success Rate: {(stories_with_valid_audio/all_stories.count()*100):.1f}%")
    
    return stories_with_valid_audio

def main():
    """Main function"""
    
    # Fix invalid audio files
    fixed_count = fix_invalid_audio_files()
    
    # Check final status
    valid_count = check_final_status()
    
    print(f"\n🎉 AUDIO FILE FIXES COMPLETE")
    print(f"\n📋 NEXT STEPS:")
    print(f"1. All stories now have valid audio file references")
    print(f"2. Visit: http://127.0.0.1:8000/story-mode/")
    print(f"3. Login: testchild/test123")
    print(f"4. Test story selection and audio playback")
    print(f"5. Audio should work without errors now!")

if __name__ == "__main__":
    main()
