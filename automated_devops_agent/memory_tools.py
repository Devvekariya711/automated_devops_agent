"""
Phase 5: Memory & Sessions Tools

Enables persistent context and learning across agent sessions.
"""

import json
import os
from pathlib import Path
from datetime import datetime


def read_project_memory() -> str:
    """
    Read project context from persistent memory file.
    
    Returns project-specific learnings, preferences, and context
    that persist across agent sessions.
    """
    memory_file = Path("config/project_context.json")
    
    if not memory_file.exists():
        return "No project memory found. Starting fresh session."
    
    try:
        with open(memory_file, 'r', encoding='utf-8') as f:
            context = json.load(f)
        
        output = "===== PROJECT MEMORY =====\n"
        output += f"Project: {context.get('project_name', 'Unknown')}\n"
        output += f"Last Updated: {context.get('last_updated', 'Never')}\n\n"
        
        if context.get('tech_stack'):
            output += "Tech Stack: " + ", ".join(context['tech_stack']) + "\n\n"
        
        if context.get('key_files'):
            output += "Key Files:\n"
            for file, desc in context['key_files'].items():
                output += f"  - {file}: {desc}\n"
            output += "\n"
        
        if context.get('learnings'):
            output += "Recent Learnings (last 5):\n"
            for learning in context['learnings'][-5:]:
                cat = learning.get('category', 'general')
                desc = learning.get('description', '')
                sol = learning.get('solution', '')
                output += f"  - [{cat}] {desc}"
                if sol:
                    output += f" → {sol}"
                output += "\n"
            output += "\n"
        
        if context.get('preferences'):
            output += "Preferences:\n"
            for key, value in context['preferences'].items():
                output += f"  - {key}: {value}\n"
        
        output += "=" * 50 + "\n"
        return output
        
    except Exception as e:
        return f"Error reading project memory: {str(e)}"


def update_project_memory(
    category: str,
    description: str,
    solution: str = ""
) -> str:
    """
    Add a learning to project memory for cross-session persistence.
    
    This enables agents to build cumulative knowledge about:
    - Bug fixes and solutions
    - Code patterns discovered
    - User preferences
    - Project-specific conventions
    
    Args:
        category: Type of learning (bug_fix, pattern, preference, refactoring)
        description: What was learned or discovered
        solution: How it was resolved (optional)
    """
    memory_file = Path("config/project_context.json")
    
    try:
        # Load existing or create new
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                context = json.load(f)
        else:
            context = {
                "project_name": "automated_devops_agent",
                "tech_stack": ["Python", "Google ADK", "pytest"],
                "key_files": {
                    "agent.py": "Root orchestrator agent",
                    "supporting_agents.py": "Specialist agents",
                    "tools.py": "All agent tools"
                },
                "learnings": [],
                "preferences": {
                   "max_retries": 5,
                    "test_framework": "pytest",
                    "linter": "pylint"
                }
            }
        
        # Add new learning
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "description": description
        }
        
        if solution:
            learning_entry["solution"] = solution
        
        context["learnings"].append(learning_entry)
        context["last_updated"] = datetime.now().isoformat()
        
        # Save
        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(context, f, indent=2)
        
        return f"✅ Memory updated: {description}"
        
    except Exception as e:
        return f"Error updating memory: {str(e)}"


# Create tool wrappers
from google.adk.tools import FunctionTool

read_memory_tool = FunctionTool(func=read_project_memory)
update_memory_tool = FunctionTool(func=update_project_memory)
