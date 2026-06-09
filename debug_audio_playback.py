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

print("🔍 DEBUGGING AUDIO PLAYBACK ISSUES...")
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

# Test 1: Check if story-mode page loads with actual content
print("\n1. Testing Story Mode Page Content...")
response = client.get('/story-mode/')
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    content = response.content.decode('utf-8')
    
    # Check for critical JavaScript functions
    js_functions = [
        'generateAudio',
        'generateCachedAudio', 
        'testAudioPlayback',
        'stopAllAudioGlobal',
        'updateTTSStatus'
    ]
    
    print("   JavaScript Functions Check:")
    for func in js_functions:
        found = func in content
        status = "✅" if found else "❌"
        print(f"   {status} {func}()")
    
    # Check for audio elements
    audio_elements = [
        'id="storyAudio"',
        'id="playTtsBtn"',
        'id="ttsStatusInline"',
        'id="ttsControls"'
    ]
    
    print("   Audio Elements Check:")
    for element in audio_elements:
        found = element in content
        status = "✅" if found else "❌"
        print(f"   {status} {element}")

# Test 2: Test with specific Malayalam story
print("\n2. Testing Malayalam Story Audio...")
malayalam_story = Story.objects.filter(language='ml').first()
if malayalam_story:
    print(f"   Story: {malayalam_story.title}")
    print(f"   Audio file: {malayalam_story.audio_file.name if malayalam_story.audio_file else 'None'}")
    
    # Get the story page
    response = client.get(f'/story-mode/?story={malayalam_story.id}&language=ml')
    print(f"   Page Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Check if audio element is properly formed
        if 'id="storyAudio"' in content:
            print("   ✅ Audio element found")
            
            # Extract the audio source
            import re
            audio_match = re.search(r'<audio[^>]*>.*?<source[^>]*src="([^"]*)"[^>]*>', content, re.DOTALL)
            if audio_match:
                audio_src = audio_match.group(1)
                print(f"   🎵 Audio source: {audio_src}")
                
                # Test if audio URL is accessible
                if audio_src.startswith('/media/'):
                    audio_response = client.get(audio_src)
                    print(f"   📡 Audio URL Status: {audio_response.status_code}")
                    if audio_response.status_code == 200:
                        print(f"   📊 Audio Size: {len(audio_response.content)} bytes")
                    else:
                        print(f"   ❌ Audio URL not accessible")
            else:
                print("   ❌ Could not extract audio source")
        else:
            print("   ❌ No audio element found")

# Test 3: Test with specific English story
print("\n3. Testing English Story Audio...")
english_story = Story.objects.filter(language='en').first()
if english_story:
    print(f"   Story: {english_story.title}")
    print(f"   Audio file: {english_story.audio_file.name if english_story.audio_file else 'None'}")
    
    # Get the story page
    response = client.get(f'/story-mode/?story={english_story.id}&language=en')
    print(f"   Page Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Check if TTS controls are present
        if 'id="ttsControls"' in content:
            print("   ✅ TTS controls found")
            
            # Check if play button is present
            if 'id="playTtsBtn"' in content:
                print("   ✅ Play button found")
                
                # Check if generateAudio function is called
                if 'onclick="generateAudio()"' in content:
                    print("   ✅ Generate audio function linked")
                else:
                    print("   ❌ Generate audio function not linked")
            else:
                print("   ❌ Play button not found")
        else:
            print("   ❌ No TTS controls found")

# Test 4: Test audio API directly
print("\n4. Testing Audio API Directly...")

# Test Malayalam audio API
if malayalam_story:
    try:
        response = client.post('/api/get-or-generate-audio/', {
            'story_id': malayalam_story.id,
            'title': malayalam_story.title,
            'text': malayalam_story.text_content[:100],
            'language': 'ml',
            'timeout': 10
        }, content_type='application/json')
        
        print(f"   Malayalam API Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   🎵 Malayalam Audio Size: {len(response.content)} bytes")
            print(f"   📄 Content-Type: {response.get('Content-Type')}")
        else:
            print(f"   ❌ Malayalam API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Malayalam API Error: {e}")

# Test English audio API
if english_story:
    try:
        response = client.post('/api/get-or-generate-audio/', {
            'story_id': english_story.id,
            'title': english_story.title,
            'text': english_story.text_content[:100],
            'language': 'en',
            'timeout': 10
        }, content_type='application/json')
        
        print(f"   English API Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   🎵 English Audio Size: {len(response.content)} bytes")
            print(f"   📄 Content-Type: {response.get('Content-Type')}")
        else:
            print(f"   ❌ English API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ English API Error: {e}")

# Test 5: Check for common JavaScript issues
print("\n5. Checking for Common Issues...")

# Check if template variables are properly set
response = client.get(f'/story-mode/?story={malayalam_story.id if malayalam_story else 1}&language=ml')
if response.status_code == 200:
    content = response.content.decode('utf-8')
    
    # Check for template variable issues
    issues = [
        ('{{ story.id|default:"" }}', 'Story ID template variable'),
        ('{{ story.title|default:"" }}', 'Story title template variable'),
        ('currentLanguage = \'{{ story.language|default:"en" }}\'', 'Current language variable'),
        ('storyText = document.querySelector(\'.story-text\').textContent', 'Story text selector')
    ]
    
    print("   Template Variable Check:")
    for pattern, description in issues:
        found = pattern in content
        status = "✅" if found else "❌"
        print(f"   {status} {description}")

print("\n" + "=" * 60)
print("🔍 DEBUGGING COMPLETE")
print("\n📋 NEXT STEPS:")
print("1. Open browser and go to: http://127.0.0.1:8000/story-mode/")
print("2. Login with: username=testchild, password=test123")
print("3. Open browser console (F12) to check for JavaScript errors")
print("4. Try clicking audio buttons and watch console output")
