import os
import subprocess
import logging

logger = logging.getLogger(__name__)

SKILLS_REPO = "https://github.com/openclaw/skills.git"
TARGET_DIR = os.path.join("moltbot_skills", "openclaw-skills")

def sync_skills():
    """Clones or updates the Awesome OpenClaw Skills repository."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(base_dir, TARGET_DIR)
    
    if not os.path.exists(target_path):
        logger.info(f"🚀 [SKILL-SYNC] Cloning repository into {TARGET_DIR}...")
        try:
            subprocess.run(["git", "clone", SKILLS_REPO, target_path], check=True)
            logger.info("✅ [SKILL-SYNC] Clone successful.")
            return True, "Repository cloned successfully."
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ [SKILL-SYNC] Clone failed: {e}")
            return False, f"Clone failed: {e}"
    else:
        logger.info(f"🔄 [SKILL-SYNC] Repo exists. Pulling latest updates...")
        try:
            # Run git pull inside the target directory
            subprocess.run(["git", "-C", target_path, "pull"], check=True)
            logger.info("✅ [SKILL-SYNC] Update successful.")
            return True, "Repository updated successfully."
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ [SKILL-SYNC] Update failed: {e}")
            return False, f"Update failed: {e}"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    success, msg = sync_skills()
    print(msg)
