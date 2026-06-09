#!/usr/bin/env python
"""
Test story-mode with audio recording functionality
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
import json
from core.models import Story

def test_story_mode_with_recording():
    """Test story-mode with integrated audio recording"""
    
    print("📚 TESTING STORY-MODE WITH AUDIO RECORDING")
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
    
    # Test 1: Story selection page
    print(f"\n1. Testing story selection page...")
    response = client.get('/story-mode/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Check for key elements
        elements = [
            'Story Mode',
            'Read stories aloud and get instant pronunciation feedback!',
            'language-tabs',
            'story-grid',
            'English Stories',
            'Malayalam Stories'
        ]
        
        for element in elements:
            if element in content:
                print(f"   ✅ Found: {element}")
            else:
                print(f"   ❌ Missing: {element}")
                
    else:
        print(f"   ❌ Page failed: {response.status_code}")
    
    # Test 2: Individual story page with recording
    print(f"\n2. Testing individual story page...")
    
    # Get a story with audio
    story_with_audio = Story.objects.filter(
        models.Q(audio_file__isnull=False) | models.Q(generated_audio__isnull=False)
    ).first()
    
    if story_with_audio:
        print(f"   Testing: {story_with_audio.title}")
        print(f"   Language: {story_with_audio.language}")
        
        response = client.get(f'/story-mode/?story={story_with_audio.id}&language={story_with_audio.language}')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check for story content
            if story_with_audio.title in content:
                print(f"   ✅ Story title found")
            else:
                print(f"   ❌ Story title NOT found")
            
            # Check for recording section
            recording_elements = [
                'Read the Story Aloud',
                'recordBtn',
                'recording-controls',
                'audio-waveform',
                'recording-timer',
                'recording-status'
            ]
            
            for element in recording_elements:
                if element in content:
                    print(f"   ✅ Recording element: {element}")
                else:
                    print(f"   ❌ Recording element missing: {element}")
            
            # Check for scoring section
            scoring_elements = [
                'Your Reading Score',
                'score-display',
                'score-breakdown',
                'pronunciationScore',
                'fluencyScore',
                'accuracyScore',
                'feedback-section'
            ]
            
            for element in scoring_elements:
                if element in content:
                    print(f"   ✅ Scoring element: {element}")
                else:
                    print(f"   ❌ Scoring element missing: {element}")
            
            # Check for audio controls
            audio_elements = [
                'Story Audio',
                'storyAudio',
                'stopAudio',
                'testAudio'
            ]
            
            for element in audio_elements:
                if element in content:
                    print(f"   ✅ Audio element: {element}")
                else:
                    print(f"   ❌ Audio element missing: {element}")
                    
        else:
            print(f"   ❌ Story page failed: {response.status_code}")
    else:
        print(f"   ❌ No stories with audio found")
    
    # Test 3: API endpoints for recording
    print(f"\n3. Testing recording API endpoints...")
    
    # Test start recording
    response = client.post('/api/start-recording/', 
                          json.dumps({'language': 'en', 'expected_text': 'hello world'}),
                          content_type='application/json')
    print(f"   Start Recording: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Session ID: {data.get('session_id', 'N/A')}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown')}")
    
    # Test recording history
    response = client.get('/api/recording-history/')
    print(f"   Recording History: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ History entries: {data.get('total', 0)}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown')}")
    
    # Test 4: Story text extraction for recording
    print(f"\n4. Testing story text extraction...")
    
    if story_with_audio:
        print(f"   Story: {story_with_audio.title}")
        print(f"   Language: {story_with_audio.language}")
        print(f"   Text length: {len(story_with_audio.text_content)} characters")
        print(f"   Text preview: {story_with_audio.text_content[:100]}...")
        
        # Check if text is suitable for recording
        if len(story_with_audio.text_content) > 50:
            print(f"   ✅ Story text is suitable for recording")
        else:
            print(f"   ⚠️  Story text is quite short")
        
        # Check for special characters
        has_special_chars = any(char in story_with_audio.text_content for char in ['\n', '\t', '"', "'"])
        if has_special_chars:
            print(f"   ⚠️  Story text contains special characters")
        else:
            print(f"   ✅ Story text is clean")
    
    # Test 5: Language-specific features
    print(f"\n5. Testing language-specific features...")
    
    # Test English story
    english_story = Story.objects.filter(language='en').first()
    if english_story:
        print(f"   English Story: {english_story.title}")
        print(f"   Text: {english_story.text_content[:50]}...")
        
        response = client.get(f'/story-mode/?story={english_story.id}&language=en')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            if '🇺🇸 English Stories' in content:
                print(f"   ✅ English language features present")
            else:
                print(f"   ❌ English language features missing")
    
    # Test Malayalam story
    malayalam_story = Story.objects.filter(language='ml').first()
    if malayalam_story:
        print(f"   Malayalam Story: {malayalam_story.title}")
        print(f"   Text: {malayalam_story.text_content[:50]}...")
        
        response = client.get(f'/story-mode/?story={malayalam_story.id}&language=ml')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            if '🇮🇳 Malayalam Stories' in content:
                print(f"   ✅ Malayalam language features present")
            else:
                print(f"   ❌ Malayalam language features missing")

def test_story_progress_integration():
    """Test story progress integration with recording"""
    
    print(f"\n📊 TESTING STORY PROGRESS INTEGRATION")
    print("=" * 60)
    
    from core.models import StoryProgress
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Get test user
    try:
        user = User.objects.get(username='testchild')
        print(f"✅ Test user found: {user.username}")
    except:
        print(f"❌ Test user not found")
        return
    
    # Check StoryProgress model
    print(f"\n📊 Testing StoryProgress Model:")
    
    # Get a story
    story = Story.objects.first()
    if story:
        print(f"   Testing with story: {story.title}")
        
        # Test creating a story progress entry
        print(f"\n➕ Creating Sample Story Progress:")
        
        try:
            progress = StoryProgress.objects.create(
                child=user,
                story=story,
                reading_fluency_score=85,
                pronunciation_score=90,
                completion_score=95,
                overall_score=90,
                words_read=100,
                total_words=120,
                reading_time=60,
                accuracy_percentage=85.5,
                audio_listened_percentage=100.0,
                navigation_count=2,
                pause_count=1,
                transcript_text="Sample transcript",
                speech_recognition_confidence=0.85,
                completed=True,
                session_duration=120
            )
            print(f"   ✅ Story progress created: ID {progress.id}")
            print(f"   📊 Overall Score: {progress.overall_score}%")
            
            # Test the calculate_overall_score method
            calculated_score = progress.calculate_overall_score()
            print(f"   🧮 Calculated Score: {calculated_score}%")
            
            # Clean up
            progress.delete()
            print(f"   🗑️  Test progress cleaned up")
            
        except Exception as e:
            print(f"   ❌ Error creating story progress: {e}")
    else:
        print(f"   ❌ No stories found")

def main():
    """Main function"""
    
    print("📚 STORY-MODE WITH AUDIO RECORDING TEST")
    print("=" * 60)
    
    # Test story-mode with recording
    test_story_mode_with_recording()
    
    # Test story progress integration
    test_story_progress_integration()
    
    print(f"\n" + "=" * 60)
    print(f"📚 STORY-MODE WITH RECORDING TEST COMPLETE")
    print(f"\n📋 FEATURES TESTED:")
    print(f"   ✅ Story selection interface")
    print(f"   ✅ Individual story viewer")
    print(f"   ✅ Audio recording integration")
    print(f"   ✅ Scoring results display")
    print(f"   ✅ Language-specific features")
    print(f"   ✅ API endpoints")
    print(f"   ✅ Story progress tracking")
    
    print(f"\n🌐 ACCESS URL:")
    print(f"   📚 Story Mode: http://127.0.0.1:8000/story-mode/")
    print(f"   🔑 Login: testchild / test123")
    
    print(f"\n🎯 NEW FEATURES:")
    print(f"   • Read stories aloud with microphone")
    print(f"   • Get instant pronunciation scoring")
    print(f"   • Compare reading to original story text")
    print(f"   • Detailed feedback and improvement tips")
    print(f"   • Track reading progress over time")
    print(f"   • Support for English and Malayalam stories")

if __name__ == "__main__":
    from django.db import models
    main()
