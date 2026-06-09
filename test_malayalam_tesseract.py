#!/usr/bin/env python3
"""
Test Malayalam Tesseract OCR functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_models'))

def test_tesseract_malayalam():
    """Test Tesseract Malayalam detection"""
    try:
        from malayalam_tesseract_detector import predict_malayalam_handwriting, check_malayalam_language
        
        print("🔍 TESTING MALAYALAM TESSERACT OCR")
        print("=" * 50)
        
        # Check if Malayalam language pack is available
        print("1. Checking Malayalam language pack...")
        if check_malayalam_language():
            print("   ✅ Malayalam language pack is available")
        else:
            print("   ❌ Malayalam language pack is NOT available")
            print("   ⚠️ This will cause detection issues!")
            return False
        
        # Test detector initialization
        print("\n2. Testing detector initialization...")
        try:
            from malayalam_tesseract_detector import get_malayalam_detector
            detector = get_malayalam_detector()
            print(f"   ✅ Detector initialized successfully!")
            print(f"   📝 Language: {detector.language}")
            print(f"   ⚙️ Tesseract config: {detector.tesseract_config}")
        except Exception as e:
            print(f"   ❌ Detector initialization failed: {e}")
            return False
        
        # Test with a simple base64 image (if available)
        print("\n3. Testing prediction functionality...")
        try:
            # Create a simple test image
            import base64
            from PIL import Image, ImageDraw
            import io
            import numpy as np
            
            # Create a simple test image with text
            img = Image.new('RGB', (200, 100), color='white')
            draw = ImageDraw.Draw(img)
            draw.text((10, 10), "അ", fill='black')
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            # Test prediction
            result = predict_malayalam_handwriting(img_str, "അ")
            
            if result.get('success', False):
                print(f"   ✅ Prediction successful!")
                print(f"   📝 Predicted: '{result.get('predicted_text', '')}'")
                print(f"   🎯 Confidence: {result.get('confidence', 0):.2f}")
                print(f"   📊 Quality score: {result.get('quality_score', 0):.1f}")
                print(f"   🏆 Handwriting score: {result.get('handwriting_score', 0)}")
                return True
            else:
                print(f"   ❌ Prediction failed: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"   ❌ Prediction test failed: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_tesseract_malayalam()
    if success:
        print("\n🎉 MALAYALAM TESSERACT OCR IS WORKING!")
    else:
        print("\n❌ MALAYALAM TESSERACT OCR HAS ISSUES!")
        print("💡 Solutions:")
        print("   1. Install Tesseract OCR")
        print("   2. Download Malayalam language pack")
        print("   3. Add mal.traineddata to tessdata directory")
