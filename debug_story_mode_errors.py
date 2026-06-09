#!/usr/bin/env python
"""
Debug story-mode page errors
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

def debug_story_mode_errors():
    """Debug story-mode page errors"""
    
    print("🔍 DEBUGGING STORY-MODE PAGE ERRORS...")
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
    
    # Test 1: Check story-mode page without parameters
    print(f"\n1. Testing story-mode page (no parameters)...")
    try:
        response = client.get('/story-mode/')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            print(f"   ✅ Page loaded successfully")
            print(f"   📄 Content length: {len(content)} characters")
            
            # Check for common errors
            if 'error' in content.lower():
                print(f"   ⚠️  Error indicators found in content")
            
            # Check for template rendering issues
            if '{%' in content and '%}' in content:
                print(f"   ⚠️  Template tags not rendered")
            
            # Check for story list
            if 'english_stories' in content or 'malayalam_stories' in content:
                print(f"   ✅ Story variables present")
            else:
                print(f"   ❌ Story variables missing")
                
        elif response.status_code == 500:
            print(f"   ❌ Server error (500)")
            
        elif response.status_code == 302:
            print(f"   ⚠️  Redirect (302) - authentication required")
            
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error accessing page: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Check story-mode page with story parameter
    print(f"\n2. Testing story-mode page (with story)...")
    
    # Get a story with audio
    story_with_audio = Story.objects.filter(
        models.Q(audio_file__isnull=False) | models.Q(generated_audio__isnull=False)
    ).first()
    
    if story_with_audio:
        print(f"   Testing with: {story_with_audio.title}")
        print(f"   Language: {story_with_audio.language}")
        
        # Determine audio type
        audio_type = "Original" if story_with_audio.audio_file else "Generated"
        audio_url = story_with_audio.audio_file.url if story_with_audio.audio_file else story_with_audio.generated_audio.url
        print(f"   Audio Type: {audio_type}")
        print(f"   Audio URL: {audio_url}")
        
        try:
            response = client.get(f'/story-mode/?story={story_with_audio.id}&language={story_with_audio.language}')
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                print(f"   ✅ Story page loaded")
                
                # Check for audio element
                if 'id="storyAudio"' in content:
                    print(f"   ✅ Audio element found")
                    
                    # Check if audio URL is in content
                    if audio_url in content:
                        print(f"   ✅ Audio URL in page")
                    else:
                        print(f"   ❌ Audio URL NOT in page")
                        
                    # Check for audio source
                    if '<source src=' in content:
                        print(f"   ✅ Audio source tags found")
                    else:
                        print(f"   ❌ Audio source tags missing")
                        
                else:
                    print(f"   ❌ Audio element NOT found")
                
                # Check for JavaScript errors
                if 'generateAudio' in content:
                    print(f"   ✅ generateAudio function present")
                else:
                    print(f"   ❌ generateAudio function missing")
                
                if 'testAudioPlayback' in content:
                    print(f"   ✅ testAudioPlayback function present")
                else:
                    print(f"   ❌ testAudioPlayback function missing")
                    
            elif response.status_code == 500:
                print(f"   ❌ Server error (500)")
                # Try to get error details
                try:
                    content = response.content.decode('utf-8')
                    if 'error' in content.lower():
                        print(f"   📄 Error content: {content[:500]}")
                except:
                    pass
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error accessing story page: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"   ❌ No stories with audio found")
    
    # Test 3: Check view function directly
    print(f"\n3. Testing view function directly...")
    
    try:
        from core.views import story_mode
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/story-mode/')
        request.user = user
        
        response = story_mode(request)
        print(f"   View Response Status: {response.status_code}")
        
        # Check if it's a TemplateResponse
        from django.template.response import TemplateResponse
        if isinstance(response, TemplateResponse):
            print(f"   ✅ TemplateResponse returned")
            
            # Check context
            context = response.context_data
            print(f"   Context keys: {list(context.keys())}")
            
            if 'english_stories' in context:
                print(f"   ✅ english_stories in context: {context['english_stories'].count()}")
            else:
                print(f"   ❌ english_stories missing from context")
                
            if 'malayalam_stories' in context:
                print(f"   ✅ malayalam_stories in context: {context['malayalam_stories'].count()}")
            else:
                print(f"   ❌ malayalam_stories missing from context")
                
        else:
            print(f"   ❌ Not a TemplateResponse: {type(response)}")
            
    except Exception as e:
        print(f"   ❌ Error testing view: {e}")
        import traceback
        traceback.print_exc()

def check_template_syntax():
    """Check template syntax"""
    
    print(f"\n4. Checking template syntax...")
    
    try:
        from django.template import Template, Context
        from core.models import Story
        
        # Load template
        template_path = 'core/templates/core/story_mode_fixed.html'
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            print(f"   📄 Template loaded: {len(template_content)} characters")
            
            # Try to compile template
            try:
                template = Template(template_content)
                print(f"   ✅ Template syntax is valid")
                
                # Try to render with sample data
                sample_story = Story.objects.first()
                if sample_story:
                    context = Context({
                        'story': sample_story,
                        'english_stories': Story.objects.filter(language='en'),
                        'malayalam_stories': Story.objects.filter(language='ml'),
                    })
                    
                    rendered = template.render(context)
                    print(f"   ✅ Template renders successfully")
                    print(f"   📄 Rendered length: {len(rendered)} characters")
                    
                else:
                    print(f"   ⚠️  No stories to test with")
                    
            except Exception as e:
                print(f"   ❌ Template compilation error: {e}")
                
        else:
            print(f"   ❌ Template file not found: {template_path}")
            
    except Exception as e:
        print(f"   ❌ Error checking template: {e}")

def main():
    """Main function"""
    
    # Debug story-mode errors
    debug_story_mode_errors()
    
    # Check template syntax
    check_template_syntax()
    
    print(f"\n" + "=" * 60)
    print(f"🔍 DEBUGGING COMPLETE")
    print(f"\n📋 NEXT STEPS:")
    print(f"1. Check browser console for JavaScript errors")
    print(f"2. Verify Django error logs")
    print(f"3. Test with specific story IDs")

if __name__ == "__main__":
    from django.db import models
    main()
