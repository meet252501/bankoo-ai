"""
Multilingual Voice Manager for Bankoo AI
Automatically switches voice characters to match language accents.

Features:
- 20+ languages with native speaker voices
- Auto-detect language and switch voice
- Male/Female voices for each language
- Natural accent matching
- Command-based language switching ("speak in Spanish")

Usage:
    voice_manager.speak("Hello", language="auto")  # Auto-detect
    voice_manager.speak("Hola", language="es")     # Force Spanish
    voice_manager.set_language("spanish")          # Switch via command
"""

import edge_tts
import asyncio
import re
from typing import Optional, Dict, Tuple

class MultilingualVoiceManager:
    """Manages voices across multiple languages with native accents"""
    
    # Voice characters for each language (Male, Female)
    VOICE_MAP: Dict[str, Tuple[str, str]] = {
        # Indian Languages
        'gujarati': ('gu-IN-NiranjanNeural', 'gu-IN-DhwaniNeural'),
        'hindi': ('hi-IN-MadhurNeural', 'hi-IN-SwaraNeural'),
        'tamil': ('ta-IN-ValluvarNeural', 'ta-IN-PallaviNeural'),
        'telugu': ('te-IN-MohanNeural', 'te-IN-ShrutiNeural'),
        'marathi': ('mr-IN-ManoharNeural', 'mr-IN-AarohiNeural'),
        'bengali': ('bn-IN-BashkarNeural', 'bn-IN-TanishaaNeural'),
        
        # European Languages
        'english': ('en-US-GuyNeural', 'en-US-JennyNeural'),
        'english-uk': ('en-GB-RyanNeural', 'en-GB-SoniaNeural'),
        'spanish': ('es-ES-AlvaroNeural', 'es-ES-ElviraNeural'),
        'french': ('fr-FR-HenriNeural', 'fr-FR-DeniseNeural'),
        'german': ('de-DE-ConradNeural', 'de-DE-KatjaNeural'),
        'italian': ('it-IT-DiegoNeural', 'it-IT-ElsaNeural'),
        'portuguese': ('pt-BR-AntonioNeural', 'pt-BR-FranciscaNeural'),
        'russian': ('ru-RU-DmitryNeural', 'ru-RU-SvetlanaNeural'),
        
        # Asian Languages  
        'chinese': ('zh-CN-YunxiNeural', 'zh-CN-XiaoxiaoNeural'),
        'japanese': ('ja-JP-KeitaNeural', 'ja-JP-NanamiNeural'),
        'korean': ('ko-KR-InJoonNeural', 'ko-KR-SunHiNeural'),
        'arabic': ('ar-SA-HamedNeural', 'ar-SA-ZariyahNeural'),
        'thai': ('th-TH-NiwatNeural', 'th-TH-PremwadeeNeural'),
        'vietnamese': ('vi-VN-NamMinhNeural', 'vi-VN-HoaiMyNeural'),
        
        # Additional Languages
        'dutch': ('nl-NL-MaartenNeural', 'nl-NL-ColetteNeural'),
        'polish': ('pl-PL-MarekNeural', 'pl-PL-ZofiaNeural'),
        'turkish': ('tr-TR-AhmetNeural', 'tr-TR-EmelNeural'),
    }
    
    # Language detection patterns
    LANGUAGE_PATTERNS = {
        'spanish': r'(hablar en español|speak in spanish|spanish)',
        'french': r'(parler en français|speak in french|french)',
        'german': r'(auf deutsch sprechen|speak in german|german)',
        'hindi': r'(हिंदी में बोलो|speak in hindi|hindi)',
        'chinese': r'(说中文|speak in chinese|chinese)',
        'japanese': r'(日本語で話す|speak in japanese|japanese)',
        'korean': r'(한국어로 말하다|speak in korean|korean)',
        'arabic': r'(تحدث بالعربية|speak in arabic|arabic)',
        'italian': r'(parlare in italiano|speak in italian|italian)',
        'portuguese': r'(falar em português|speak in portuguese|portuguese)',
        'russian': r'(говорить по-русски|speak in russian|russian)',
    }
    
    def __init__(self, default_language: str = 'gujarati', default_gender: str = 'male'):
        self.current_language = default_language
        self.current_gender = default_gender  # 'male' or 'female'
        
    def get_voice(self, language: Optional[str] = None, gender: Optional[str] = None) -> str:
        """Get the voice ID for specified language and gender"""
        lang = language or self.current_language
        gnd = gender or self.current_gender
        
        if lang not in self.VOICE_MAP:
            lang = 'english'  # Fallback
            
        male_voice, female_voice = self.VOICE_MAP[lang]
        return male_voice if gnd == 'male' else female_voice
    
    def detect_language_command(self, text: str) -> Optional[str]:
        """Detect if user wants to switch language"""
        text_lower = text.lower()
        
        for lang, pattern in self.LANGUAGE_PATTERNS.items():
            if re.search(pattern, text_lower, re.IGNORECASE):
                return lang
                
        return None
    
    def set_language(self, language: str, gender: Optional[str] = None) -> str:
        """Switch to a new language"""
        if language in self.VOICE_MAP:
            self.current_language = language
            if gender:
                self.current_gender = gender
            voice = self.get_voice()
            return f"✅ Switched to {language.title()} voice: {voice}"
        else:
            available = ', '.join(self.VOICE_MAP.keys())
            return f"❌ Language '{language}' not supported. Available: {available}"
    
    def toggle_gender(self) -> str:
        """Switch between male and female voice"""
        self.current_gender = 'female' if self.current_gender == 'male' else 'male'
        voice = self.get_voice()
        return f"✅ Switched to {self.current_gender} voice: {voice}"
    
    async def speak_async(self, text: str, language: Optional[str] = None, 
                         gender: Optional[str] = None, output_file: str = "output.mp3") -> str:
        """Generate speech with specified voice"""
        voice = self.get_voice(language, gender)
        
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_file)
            return f"✅ Speech generated: {output_file} (Voice: {voice})"
        except Exception as e:
            return f"❌ TTS Error: {e}"
    
    def speak(self, text: str, language: Optional[str] = None, 
             gender: Optional[str] = None, output_file: str = "output.mp3") -> str:
        """Synchronous wrapper for speak_async"""
        return asyncio.run(self.speak_async(text, language, gender, output_file))
    
    def get_available_languages(self) -> list:
        """Return list of supported languages"""
        return sorted(self.VOICE_MAP.keys())
    
    def get_voice_info(self, language: Optional[str] = None) -> dict:
        """Get detailed info about current or specified language voices"""
        lang = language or self.current_language
        
        if lang not in self.VOICE_MAP:
            return {"error": f"Language '{lang}' not found"}
            
        male, female = self.VOICE_MAP[lang]
        
        return {
            "language": lang,
            "male_voice": male,
            "female_voice": female,
            "current_voice": self.get_voice(),
            "current_gender": self.current_gender
        }


# Example Integration with Bankoo Assistant
class VoiceIntegration:
    """Helper to integrate multilingual voices into Bankoo"""
    
    def __init__(self):
        self.voice_manager = MultilingualVoiceManager(
            default_language='gujarati',
            default_gender='male'
        )
    
    def process_voice_command(self, user_text: str) -> Optional[str]:
        """
        Check if user wants to switch voice language
        Returns: Status message if language switched, None otherwise
        """
        # Check for language switch command
        detected_lang = self.voice_manager.detect_language_command(user_text)
        
        if detected_lang:
            return self.voice_manager.set_language(detected_lang)
        
        # Check for gender switch
        if re.search(r'(switch to (male|female) voice|change voice gender)', user_text, re.IGNORECASE):
            return self.voice_manager.toggle_gender()
        
        return None
    
    def speak_response(self, text: str, auto_detect: bool = True) -> str:
        """Generate speech for AI response"""
        # Auto-detect language from text if enabled
        if auto_detect:
            detected_lang = self.detect_text_language(text)
            if detected_lang:
                return self.voice_manager.speak(text, language=detected_lang)
        
        # Use current language
        return self.voice_manager.speak(text)
    
    def detect_text_language(self, text: str) -> Optional[str]:
        """Simple language detection based on character sets"""
        # This is a simplified version - you can use langdetect library for better accuracy
        
        # Check for specific scripts
        if re.search(r'[\u0900-\u097F]', text):  # Devanagari (Hindi)
            return 'hindi'
        elif re.search(r'[\u0A80-\u0AFF]', text):  # Gujarati
            return 'gujarati'
        elif re.search(r'[\u4E00-\u9FFF]', text):  # Chinese
            return 'chinese'
        elif re.search(r'[\u3040-\u30FF]', text):  # Japanese
            return 'japanese'
        elif re.search(r'[\uAC00-\uD7AF]', text):  # Korean
            return 'korean'
        elif re.search(r'[\u0600-\u06FF]', text):  # Arabic
            return 'arabic'
        
        # Default to current language
        return None


# Usage Examples
if __name__ == "__main__":
    # Initialize
    vm = MultilingualVoiceManager()
    
    print("🎤 Multilingual Voice Manager Demo\n")
    
    # Show available languages
    print(f"📋 Available Languages ({len(vm.get_available_languages())}):")
    for lang in vm.get_available_languages():
        print(f"   • {lang.title()}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 1: Switch to Spanish
    print("Example 1: Switch to Spanish")
    print(vm.set_language('spanish'))
    print(vm.speak("Hola, ¿cómo estás?"))
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Switch to Hindi Female
    print("Example 2: Switch to Hindi Female")
    print(vm.set_language('hindi', 'female'))
    print(vm.speak("नमस्ते, आप कैसे हैं?"))
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Language detection in command
    print("Example 3: Auto-detect from command")
    integration = VoiceIntegration()
    result = integration.process_voice_command("Please speak in French")
    if result:
        print(result)
        print(integration.voice_manager.speak("Bonjour, comment allez-vous?"))
    
    print("\n" + "="*50 + "\n")
    
    # Example 4: Get voice info
    print("Example 4: Voice Information")
    info = vm.get_voice_info()
    for key, value in info.items():
        print(f"   {key}: {value}")
