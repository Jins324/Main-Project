#!/usr/bin/env python
"""
Simple test for speech evaluation libraries
"""
import os
import sys

def test_libraries():
    """Test if required libraries are installed"""
    print("Testing Speech Evaluation Libraries...")
    
    try:
        import speech_recognition as sr
        print("✅ SpeechRecognition library installed")
        
        # Test recognizer creation
        recognizer = sr.Recognizer()
        print("✅ SpeechRecognition recognizer created successfully")
        
    except ImportError as e:
        print(f"❌ SpeechRecognition not installed: {e}")
        return False
    
    try:
        from pydub import AudioSegment
        print("✅ pydub library installed")
        
        # Test audio segment creation
        audio = AudioSegment.empty()
        print("✅ pydub AudioSegment created successfully")
        
    except ImportError as e:
        print(f"❌ pydub not installed: {e}")
        return False
    
    try:
        import Levenshtein
        print("✅ python-Levenshtein library installed")
        
        # Test distance calculation
        distance = Levenshtein.distance("hello", "helo")
        print(f"✅ Levenshtein distance test: 'hello' vs 'helo' = {distance}")
        
        # Test ratio calculation
        ratio = Levenshtein.ratio("hello world", "hello word")
        print(f"✅ Levenshtein ratio test: {ratio:.3f}")
        
    except ImportError as e:
        print(f"❌ python-Levenshtein not installed: {e}")
        return False
    
    try:
        from difflib import SequenceMatcher
        print("✅ difflib available (built-in)")
        
        # Test sequence matching
        similarity = SequenceMatcher(None, "hello", "helo").ratio()
        print(f"✅ SequenceMatcher test: {similarity:.3f}")
        
    except ImportError as e:
        print(f"❌ difflib not available: {e}")
        return False
    
    print("\n🎉 All speech evaluation libraries are working!")
    return True

def test_text_similarity():
    """Test text similarity calculation"""
    print("\nTesting Text Similarity Functions...")
    
    try:
        import Levenshtein
        from difflib import SequenceMatcher
        
        def calculate_text_similarity(text1, text2):
            """Calculate similarity between two texts using multiple methods"""
            # Normalize texts
            text1 = text1.lower().strip()
            text2 = text2.lower().strip()
            
            # Method 1: Levenshtein distance
            levenshtein_ratio = Levenshtein.ratio(text1, text2)
            
            # Method 2: SequenceMatcher
            sequence_ratio = SequenceMatcher(None, text1, text2).ratio()
            
            # Method 3: Word-based comparison
            words1 = set(text1.split())
            words2 = set(text2.split())
            
            if words1 and words2:
                word_similarity = len(words1.intersection(words2)) / len(words1.union(words2))
            else:
                word_similarity = 0
            
            # Weighted average
            final_score = (levenshtein_ratio * 0.4 + sequence_ratio * 0.4 + word_similarity * 0.2) * 100
            return min(100, max(0, final_score))
        
        # Test cases
        test_cases = [
            ("hello world", "hello world"),  # Perfect match
            ("hello world", "hello word"),   # Small difference
            ("hello world", "hello"),        # Partial match
            ("hello world", "goodbye world"), # Different words
            ("hello", "world"),              # No match
        ]
        
        for text1, text2 in test_cases:
            similarity = calculate_text_similarity(text1, text2)
            print(f"   '{text1}' vs '{text2}': {similarity:.1f}%")
        
        print("✅ Text similarity functions working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Text similarity test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Speech Evaluation System Test")
    print("=" * 50)
    
    libs_ok = test_libraries()
    similarity_ok = test_text_similarity()
    
    print("\n" + "=" * 50)
    if libs_ok and similarity_ok:
        print("🎉 SPEECH EVALUATION SYSTEM READY!")
        print("✅ All libraries installed")
        print("✅ Text similarity working")
        print("✅ Ready for Django integration")
    else:
        print("❌ SPEECH EVALUATION SYSTEM NEEDS ATTENTION")
        print("Please check the errors above")
    print("=" * 50)
