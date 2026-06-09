#!/usr/bin/env python
"""
Debug template rendering issues
"""
import os
import sys
import django

# Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kids_learning_tool.settings')
django.setup()

from django.template import Template, Context
from core.models import Story

def debug_template_rendering():
    """Debug template rendering issues"""
    
    print("🔍 DEBUGGING TEMPLATE RENDERING...")
    print("=" * 60)
    
    # Test 1: Check if template compiles
    print(f"\n1. Testing template compilation...")
    
    template_path = 'core/templates/core/story_mode_simple.html'
    if os.path.exists(template_path):
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            print(f"   📄 Template loaded: {len(template_content)} characters")
            
            # Try to compile template
            template = Template(template_content)
            print(f"   ✅ Template compiles successfully")
            
        except Exception as e:
            print(f"   ❌ Template compilation error: {e}")
            return
    else:
        print(f"   ❌ Template file not found: {template_path}")
        return
    
    # Test 2: Test template rendering with sample data
    print(f"\n2. Testing template rendering...")
    
    try:
        # Get sample data
        english_stories = Story.objects.filter(language='en')
        malayalam_stories = Story.objects.filter(language='ml')
        selected_story = Story.objects.first()
        
        context = {
            'english_stories': english_stories,
            'malayalam_stories': malayalam_stories,
            'story': selected_story,
            'total_stories': english_stories.count() + malayalam_stories.count(),
            'selected_story_id': selected_story.id if selected_story else None,
            'selected_language': 'en',
            'available_languages': Story.LANGUAGE_CHOICES
        }
        
        print(f"   Context data:")
        print(f"     english_stories: {english_stories.count()} items")
        print(f"     malayalam_stories: {malayalam_stories.count()} items")
        print(f"     story: {selected_story.title if selected_story else 'None'}")
        print(f"     total_stories: {context['total_stories']}")
        
        # Render template
        rendered = template.render(Context(context))
        print(f"   ✅ Template renders successfully")
        print(f"   📄 Rendered length: {len(rendered)} characters")
        
        # Check for template variables
        if selected_story:
            if selected_story.title in rendered:
                print(f"   ✅ Story title found in rendered content")
            else:
                print(f"   ❌ Story title NOT found in rendered content")
            
            if 'english_stories' in rendered:
                print(f"   ✅ english_stories variable found")
            else:
                print(f"   ❌ english_stories variable NOT found")
        
        # Save rendered content for inspection
        try:
            with open('debug_rendered_template.html', 'w', encoding='utf-8') as f:
                f.write(rendered)
            print(f"   💾 Rendered content saved to: debug_rendered_template.html")
        except Exception as e:
            print(f"   ❌ Could not save rendered content: {e}")
            
    except Exception as e:
        print(f"   ❌ Template rendering error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Check view function
    print(f"\n3. Testing view function...")
    
    try:
        from django.test.client import Client
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        client = Client()
        
        # Login
        try:
            user = User.objects.get(username='testchild')
            client.login(username='testchild', password='test123')
        except:
            user = User.objects.create_user(username='testchild', password='test123', is_parent=False)
            client.login(username='testchild', password='test123')
        
        # Test view with story parameter
        if selected_story:
            response = client.get(f'/story-mode/?story={selected_story.id}&language=en')
            print(f"   View Response Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                # Check if story title is in content
                if selected_story.title in content:
                    print(f"   ✅ Story title found in view response")
                else:
                    print(f"   ❌ Story title NOT found in view response")
                
                # Check for template variables
                if 'english_stories' in content:
                    print(f"   ✅ english_stories found in view response")
                else:
                    print(f"   ❌ english_stories NOT found in view response")
                    
            else:
                print(f"   ❌ View failed: {response.status_code}")
        
    except Exception as e:
        print(f"   ❌ View test error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function"""
    debug_template_rendering()
    
    print(f"\n" + "=" * 60)
    print(f"🔍 TEMPLATE DEBUGGING COMPLETE")
    print(f"\n📋 FILES CREATED:")
    print(f"   debug_rendered_template.html - Rendered template for inspection")

if __name__ == "__main__":
    main()
