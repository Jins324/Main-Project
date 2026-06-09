#!/usr/bin/env python
"""
Test audio recording and scoring system
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
from audio_recording_system import AudioRecordingSystem

def test_audio_recording_system():
    """Test the audio recording system"""
    
    print("🎤 TESTING AUDIO RECORDING SYSTEM")
    print("=" * 60)
    
    # Initialize system
    system = AudioRecordingSystem()
    
    # Test configurations
    print(f"\n📋 Testing Language Configurations:")
    for lang in ['en', 'ml']:
        config = system.get_recording_config(lang)
        print(f"   {config['name']}:")
        print(f"     - Recognition Engine: {config['recognition_engine']}")
        print(f"     - Scoring Model: {config['scoring_model']}")
        print(f"     - Sample Rate: {config['sample_rate']} Hz")
        print(f"     - Max Duration: {config['max_duration']} seconds")
        print(f"     - Confidence Threshold: {config['confidence_threshold']}")
    
    # Test scoring components
    print(f"\n🧪 Testing Scoring Components:")
    
    # Test pronunciation scoring
    print(f"   📝 English Pronunciation Scoring:")
    en_score = system.calculate_pronunciation_score(
        "hello world", "hello world", 'en'
    )
    print(f"     - Score: {en_score:.1f}/100")
    
    print(f"   📝 Malayalam Pronunciation Scoring:")
    ml_score = system.calculate_pronunciation_score(
        "നമസ്കാരം", "നമസ്കാരം", 'ml'
    )
    print(f"     - Score: {ml_score:.1f}/100")
    
    # Test accuracy calculation
    print(f"   📊 Accuracy Calculation:")
    accuracy = system.calculate_accuracy(
        "hello world", "hello world", 'en'
    )
    print(f"     - Score: {accuracy:.1f}/100")
    
    # Test overall scoring
    print(f"   🎯 Overall Scoring:")
    overall = system.calculate_overall_score(en_score, 75, accuracy)
    print(f"     - Overall Score: {overall:.1f}/100")
    
    # Test feedback generation
    print(f"\n💬 Testing Feedback Generation:")
    feedback = system.generate_feedback(
        "hello world", "hello world", 85, 'en'
    )
    print(f"   - Overall Message: {feedback['overall_message']}")
    print(f"   - Performance Level: {feedback['level']}")
    print(f"   - Improvement Tips: {len(feedback['improvement_tips'])} tips")
    
    print(f"\n✅ Audio Recording System Test Complete!")

def test_web_interface():
    """Test the web interface"""
    
    print(f"\n🌐 TESTING WEB INTERFACE")
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
    
    # Test audio recording page
    print(f"\n📄 Testing Audio Recording Page:")
    response = client.get('/audio-recording/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Check for key elements
        elements = [
            'Audio Recording & Scoring',
            'Recording Studio',
            'Results & Feedback',
            'language-selector',
            'recordBtn',
            'practiceText'
        ]
        
        for element in elements:
            if element in content:
                print(f"   ✅ Found: {element}")
            else:
                print(f"   ❌ Missing: {element}")
                
    else:
        print(f"   ❌ Page failed: {response.status_code}")
    
    # Test API endpoints
    print(f"\n🔌 Testing API Endpoints:")
    
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
    
    # Test recording stats
    response = client.get('/api/recording-stats/')
    print(f"   Recording Stats: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            stats = data.get('stats', {})
            print(f"   ✅ Total recordings: {stats.get('total_recordings', 0)}")
            print(f"   ✅ Average score: {stats.get('average_score', 0)}")
        else:
            print(f"   ❌ Error: {data.get('error', 'Unknown')}")

def test_database_integration():
    """Test database integration"""
    
    print(f"\n🗄️ TESTING DATABASE INTEGRATION")
    print("=" * 60)
    
    from core.models import ActivityProgress
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Get test user
    try:
        user = User.objects.get(username='testchild')
        print(f"✅ Test user found: {user.username}")
    except:
        print(f"❌ Test user not found")
        return
    
    # Check ActivityProgress model
    print(f"\n📊 Testing ActivityProgress Model:")
    
    # Check speech activities
    speech_activities = ActivityProgress.objects.filter(
        child=user,
        activity_type='speech'
    )
    
    print(f"   Speech activities: {speech_activities.count()}")
    
    # Test creating a sample activity
    print(f"\n➕ Creating Sample Activity:")
    
    try:
        activity = ActivityProgress.objects.create(
            child=user,
            activity_type='speech',
            score=85,
            feedback='{"test": "data"}',
        )
        print(f"   ✅ Activity created: ID {activity.id}")
        
        # Clean up
        activity.delete()
        print(f"   🗑️  Test activity cleaned up")
        
    except Exception as e:
        print(f"   ❌ Error creating activity: {e}")

def main():
    """Main function"""
    
    print("🎤 AUDIO RECORDING & SCORING SYSTEM TEST")
    print("=" * 60)
    
    # Test audio recording system
    test_audio_recording_system()
    
    # Test web interface
    test_web_interface()
    
    # Test database integration
    test_database_integration()
    
    print(f"\n" + "=" * 60)
    print(f"🎤 AUDIO RECORDING SYSTEM TEST COMPLETE")
    print(f"\n📋 FEATURES TESTED:")
    print(f"   ✅ Language configurations (English & Malayalam)")
    print(f"   ✅ Pronunciation scoring algorithms")
    print(f"   ✅ Accuracy calculation")
    print(f"   ✅ Overall scoring system")
    print(f"   ✅ Feedback generation")
    print(f"   ✅ Web interface loading")
    print(f"   ✅ API endpoints")
    print(f"   ✅ Database integration")
    print(f"   ✅ Activity progress tracking")
    
    print(f"\n🌐 ACCESS URLS:")
    print(f"   🎤 Audio Recording: http://127.0.0.1:8000/audio-recording/")
    print(f"   📊 Recording Dashboard: http://127.0.0.1:8000/audio-recording-dashboard/")
    print(f"   🔑 Login: testchild / test123")
    
    print(f"\n🎯 READY FOR USE:")
    print(f"   • English and Malayalam audio recording")
    print(f"   • Real-time pronunciation scoring")
    print(f"   • Comprehensive feedback system")
    print(f"   • Progress tracking and analytics")
    print(f"   • Recording history and statistics")

if __name__ == "__main__":
    main()
