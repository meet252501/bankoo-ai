"""
Whisper STT - High-Accuracy Speech Recognition (Free, Local)
Replaces Vosk with OpenAI Whisper for 2x better accuracy
"""
import os
import tempfile
import subprocess
import shutil

class WhisperSTT:
    def __init__(self, model_size="base"):
        """
        Initialize Whisper STT Engine
        
        Model sizes (accuracy vs speed):
        - tiny: Fastest, ~40MB (okay for simple commands)
        - base: Good balance, ~150MB (RECOMMENDED)
        - small: Better accuracy, ~500MB
        - medium: High accuracy, ~1.5GB
        - large: Best accuracy, ~3GB (GPU recommended)
        """
        self.model = None
        self.model_size = model_size
        print(f"Whisper STT initialized (model: {model_size})")
        
    def _lazy_init(self):
        """Load model on first use (saves startup time)"""
        if self.model:
            return True
            
        try:
            print(f"📥 Loading Whisper model ({self.model_size})...")
            import whisper
            self.model = whisper.load_model(self.model_size)
            print("✅ Whisper model loaded successfully!")
            return True
        except ImportError:
            print("❌ Whisper not installed. Run: pip install openai-whisper")
            return False
        except Exception as e:
            print(f"❌ Whisper init error: {e}")
            return False
    
    def transcribe(self, audio_data, language=None):
        """
        Transcribe audio bytes to text
        
        Args:
            audio_data: Raw audio bytes (any format - mp3, webm, wav, etc.)
            language: Optional language code ('en', 'hi', 'gu', etc.)
                     If None, Whisper will auto-detect
        
        Returns:
            str: Transcribed text with punctuation
        """
        if not self._lazy_init():
            return None
        
        # Create temp file for audio conversion
        temp_input = None
        temp_output = None
        
        try:
            # Save raw audio bytes to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.raw') as f:
                temp_input = f.name
                f.write(audio_data)
            
            # Convert to WAV using FFmpeg (Whisper needs audio file format)
            temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
            
            # Find FFmpeg
            ffmpeg_path = self._find_ffmpeg()
            
            conv_cmd = [
                ffmpeg_path, '-y', '-i', temp_input,
                '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000',
                temp_output
            ]
            
            # Run conversion (suppress output)
            subprocess.run(conv_cmd, capture_output=True, check=True)
            
            if not os.path.exists(temp_output):
                print("❌ Audio conversion failed")
                return None
            
            # Transcribe with Whisper
            print("🎤 Transcribing with Whisper...")
            result = self.model.transcribe(
                temp_output,
                language=language,  # Auto-detect if None
                fp16=False  # CPU compatibility
            )
            
            text = result["text"].strip()
            print(f"✅ Transcription: '{text}'")
            return text
            
        except subprocess.CalledProcessError as e:
            print(f"❌ FFmpeg error: {e}")
            return None
        except Exception as e:
            print(f"❌ Whisper transcription error: {e}")
            return None
        finally:
            # Cleanup temp files
            for f in [temp_input, temp_output]:
                if f and os.path.exists(f):
                    try:
                        os.remove(f)
                    except:
                        pass
    
    def _find_ffmpeg(self):
        """Locate FFmpeg binary"""
        # Check if in PATH
        if shutil.which("ffmpeg"):
            return "ffmpeg"
        
        # Check WinGet installation (Windows)
        winget_path = os.path.expandvars(
            r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
        )
        
        if os.path.exists(winget_path):
            for root, dirs, files in os.walk(winget_path):
                if "ffmpeg.exe" in files:
                    return os.path.join(root, "ffmpeg.exe")
        
        # Fallback
        return "ffmpeg"

# Test block
if __name__ == "__main__":
    print("Testing Whisper STT Engine...")
    stt = WhisperSTT(model_size="base")
    
    # Test with sample audio (you'd need a real audio file)
    # with open("test_audio.wav", "rb") as f:
    #     audio = f.read()
    #     result = stt.transcribe(audio, language="hi")
    #     print(f"Result: {result}")
