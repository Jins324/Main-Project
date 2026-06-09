#!/usr/bin/env python
"""
Test the fixed story-mode page
"""
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

def test_fixed_story_mode():
    """Test the fixed story-mode page"""
    
    print("🔧 TESTING FIXED STORY-MODE PAGE...")
    print("=" * 60)
    
    User = get_user_model()
    client = Client()
    
    # Login
    try:
        user = User.objects.get(username='testchild')
        client.login(username='testchild', password='test123')
        print("✅ Logged in successfully")
    except:
        user = User.objects.create_user(username='testchild', password='test123', is_parent=False)
        client.login(username='testchild', password='test123')
        print("✅ Created and logged in test user")
    
    # Test 1: Story selection page
    print(f"\n1. Testing story selection page...")
    response = client.get('/story-mode/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Check for proper template rendering
        if 'Story Mode' in content:
            print(f"   ✅ Page title found")
        
        if 'english_stories' in content or 'malayalam_stories' in content:
            print(f"   ✅ Story variables present")
        else:
            print(f"   ❌ Story variables missing")
        
        # Check for story cards
        if 'story-card' in content:
            print(f"   ✅ Story cards present")
        else:
            print(f"   ❌ Story cards missing")
        
        # Check for JavaScript
        if 'selectStory' in content:
            print(f"   ✅ JavaScript functions present")
        else:
            print(f"   ❌ JavaScript functions missing")
            
    else:
        print(f"   ❌ Page failed: {response.status_code}")
    
    # Test 2: Individual story page
    print(f"\n2. Testing individual story page...")
    
    # Get a story with audio
    story_with_audio = Story.objects.filter(
        models.Q(audio_file__isnull=False) | models.Q(generated_audio__isnull=False)
    ).first()
    
    if story_with_audio:
        print(f"   Testing: {story_with_audio.title}")
        print(f"   Language: {story_with_audio.language}")
        
        response = client.get(f'/story-mode/?story={story_with_audio.id}&language={story_with_audio.language}')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check if story title is present
            if story_with_audio.title in content:
                print(f"   ✅ Story title found")
            else:
                print(f"   ❌ Story title NOT found")
            
            # Check if story content is present
            if story_with_audio.text_content[:100] in content:
                print(f"   ✅ Story content found")
            else:
                print(f"   ❌ Story content NOT found")
            
            # Check for audio element
            if 'id="storyAudio"' in content:
                print(f"   ✅ Audio element found")
                
                # Check audio URL
                audio_url = story_with_audio.audio_file.url if story_with_audio.audio_file else story_with_audio.generated_audio.url
                if audio_url in content:
                    print(f"   ✅ Audio URL found: {audio_url}")
                else:
                    print(f"   ❌ Audio URL NOT found")
            else:
                print(f"   ❌ Audio element NOT found")
            
            # Check for audio controls
            if 'stopAudio' in content and 'testAudio' in content:
                print(f"   ✅ Audio controls present")
            else:
                print(f"   ❌ Audio controls missing")
                
        else:
            print(f"   ❌ Story page failed: {response.status_code}")
    else:
        print(f"   ❌ No stories with audio found")
    
    # Test 3: Test audio playback functionality
    print(f"\n3. Testing audio functionality...")
    
    # Test English story
    english_story = Story.objects.filter(language='en').first()
    if english_story:
        print(f"   Testing English story: {english_story.title}")
        
        response = client.get(f'/story-mode/?story={english_story.id}&language=en')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            if 'generateAudio' in content:
                print(f"   ✅ Generate audio function present")
            else:
                print(f"   ❌ Generate audio function missing")
    
    # Test Malayalam story
    malayalam_story = Story.objects.filter(language='ml').first()
    if malayalam_story:
        print(f"   Testing Malayalam story: {malayalam_story.title}")
        
        response = client.get(f'/story-mode/?story={malayalam_story.id}&language=ml')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            if 'testAudio' in content:
                print(f"   ✅ Test audio function present")
            else:
                print(f"   ❌ Test audio function missing")
    
    print(f"\n" + "=" * 60)
    print(f"🔧 FIXED STORY-MODE TEST COMPLETE")
    print(f"\n📋 NEXT STEPS:")
    print(f"1. Visit: http://127.0.0.1:8000/story-mode/")
    print(f"2. Login: testchild/test123")
    print(f"3. Test story selection and audio playback")
    print(f"4. Check browser console for any JavaScript errors")

def main():
    """Main function"""
    test_fixed_story_mode()

if __name__ == "__main__":
    from django.db import models
    main()
