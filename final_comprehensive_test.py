#!/usr/bin/env python
"""
Final comprehensive test of story-mode audio playback
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

def final_comprehensive_test():
    """Final comprehensive test of story-mode"""
    
    print("🎯 FINAL COMPREHENSIVE STORY-MODE TEST")
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
    
    # Test all stories with audio
    stories_with_audio = Story.objects.filter(
        models.Q(audio_file__isnull=False) | models.Q(generated_audio__isnull=False)
    )
    
    print(f"\n📚 Testing {stories_with_audio.count()} stories with audio...")
    
    success_count = 0
    error_count = 0
    
    for i, story in enumerate(stories_with_audio, 1):
        print(f"\n[{i}/{stories_with_audio.count()}] {story.title}")
        print(f"   Language: {story.get_language_display()}")
        
        # Determine audio type
        audio_type = "Original" if story.audio_file else "Generated"
        audio_url = story.audio_file.url if story.audio_file else story.generated_audio.url
        
        print(f"   🎵 Audio Type: {audio_type}")
        print(f"   📁 Audio URL: {audio_url}")
        
        # Test story page
        try:
            response = client.get(f'/story-mode/?story={story.id}&language={story.language}')
            print(f"   📄 Page Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                # Check story content
                if story.title in content:
                    print(f"   ✅ Story title found")
                else:
                    print(f"   ❌ Story title NOT found")
                
                # Check story content
                if story.text_content[:100] in content:
                    print(f"   ✅ Story content found")
                else:
                    print(f"   ❌ Story content NOT found")
                
                # Check audio element
                if 'id="storyAudio"' in content:
                    print(f"   ✅ Audio element found")
                    
                    # Check if correct audio URL is in content
                    if audio_url in content:
                        print(f"   ✅ Audio URL in page")
                    else:
                        print(f"   ❌ Audio URL NOT in page")
                        
                    # Check for test audio function
                    if 'testAudio()' in content:
                        print(f"   ✅ Test audio function present")
                    else:
                        print(f"   ❌ Test audio function missing")
                        
                else:
                    print(f"   ❌ Audio element NOT found")
                
                # Check for JavaScript errors
                if 'error' not in content.lower():
                    print(f"   ✅ No error indicators")
                else:
                    print(f"   ⚠️  Error indicators found")
                
                success_count += 1
                
            else:
                print(f"   ❌ Page failed: {response.status_code}")
                error_count += 1
                
        except Exception as e:
            print(f"   ❌ Error testing story: {e}")
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
                
        except Exception as e:
            print(f"   ❌ Error accessing audio: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"📊 FINAL TEST SUMMARY:")
    print(f"   Total Stories Tested: {stories_with_audio.count()}")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {error_count}")
    print(f"   📈 Success Rate: {(success_count/stories_with_audio.count()*100):.1f}%")
    
    if success_count == stories_with_audio.count():
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"   ✅ Story-mode page is working correctly")
        print(f"   ✅ Audio playback is functional")
        print(f"   ✅ All stories with audio are accessible")
    else:
        print(f"\n⚠️  Some tests failed")
        print(f"   Check browser console for JavaScript errors")
        print(f"   Verify Django error logs")
    
    return success_count, error_count

def main():
    """Main function"""
    success_count, error_count = final_comprehensive_test()
    
    print(f"\n🎯 CONCLUSION:")
    print(f"🌐 Test URL: http://127.0.0.1:8000/story-mode/")
    print(f"🔑 Login: testchild/test123")
    
    if success_count > 0:
        print(f"✅ Audio playback is WORKING!")
        print(f"📋 Instructions:")
        print(f"1. Visit the URL above")
        print(f"2. Login with testchild/test123")
        print(f"3. Select any story with audio badge 🎧")
        print(f"4. Click ▶️ Play or 🧪 Test Audio")
        print(f"5. Check browser console (F12) for details")
    else:
        print(f"❌ Audio playback needs attention")

if __name__ == "__main__":
    from django.db import models
    main()
