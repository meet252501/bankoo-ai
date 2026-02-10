# Security Policy

## 🔒 Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## 🚨 Reporting a Vulnerability

We take the security of Bankoo AI seriously. If you discover a security vulnerability, please follow these steps:

### 1. **DO NOT** Open a Public Issue

Security vulnerabilities should not be disclosed publicly until a fix is available.

### 2. Report Privately

Send an email to: **security@bankoo-ai.com** (or your email)

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: 30-90 days

### 4. Disclosure Policy

- We will acknowledge your report within 48 hours
- We will provide regular updates on our progress
- We will notify you when the vulnerability is fixed
- We will publicly disclose the vulnerability after a fix is released
- We will credit you in the security advisory (unless you prefer to remain anonymous)

## 🛡️ Security Best Practices

### For Users

1. **API Keys**
   - Never commit API keys to version control
   - Use `.env` files (excluded by `.gitignore`)
   - Rotate keys regularly
   - Use environment-specific keys

2. **Dependencies**
   - Keep dependencies up to date
   - Run `pip install --upgrade -r requirements.txt` monthly
   - Monitor security advisories

3. **Network Security**
   - Use HTTPS for production deployments
   - Don't expose Flask debug mode in production
   - Use firewall rules to restrict access

4. **Data Privacy**
   - Don't share sensitive data in chat logs
   - Clear conversation history regularly
   - Use local deployment for sensitive work

### For Developers

1. **Code Review**
   - All PRs require review before merging
   - Security-sensitive changes require additional review
   - Use automated security scanning (Bandit, Safety)

2. **Input Validation**
   - Sanitize all user inputs
   - Use parameterized queries for databases
   - Validate file uploads

3. **Authentication**
   - Use secure session management
   - Implement rate limiting
   - Add CSRF protection

4. **Logging**
   - Don't log sensitive data (API keys, passwords)
   - Implement audit logging for security events
   - Monitor for suspicious activity

## 🔍 Known Security Considerations

### API Key Management

- API keys are stored in `.env` files
- Ensure `.env` is in `.gitignore`
- Never hardcode keys in source code

### Local Deployment

- Bankoo runs locally by default (localhost:5000)
- Not exposed to internet unless explicitly configured
- Use ngrok or similar for temporary external access

### Third-Party APIs

- We use: OpenAI, Google Gemini, Groq, TMDB
- Review their security policies
- Monitor API usage for anomalies

## 📋 Security Checklist

Before deploying:

- [ ] All API keys in `.env` (not in code)
- [ ] `.env` is in `.gitignore`
- [ ] Dependencies are up to date
- [ ] Debug mode is disabled
- [ ] HTTPS is enabled (for production)
- [ ] Firewall rules are configured
- [ ] Security headers are set
- [ ] Rate limiting is enabled

## 🏆 Hall of Fame

We recognize security researchers who responsibly disclose vulnerabilities:

<!-- List will be updated as vulnerabilities are reported and fixed -->

- _No vulnerabilities reported yet_

## 📞 Contact

- **Security Email**: security@bankoo-ai.com
- **General Issues**: [GitHub Issues](https://github.com/yourusername/bankoo-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/bankoo-ai/discussions)

---

**Thank you for helping keep Bankoo AI secure!** 🔒
