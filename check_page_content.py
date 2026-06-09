#!/usr/bin/env python
"""
Check actual story-mode page content
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

def check_page_content():
    """Check actual page content for issues"""
    
    print("🔍 CHECKING ACTUAL PAGE CONTENT...")
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
    
    # Get story-mode page
    response = client.get('/story-mode/')
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        print(f"📄 Page Content Analysis:")
        print(f"   Total length: {len(content)} characters")
        
        # Look for error indicators
        error_patterns = [
            'error',
            'Error',
            'ERROR',
            'exception',
            'Exception',
            'Traceback',
            '500',
            'Internal Server Error'
        ]
        
        found_errors = []
        for pattern in error_patterns:
            if pattern in content:
                found_errors.append(pattern)
                # Find context around error
                index = content.lower().find(pattern.lower())
                if index != -1:
                    start = max(0, index - 100)
                    end = min(len(content), index + 100)
                    context = content[start:end]
                    print(f"   ❌ Found '{pattern}' near: {context[:200]}...")
        
        if not found_errors:
            print(f"   ✅ No error indicators found")
        
        # Check for template variables not rendered
        if '{{' in content and '}}' in content:
            print(f"   ⚠️  Template variables not rendered")
            
            # Find unrendered template variables
            import re
            template_vars = re.findall(r'\{\{[^}]*\}\}', content)
            unique_vars = list(set(template_vars))
            print(f"   Unrendered variables: {unique_vars[:10]}")  # Show first 10
        
        # Check for story variables
        story_vars = ['story.audio_file', 'story.generated_audio', 'story.title', 'story.language']
        for var in story_vars:
            if var in content:
                print(f"   ✅ Found: {var}")
            else:
                print(f"   ❌ Missing: {var}")
        
        # Check for audio elements
        if 'id="storyAudio"' in content:
            print(f"   ✅ Audio element found")
            
            # Extract audio source
            import re
            audio_match = re.search(r'<audio[^>]*>.*?<source[^>]*src="([^"]*)"[^>]*>', content, re.DOTALL)
            if audio_match:
                audio_src = audio_match.group(1)
                print(f"   🎵 Audio source: {audio_src}")
            else:
                print(f"   ❌ Could not extract audio source")
        else:
            print(f"   ❌ No audio element found")
        
        # Check for JavaScript functions
        js_functions = ['generateAudio', 'testAudioPlayback', 'stopHtml5Audio']
        for func in js_functions:
            if f'function {func}' in content or f'{func}(' in content:
                print(f"   ✅ Found: {func}")
            else:
                print(f"   ❌ Missing: {func}")
        
        # Save content for inspection
        try:
            with open('debug_story_mode_content.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   💾 Content saved to: debug_story_mode_content.html")
        except Exception as e:
            print(f"   ❌ Could not save content: {e}")
        
    else:
        print(f"   ❌ Page failed: {response.status_code}")

def test_specific_story():
    """Test with specific story"""
    
    print(f"\n🎯 TESTING SPECIFIC STORY...")
    print("=" * 60)
    
    User = get_user_model()
    client = Client()
    user = User.objects.get(username='testchild')
    client.login(username='testchild', password='test123')
    
    # Get a story with audio
    story = Story.objects.filter(
        models.Q(audio_file__isnull=False) | models.Q(generated_audio__isnull=False)
    ).first()
    
    if story:
        print(f"Testing: {story.title}")
        print(f"Language: {story.language}")
        
        # Test with story parameter
        response = client.get(f'/story-mode/?story={story.id}&language={story.language}')
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check if story is in content
            if story.title in content:
                print(f"   ✅ Story title found in content")
            else:
                print(f"   ❌ Story title NOT found in content")
            
            # Check for audio element
            if 'id="storyAudio"' in content:
                print(f"   ✅ Audio element found")
                
                # Check if correct audio URL is there
                audio_url = story.audio_file.url if story.audio_file else story.generated_audio.url
                if audio_url in content:
                    print(f"   ✅ Audio URL found: {audio_url}")
                else:
                    print(f"   ❌ Audio URL NOT found")
            else:
                print(f"   ❌ Audio element NOT found")
            
            # Look for any errors
            if 'error' in content.lower():
                print(f"   ⚠️  Error indicators present")
            else:
                print(f"   ✅ No error indicators")
                
        else:
            print(f"   ❌ Failed: {response.status_code}")

def main():
    """Main function"""
    
    # Check page content
    check_page_content()
    
    # Test specific story
    test_specific_story()
    
    print(f"\n" + "=" * 60)
    print(f"🔍 CONTENT ANALYSIS COMPLETE")
    print(f"\n📋 FILES CREATED:")
    print(f"   debug_story_mode_content.html - Full page content for inspection")

if __name__ == "__main__":
    from django.db import models
    main()
