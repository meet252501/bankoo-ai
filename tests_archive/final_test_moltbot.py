import sys
import os
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio

# Fix path to find modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Prevent Sentinel thread from starting during import/init
with patch('bankoo_bridge.Sentinel.start'):
    import bankoo_bridge

class TestMoltbotFinal(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Initialize agent with mocked auth
        self.agent = bankoo_bridge.MoltbotAgent()
        self.agent.is_authorized = MagicMock(return_value=True)

    def create_mocks(self, text="/test", args=[]):
        """Helper to create async-ready update/context mocks"""
        update = MagicMock()
        update.message.text = text
        # Mock all reply methods as AsyncMock
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

    async def test_cmd_status(self):
        """Test /status"""
        update, context = self.create_mocks("/status")
        await self.agent.handle_status(update, context)
        # Check if it replied with markdown containing "Status"
        update.message.reply_markdown.assert_called()
        msg = update.message.reply_markdown.call_args[0][0]
        self.assertIn("Status", msg)
        print("✅ /status Verified")

    @patch('bankoo_bridge.ctypes')
    async def test_cmd_lock(self, mock_ctypes):
        """Test /lock"""
        update, context = self.create_mocks("/lock")
        await self.agent.handle_lock(update, context)
        mock_ctypes.windll.user32.LockWorkStation.assert_called()
        update.message.reply_text.assert_called_with("🔒 Gateway Locked.")
        print("✅ /lock Verified")

    @patch('bankoo_bridge.pyperclip')
    async def test_cmd_copy(self, mock_clip):
        """Test /copy (Sync)"""
        update, context = self.create_mocks("/copy", args=["test", "msg"])
        await self.agent.handle_copy(update, context)
        mock_clip.copy.assert_called_with("test msg")
        update.message.reply_text.assert_called()
        print("✅ /copy Verified")

    @patch('bankoo_bridge.requests.get')
    async def test_cmd_google(self, mock_get):
        """Test /google (Web)"""
        # Mock HTML response for regex
        mock_response = MagicMock()
        mock_response.text = 'result__a" href="http://example.com">Example Result</a>'
        mock_get.return_value = mock_response

        update, context = self.create_mocks("/google", args=["query"])
        
        # Disable threading for test simplicity or mock executor?
        # handle_google uses loop.run_in_executor
        # We can rely on real executor or patch it.
        # Patching bankoo_bridge.requests.get affects the thread execution too.
        
        await self.agent.handle_google(update, context)
        
        # Verify reply markdown called
        update.message.reply_markdown.assert_called()
        msg = update.message.reply_markdown.call_args[0][0]
        self.assertIn("Example Result", msg)
        print("✅ /google Verified")

    async def test_cmd_ls(self):
        """Test /ls (Omni)"""
        update, context = self.create_mocks("/ls", args=["."])
        await self.agent.handle_ls(update, context)
        
        update.message.reply_markdown.assert_called()
        msg = update.message.reply_markdown.call_args[0][0]
        self.assertIn("bankoo_bridge.py", msg)
        print("✅ /ls Verified")

    @patch('bankoo_bridge.pyautogui')
    async def test_cmd_media(self, mock_gui):
        """Test /play and /vol (Media)"""
        # Case 1: /play
        update, context = self.create_mocks("/play")
        await self.agent.handle_media(update, context)
        mock_gui.press.assert_called_with('playpause')
        
        # Case 2: /vol up
        update2, context2 = self.create_mocks("/vol", args=["up"])
        await self.agent.handle_media(update2, context2)
        mock_gui.press.assert_called_with('volumeup', presses=5)
        print("✅ /play & /vol Verified")

    @patch('bankoo_bridge.edge_tts.Communicate')
    async def test_cmd_say(self, mock_tts):
        """Test /say (Voice)"""
        update, context = self.create_mocks("/say", args=["hello"])
        mock_instance = AsyncMock()
        mock_tts.return_value = mock_instance
        
        # Mock file IO
        with patch('builtins.open', MagicMock()), \
             patch('os.path.exists', return_value=True), \
             patch('os.remove', MagicMock()):
            
            await self.agent.handle_speak(update, context)
            
        mock_instance.save.assert_called()
        update.message.reply_voice.assert_called()
        print("✅ /say Verified")

    async def test_cmd_calendar(self):
        """Test /calendar (Life)"""
        update, context = self.create_mocks("/calendar")
        await self.agent.handle_calendar(update, context)
        update.message.reply_text.assert_called()
        args = update.message.reply_text.call_args[0][0]
        self.assertIn("Calendar (Mock)", args)
        print("✅ /calendar Verified")

    async def test_proactive_briefing(self):
        """Test Morning Briefing Task"""
        _, context = self.create_mocks()
        await self.agent.send_briefing(context)
        context.bot.send_message.assert_called()
        msg = context.bot.send_message.call_args[1]['text'] # kwargs: text=...
        self.assertIn("Good Morning", msg)
        print("✅ Morning Briefing Verified")

if __name__ == '__main__':
    unittest.main()
