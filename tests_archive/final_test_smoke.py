import sys
import os
import unittest
from unittest.mock import MagicMock, patch, AsyncMock

# Fix path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Prevent Sentinel thread
with patch('bankoo_bridge.Sentinel.start'):
    import bankoo_bridge

class TestMoltbotSmoke(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.agent = bankoo_bridge.MoltbotAgent()
        self.agent.is_authorized = MagicMock(return_value=True)

    def create_mocks(self, text, args=[]):
        update = MagicMock()
        update.message.text = text
        # Async mocks for reply methods
        update.message.reply_text = AsyncMock()
        update.message.reply_markdown = AsyncMock()
        update.message.reply_voice = AsyncMock()
        update.message.reply_photo = AsyncMock()
        update.message.reply_document = AsyncMock()
        
        context = MagicMock()
        context.args = args
        context.bot.send_message = AsyncMock()
        context.bot.send_chat_action = AsyncMock()
        return update, context

    async def test_smoke_all_commands(self):
        """Run all handlers to ensure no runtime errors"""
        
        # 1. Status
        u, c = self.create_mocks("/status")
        await self.agent.handle_status(u, c)
        u.message.reply_markdown.assert_called()
        
        # 2. Lock (Mock ctypes)
        with patch('bankoo_bridge.ctypes'):
            u, c = self.create_mocks("/lock")
            await self.agent.handle_lock(u, c)
            u.message.reply_text.assert_called()

        # 3. Copy (Mock pyperclip)
        with patch('bankoo_bridge.pyperclip'):
            u, c = self.create_mocks("/copy", ["test"])
            await self.agent.handle_copy(u, c)
            u.message.reply_text.assert_called()

        # 4. LS (Omni)
        u, c = self.create_mocks("/ls", ["."])
        await self.agent.handle_ls(u, c)
        u.message.reply_markdown.assert_called()

        # 5. Media (Mock pyautogui)
        with patch('bankoo_bridge.pyautogui'):
            u, c = self.create_mocks("/play")
            await self.agent.handle_media(u, c)
            u.message.reply_text.assert_called()

        # 6. Speak (Mock edge_tts)
        with patch('bankoo_bridge.edge_tts.Communicate') as mock_tts:
            mock_inst = AsyncMock()
            mock_tts.return_value = mock_inst
            
            with patch('builtins.open', MagicMock()), \
                 patch('os.path.exists', return_value=True), \
                 patch('os.remove'):
                
                u, c = self.create_mocks("/say", ["hi"])
                await self.agent.handle_speak(u, c)
                u.message.reply_voice.assert_called()

        # 7. Calendar
        u, c = self.create_mocks("/calendar")
        await self.agent.handle_calendar(u, c)
        u.message.reply_text.assert_called()

        print("✅ ALL COMMANDS EXECUTED SUCCESSFULLY")

if __name__ == '__main__':
    unittest.main()
