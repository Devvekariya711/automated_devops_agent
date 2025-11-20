# Contributing to Automated DevOps Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/automated-devops-agent.git
   cd automated-devops-agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies (including dev tools)**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"  # Install with dev dependencies from pyproject.toml
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your GOOGLE_API_KEY to .env
   ```

## 📝 Code Style

### Python Style Guide

- Follow **PEP 8** conventions
- Use **type hints** where applicable
- Maximum line length: **100 characters**
- Use **docstrings** for all functions and classes

### Formatting Tools

We use `black` for code formatting:

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .
```

### Linting

Run `flake8` to check for common issues:

```bash
flake8 devops_automator/ --max-line-length=100
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest target_code/ -v

# Run with coverage
pytest target_code/ --cov=devops_automator --cov-report=html

# Run specific test file
python target_code/test_agent.py
```

### Writing Tests

- Place tests in the `target_code/` directory
- Name test files: `test_*.py` or `*_test.py`
- Use descriptive test names: `test_<what>_<when>_<expected>`

Example:
```python
def test_agent_routing_redirects_to_security_scanner():
    """Test that security requests route to security_scanner agent"""
    # Test implementation
```

## 🔧 Making Changes

### Branch Naming

- Feature: `feature/your-feature-name`
- Bug fix: `fix/bug-description`
- Documentation: `docs/description`

### Commit Messages

Use clear, descriptive commit messages:

```
<type>: <short summary>

<optional detailed description>

<optional footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes (formatting)
- `chore`: Maintenance tasks

Examples:
```
feat: Add tool for executing shell commands

fix: Prevent path traversal in file reader tool

docs: Update README with installation instructions
```

## 🎯 Adding New Features

### Adding a New Agent

1. Define the agent in `devops_automator/supporting_agents.py`:
   ```python
   new_agent = Agent(
       name="agent_name",
       model=MODEL_NAME,
       description="Brief description",
       instruction="Detailed instructions",
       tools=[...]
   )
   ```

2. Register it in `devops_automator/agent.py`:
   ```python
   sub_agents=[..., new_agent]
   ```

3. Update root agent instructions for routing

4. Add tests in `target_code/`

### Adding a New Tool

1. Create function in `devops_automator/tools.py`:
   ```python
   def my_tool(param: str) -> str:
       """Docstring with description, args, and returns"""
       # Implementation
       return result
   
   my_tool_instance = FunctionTool(func=my_tool)
   ```

2. Import and add to agent's tools list

3. Write tests for the tool

## 📤 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG** (if applicable)
5. **Create pull request** with:
   - Clear title describing the change
   - Description of what changed and why
   - Any breaking changes noted
   - Link to related issues

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages are clear

## 🐛 Reporting Bugs

### Before Submitting

- Check existing issues to avoid duplicates
- Verify the bug with the latest version

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. ...
2. ...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 11]
- Python version: [e.g., 3.11]
- ADK version: [e.g., 0.1.0]

**Additional Context**
Any other relevant information
```

## 💡 Feature Requests

Feature requests are welcome! Please:
- Describe the feature and use case
- Explain why it would be valuable
- Provide examples if possible

## ❓ Questions

For questions:
1. Check the README and documentation first
2. Search existing issues
3. Open a new issue with the "question" label

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the project

## 🙏 Thank You

Your contributions make this project better for everyone!
