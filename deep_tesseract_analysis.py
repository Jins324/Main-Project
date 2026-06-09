#!/usr/bin/env python3
"""
Deep Analysis of Tesseract Malayalam Performance Issues
"""

import os
import sys
import cv2
import numpy as np
import base64
from PIL import Image, ImageDraw, ImageFont
import io

# Add ml_models to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ml_models'))

def analyze_tesseract_malayalam_issues():
    """Deep analysis of Tesseract Malayalam performance problems"""
    
    print("🔍 DEEP ANALYSIS: TESSERACT MALAYALAM PERFORMANCE")
    print("=" * 60)
    
    # 1. Check Tesseract installation and paths
    print("\n1. TESSERACT INSTALLATION ANALYSIS:")
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"   ✅ Tesseract version: {version}")
        print(f"   📁 Tesseract command: {pytesseract.pytesseract.tesseract_cmd}")
        
        # Check tessdata directory
        tessdata_dir = os.path.join(os.path.dirname(pytesseract.pytesseract.tesseract_cmd), 'tessdata')
        if os.path.exists(tessdata_dir):
            print(f"   📁 Tessdata directory: {tessdata_dir}")
            mal_data = os.path.join(tessdata_dir, 'mal.traineddata')
            if os.path.exists(mal_data):
                print(f"   ✅ mal.traineddata found: {mal_data}")
                size = os.path.getsize(mal_data)
                print(f"   📊 mal.traineddata size: {size:,} bytes")
            else:
                print(f"   ❌ mal.traineddata NOT found: {mal_data}")
        else:
            print(f"   ❌ Tessdata directory not found: {tessdata_dir}")
            
    except Exception as e:
        print(f"   ❌ Tesseract check failed: {e}")
    
    # 2. Check available languages
    print("\n2. LANGUAGE PACK ANALYSIS:")
    try:
        languages = pytesseract.get_languages(config='')
        print(f"   📝 Available languages: {len(languages)}")
        print(f"   🌐 Languages: {languages}")
        
        if 'mal' in languages:
            print("   ✅ Malayalam (mal) is available")
        else:
            print("   ❌ Malayalam (mal) is NOT available")
            
        if 'eng' in languages:
            print("   ✅ English (eng) is available")
        else:
            print("   ❌ English (eng) is NOT available")
            
    except Exception as e:
        print(f"   ❌ Language check failed: {e}")
    
    # 3. Test different Tesseract configurations for Malayalam
    print("\n3. TESSERACT CONFIGURATION TESTING:")
    
    # Test configurations
    configs = [
        '--psm 6',           # Single uniform block
        '--psm 7',           # Single text line
        '--psm 8',           # Single word
        '--psm 10',          # Single character
        '--psm 13',          # Raw line
        '--oem 1',           # LSTM OCR engine
        '--oem 3',           # Default OCR engine
        '--psm 10 --oem 1',  # Character + LSTM
        '--psm 6 -c preserve_interword_spaces=1',
        '--psm 10 -c tessedit_char_whitelist=അആഇഈഉഊഋഎഏഐഒഓഔകഖഗഘങചഛജഝഞടഠഡഢണതഥദധനപഫബഭമയരറലളഴവശഷസഹഺ഻ഽാീുൂൃെേൈൊോൌൎ൏൐൑൒൓ൔൕൖൗ൘൙൚൛൜൝൞ൟ'
    ]
    
    # Create test image
    test_char = "അ"
    img = Image.new('RGB', (200, 100), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a Malayalam font
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 20), test_char, fill='black', font=font)
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    # Preprocess image for Tesseract
    image_array = np.array(img)
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    
    # Test each configuration
    results = {}
    for i, config in enumerate(configs):
        try:
            text = pytesseract.image_to_string(gray, lang='mal', config=config)
            confidence = 0.0
            
            try:
                data = pytesseract.image_to_data(gray, lang='mal', config=config, output_type=pytesseract.Output.DICT)
                confidences = [conf for conf in data['conf'] if conf > 0]
                if confidences:
                    confidence = sum(confidences) / len(confidences)
            except:
                pass
                
            results[config] = {
                'text': text.strip(),
                'confidence': confidence,
                'length': len(text.strip())
            }
            
            print(f"   Config {i+1}: {config}")
            print(f"      Text: '{text.strip()}'")
            print(f"      Confidence: {confidence:.2f}")
            print(f"      Length: {len(text.strip())}")
            
        except Exception as e:
            print(f"   Config {i+1}: {config} - FAILED: {e}")
    
    # Find best configuration
    print("\n4. BEST CONFIGURATION ANALYSIS:")
    best_config = None
    best_score = 0
    
    for config, result in results.items():
        # Score based on text detection and confidence
        score = 0
        if result['text']:
            score += 50  # Bonus for detecting text
        score += result['confidence'] * 50  # Confidence bonus
        score -= result['length'] * 2  # Penalty for too much text
        
        if score > best_score:
            best_score = score
            best_config = config
    
    if best_config:
        print(f"   🏆 Best config: {best_config}")
        print(f"   📊 Best score: {best_score:.2f}")
        print(f"   📝 Best result: {results[best_config]}")
    
    # 5. Compare with English performance
    print("\n5. MALAYALAM vs ENGLISH COMPARISON:")
    try:
        # Test English
        eng_text = pytesseract.image_to_string(gray, lang='eng', config='--psm 10')
        eng_conf = 0.0
        try:
            eng_data = pytesseract.image_to_data(gray, lang='eng', config='--psm 10', output_type=pytesseract.Output.DICT)
            eng_confs = [conf for conf in eng_data['conf'] if conf > 0]
            if eng_confs:
                eng_conf = sum(eng_confs) / len(eng_confs)
        except:
            pass
        
        # Test Malayalam with best config
        mal_text = pytesseract.image_to_string(gray, lang='mal', config=best_config or '--psm 10')
        mal_conf = 0.0
        try:
            mal_data = pytesseract.image_to_data(gray, lang='mal', config=best_config or '--psm 10', output_type=pytesseract.Output.DICT)
            mal_confs = [conf for conf in mal_data['conf'] if conf > 0]
            if mal_confs:
                mal_conf = sum(mal_confs) / len(mal_confs)
        except:
            pass
        
        print(f"   🇺🇸 English: '{eng_text.strip()}' (conf: {eng_conf:.2f})")
        print(f"   🇮🇳 Malayalam: '{mal_text.strip()}' (conf: {mal_conf:.2f})")
        
        if mal_conf < eng_conf:
            print(f"   ⚠️ Malayalam confidence is {((eng_conf - mal_conf) / eng_conf * 100):.1f}% lower than English")
        
    except Exception as e:
        print(f"   ❌ Comparison failed: {e}")
    
    # 6. Image preprocessing analysis
    print("\n6. IMAGE PREPROCESSING ANALYSIS:")
    
    # Test different preprocessing
    preprocessing_methods = {
        'original': gray,
        'threshold': cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1],
        'otsu': cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
        'adaptive': cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2),
        'blur_threshold': cv2.threshold(cv2.GaussianBlur(gray, (5, 5), 0), 0, 255, cv2.THRESH_BINARY)[1]
    }
    
    for method_name, processed_img in preprocessing_methods.items():
        try:
            text = pytesseract.image_to_string(processed_img, lang='mal', config=best_config or '--psm 10')
            print(f"   {method_name}: '{text.strip()}'")
        except Exception as e:
            print(f"   {method_name}: FAILED - {e}")
    
    # 7. Recommendations
    print("\n7. RECOMMENDATIONS:")
    
    if 'mal' not in pytesseract.get_languages(config=''):
        print("   ❌ Install Malayalam language pack")
        print("   📥 Download: https://github.com/tesseract-ocr/tessdata")
        print("   📁 Place mal.traineddata in tessdata directory")
    
    if best_config:
        print(f"   ✅ Use optimal config: {best_config}")
    
    print("   🎨 Try different preprocessing methods")
    print("   📏 Use appropriate image sizes (100-200px)")
    print("   🔤 Consider character whitelist for Malayalam")
    print("   🧪 Test with different font styles")

if __name__ == "__main__":
    analyze_tesseract_malayalam_issues()
