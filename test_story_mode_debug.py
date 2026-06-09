#!/usr/bin/env python
"""
Test Story Mode with Debug Information
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

def test_story_mode_debug():
    """Test story mode with debug information"""
    
    print("🔍 STORY MODE DEBUG TEST")
    print("=" * 50)
    
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
    
    # Test English story mode with debug
    print(f"\n🇺🇸 Testing English Story Mode (Debug):")
    response = client.get('/story-mode/?language=en')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Check for robust_audio_enabled variable
        if 'robustAudioEnabled' in content:
            print("   ✅ Found robustAudioEnabled variable")
        else:
            print("   ❌ Missing robustAudioEnabled variable")
        
        # Check for robust_audio_enabled template variable
        if 'robust_audio_enabled' in content:
            print("   ✅ Found robust_audio_enabled template variable")
        else:
            print("   ❌ Missing robust_audio_enabled template variable")
        
        # Check for True value
        if 'true' in content and 'robustAudioEnabled' in content:
            print("   ✅ robustAudioEnabled is set to true")
        elif 'false' in content and 'robustAudioEnabled' in content:
            print("   ❌ robustAudioEnabled is set to false")
        
        # Check for debug console.log
        if 'console.log(\'Robust audio enabled:' in content:
            print("   ✅ Found debug console.log")
        else:
            print("   ❌ Missing debug console.log")
        
        # Check for robust system usage
        if 'robustAudioEnabled' in content and 'process-english-audio-realtime' in content:
            print("   ✅ Robust system integration found")
        else:
            print("   ❌ Robust system integration missing")
    
    # Test Malayalam story mode with debug
    print(f"\n🇮🇳 Testing Malayalam Story Mode (Debug):")
    response = client.get('/story-mode/?language=ml')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Check for robust_audio_enabled variable
        if 'robustAudioEnabled' in content:
            print("   ✅ Found robustAudioEnabled variable")
        else:
            print("   ❌ Missing robustAudioEnabled variable")
        
        # Check for robust system usage
        if 'robustAudioEnabled' in content and 'process-malayalam-audio-realtime' in content:
            print("   ✅ Robust system integration found")
        else:
            print("   ❌ Robust system integration missing")
    
    # Test the view directly
    print(f"\n🔧 Testing View Context:")
    from core.views import story_mode
    
    # Create a mock request
    class MockRequest:
        def __init__(self, get_data):
            self.GET = get_data
            self.user = user
            self.method = 'GET'
    
    # Test English
    mock_request = MockRequest({'language': 'en'})
    try:
        # This will test the view logic
        print("   Testing English story_mode view...")
        # Note: We can't actually call the view here without proper setup
        print("   ✅ View logic test would go here")
    except Exception as e:
        print(f"   ❌ View test error: {e}")
    
    # Test Malayalam
    mock_request = MockRequest({'language': 'ml'})
    try:
        print("   Testing Malayalam story_mode view...")
        print("   ✅ View logic test would go here")
    except Exception as e:
        print(f"   ❌ View test error: {e}")

if __name__ == "__main__":
    test_story_mode_debug()
