#!/usr/bin/env python
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

print("🔍 DEBUGGING TEMPLATE CONTEXT...")
print("=" * 60)

User = get_user_model()
client = Client()
user = User.objects.get(username='testchild')
client.login(username='testchild', password='test123')

# Test with Malayalam story
malayalam_story = Story.objects.filter(language='ml').first()
print(f"\nTesting with: {malayalam_story.title}")
print(f"Story ID: {malayalam_story.id}")
print(f"Has audio: {bool(malayalam_story.audio_file)}")

# Create a debug view to see the context
from core.views import story_mode
from django.test import RequestFactory

factory = RequestFactory()
request = factory.get(f'/story-mode/?story={malayalam_story.id}&language=ml')
request.user = user

# Call the view and capture the response
try:
    response = story_mode(request)
    print(f"View Response Status: {response.status_code}")
    
    # Check if it's a TemplateResponse
    from django.template.response import TemplateResponse
    if isinstance(response, TemplateResponse):
        print("✅ TemplateResponse detected")
        
        # Get the context
        context = response.context_data
        print(f"Context keys: {list(context.keys())}")
        
        if 'story' in context:
            story = context['story']
            print(f"Story in context: {story}")
            print(f"Story title: {story.title if story else 'None'}")
            print(f"Story audio_file: {story.audio_file if story else 'None'}")
            print(f"Story audio_file type: {type(story.audio_file) if story else 'None'}")
            
            if story and story.audio_file:
                print(f"Audio file name: {story.audio_file.name}")
                print(f"Audio file URL: {story.audio_file.url}")
                print(f"Audio file exists: {story.audio_file.storage.exists(story.audio_file.name)}")
        else:
            print("❌ No 'story' key in context")
    else:
        print("❌ Not a TemplateResponse")
        print(f"Response type: {type(response)}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test the template rendering directly
print("\n" + "=" * 60)
print("🔍 TESTING TEMPLATE RENDERING...")

try:
    from django.template import Template, Context
    from core.models import Story
    
    # Create a simple template to test the conditional
    template_content = """
    {% if story %}
        Story: {{ story.title }}
        {% if story.audio_file %}
            HAS AUDIO: {{ story.audio_file.name }}
            <audio id="storyAudio" controls>
                <source src="{{ story.audio_file.url }}">
            </audio>
        {% else %}
            NO AUDIO - TTS Controls
        {% endif %}
    {% else %}
        NO STORY
    {% endif %}
    """
    
    template = Template(template_content)
    context = Context({
        'story': malayalam_story
    })
    
    rendered = template.render(context)
    print("Template Rendered:")
    print(rendered)
    
    # Check if audio element is in the rendered output
    if 'id="storyAudio"' in rendered:
        print("✅ Audio element in rendered template")
    else:
        print("❌ Audio element NOT in rendered template")
        
    if 'HAS AUDIO' in rendered:
        print("✅ Audio condition triggered")
    else:
        print("❌ Audio condition NOT triggered")
        
    if 'NO AUDIO' in rendered:
        print("✅ No audio condition triggered")
    else:
        print("❌ No audio condition NOT triggered")
        
except Exception as e:
    print(f"❌ Template rendering error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("🔍 TEMPLATE CONTEXT ANALYSIS COMPLETE")
