"""
🚀 BANKOO AI - ULTIMATE SETUP WIZARD
PyQt GUI matching HTML design exactly - Beautiful + Functional!

Complete Features:
- API Key Setup (6 providers with guidance)
- 16 AI Council Agents
- 12 Brain Modules
- 23 Language Voices
- Deep Preferences
- Auto .env & config generation
- One-time complete setup

Author: Bankoo Team
Version: 2.0 Ultimate
"""

import sys
import os
import json
import webbrowser
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# === STYLES (Matching HTML) ===
STYLE_ULTIMATE = """
QMainWindow, QDialog {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0a0e27, stop:0.5 #1a1d3a, stop:1 #0f1628);
}

QLabel {
    color: #ffffff;
}

QLabel[heading="true"] {
    color: #00d4ff;
    font-size: 32pt;
    font-weight: bold;
}

QLabel[subtitle="true"] {
    color: rgba(255, 255, 255, 150);
    font-size: 14pt;
}

QLabel[cardTitle="true"] {
    color: #00d4ff;
    font-size: 18pt;
    font-weight: 600;
}

/* Cards */
QFrame[card="true"] {
    background: rgba(255, 255, 255, 15);
    border: 2px solid rgba(0, 212, 255, 77);
    border-radius: 20px;
    padding: 20px;
}

QFrame[card="true"]:hover {
    background: rgba(255, 255, 255, 20);
    border: 2px solid rgba(0, 212, 255, 153);
}

/* API Provider Cards */
QFrame[apiCard="true"] {
    background: rgba(0, 0, 0, 77);
    border: 2px solid rgba(0, 212, 255, 51);
    border-radius: 15px;
    padding: 15px;
}

/* Input Fields */
QLineEdit {
    background: rgba(0, 0, 0, 128);
    border: 2px solid rgba(0, 212, 255, 77);
    border-radius: 10px;
    color: #ffffff;
    padding: 12px;
    font-size: 11pt;
    min-height: 35px;
}

QLineEdit:focus {
    border: 2px solid rgba(0, 212, 255, 204);
}

/* Buttons */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #00d4ff, stop:0.5 #7b2ff7, stop:1 #ff006e);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 14px 28px;
    font-size: 13pt;
    font-weight: bold;
    min-height: 45px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #00b8e6, stop:0.5 #6a28d9, stop:1 #e6005c);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #009cc7, stop:0.5 #5a1fb8, stop:1 #cc0052);
}

QPushButton[secondary="true"] {
    background: rgba(255, 255, 255, 25);
    color: rgba(255, 255, 255, 204);
    border: 2px solid rgba(255, 255, 255, 51);
}

QPushButton[link="true"] {
    background: transparent;
    border: 2px solid rgba(0, 212, 255, 128);
    color: #00d4ff;
    padding: 10px 20px;
    min-height: 35px;
}

/* ComboBox */
QComboBox {
    background: rgba(0, 0, 0, 128);
    border: 2px solid rgba(0, 212, 255, 77);
    border-radius: 10px;
    color: #ffffff;
    padding: 12px;
    font-size: 11pt;
    min-height: 40px;
}

QComboBox:hover {
    border: 2px solid rgba(0, 212, 255, 153);
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border: 5px solid transparent;
    border-top: 5px solid #00d4ff;
}

QComboBox QAbstractItemView {
    background: #1a1d3a;
    color: white;
    selection-background-color: #00d4ff;
}

/* CheckBox */
QCheckBox {
    color: #ffffff;
    font-size: 12pt;
    spacing: 10px;
}

QCheckBox::indicator {
    width: 24px;
    height: 24px;
    border-radius: 6px;
    border: 2px solid rgba(0, 212, 255, 128);
    background: rgba(0, 0, 0, 128);
}

QCheckBox::indicator:checked {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #00d4ff, stop:1 #7b2ff7);
    border: 2px solid #00d4ff;
}

QCheckBox::indicator:hover {
    border: 2px solid rgba(0, 212, 255, 204);
}

/* ScrollArea */
QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:vertical {
    background: rgba(0, 0, 0, 128);
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: rgba(0, 212, 255, 128);
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(0, 212, 255, 204);
}

/* Badges */
QLabel[badge="free"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #00ff88, stop:1 #00d4ff);
    color: #000000;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 9pt;
    font-weight: bold;
}

QLabel[badge="paid"] {
    background: #ff006e;
    color: #ffffff;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 9pt;
    font-weight: bold;
}
"""


# === DATA ===
API_PROVIDERS = {
    "Groq": {
        "url": "https://console.groq.com/",
        "free": True,
        "info": "Ultra-fast (600+ tokens/sec) • 14,400 requests/day free",
        "key": "GROQ_API_KEY"
    },
    "Cerebras": {
        "url": "https://cloud.cerebras.ai/",
        "free": True,
        "info": "Fastest inference available • Generous free tier",
        "key": "CEREBRAS_API_KEY"
    },
    "DeepSeek": {
        "url": "https://platform.deepseek.com/",
        "free": False,
        "info": "SOTA Coding Model • $0.27/1M tokens (very cheap)",
        "key": "DEEPSEEK_API_KEY"
    },
    "Gemini": {
        "url": "https://makersuite.google.com/app/apikey",
        "free": True,
        "info": "60 requests/min free • Multimodal capabilities",
        "key": "GEMINI_API_KEY"
    },
    "OpenRouter": {
        "url": "https://openrouter.ai/",
        "free": False,
        "info": "100+ models • GPT-4, Claude, etc. • Pay-per-use",
        "key": "OPENROUTER_API_KEY"
    },
    "OpenAI": {
        "url": "https://platform.openai.com/api-keys",
        "free": False,
        "info": "GPT-4 Turbo • $10-30/1M tokens • Industry standard",
        "key": "OPENAI_API_KEY"
    }
}

COUNCIL_AGENTS = {
    "Executive Leadership": [
        ("CEO", "Chief Executive Officer (Decision Maker)"),
        ("CTO", "Chief Technology Officer (Architecture)"),
        ("CSO", "Chief Strategy Officer (Planning)"),
        ("CISO", "Chief Security Officer"),
        ("CDO", "Chief Design Officer (Visual Design)"),
        ("CCO", "Chief Communications Officer"),
        ("CRO", "Chief Risk Officer (Code Review)")
    ],
    "Engineering Team": [
        ("VP Engineering", "Complex Logic"),
        ("Chief Scientist", "Math & Deep Logic"),
        ("QA Lead", "Quality Assurance"),
        ("Principal Engineer", "Debugging"),
        ("Senior Engineer", "Fast Features"),
        ("Data Architect", "Database Expert"),
        ("Platform Architect", "API & Systems"),
        ("Performance Engineer", "Optimization"),
        ("Technical Writer", "Documentation")
    ]
}

BRAIN_MODULES = {
    "Core": [("Assistant Brain", "Required", True), ("Memory Brain", "Persistence", False)],
    "Analysis": [
        ("Vision Brain", "Image Analysis", False),
        ("YouTube Brain", "Video Analysis", False),
        ("Doc Brain", "PDF Processing", False),
        ("Analytics Brain", "Data Analysis", False)
    ],
    "Automation": [
        ("Scraper Brain", "Web Scraping", False),
        ("OWL Brain", "Task Execution", False)
    ],
    "Advanced": [
        ("AirLLM Brain", "Local AI Models", False),
        ("Smart Notes", "Note-taking", False),
        ("Civitai Brain", "AI Art", False)
    ]
}

LANGUAGES = {
    "Indian": ["Gujarati", "Hindi", "Tamil", "Telugu", "Marathi", "Bengali"],
    "European": ["English (US)", "English (UK)", "Spanish", "French", "German", 
                 "Italian", "Portuguese", "Russian", "Dutch", "Polish", "Turkish"],
    "Asian": ["Chinese", "Japanese", "Korean", "Arabic", "Thai", "Vietnamese"]
}


class UltimateSetupWizard(QWizard):
    """Ultimate Setup Wizard matching HTML design"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("🧠 Bankoo AI - Ultimate Setup")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(STYLE_ULTIMATE)
        
        # Store configuration
        self.config = {
            "api_keys": {},
            "agents": {},
            "modules": {},
            "voice": {},
            "preferences": {}
        }
        
        # Add pages
        self.addPage(WelcomePage())
        self.addPage(APIKeysPage())
        self.addPage(AgentsPage())
        self.addPage(ModulesPage())
        self.addPage(VoicePage())
        self.addPage(PreferencesPage())
        self.addPage(CompletePage())
        
    def accept(self):
        """Save configuration and finish"""
        self.save_configuration()
        super().accept()
        
    def save_configuration(self):
        """Save all configs to files"""
        base_path = Path(__file__).parent.parent
        
        # Save .env file
        env_content = ""
        for key, value in self.config["api_keys"].items():
            if value:
                env_content += f"{key}={value}\n"
        
        env_path = base_path / ".env"
        with open(env_path, "w") as f:
            f.write(env_content)
        
        # Save JSON config
        config_path = base_path / "installer_config.json"
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=2)
        
        print(f"✅ Saved configuration to {env_path} and {config_path}")


class WelcomePage(QWizardPage):
    """Welcome page matching HTML"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("")
        
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Title
        title = QLabel("🧠 BANKOO AI")
        title.setProperty("heading", True)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Ultimate Professional Setup Wizard")
        subtitle.setProperty("subtitle", True)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16pt; color: rgba(255,255,255,180); padding-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # What you'll configure card
        config_card = self.create_card("🎯 What You'll Configure", [
            "API Keys for 6+ providers (with free options)",
            "16 AI Council Agents selection",
            "12 Brain Modules selection",
            "23 Language voices",
            "Deep preferences & customization"
        ])
        layout.addWidget(config_card)
        
        # Recommended setup card
        rec_card = QFrame()
        rec_card.setProperty("card", True)
        rec_layout = QVBoxLayout()
        
        rec_title = QLabel("💡 Recommended Setup")
        rec_title.setProperty("cardTitle", True)
        rec_layout.addWidget(rec_title)
        
        rec_text = QLabel(
            "<b style='color: #00ff88;'>Free Option:</b> Groq + Cerebras + Gemini (100% free)<br>"
            "<b style='color: #00d4ff;'>Best Value:</b> Add DeepSeek ($0.27/1M) for SOTA coding<br>"
            "<b style='color: #ff006e;'>Full Power:</b> All providers including GPT-4"
        )
        rec_text.setWordWrap(True)
        rec_text.setStyleSheet("font-size: 11pt; line-height: 1.8; padding: 10px;")
        rec_layout.addWidget(rec_text)
        
        rec_card.setLayout(rec_layout)
        layout.addWidget(rec_card)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def create_card(self, title, items):
        """Create a feature card"""
        card = QFrame()
        card.setProperty("card", True)
        card_layout = QVBoxLayout()
        
        card_title = QLabel(title)
        card_title.setProperty("cardTitle", True)
        card_layout.addWidget(card_title)
        
        for item in items:
            item_label = QLabel(f"✅ {item}")
            item_label.setStyleSheet("font-size: 11pt; padding: 6px 0;")
            card_layout.addWidget(item_label)
        
        card.setLayout(card_layout)
        return card


class APIKeysPage(QWizardPage):
    """API Keys page with providers"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 30, 50, 30)
        
        # Title
        title = QLabel("Configure API Keys")
        title.setProperty("heading", True)
        title.setStyleSheet("font-size: 28pt;")
        layout.addWidget(title)
        
        subtitle = QLabel("Get your free API keys - we'll guide you through each one")
        subtitle.setProperty("subtitle", True)
        subtitle.setStyleSheet("padding-bottom: 15px;")
        layout.addWidget(subtitle)
        
        # Scroll area for providers
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        
        # Store input fields
        self.key_inputs = {}
        
        # Add each provider
        for provider_name, provider_info in API_PROVIDERS.items():
            provider_widget = self.create_provider_card(provider_name, provider_info)
            content_layout.addWidget(provider_widget)
        
        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
    
    def create_provider_card(self, name, info):
        """Create provider card"""
        card = QFrame()
        card.setProperty("apiCard", True)
        card_layout = QVBoxLayout()
        card_layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        
        provider_label = QLabel(f"{'⚡' if info['free'] else '💎'} {name}")
        provider_label.setStyleSheet("font-size: 16pt; font-weight: 600;")
        header_layout.addWidget(provider_label)
        
        header_layout.addStretch()
        
        badge = QLabel("FREE" if info["free"] else "PAID")
        badge.setProperty("badge", "free" if info["free"] else "paid")
        badge.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(badge)
        
        card_layout.addLayout(header_layout)
        
        # Info
        info_label = QLabel(info["info"])
        info_label.setStyleSheet("color: rgba(255,255,255,150); font-size: 10pt;")
        info_label.setWordWrap(True)
        card_layout.addWidget(info_label)
        
        # Input row
        input_layout = QHBoxLayout()
        
        key_input = QLineEdit()
        key_input.setPlaceholderText(f"Paste your {name} API key")
        key_input.setEchoMode(QLineEdit.Password)
        self.key_inputs[info["key"]] = key_input
        input_layout.addWidget(key_input, stretch=4)
        
        get_key_btn = QPushButton("Get Key")
        get_key_btn.setProperty("link", True)
        get_key_btn.clicked.connect(lambda: webbrowser.open(info["url"]))
        get_key_btn.setMaximumWidth(120)
        input_layout.addWidget(get_key_btn)
        
        card_layout.addLayout(input_layout)
        
        card.setLayout(card_layout)
        return card
    
    def validatePage(self):
        """Save API keys"""
        wizard = self.wizard()
        for key_name, input_field in self.key_inputs.items():
            wizard.config["api_keys"][key_name] = input_field.text()
        return True


class AgentsPage(QWizardPage):
    """AI Agents selection page"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 30, 50, 30)
        
        title = QLabel("Select AI Council Agents")
        title.setProperty("heading", True)
        title.setStyleSheet("font-size: 28pt;")
        layout.addWidget(title)
        
        subtitle = QLabel("Choose which expert agents to enable (recommended: all)")
        subtitle.setProperty("subtitle", True)
        layout.addWidget(subtitle)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        
        self.agent_checkboxes = {}
        
        for category, agents in COUNCIL_AGENTS.items():
            card = self.create_agent_card(category, agents)
            content_layout.addWidget(card)
        
        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
    
    def create_agent_card(self, category, agents):
        """Create agent category card"""
        card = QFrame()
        card.setProperty("card", True)
        card_layout = QVBoxLayout()
        
        title = QLabel(f"{'👔' if 'Executive' in category else '👨‍💻'} {category}")
        title.setProperty("cardTitle", True)
        card_layout.addWidget(title)
        
        # Grid of checkboxes
        grid = QGridLayout()
        grid.setSpacing(15)
        
        for i, (agent_name, agent_desc) in enumerate(agents):
            row = i // 3
            col = i % 3
            
            checkbox = QCheckBox(f"{agent_name}\n{agent_desc}")
            checkbox.setChecked(True)
            checkbox.setStyleSheet("padding: 10px;")
            self.agent_checkboxes[agent_name] = checkbox
            grid.addWidget(checkbox, row, col)
        
        card_layout.addLayout(grid)
        card.setLayout(card_layout)
        return card
    
    def validatePage(self):
        """Save agent selections"""
        wizard = self.wizard()
        for agent_name, checkbox in self.agent_checkboxes.items():
            wizard.config["agents"][agent_name] = checkbox.isChecked()
        return True


class ModulesPage(QWizardPage):
    """Brain Modules selection"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 30, 50, 30)
        
        title = QLabel("Select Brain Modules")
        title.setProperty("heading", True)
        title.setStyleSheet("font-size: 28pt;")
        layout.addWidget(title)
        
        subtitle = QLabel("Choose which capabilities to enable")
        subtitle.setProperty("subtitle", True)
        layout.addWidget(subtitle)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)
        
        self.module_checkboxes = {}
        
        for category, modules in BRAIN_MODULES.items():
            card = self.create_module_card(category, modules)
            content_layout.addWidget(card)
        
        content.setLayout(content_layout)
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
    
    def create_module_card(self, category, modules):
        """Create module category card"""
        card = QFrame()
        card.setProperty("card", True)
        card_layout = QVBoxLayout()
        
        title = QLabel(f"{'🧠' if category == 'Core' else '📊' if category == 'Analysis' else '🤖' if category == 'Automation' else '🚀'} {category} Modules")
        title.setProperty("cardTitle", True)
        card_layout.addWidget(title)
        
        grid = QGridLayout()
        grid.setSpacing(15)
        
        for i, (module_name, module_desc, required) in enumerate(modules):
            row = i // 3
            col = i % 3
            
            checkbox = QCheckBox(f"{module_name}\n{module_desc}")
            checkbox.setChecked(True)
            if required:
                checkbox.setEnabled(False)
            checkbox.setStyleSheet("padding: 10px;")
            self.module_checkboxes[module_name] = checkbox
            grid.addWidget(checkbox, row, col)
        
        card_layout.addLayout(grid)
        card.setLayout(card_layout)
        return card
    
    def validatePage(self):
        """Save module selections"""
        wizard = self.wizard()
        for module_name, checkbox in self.module_checkboxes.items():
            wizard.config["modules"][module_name] = checkbox.isChecked()
        return True


class VoicePage(QWizardPage):
    """Voice configuration"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("")
        
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(50, 30, 50, 30)
        
        title = QLabel("Voice Configuration")
        title.setProperty("heading", True)
        title.setStyleSheet("font-size: 28pt;")
        layout.addWidget(title)
        
        subtitle = QLabel("Select default language and voice preferences")
        subtitle.setProperty("subtitle", True)
        layout.addWidget(subtitle)
        
        card = QFrame()
        card.setProperty("card", True)
        card_layout = QVBoxLayout()
        card_layout.setSpacing(20)
        
        # Language
        lang_label = QLabel("🎤 Default Voice Language")
        lang_label.setProperty("cardTitle", True)
        card_layout.addWidget(lang_label)
        
        self.lang_combo = QComboBox()
        for category, langs in LANGUAGES.items():
            for lang in langs:
                self.lang_combo.addItem(lang)
        card_layout.addWidget(self.lang_combo)
        
        # Gender
        gender_label = QLabel("🎙️ Voice Gender")
        gender_label.setProperty("cardTitle", True)
        card_layout.addWidget(gender_label)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female"])
        card_layout.addWidget(self.gender_combo)
        
        # Auto switch
        self.auto_switch = QCheckBox("Enable Auto Voice Switching")
        self.auto_switch.setChecked(True)
        self.auto_switch.setStyleSheet("font-size: 12pt; padding: 15px;")
        card_layout.addWidget(self.auto_switch)
        
        auto_desc = QLabel("Automatically use native voice when you say 'speak in Spanish', etc.")
        auto_desc.setStyleSheet("color: rgba(255,255,255,120); font-size: 10pt; padding-left: 40px;")
        card_layout.addWidget(auto_desc)
        
        card.setLayout(card_layout)
        layout.addWidget(card)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def validatePage(self):
        """Save voice config"""
        wizard = self.wizard()
        wizard.config["voice"] = {
            "default_language": self.lang_combo.currentText(),
            "gender": self.gender_combo.currentText(),
            "auto_switch": self.auto_switch.isChecked()
        }
        return True


class PreferencesPage(QWizardPage):
    """Additional preferences"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("")
        
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(50, 30, 50, 30)
        
        title = QLabel("Additional Preferences")
        title.setProperty("heading", True)
        title.setStyleSheet("font-size: 28pt;")
        layout.addWidget(title)
        
        subtitle = QLabel("Fine-tune your Bankoo AI experience")
        subtitle.setProperty("subtitle", True)
        layout.addWidget(subtitle)
        
        # Theme card
        theme_card = QFrame()
        theme_card.setProperty("card", True)
        theme_layout = QVBoxLayout()
        
        theme_label = QLabel("🎨 UI Theme")
        theme_label.setProperty("cardTitle", True)
        theme_layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark (Default)", "Light", "Cyberpunk"])
        theme_layout.addWidget(self.theme_combo)
        
        theme_card.setLayout(theme_layout)
        layout.addWidget(theme_card)
        
        # Models card
        models_card = QFrame()
        models_card.setProperty("card", True)
        models_layout = QVBoxLayout()
        models_layout.setSpacing(15)
        
        models_label = QLabel("🤖 AI Model Assignments")
        models_label.setProperty("cardTitle", True)
        models_layout.addWidget(models_label)
        
        primary_label = QLabel("Primary Chat Model")
        primary_label.setStyleSheet("color: rgba(255,255,255,200); padding-top: 10px;")
        models_layout.addWidget(primary_label)
        
        self.primary_combo = QComboBox()
        self.primary_combo.addItems([
            "Llama 3.3 70B (Cerebras)",
            "Llama 3.3 70B (Groq)",
            "DeepSeek Chat V3"
        ])
        models_layout.addWidget(self.primary_combo)
        
        coding_label = QLabel("Coding Model")
        coding_label.setStyleSheet("color: rgba(255,255,255,200); padding-top: 10px;")
        models_layout.addWidget(coding_label)
        
        self.coding_combo = QComboBox()
        self.coding_combo.addItems([
            "DeepSeek Chat V3 (SOTA)",
            "Llama 3.3 70B"
        ])
        models_layout.addWidget(self.coding_combo)
        
        models_card.setLayout(models_layout)
        layout.addWidget(models_card)
        
        # Features card
        features_card = QFrame()
        features_card.setProperty("card", True)
        features_layout = QVBoxLayout()
        
        features_label = QLabel("⚙️ Features")
        features_label.setProperty("cardTitle", True)
        features_layout.addWidget(features_label)
        
        self.animations_cb = QCheckBox("Enable UI Animations")
        self.animations_cb.setChecked(True)
        features_layout.addWidget(self.animations_cb)
        
        self.typing_cb = QCheckBox("Show Typing Indicator")
        self.typing_cb.setChecked(True)
        features_layout.addWidget(self.typing_cb)
        
        self.council_cb = QCheckBox("Enable AI Council")
        self.council_cb.setChecked(True)
        features_layout.addWidget(self.council_cb)
        
        features_card.setLayout(features_layout)
        layout.addWidget(features_card)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def validatePage(self):
        """Save preferences"""
        wizard = self.wizard()
        wizard.config["preferences"] = {
            "ui_theme": self.theme_combo.currentText(),
            "primary_model": self.primary_combo.currentText(),
            "coding_model": self.coding_combo.currentText(),
            "animations": self.animations_cb.isChecked(),
            "typing_indicator": self.typing_cb.isChecked(),
            "ai_council": self.council_cb.isChecked()
        }
        return True


class CompletePage(QWizardPage):
    """Completion page"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("")
        
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Success icon
        success = QLabel("🎉")
        success.setAlignment(Qt.AlignCenter)
        success.setStyleSheet("font-size: 90pt;")
        layout.addWidget(success)
        
        # Title
        title = QLabel("Setup Complete!")
        title.setProperty("heading", True)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Your configuration has been saved")
        subtitle.setProperty("subtitle", True)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Summary card
        summary_card = QFrame()
        summary_card.setProperty("card", True)
        summary_layout = QVBoxLayout()
        
        summary_title = QLabel("✅ Configuration Summary")
        summary_title.setProperty("cardTitle", True)
        summary_layout.addWidget(summary_title)
        
        self.summary_text = QLabel()
        self.summary_text.setStyleSheet("font-size: 12pt; line-height: 1.8; padding: 15px;")
        self.summary_text.setWordWrap(True)
        summary_layout.addWidget(self.summary_text)
        
        summary_card.setLayout(summary_layout)
        layout.addWidget(summary_card)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def initializePage(self):
        """Display summary"""
        wizard = self.wizard()
        config = wizard.config
        
        key_count = sum(1 for v in config["api_keys"].values() if v)
        agent_count = sum(1 for v in config["agents"].values() if v)
        module_count = sum(1 for v in config["modules"].values() if v)
        
        summary = f"""
        ✅ {key_count} API key(s) configured<br>
        ✅ {agent_count} AI agents enabled<br>
        ✅ {module_count} brain modules enabled<br>
        ✅ Voice: {config["voice"]["default_language"]} ({config["voice"]["gender"]})<br>
        ✅ Primary model: {config["preferences"]["primary_model"]}<br>
        ✅ Coding model: {config["preferences"]["coding_model"]}<br>
        ✅ UI theme: {config["preferences"]["ui_theme"]}
        """
        
        self.summary_text.setText(summary)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    wizard = UltimateSetupWizard()
    wizard.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
