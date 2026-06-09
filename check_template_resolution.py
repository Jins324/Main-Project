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

print("🔍 CHECKING TEMPLATE RESOLUTION...")
print("=" * 60)

User = get_user_model()
client = Client()
user = User.objects.get(username='testchild')
client.login(username='testchild', password='test123')

# Test 1: Check which template is actually being used
print("\n1. Checking Template Resolution...")

malayalam_story = Story.objects.filter(language='ml').first()
response = client.get(f'/story-mode/?story={malayalam_story.id}&language=ml')

if response.status_code == 200:
    content = response.content.decode('utf-8')
    
    # Check for unique identifiers from each template
    fixed_template_markers = [
        'language-sections',
        '🇺🇸 English Stories',
        '🇮🇳 Malayalam Stories',
        'generateCachedAudio',
        'forceGenerateAudio'
    ]
    
    original_template_markers = [
        'story-container',
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'generateBackendTTS'
    ]
    
    print("   Checking for Fixed Template Markers:")
    for marker in fixed_template_markers:
        found = marker in content
        status = "✅" if found else "❌"
        print(f"   {status} {marker}")
    
    print("   Checking for Original Template Markers:")
    for marker in original_template_markers:
        found = marker in content
        status = "✅" if found else "❌"
        print(f"   {status} {marker}")
    
    # Determine which template is being used
    fixed_count = sum(1 for marker in fixed_template_markers if marker in content)
    original_count = sum(1 for marker in original_template_markers if marker in content)
    
    print(f"\n   Template Analysis:")
    print(f"   Fixed Template Markers: {fixed_count}/{len(fixed_template_markers)}")
    print(f"   Original Template Markers: {original_count}/{len(original_template_markers)}")
    
    if fixed_count > original_count:
        print("   🎯 Using: story_mode_fixed.html")
    elif original_count > fixed_count:
        print("   🎯 Using: story_mode.html (ORIGINAL)")
    else:
        print("   ❓ Template unclear")

# Test 2: Check if the fixed template file exists
print("\n2. Checking Template Files...")

import os
fixed_template_path = 'core/templates/core/story_mode_fixed.html'
original_template_path = 'core/templates/core/story_mode.html'

if os.path.exists(fixed_template_path):
    print(f"   ✅ Fixed template exists: {fixed_template_path}")
    with open(fixed_template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"   📄 Fixed template size: {len(content)} characters")
        if 'id="storyAudio"' in content:
            print("   ✅ Fixed template has storyAudio element")
        else:
            print("   ❌ Fixed template missing storyAudio element")
else:
    print(f"   ❌ Fixed template missing: {fixed_template_path}")

if os.path.exists(original_template_path):
    print(f"   ✅ Original template exists: {original_template_path}")
    with open(original_template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"   📄 Original template size: {len(content)} characters")
        if 'id="storyAudio"' in content:
            print("   ✅ Original template has storyAudio element")
        else:
            print("   ❌ Original template missing storyAudio element")
else:
    print(f"   ❌ Original template missing: {original_template_path}")

# Test 3: Check the view configuration
print("\n3. Checking View Configuration...")

try:
    from core.views import story_mode
    import inspect
    
    # Get the source code of the view
    source = inspect.getsource(story_mode)
    
    if 'story_mode_fixed.html' in source:
        print("   ✅ View configured to use story_mode_fixed.html")
    elif 'story_mode.html' in source:
        print("   ❌ View configured to use story_mode.html (ORIGINAL)")
    else:
        print("   ❓ View template unclear")
        
    # Look for the render call
    if "return render(request, 'core/story_mode_fixed.html'" in source:
        print("   ✅ Found render call for fixed template")
    elif "return render(request, 'core/story_mode.html'" in source:
        print("   ❌ Found render call for original template")
    else:
        print("   ❓ Render call unclear")
        
except Exception as e:
    print(f"   ❌ Error checking view: {e}")

print("\n" + "=" * 60)
print("🔍 TEMPLATE RESOLUTION ANALYSIS COMPLETE")
