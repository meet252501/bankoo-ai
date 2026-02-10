import time
import math
import os
from PIL import Image, ImageDraw, ImageChops

class VisionUtils:
    """Optical Support Tools for Zenith v6"""

    @staticmethod
    def draw_grid(image_path, output_path, rows=5, cols=5):
        """Overlay a numbered red grid on the screenshot"""
        try:
            with Image.open(image_path) as img:
                draw = ImageDraw.Draw(img)
                width, height = img.size
                col_step = width / cols
                row_step = height / rows

                # Draw Lines
                for x in range(1, cols):
                    draw.line([(x * col_step, 0), (x * col_step, height)], fill="red", width=2)
                for y in range(1, rows):
                    draw.line([(0, y * row_step), (width, y * row_step)], fill="red", width=2)

                # Draw Numbers
                for r in range(rows):
                    for c in range(cols):
                        cell_id = r * cols + c + 1
                        # Calculate center of cell
                        cx = (c * col_step) + (col_step / 2)
                        cy = (r * row_step) + (row_step / 2)
                        
                        # Draw Text (Simple fallback if font fails)
                        draw.text((cx-5, cy-5), str(cell_id), fill="red")
                
                img.save(output_path)
                return True
        except Exception as e:
            print(f"Grid Error: {e}")
            return False

    @staticmethod
    def calculate_diff(img1_path, img2_path):
        """Calculate percentage difference between two images"""
        try:
            with Image.open(img1_path) as img1, Image.open(img2_path) as img2:
                diff = ImageChops.difference(img1, img2)
                bbox = diff.getbbox()
                if not bbox: return 0.0 # Identical
                
                # Simple heuristic: sum of pixel differences
                # For speed in pure python, we might just rely on bbox existence for now
                return 1.0 # Changed
        except:
            return 0.0

    @staticmethod
    def wait_for_settle(capture_func, timeout=5):
        """Smart Wait: Blocks until screen stops moving (pixels settle)"""
        import uuid
        session_id = str(uuid.uuid4())[:8]
        last_snap = f"v_settle_{session_id}_1.jpg"
        curr_snap = f"v_settle_{session_id}_2.jpg"
        
        start = time.time()
        
        try:
            # Initial Snap
            capture_func(last_snap)
            time.sleep(0.5) 
            
            settled = False
            while time.time() - start < timeout:
                capture_func(curr_snap)
                
                # Compare
                is_same = False
                try:
                    with Image.open(last_snap) as i1, Image.open(curr_snap) as i2:
                        i1.load() # Force load into memory
                        i2.load()
                        diff = ImageChops.difference(i1, i2)
                        if not diff.getbbox():
                            is_same = True
                except Exception as e:
                    print(f"Settle Compare Error: {e}")
                
                if is_same:
                    settled = True
                    break
                
                # Swap files safely
                try:
                    if os.path.exists(last_snap): os.remove(last_snap)
                    time.sleep(0.1) # Windows grace period
                    os.rename(curr_snap, last_snap)
                except: pass
                
                time.sleep(0.4)

            return settled
        finally:
            # Cleanup
            for f in [last_snap, curr_snap]:
                try:
                    if os.path.exists(f): os.remove(f)
                except: pass

