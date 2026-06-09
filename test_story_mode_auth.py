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

print("🔍 Testing Story Mode with Authentication...")
print("=" * 60)

User = get_user_model()
client = Client()

# Create or get test user
try:
    user = User.objects.get(username='testchild')
    print(f"✅ Found test user: {user.username}")
except User.DoesNotExist:
    user = User.objects.create_user(username='testchild', password='test123', is_parent=False)
    print(f"✅ Created test user: {user.username}")

# Login the user
login_success = client.login(username='testchild', password='test123')
print(f"Login Success: {login_success}")

# Test 1: Check story-mode page with authentication
print("\n1. Testing Story Mode Page (Authenticated)...")
try:
    response = client.get('/story-mode/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Story mode page loads successfully")
        # Check if it uses the fixed template
        content = response.content.decode('utf-8')
        if 'story_mode_fixed.html' in content or 'language-sections' in content:
            print("   ✅ Using enhanced story mode template")
        else:
            print("   ⚠️  Using original template")
    else:
        print(f"   ❌ Story mode page failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error loading story mode: {e}")

# Test 2: Test with specific story
print("\n2. Testing Story Mode with Specific Story...")
malayalam_story = Story.objects.filter(language='ml').first()
if malayalam_story:
    print(f"   Testing Malayalam story: {malayalam_story.title}")
    try:
        response = client.get(f'/story-mode/?story={malayalam_story.id}&language=ml')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Malayalam story loads successfully")
        else:
            print(f"   ❌ Malayalam story failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error loading Malayalam story: {e}")

english_story = Story.objects.filter(language='en').first()
if english_story:
    print(f"   Testing English story: {english_story.title}")
    try:
        response = client.get(f'/story-mode/?story={english_story.id}&language=en')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ English story loads successfully")
        else:
            print(f"   ❌ English story failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error loading English story: {e}")

# Test 3: Test audio caching API again
print("\n3. Testing Audio Caching API (Fixed)...")
test_story = malayalam_story if malayalam_story else english_story

if test_story:
    print(f"   Testing with story: {test_story.title} (ID: {test_story.id})")
    
    try:
        response = client.post('/api/get-or-generate-audio/', {
            'story_id': test_story.id,
            'title': test_story.title,
            'text': test_story.text_content[:200],
            'language': test_story.language,
            'timeout': 15
        }, content_type='application/json')
        
        print(f"   API Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Audio caching API works")
            print(f"   Content-Type: {response.get('Content-Type')}")
            content_length = response.get('Content-Length')
            if content_length:
                print(f"   Content-Length: {content_length} bytes")
        else:
            print(f"   ❌ Audio caching API failed: {response.status_code}")
            try:
                data = response.json()
                print(f"   Error: {data.get('error')}")
            except:
                print(f"   Response: {response.content[:200]}")
    except Exception as e:
        print(f"   ❌ Audio caching API Error: {e}")

print("\n" + "=" * 60)
print("✅ Story Mode Analysis Complete")
