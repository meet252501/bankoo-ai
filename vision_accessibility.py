from pywinauto import Desktop
import logging
import pyautogui

logger = logging.getLogger(__name__)

class AccessibilityAgent:
    """Finds UI elements using the Windows Accessibility Tree (Zero Cost)"""
    
    def find_element(self, target_name):
        """Search for a UI element by its accessible name"""
        try:
            # Connect to the desktop
            desktop = Desktop(backend="uia")
            
            # Search for the element across all windows
            # Note: This can be slow if there are many elements. We'll limit the search.
            logger.info(f"🔍 Searching Accessibility Tree for: {target_name}")
            
            # Simple heuristic: look for windows first, then children
            for win in desktop.windows():
                try:
                    # Look for exact match or substring in the window title or its children
                    if target_name.lower() in win.window_text().lower():
                        rect = win.rectangle()
                        return self._rect_to_normalized(rect)
                        
                    # Find child element (e.g. Button)
                    elem = win.child_window(title_re=f".*{target_name}.*", control_type="Button", found_index=0)
                    if elem.exists():
                        rect = elem.rectangle()
                        return self._rect_to_normalized(rect)
                except:
                    continue
                    
            return {"error": "Element not found in Accessibility Tree."}
        except Exception as e:
            return {"error": f"Accessibility Error: {e}"}

    def _rect_to_normalized(self, rect):
        """Convert pywinauto rect to normalized 0-1000 coordinates"""
        sw, sh = pyautogui.size()
        cx = (rect.left + rect.right) // 2
        cy = (rect.top + rect.bottom) // 2
        
        nx = int((cx / sw) * 1000)
        ny = int((cy / sh) * 1000)
        return {"x": nx, "y": ny}
