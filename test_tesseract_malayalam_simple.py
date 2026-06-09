#!/usr/bin/env python3
"""
Simple test of Tesseract Malayalam configuration
"""

import pytesseract
import cv2
import numpy as np
from PIL import Image, ImageDraw
import io
import base64

def test_tesseract_malayalam_simple():
    """Test Tesseract Malayalam with simple approach"""
    print("🔍 SIMPLE TESSERACT MALAYALAM TEST")
    print("=" * 40)
    
    # Check available languages
    try:
        languages = pytesseract.get_languages(config='')
        print(f"Available languages: {languages}")
        print(f"Malayalam available: {'mal' in languages}")
        print(f"English available: {'eng' in languages}")
    except Exception as e:
        print(f"Error checking languages: {e}")
        return
    
    # Create a simple test image with clear Malayalam character
    img = Image.new('RGB', (300, 150), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw large, clear Malayalam character
    draw.text((50, 30), "ക", fill='black')
    
    # Convert to OpenCV
    image_array = np.array(img)
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    
    # Save for debugging
    cv2.imwrite('test_malayalam.png', gray)
    print("Saved test image as 'test_malayalam.png'")
    
    # Test different configurations
    configs = [
        ('--psm 10', 'Single character'),
        ('--psm 6', 'Single uniform block'),
        ('--psm 7', 'Single text line'),
        ('--psm 8', 'Single word'),
        ('--psm 10 -c tessedit_char_whitelist=അആഇഈഉഊഋഎഏഐഒഓഔകഖഗഘങചഛജഝഞടഠഡഢണതഥദധനപഫബഭമയരറലളഴവശഷസഹ', 'With whitelist'),
        ('-l mal --psm 10', 'Explicit Malayalam'),
        ('-l eng --psm 10', 'English for comparison')
    ]
    
    print("\nTesting different configurations:")
    print("-" * 50)
    
    for config, description in configs:
        try:
            print(f"\n{description}:")
            print(f"  Config: {config}")
            
            # Test with Malayalam
            if 'mal' in config:
                text = pytesseract.image_to_string(gray, lang='mal', config=config)
            elif 'eng' in config:
                text = pytesseract.image_to_string(gray, lang='eng', config=config)
            else:
                text = pytesseract.image_to_string(gray, lang='mal', config=config)
            
            text = text.strip()
            print(f"  Result: '{text}'")
            
            # Get confidence
            try:
                data = pytesseract.image_to_data(gray, lang='mal' if 'mal' in config else 'eng', config=config, output_type=pytesseract.Output.DICT)
                confidences = [conf for conf in data['conf'] if conf > 0]
                if confidences:
                    avg_conf = sum(confidences) / len(confidences)
                    print(f"  Confidence: {avg_conf:.2f}")
                else:
                    print(f"  Confidence: N/A")
            except:
                print(f"  Confidence: N/A")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    # Test with different preprocessing
    print(f"\nTesting preprocessing methods:")
    print("-" * 50)
    
    # Method 1: Original grayscale
    print("1. Original grayscale:")
    text = pytesseract.image_to_string(gray, lang='mal', config='--psm 10')
    print(f"   Result: '{text.strip()}'")
    
    # Method 2: Threshold
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    print("2. Binary threshold:")
    text = pytesseract.image_to_string(thresh, lang='mal', config='--psm 10')
    print(f"   Result: '{text.strip()}'")
    
    # Method 3: Otsu
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print("3. Otsu threshold:")
    text = pytesseract.image_to_string(otsu, lang='mal', config='--psm 10')
    print(f"   Result: '{text.strip()}'")
    
    # Method 4: Inverted
    inverted = 255 - gray
    print("4. Inverted:")
    text = pytesseract.image_to_string(inverted, lang='mal', config='--psm 10')
    print(f"   Result: '{text.strip()}'")

if __name__ == "__main__":
    test_tesseract_malayalam_simple()
