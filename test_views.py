import sys
import os
sys.path.append(os.path.dirname(__file__))

from ml_models.robust_template_detector import predict_robust_handwriting
from PIL import Image, ImageDraw, ImageFont
import io
import base64

def generate_base64_drawing(char):
    # simulate user drawing an "A"
    img = Image.new('L', (400, 400), color=255)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("ml_models/NotoSansMalayalam.ttf", 300)
    except:
        font = ImageFont.load_default()
    draw.text((50, 50), char, font=font, fill=0)
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

test_image = generate_base64_drawing("ക")
result = predict_robust_handwriting(test_image, "ക")
print("EXPECTED 'ക':", result)

result2 = predict_robust_handwriting(test_image, "മ")
print("EXPECTED 'മ':", result2)

# Empty expected
result3 = predict_robust_handwriting(test_image, "")
print("EXPECTED EMPTY:", result3)
