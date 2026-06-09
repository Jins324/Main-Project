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
from django.template import Template, Context

print("🔧 CREATING SIMPLE AUDIO TEST...")
print("=" * 60)

User = get_user_model()
client = Client()
user = User.objects.get(username='testchild')
client.login(username='testchild', password='test123')

# Get stories
malayalam_story = Story.objects.filter(language='ml').first()
english_story = Story.objects.filter(language='en').first()

print(f"Malayalam Story: {malayalam_story.title}")
print(f"English Story: {english_story.title}")

# Create a simple HTML page for testing
test_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Audio Test Page</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .story-section {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .story-title {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .story-content {{
            font-size: 16px;
            line-height: 1.6;
            margin: 15px 0;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 5px;
        }}
        .audio-controls {{
            margin: 15px 0;
            padding: 15px;
            background: #e8f5e8;
            border-radius: 5px;
            text-align: center;
        }}
        .status {{
            margin: 10px 0;
            padding: 10px;
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            text-align: center;
        }}
        button {{
            margin: 5px;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }}
        .btn-primary {{ background: #007bff; color: white; }}
        .btn-success {{ background: #28a745; color: white; }}
        .btn-danger {{ background: #dc3545; color: white; }}
        .btn-warning {{ background: #ffc107; color: black; }}
    </style>
</head>
<body>
    <h1>🎵 Audio Playback Test</h1>
    
    <div class="story-section">
        <div class="story-title">🇮🇳 {malayalam_story.title}</div>
        <div class="story-content">{malayalam_story.text_content[:200]}...</div>
        
        <div class="audio-controls">
            <div class="status" id="malayalamStatus">Testing Malayalam audio...</div>
            
            <!-- Malayalam Audio Element -->
            <audio id="malayalamAudio" controls preload="auto">
                <source src="{malayalam_story.audio_file.url}" type="audio/mpeg">
                <source src="{malayalam_story.audio_file.url}" type="audio/wav">
                <source src="{malayalam_story.audio_file.url}" type="audio/ogg">
                Your browser does not support the audio element.
            </audio>
            
            <div style="margin-top: 10px;">
                <button class="btn-success" onclick="playMalayalam()">▶️ Play</button>
                <button class="btn-danger" onclick="stopMalayalam()">⏹️ Stop</button>
                <button class="btn-warning" onclick="testMalayalam()">🧪 Test</button>
            </div>
        </div>
    </div>
    
    <div class="story-section">
        <div class="story-title">🇺🇸 {english_story.title}</div>
        <div class="story-content">{english_story.text_content[:200]}...</div>
        
        <div class="audio-controls">
            <div class="status" id="englishStatus">Testing English audio...</div>
            
            <!-- English TTS Controls (no pre-recorded audio) -->
            <div id="englishTtsControls">
                <button class="btn-success" onclick="generateEnglishAudio()">🎤 Generate Audio</button>
                <div id="englishAudioContainer"></div>
            </div>
        </div>
    </div>
    
    <script>
        // Malayalam Audio Functions
        function playMalayalam() {{
            const audio = document.getElementById('malayalamAudio');
            const status = document.getElementById('malayalamStatus');
            
            try {{
                audio.play();
                status.textContent = '🎵 Playing Malayalam audio...';
                status.style.background = '#d4edda';
                status.style.borderColor = '#c3e6cb';
            }} catch (error) {{
                status.textContent = '❌ Error playing Malayalam: ' + error.message;
                status.style.background = '#f8d7da';
                status.style.borderColor = '#f5c6cb';
            }}
        }}
        
        function stopMalayalam() {{
            const audio = document.getElementById('malayalamAudio');
            const status = document.getElementById('malayalamStatus');
            
            audio.pause();
            audio.currentTime = 0;
            status.textContent = '⏹️ Malayalam audio stopped';
            status.style.background = '#fff3cd';
            status.style.borderColor = '#ffeaa7';
        }}
        
        function testMalayalam() {{
            const audio = document.getElementById('malayalamAudio');
            const status = document.getElementById('malayalamStatus');
            
            status.textContent = '🧪 Testing Malayalam audio...';
            
            // Test audio properties
            console.log('Malayalam Audio Test:');
            console.log('src:', audio.src);
            console.log('readyState:', audio.readyState);
            console.log('networkState:', audio.networkState);
            console.log('duration:', audio.duration);
            console.log('paused:', audio.paused);
            console.log('ended:', audio.ended);
            
            // Try to play
            audio.play().then(() => {{
                status.textContent = '✅ Malayalam audio test successful!';
                status.style.background = '#d4edda';
                status.style.borderColor = '#c3e6cb';
            }}).catch(error => {{
                status.textContent = '❌ Malayalam audio test failed: ' + error.message;
                status.style.background = '#f8d7da';
                status.style.borderColor = '#f5c6cb';
            }});
        }}
        
        // English Audio Functions
        function generateEnglishAudio() {{
            const status = document.getElementById('englishStatus');
            const container = document.getElementById('englishAudioContainer');
            
            status.textContent = '🎤 Generating English audio...';
            
            // Fetch English TTS
            fetch('/api/get-or-generate-audio/', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }},
                body: JSON.stringify({{
                    story_id: {english_story.id},
                    title: '{english_story.title}',
                    text: '{english_story.text_content[:200]}',
                    language: 'en',
                    timeout: 15
                }})
            }})
            .then(response => {{
                if (response.ok) {{
                    return response.blob();
                }} else {{
                    throw new Error('Audio generation failed');
                }}
            }})
            .then(blob => {{
                const audioUrl = URL.createObjectURL(blob);
                const audio = new Audio(audioUrl);
                
                // Create audio element
                container.innerHTML = `
                    <audio id="englishAudio" controls>
                        <source src="${{audioUrl}}" type="audio/mpeg">
                    </audio>
                `;
                
                // Auto play
                setTimeout(() => {{
                    const englishAudio = document.getElementById('englishAudio');
                    englishAudio.play();
                    status.textContent = '🎵 Playing English audio...';
                    status.style.background = '#d4edda';
                    status.style.borderColor = '#c3e6cb';
                }}, 1000);
                
            }})
            .catch(error => {{
                status.textContent = '❌ English audio failed: ' + error.message;
                status.style.background = '#f8d7da';
                status.style.borderColor = '#f5c6cb';
            }});
        }}
        
        // Helper function to get CSRF token
        function getCookie(name) {{
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {{
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {{
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {{
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }}
                }}
            }}
            return cookieValue;
        }}
        
        // Initialize page
        window.onload = function() {{
            console.log('Audio Test Page Loaded');
            
            // Test Malayalam audio element
            const malayalamAudio = document.getElementById('malayalamAudio');
            malayalamAudio.addEventListener('play', () => {{
                document.getElementById('malayalamStatus').textContent = '🎵 Playing Malayalam audio...';
            }});
            
            malayalamAudio.addEventListener('pause', () => {{
                document.getElementById('malayalamStatus').textContent = '⏸️ Malayalam audio paused';
            }});
            
            malayalamAudio.addEventListener('ended', () => {{
                document.getElementById('malayalamStatus').textContent = '✅ Malayalam audio completed';
            }});
            
            malayalamAudio.addEventListener('error', (e) => {{
                document.getElementById('malayalamStatus').textContent = '❌ Malayalam audio error: ' + e.message;
            }});
        }};
    </script>
</body>
</html>
"""

# Write the test HTML file
test_file_path = 'static/audio_test.html'
try:
    os.makedirs('static', exist_ok=True)
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(test_html)
    print(f"✅ Test HTML file created: {test_file_path}")
except Exception as e:
    print(f"❌ Error creating test file: {e}")

# Create a simple view to serve this file
from django.http import HttpResponse
from django.conf import settings
import os

def audio_test_view(request):
    """Simple view to serve audio test page"""
    try:
        with open(test_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse("Test file not found", status=404)

# Add the view to URLs temporarily
from django.urls import path
from core import views

# Test the view
try:
    from django.test import RequestFactory
    factory = RequestFactory()
    request = factory.get('/audio-test/')
    request.user = user
    
    response = audio_test_view(request)
    print(f"Audio Test View Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Audio test view working")
        print(f"📄 Content length: {len(response.content)} characters")
        print("🌐 Test URL: http://127.0.0.1:8000/audio-test/")
        print("🔧 Use this page to test audio playback directly")
    else:
        print(f"❌ Audio test view failed: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error testing view: {e}")

print("\n" + "=" * 60)
print("🔧 AUDIO TEST PAGE CREATED")
print("\n📋 INSTRUCTIONS:")
print("1. Add this to urls.py:")
print("   path('audio-test/', views.audio_test_view, name='audio_test'),")
print("2. Visit: http://127.0.0.1:8000/audio-test/")
print("3. Test both Malayalam and English audio")
print("4. Check browser console for detailed logs")
