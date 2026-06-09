#!/usr/bin/env python
"""
Test script for speech evaluation functionality
"""
import os
import sys
import base64
import tempfile
import wave
import numpy as np
from io import BytesIO

# Add core to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

def create_test_audio():
    """Create a simple test audio file (silent WAV with basic structure)"""
    # Create a simple WAV file with silence
    sample_rate = 16000
    duration = 2  # 2 seconds
    frequency = 440  # A4 note
    
    # Generate sine wave
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.sin(frequency * 2 * np.pi * t) * 0.3  # 30% volume
    
    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Create WAV file in memory
    with BytesIO() as wav_buffer:
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        wav_buffer.seek(0)
        wav_bytes = wav_buffer.read()
    
    # Convert to base64
    wav_base64 = base64.b64encode(wav_bytes).decode()
    return f"data:audio/wav;base64,{wav_base64}"

def test_speech_evaluation():
    """Test the speech evaluation functions"""
    try:
        from core.views import process_audio_blob, calculate_text_similarity, transcribe_audio
        
        print("Testing Speech Evaluation Pipeline...")
        
        # Test 1: Text similarity
        print("\n1. Testing text similarity...")
        text1 = "hello world"
        text2 = "hello word"
        similarity = calculate_text_similarity(text1, text2)
        print(f"   Similarity between '{text1}' and '{text2}': {similarity:.2f}%")
        
        # Test 2: Audio processing
        print("\n2. Testing audio processing...")
        test_audio = create_test_audio()
        expected_text = "hello"
        
        result = process_audio_blob(test_audio, expected_text)
        print(f"   Audio processing result: {result['success']}")
        if result['success']:
            print(f"   Transcription: '{result['transcription']}'")
            print(f"   Similarity score: {result['similarity_score']:.2f}%")
            print(f"   Method used: {result['method']}")
        else:
            print(f"   Error: {result['error']}")
        
        # Test 3: Direct transcription
        print("\n3. Testing direct transcription...")
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_path = temp_file.name
        
        # Write test audio to temporary file
        wav_data = base64.b64decode(test_audio.split('base64,')[1])
        with open(temp_path, 'wb') as f:
            f.write(wav_data)
        
        try:
            transcription_result = transcribe_audio(temp_path, expected_text)
            print(f"   Transcription success: {transcription_result['success']}")
            if transcription_result['success']:
                print(f"   Transcribed text: '{transcription_result['transcription']}'")
                print(f"   Method: {transcription_result['method']}")
            else:
                print(f"   Transcription error: {transcription_result['error']}")
        finally:
            # Clean up
            try:
                os.unlink(temp_path)
            except:
                pass
        
        print("\n✅ Speech evaluation pipeline test completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install SpeechRecognition pydub python-Levenshtein")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_speech_evaluation()
    if success:
        print("\n🎉 Speech evaluation system is ready!")
    else:
        print("\n❌ Speech evaluation system needs attention!")
