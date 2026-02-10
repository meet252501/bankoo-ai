import threading
import time
import logging
import psutil
import requests
import os

logger = logging.getLogger(__name__)

class ProactiveButler:
    """
    Zenith v19: The Proactive Butler Engine.
    Runs background monitors and notifies the user via the Neural Orb.
    100% Free & Local.
    """
    def __init__(self, ui_callback=None):
        self.ui_callback = ui_callback
        self.running = False
        self.monitor_thread = None
        self.last_battery_alert = 0
        self.last_github_check = 0
        
    def start(self):
        """Starts the background monitoring loop."""
        if self.running: return
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("🤖 [BUTLER] Proactive Butler is now ON DUTY.")

    def stop(self):
        """Stops the monitoring loop."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)

    def _notify(self, message, cmd="console_log", log_type="sys", importance="low"):
        """Sends a notification to the Bankoo UI."""
        if self.ui_callback:
            # Change Orb Color if important
            if importance == "high":
                 self.ui_callback("ui_cmd", cmd="set_state", state="thinking") # Pulse Gold
            
            self.ui_callback("ui_cmd", cmd=cmd, content=message, log_type=log_type)
            logger.info(f"🤖 [BUTLER] Notified: {message}")

    def _check_system_health(self):
        """Monitors CPU and Battery."""
        cpu = psutil.cpu_percent()
        if cpu > 90:
            self._notify(f"⚠️ High CPU Load detected: {cpu}%", importance="high")

        # Battery check if laptop
        battery = psutil.sensors_battery()
        if battery and battery.percent < 20 and not battery.power_plugged:
            if time.time() - self.last_battery_alert > 600: # Every 10 mins
                self._notify(f"🔋 Battery Low: {battery.percent}%! Please plug in.", importance="high")
                self.last_battery_alert = time.time()

    def _check_github(self):
        """Monitors GitHub for activity (Simulated/Token-based)."""
        # This would use the GITHUB_TOKEN if configured
        # For now, we simulate a 'clean checkout' notification or system check
        pass

    def _monitor_loop(self):
        """The core loop that runs every 60 seconds."""
        # Initial wait to let system settle
        time.sleep(10)
        
        while self.running:
            try:
                self._check_system_health()
                # self._check_github()
                
                # Sleep between checks
                time.sleep(60)
            except Exception as e:
                logger.error(f"🤖 [BUTLER] Monitoring error: {e}")
                time.sleep(30)

# Implementation Note:
# To enable this, add `butler = ProactiveButler(ui_callback=self.ui_callback)` 
# to Assistant.__init__ and call `butler.start()`.
