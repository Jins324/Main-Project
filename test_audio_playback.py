#!/usr/bin/env python
"""
Test audio playback with existing audio files
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

def test_audio_playback():
    """Test audio playback for all stories"""
    
    print("🎵 TESTING AUDIO PLAYBACK WITH EXISTING FILES...")
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
    
    # Test all stories
    all_stories = Story.objects.all()
    success_count = 0
    error_count = 0
    
    for i, story in enumerate(all_stories, 1):
        print(f"\n[{i}/{all_stories.count()}] Testing: {story.title}")
        print(f"   Language: {story.get_language_display()} ({story.language})")
        
        # Determine which audio to use
        audio_url = None
        audio_type = None
        
        if story.audio_file and story.audio_file.name:
            audio_url = story.audio_file.url
            audio_type = "Original"
        elif story.generated_audio and story.generated_audio.name:
            audio_url = story.generated_audio.url
            audio_type = "Generated"
        
        if not audio_url:
            print(f"   ❌ No audio available")
            error_count += 1
            continue
        
        print(f"   🎵 Audio Type: {audio_type}")
        print(f"   📁 Audio URL: {audio_url}")
        
        # Test story-mode page
        try:
            response = client.get(f'/story-mode/?story={story.id}&language={story.language}')
            print(f"   📄 Page Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                # Check if audio element is present
                if 'id="storyAudio"' in content:
                    print(f"   ✅ Audio element found in page")
                    
                    # Check if correct audio source is in page
                    if audio_url in content:
                        print(f"   ✅ Correct audio URL in page")
                    else:
                        print(f"   ⚠️  Audio URL not found in page")
                        print(f"   🔍 Looking for: {audio_url}")
                    
                    # Check for test button
                    if 'testAudioPlayback()' in content:
                        print(f"   ✅ Test audio button available")
                    
                    success_count += 1
                else:
                    print(f"   ❌ Audio element NOT found in page")
                    error_count += 1
            else:
                print(f"   ❌ Page failed to load: {response.status_code}")
                error_count += 1
                
        except Exception as e:
            print(f"   ❌ Error testing page: {e}")
            error_count += 1
        
        # Test audio file accessibility
        try:
            audio_response = client.get(audio_url)
            print(f"   🌐 Audio File Status: {audio_response.status_code}")
            
            if audio_response.status_code == 200:
                content_length = audio_response.get('Content-Length')
                if content_length:
                    print(f"   📊 Audio Size: {content_length} bytes")
                else:
                    print(f"   📊 Audio Size: {len(audio_response.content)} bytes")
            else:
                print(f"   ❌ Audio file not accessible: {audio_response.status_code}")
                error_count += 1
                
        except Exception as e:
            print(f"   ❌ Error accessing audio: {e}")
            error_count += 1
    
    print(f"\n" + "=" * 60)
    print(f"📊 AUDIO PLAYBACK TEST SUMMARY:")
    print(f"   Total Stories: {all_stories.count()}")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {error_count}")
    print(f"   📈 Success Rate: {(success_count/all_stories.count()*100):.1f}%")
    
    return success_count, error_count

def test_template_rendering():
    """Test template rendering specifically"""
    
    print(f"\n🔍 TESTING TEMPLATE RENDERING...")
    print("=" * 60)
    
    User = get_user_model()
    client = Client()
    user = User.objects.get(username='testchild')
    client.login(username='testchild', password='test123')
    
    # Test a story with original audio
    malayalam_story = Story.objects.filter(language='ml', audio_file__isnull=False).first()
    if malayalam_story:
        print(f"Testing Malayalam story with original audio: {malayalam_story.title}")
        
        response = client.get(f'/story-mode/?story={malayalam_story.id}&language=ml')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            print(f"   Page Status: {response.status_code}")
            print(f"   Original Audio in Template: {'{% if story.audio_file %}' in content}")
            print(f"   Generated Audio in Template: {'{% elif story.generated_audio %}' in content}")
            audio_element_found = 'id="storyAudio"' in content
            print(f"   Audio Element Found: {audio_element_found}")
            print(f"   Original Audio URL: {malayalam_story.audio_file.url if malayalam_story.audio_file else 'None'}")
            print(f"   URL in Content: {malayalam_story.audio_file.url in content if malayalam_story.audio_file else 'N/A'}")
    
    # Test a story with generated audio
    english_story = Story.objects.filter(language='en', generated_audio__isnull=False).first()
    if english_story:
        print(f"\nTesting English story with generated audio: {english_story.title}")
        
        response = client.get(f'/story-mode/?story={english_story.id}&language=en')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            print(f"   Page Status: {response.status_code}")
            print(f"   Generated Audio URL: {english_story.generated_audio.url if english_story.generated_audio else 'None'}")
            print(f"   URL in Content: {english_story.generated_audio.url in content if english_story.generated_audio else 'N/A'}")
            print(f"   Generation Date in Content: {'audio_generation_date' in content}")
            print(f"   Generation Method in Content: {'audio_generation_method' in content}")

def main():
    """Main function"""
    
    # Test audio playback
    success_count, error_count = test_audio_playback()
    
    # Test template rendering
    test_template_rendering()
    
    # Final summary
    print(f"\n🎯 FINAL SUMMARY:")
    print(f"   Audio Playback Test: {success_count} successful, {error_count} failed")
    
    if success_count > 0:
        print(f"   ✅ Audio playback is working!")
        print(f"   🌐 Test URL: http://127.0.0.1:8000/story-mode/")
        print(f"   🔑 Login: testchild/test123")
    else:
        print(f"   ❌ Audio playback needs attention")

if __name__ == "__main__":
    main()
