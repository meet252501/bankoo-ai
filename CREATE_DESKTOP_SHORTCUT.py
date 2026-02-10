"""
Bankoo AI Desktop Shortcut Creator with Custom Icon
Run this script to create a desktop shortcut with the Bankoo AI logo
"""
import os
import sys
from pathlib import Path

def create_desktop_shortcut():
    try:
        import win32com.client
        from PIL import Image
        
        # Paths
        desktop = Path.home() / "Desktop"
        app_dir = Path(__file__).parent
        logo_source = r"C:\Users\Meet Sutariya\.gemini\antigravity\brain\80b37290-ecfb-48c2-91cf-9896683dd2da\bankoo_logo_1769083479683.png"
        icon_path = app_dir / "bankoo_icon.ico"
        bat_path = app_dir / "START_BANKOO.bat"
        shortcut_path = desktop / "Bankoo AI.lnk"
        
        print("🎨 Creating Bankoo AI icon...")
        
        # Step 1: Convert PNG to ICO
        if os.path.exists(logo_source):
            try:
                img = Image.open(logo_source)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Create icon with multiple sizes
                icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
                img.save(str(icon_path), format='ICO', sizes=icon_sizes)
                print(f"   ✅ Icon created: {icon_path}")
            except Exception as e:
                print(f"   ⚠️ Could not create icon: {e}")
                print("   📝 Will create shortcut without custom icon")
                icon_path = None
        else:
            print("   ⚠️ Logo source not found, using default icon")
            icon_path = None
        
        # Step 2: Create desktop shortcut
        print("\n🔗 Creating desktop shortcut...")
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = str(bat_path)
        shortcut.WorkingDirectory = str(app_dir)
        shortcut.Description = "Bankoo AI - Your Intelligent Desktop Assistant"
        
        if icon_path and icon_path.exists():
            shortcut.IconLocation = str(icon_path)
            print(f"   🎨 Using custom icon: {icon_path.name}")
        
        shortcut.save()
        
        print(f"\n✅ Desktop shortcut created successfully!")
        print(f"📍 Location: {shortcut_path}")
        print(f"\n🚀 Double-click 'Bankoo AI' on your desktop to launch!")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ Missing required library: {e}")
        print("📦 Install with: pip install pywin32 pillow")
        return False
    except Exception as e:
        print(f"\n❌ Error creating shortcut: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  BANKOO AI - Desktop Shortcut Creator")
    print("=" * 60)
    print()
    
    success = create_desktop_shortcut()
    
    print()
    input("Press Enter to exit...")
    sys.exit(0 if success else 1)
