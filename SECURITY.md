
# Security Policy
## 🔒 Reporting a Vulnerability
We take security seriously. If you discover a security vulnerability in the Automated DevOps Agent, please report it responsibly.
### How to Report
**Option 1: Private Security Advisory** (Preferred)
1. Go to [Security Advisories](https://github.com/Devvekariya711/automated_devops_agent/security/advisories)
2. Click "Report a vulnerability"
3. Fill in the details
4. Submit privately
**Option 2: Email**
- Email: devvekariya711@gmail.com
- Subject: "SECURITY: [Brief Description]"
- Include:
  - Description of the vulnerability
  - Steps to reproduce
  - Potential impact
  - Suggested fix (if any)
### ⚠️ Please Do NOT:
- ❌ Open public GitHub issues for security bugs
- ❌ Disclose the vulnerability publicly before we've had a chance to fix it
- ❌ Test the vulnerability on production systems
### Response Timeline
- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity (critical: < 7 days, high: < 30 days)
---
## 🛡️ Supported Versions
We currently support the following versions with security updates:
| Version | Supported          | Status    |
| ------- | ------------------ | --------- |
| 1.0.x   | :white_check_mark: | Active    |
| < 1.0   | :x:                | Deprecated|
---
## ⚙️ Security Considerations
### Code Execution Risks
**⚠️ CRITICAL**: This agent executes generated code via pytest and shell commands.
**Potential Risks:**
1. **Arbitrary Code Execution**: The debugging agent can write and run Python code
2. **File System Access**: Agents can read/write files in the project directory
3. **Network Requests**: The `google_search_tool` makes external HTTP requests
4. **Shell Commands**: The `shell_executor_tool` runs system commands
### Safe Usage Guidelines
#### ✅ DO:
- Run in **isolated Virtual Machines** (VirtualBox, VMware, etc.)
- Use **Docker containers** with resource limits
- Run in **WSL2** with limited permissions (Windows users)
- Use **Python virtual environments**
- Keep **git** for instant rollback
- Review code before running autonomous fixes
- Set environment variable limits (e.g., max file size)
- Monitor resource usage
#### ❌ DON'T:
- Run on production servers
- Give elevated privileges (sudo/admin)
- Run on systems with sensitive data
- Allow access outside project directory
- Run on corporate networks without approval
- Execute on untrusted/unknown code
- Use your primary development machine without VM
