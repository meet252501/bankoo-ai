# Contributing to Bankoo AI

Thank you for your interest in contributing to Bankoo AI! 🎉

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/bankoo-ai.git`
3. **Create a branch**: `git checkout -b feature/amazing-feature`
4. **Make changes** and commit: `git commit -m 'Add amazing feature'`
5. **Push** to your fork: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

## 📋 Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env

# Add your API keys to .env
notepad .env

# Run in debug mode
DEBUG_START.bat
```

## 🎯 How to Contribute

### Reporting Bugs 🐛

Use [GitHub Issues](https://github.com/yourusername/bankoo-ai/issues) with:

- **Clear title** describing the bug
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **System info** (OS, Python version, browser)
- **Screenshots** if applicable

### Suggesting Features 💡

Open an issue with:

- **Feature description** - What should it do?
- **Use case** - Why is it needed?
- **Proposed solution** - How might it work?

### Code Contributions 💻

We welcome:

- Bug fixes
- New AI agents
- UI improvements
- Documentation updates
- Performance optimizations
- Test coverage

## 📝 Code Style

### Python

- Follow **PEP 8** style guide
- Use **meaningful variable names**
- Add **docstrings** to functions
- Keep functions **small and focused**
- Comment **complex logic**

Example:

```python
def process_user_query(query: str, context: dict) -> str:
    """
    Process user query with AI and return response.

    Args:
        query: User's input text
        context: Conversation context dictionary

    Returns:
        AI-generated response string
    """
    # Implementation here
    pass
```

### JavaScript

- Use **ES6+** syntax
- Prefer **const/let** over var
- Use **async/await** for promises
- Add **JSDoc comments**

### HTML/CSS

- Use **semantic HTML5** tags
- Follow **BEM naming** for CSS classes
- Keep styles **modular and reusable**

## 🧪 Testing

Before submitting:

- [ ] Code runs without errors
- [ ] Existing features still work
- [ ] New features have been tested
- [ ] No console errors in browser

Run tests:

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_assistant.py
```

## 📦 Pull Request Guidelines

### Good PR Checklist

- [ ] Descriptive title (e.g., "Add voice recognition for Spanish")
- [ ] Clear description of changes
- [ ] Links to related issues
- [ ] Screenshots for UI changes
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No merge conflicts

### PR Title Format

```
[Type] Brief description

Types:
- [Feature] - New functionality
- [Fix] - Bug fix
- [Docs] - Documentation only
- [Style] - Code style/formatting
- [Refactor] - Code restructuring
- [Test] - Adding tests
- [Chore] - Maintenance tasks
```

Example: `[Feature] Add German language support for voice input`

## 🌟 Areas We Need Help

### High Priority

- [ ] Linux/macOS compatibility
- [ ] Docker containerization
- [ ] More language support (Spanish, French, etc.)
- [ ] Mobile app development
- [ ] Performance optimization

### Medium Priority

- [ ] Additional AI agents (Finance, Health, Education)
- [ ] Plugin system architecture
- [ ] Advanced vision models
- [ ] Cloud deployment guides

### Low Priority

- [ ] UI themes (dark mode variations)
- [ ] Keyboard shortcuts
- [ ] Export/import settings
- [ ] Browser extension

## 🏆 Recognition

Contributors will be:

- Listed in README.md
- Mentioned in release notes
- Given credit in commit history
- Invited to join core team (for significant contributions)

## 📞 Questions?

- **Issues**: [GitHub Issues](https://github.com/yourusername/bankoo-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/bankoo-ai/discussions)
- **Email**: your.email@example.com

## 📜 Code of Conduct

Be respectful, inclusive, and professional. We're all here to build something amazing together!

---

**Thank you for contributing to Bankoo AI!** 🚀
