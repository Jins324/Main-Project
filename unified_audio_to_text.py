"""
Unified Audio-to-Text Coordinator
Manages English and Malayalam audio-to-text conversion systems
"""
import os
import logging
from english_audio_to_text import EnglishAudioToText
from malayalam_audio_to_text import MalayalamAudioToText

logger = logging.getLogger(__name__)

class UnifiedAudioToText:
    """Coordinator for language-specific audio-to-text conversion"""
    
    def __init__(self):
        # Initialize language-specific converters
        self.english_converter = EnglishAudioToText()
        self.malayalam_converter = MalayalamAudioToText()
        
        # Language mapping
        self.converters = {
            'en': self.english_converter,
            'english': self.english_converter,
            'ml': self.malayalam_converter,
            'malayalam': self.malayalam_converter
        }
        
        logger.info("Unified Audio-to-Text Coordinator initialized")
    
    def convert_audio_to_text(self, audio_file_path: str, language: str = 'auto', engine: str = 'auto') -> dict:
        """Convert audio to text using language-specific converter"""
        
        try:
            # Auto-detect language if specified
            if language == 'auto':
                language = self._detect_language(audio_file_path)
                logger.info(f"Auto-detected language: {language}")
            
            # Normalize language code
            lang_code = language.lower()
            if lang_code not in self.converters:
                logger.error(f"Unsupported language: {language}")
                return {
                    'success': False,
                    'text': '',
                    'confidence': 0.0,
                    'language': language,
                    'engine': 'none',
                    'error': f'Unsupported language: {language}'
                }
            
            # Get appropriate converter
            converter = self.converters[lang_code]
            
            # Use language-specific conversion
            result = converter.convert_audio_to_text(audio_file_path, engine)
            
            # Add language information to result
            result['language'] = lang_code
            
            logger.info(f"Audio-to-text conversion completed for {language}: '{result.get('text', '')[:50]}...'")
            return result
            
        except Exception as e:
            logger.error(f"Audio-to-text conversion error: {e}")
            return {
                'success': False,
                'text': '',
                'confidence': 0.0,
                'language': language,
                'engine': 'error',
                'error': str(e)
            }
    
    def _detect_language(self, audio_file_path: str) -> str:
        """Auto-detect language from audio"""
        
        try:
            # Try English first (more common)
            result = self.english_converter.convert_audio_to_text(audio_file_path, 'google')
            
            if result['success'] and result['confidence'] > 0.6:
                # Validate if it's actually English
                if self._is_english_text(result['text']):
                    return 'en'
            
            # Try Malayalam
            result = self.malayalam_converter.convert_audio_to_text(audio_file_path, 'google')
            
            if result['success'] and result['confidence'] > 0.4:
                # Validate if it's actually Malayalam
                validation = self.malayalam_converter.validate_malayalam_text(result['text'])
                if validation['is_malayalam']:
                    return 'ml'
            
            # Default to English if uncertain
            return 'en'
            
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return 'en'  # Default to English
    
    def _is_english_text(self, text: str) -> bool:
        """Check if text is English"""
        
        try:
            if not text:
                return False
            
            # Check for English characters
            english_chars = sum(1 for c in text if c.isalpha() and ord(c) < 128)
            total_chars = sum(1 for c in text if c.isalpha())
            
            if total_chars == 0:
                return False
            
            english_ratio = english_chars / total_chars
            return english_ratio > 0.8
            
        except Exception:
            return False
    
    def convert_english_audio(self, audio_file_path: str, engine: str = 'auto') -> dict:
        """Convert English audio to text"""
        
        return self.convert_audio_to_text(audio_file_path, 'en', engine)
    
    def convert_malayalam_audio(self, audio_file_path: str, engine: str = 'auto') -> dict:
        """Convert Malayalam audio to text"""
        
        return self.convert_audio_to_text(audio_file_path, 'ml', engine)
    
    def get_supported_languages(self) -> dict:
        """Get list of supported languages"""
        
        return {
            'en': {
                'name': 'English',
                'code': 'en',
                'converter': 'english_converter',
                'engines': list(self.english_converter.get_supported_engines().keys())
            },
            'ml': {
                'name': 'Malayalam',
                'code': 'ml',
                'converter': 'malayalam_converter',
                'engines': list(self.malayalam_converter.get_supported_engines().keys())
            }
        }
    
    def get_all_engines(self) -> dict:
        """Get all available engines for all languages"""
        
        engines = {}
        
        for lang_code, converter in self.converters.items():
            engines[lang_code] = converter.get_supported_engines()
        
        return engines
    
    def test_conversion(self, audio_file_path: str, language: str = 'auto') -> dict:
        """Test audio-to-text conversion with all engines"""
        
        try:
            # Auto-detect language if needed
            if language == 'auto':
                language = self._detect_language(audio_file_path)
            
            # Normalize language code
            lang_code = language.lower()
            if lang_code not in self.converters:
                return {
                    'success': False,
                    'error': f'Unsupported language: {language}'
                }
            
            # Get appropriate converter
            converter = self.converters[lang_code]
            
            # Test all engines
            results = converter.test_all_engines(audio_file_path)
            
            # Add language information
            results['language'] = lang_code
            
            return results
            
        except Exception as e:
            logger.error(f"Test conversion error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def batch_convert(self, audio_files: list, languages: list = None) -> list:
        """Convert multiple audio files"""
        
        results = []
        
        for i, audio_file in enumerate(audio_files):
            try:
                # Determine language
                if languages and i < len(languages):
                    language = languages[i]
                else:
                    language = 'auto'
                
                # Convert audio
                result = self.convert_audio_to_text(audio_file, language)
                result['file_path'] = audio_file
                result['file_index'] = i
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Batch conversion error for {audio_file}: {e}")
                results.append({
                    'success': False,
                    'file_path': audio_file,
                    'file_index': i,
                    'error': str(e)
                })
        
        return results
    
    def get_conversion_stats(self) -> dict:
        """Get conversion system statistics"""
        
        stats = {
            'supported_languages': len(self.converters),
            'total_engines': 0,
            'engines_by_language': {}
        }
        
        for lang_code, converter in self.converters.items():
            engines = converter.get_supported_engines()
            stats['engines_by_language'][lang_code] = {
                'count': len(engines),
                'engines': list(engines.keys())
            }
            stats['total_engines'] += len(engines)
        
        return stats

# Test the unified system
if __name__ == "__main__":
    converter = UnifiedAudioToText()
    
    print("🌍 UNIFIED AUDIO-TO-TEXT SYSTEM")
    print("=" * 50)
    
    # Test system info
    languages = converter.get_supported_languages()
    print(f"Supported Languages:")
    for code, info in languages.items():
        print(f"  {code}: {info['name']} ({len(info['engines'])} engines)")
    
    # Test conversion stats
    stats = converter.get_conversion_stats()
    print(f"\n📊 System Statistics:")
    print(f"  Languages: {stats['supported_languages']}")
    print(f"  Total Engines: {stats['total_engines']}")
    
    # Test individual converters
    print(f"\n🧪 Testing Individual Converters:")
    
    # Test English
    print(f"\n🇺🇸 English Converter Test:")
    english_result = converter.convert_english_audio("test_en.wav", "google")
    print(f"  Result: {english_result.get('success', False)}")
    if english_result.get('success'):
        print(f"  Text: '{english_result.get('text', '')[:30]}...'")
        print(f"  Confidence: {english_result.get('confidence', 0):.2f}")
    
    # Test Malayalam
    print(f"\n🇮🇳 Malayalam Converter Test:")
    malayalam_result = converter.convert_malayalam_audio("test_ml.wav", "google")
    print(f"  Result: {malayalam_result.get('success', False)}")
    if malayalam_result.get('success'):
        print(f"  Text: '{malayalam_result.get('text', '')[:30]}...'")
        print(f"  Confidence: {malayalam_result.get('confidence', 0):.2f}")
    
    print(f"\n✅ Unified Audio-to-Text System Ready!")
