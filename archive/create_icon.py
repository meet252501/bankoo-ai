"""
Icon Converter - Converts PNG to ICO for Windows shortcuts
"""
from PIL import Image
import os

def create_icon():
    # Use the new generated logo
    logo_path = r"C:\Users\Meet Sutariya\.gemini\antigravity\brain\66d0a0ff-21d9-41b3-b96c-e21295f502d3\bankoo_ai_logo_1769744007519.png"
    icon_path = r"C:\Users\Meet Sutariya\Desktop\final banko.ai\bankoo_icon.ico"
    
    if not os.path.exists(logo_path):
        print(f"❌ Logo not found at: {logo_path}")
        return False
    
    try:
        # Open the PNG image
        img = Image.open(logo_path)
        
        # Convert to RGB if necessary (ICO needs RGB)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to standard icon sizes
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        
        # Save as ICO with multiple sizes
        img.save(icon_path, format='ICO', sizes=icon_sizes)
        
        print(f"✅ Icon created successfully at: {icon_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating icon: {e}")
        return False

if __name__ == "__main__":
    create_icon()
