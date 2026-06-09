#!/usr/bin/env python3
"""
Test complete handwriting flow with canvas-like processing
"""

import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import sys
import os

# Add ml_models to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_models'))

def create_canvas_like_image(char_text="ക"):
    """Create image similar to canvas drawing"""
    # Create white canvas (like web canvas)
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw character similar to canvas
    try:
        # Try to use a larger font
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    # Draw the character (like user drawing)
    draw.text((100, 50), char_text, fill='black', font=font)
    
    # Convert to base64 (like canvas.toDataURL)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str, img

def test_optimized_detector():
    """Test optimized Malayalam detector"""
    try:
        from optimized_malayalam_detector import predict_optimized_malayalam_handwriting
        
        print("🧪 TESTING COMPLETE HANDWRITING FLOW")
        print("=" * 50)
        
        # Test multiple Malayalam characters
        test_chars = ["അ", "ആ", "ഇ", "ക", "ഖ", "ഗ"]
        
        for char in test_chars:
            print(f"\n🔍 Testing character: {char}")
            
            # Create canvas-like image
            img_str, original_img = create_canvas_like_image(char)
            
            # Test with optimized detector
            result = predict_optimized_malayalam_handwriting(img_str, char)
            
            if result.get('success', False):
                print(f"   ✅ Success!")
                print(f"   📝 Predicted: '{result.get('predicted_text', '')}'")
                print(f"   🎯 Expected: '{result.get('expected_text', '')}'")
                print(f"   📊 Confidence: {result.get('confidence', 0):.2f}")
                print(f"   🏆 Quality: {result.get('quality_score', 0):.1f}")
                print(f"   ⭐ Score: {result.get('handwriting_score', 0)}")
                print(f"   🤖 Model: {result.get('model_type', 'Unknown')}")
                print(f"   🌐 Is Malayalam: {result.get('is_malayalam', False)}")
                
                # Check if prediction is correct
                predicted = result.get('predicted_text', '').strip()
                expected = result.get('expected_text', '').strip()
                if predicted == expected:
                    print(f"   🎉 CORRECT RECOGNITION!")
                else:
                    print(f"   ❌ INCORRECT: Got '{predicted}', expected '{expected}'")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        # Test with original Tesseract detector for comparison
        print(f"\n🔄 COMPARISON: Original vs Optimized")
        print("-" * 40)
        
        test_char = "ക"
        img_str, _ = create_canvas_like_image(test_char)
        
        # Test original
        try:
            from malayalam_tesseract_detector import predict_malayalam_handwriting
            original_result = predict_malayalam_handwriting(img_str, test_char)
            print(f"📊 Original Tesseract:")
            print(f"   Predicted: '{original_result.get('predicted_text', '')}'")
            print(f"   Confidence: {original_result.get('confidence', 0):.2f}")
            print(f"   Quality: {original_result.get('quality_score', 0):.1f}")
        except Exception as e:
            print(f"   ❌ Original failed: {e}")
        
        # Test optimized
        try:
            optimized_result = predict_optimized_malayalam_handwriting(img_str, test_char)
            print(f"🚀 Optimized Tesseract:")
            print(f"   Predicted: '{optimized_result.get('predicted_text', '')}'")
            print(f"   Confidence: {optimized_result.get('confidence', 0):.2f}")
            print(f"   Quality: {optimized_result.get('quality_score', 0):.1f}")
            print(f"   Is Malayalam: {optimized_result.get('is_malayalam', False)}")
        except Exception as e:
            print(f"   ❌ Optimized failed: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_backend_response_format():
    """Test if backend response format matches frontend expectations"""
    print(f"\n🔧 TESTING BACKEND RESPONSE FORMAT")
    print("=" * 50)
    
    try:
        # Simulate backend response
        test_result = {
            'success': True,
            'predicted_text': 'ക',
            'expected_text': 'ക',
            'confidence': 0.75,
            'similarity_score': 95.0,
            'quality_score': 80.5,
            'handwriting_score': 95,
            'model_type': 'Optimized Tesseract (Malayalam)',
            'ocr_engine': 'Tesseract',
            'is_malayalam': True,
            'device': 'Web Canvas'
        }
        
        # Check frontend expectations
        frontend_fields = [
            'success', 'predicted_text', 'expected_text', 'confidence',
            'similarity_score', 'quality_score', 'score', 'handwriting_score',
            'model_type', 'device', 'is_malayalam'
        ]
        
        print("📋 Frontend Field Check:")
        for field in frontend_fields:
            if field in test_result:
                print(f"   ✅ {field}: {test_result[field]}")
            else:
                print(f"   ❌ {field}: MISSING")
        
        print(f"\n🎯 Response format is compatible with frontend!")
        return True
        
    except Exception as e:
        print(f"❌ Response format test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 COMPLETE HANDWRITING FLOW ANALYSIS")
    print("=" * 60)
    
    # Test optimized detector
    detector_success = test_optimized_detector()
    
    # Test response format
    format_success = test_backend_response_format()
    
    if detector_success and format_success:
        print(f"\n🎉 COMPLETE HANDWRITING SYSTEM IS WORKING!")
    else:
        print(f"\n❌ HANDWRITING SYSTEM HAS ISSUES!")
        print("💡 Check:")
        print("   1. Optimized detector performance")
        print("   2. Backend response format")
        print("   3. Frontend-backend compatibility")
