import json
import wave
import sys
import os
import shutil
import subprocess
from vosk import Model, KaldiRecognizer

class VoskSTT:
    def __init__(self, model_path="vosk_model"):
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        
        # Determine base directory
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Path Discovery: Favor Large 0.42 model if extracted
        large_path = os.path.join(self.base_dir, "vosk-model-gu-0.42", "vosk-model-gu-0.42")
        if os.path.exists(large_path):
            self.abs_model_path = large_path
            print(f"✨ Large Model Detected: {large_path}")
        else:
            self.abs_model_path = os.path.join(self.base_dir, self.model_path)
            
    def _lazy_init(self):
        if self.model: return True
        
        if not os.path.exists(self.abs_model_path):
            print(f"❌ Vosk Model not found at {self.abs_model_path}")
            return False
            
        try:
            print(f"📂 Loading Vosk Gujarati Model from {self.model_path}...")
            self.model = Model(self.abs_model_path)
            self.recognizer = KaldiRecognizer(self.model, 16000)
            print("✅ Vosk Model Loaded Successfully.")
            return True
        except Exception as e:
            print(f"❌ Vosk Init Error: {e}")
            return False

    def transcribe(self, audio_data):
        """
        Accepts audio bytes (WebM, MP3, or PCM)
        Converts to 16kHz mono PCM via FFmpeg if necessary.
        """
        if not self._lazy_init(): return None
        
        # Save temp audio for conversion
        temp_input = "stt_input_temp.raw"
        temp_output = "stt_output_pcm.wav"
        
        try:
            with open(temp_input, "wb") as f:
                f.write(audio_data)
            
            # Use FFmpeg to convert ANY format to Vosk-compatible PCM
            # Check for absolute path if 'ffmpeg' is not in system PATH yet
            ffmpeg_path = "ffmpeg"
            winget_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe")
            if not shutil.which("ffmpeg"):
                # Drill down to find the bin
                for root, dirs, files in os.walk(winget_path):
                    if "ffmpeg.exe" in files:
                        ffmpeg_path = os.path.join(root, "ffmpeg.exe")
                        break

            conv_cmd = [
                ffmpeg_path, "-y", "-i", temp_input,
                "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000",
                "-f", "wav", temp_output
            ]
            
            # Suppress logs for speed
            result = subprocess.run(conv_cmd, capture_output=True, check=False)
            
            if not os.path.exists(temp_output):
                # Fallback: maybe it's already PCM?
                print("⚠️ FFmpeg conversion failed. Attempting raw processing...")
                pcm_data = audio_data
            else:
                with open(temp_output, "rb") as f:
                    # Skip WAV header (first 44 bytes) to get raw data
                    f.seek(44)
                    pcm_data = f.read()

            # Process with Vosk
            if self.recognizer.AcceptWaveform(pcm_data):
                res = json.loads(self.recognizer.Result())
                text = res.get("text", "")
            else:
                res = json.loads(self.recognizer.PartialResult())
                text = ""

            final_res = json.loads(self.recognizer.FinalResult())
            final_text = final_res.get("text", "")
            
            return final_text if final_text else text
            
        except Exception as e:
            print(f"❌ Vosk Transcription Error: {e}")
            return None
        finally:
            # Cleanup
            for f in [temp_input, temp_output]:
                if os.path.exists(f): 
                    try: os.remove(f)
                    except: pass

if __name__ == "__main__":
    # Test block
    stt = VoskSTT()
    print("Testing Vosk STT Engine...")
    # Add dummy test if needed
