# Bankoo AI Installer

Professional GUI installer for easy Bankoo AI setup.

## Features

- ✅ **Auto-detect Python** - Verifies Python installation
- ✅ **One-click dependency install** - Installs all 40+ packages with progress tracking
- ✅ **API key wizard** - Easy configuration of AI service keys
- ✅ **Connection testing** - Validates API keys work
- ✅ **Auto-launch** - Opens Bankoo after setup

## Usage

### For End Users

**Double-click:** `SETUP.bat`

That's it! The wizard will guide you through the rest.

### Manual Launch

```bash
python installer/setup_wizard.py
```

## Wizard Pages

1. **Welcome** - Introduction and features overview
2. **System Check** - Verify Python and pip installation
3. **Dependencies** - Install all required packages
4. **API Keys** - Configure AI service credentials
5. **Complete** - Launch Bankoo

## Screenshots

![Setup Wizard](../screenshots/setup-wizard.png)

## Technical Details

### Technology Stack

- **PyQt5** - Modern GUI framework
- **Threading** - Non-blocking installation
- **Subprocess** - Package management

### File Structure

```
installer/
├── setup_wizard.py      # Main wizard application
├── README.md           # This file
└── assets/            # Icons and images (future)
```

## Building Standalone Installer

To create a standalone `.exe` installer:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "BankooSetup" installer/setup_wizard.py

# Output will be in dist/BankooSetup.exe
```

### Advanced: Inno Setup

For a professional Windows installer with uninstaller:

1. Install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Create `installer_config.iss` script
3. Compile to create `BankooInstaller.exe`

## Customization

### Change Colors

Edit the `setStyleSheet` in `BankooSetupWizard.__init__()`:

```python
QPushButton {
    background-color: #00d4ff;  # Change this color
}
```

### Add Logo

1. Add logo image to `installer/assets/logo.png`
2. Update `WelcomePage` to display it:

```python
logo = QLabel()
logo.setPixmap(QPixmap("installer/assets/logo.png"))
layout.addWidget(logo)
```

## Troubleshooting

### "PyQt5 not found"

The wizard auto-installs PyQt5, but if it fails:

```bash
pip install PyQt5
```

### "requirements.txt not found"

Make sure you run from the project root directory.

### Installation fails

Check the log in the wizard for specific package errors.

## Future Enhancements

- [ ] Progress animation with custom graphics
- [ ] Dark mode support
- [ ] Multi-language support
- [ ] Automatic updates checker
- [ ] Uninstaller
- [ ] Desktop shortcut creation
- [ ] Start menu integration

---

**Made with ❤️ by the Bankoo Team**
