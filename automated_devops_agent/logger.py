"""
Phase 6: Observability - Structured Logging and Monitoring

Provides comprehensive logging, token tracking, cost estimation,
and performance monitoring for all agent operations.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional


class AgentLogger:
    """
    Structured JSON logger for agent actions.
    
    Logs to: logs/agent_activity.jsonl (one JSON object per line)
    Each line is a complete JSON object for easy parsing and analysis.
    """
    
    def __init__(self, log_file: str = "logs/agent_activity.jsonl"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True, parents=True)
        
        # Initialize token tracker
        self.token_tracker = TokenTracker()
    
    def log_agent_call(
        self,
        agent_name: str,
        action: str,
        input_text: str = "",
        output_text: str = "",
        tokens_used: int = 0,
        duration_ms: int = 0,
        status: str = "success"
    ) -> None:
        """
        Log a single agent interaction.
        
        Args:
            agent_name: Name of the agent (e.g., 'debugging_agent')
            action: Action performed (e.g., 'code_review', 'bug_fix')
            input_text: Input provided to agent
            output_text: Agent's response
            tokens_used: Estimated tokens consumed
            duration_ms: Execution time in milliseconds
            status: success, error, or warning
        """
        # Estimate tokens if not provided
        if tokens_used == 0 and (input_text or output_text):
            tokens_used = self._estimate_tokens(input_text, output_text)
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "action": action,
            "input_length": len(input_text),
            "output_length": len(output_text),
            "tokens_used": tokens_used,
            "duration_ms": duration_ms,
            "cost_usd": self.token_tracker.estimate_cost(tokens_used),
            "status": status
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
    
    def _estimate_tokens(self, input_text: str, output_text: str) -> int:
        """
        Rough token estimation (4 chars ≈ 1 token for English).
        For accurate tracking, use actual API response.
        """
        total_chars = len(input_text) + len(output_text)
        return total_chars // 4


class TokenTracker:
    """
    Track token usage and estimate costs.
    
    Uses Gemini 2.5 Flash pricing:
    - Input: $0.075 per 1M tokens
    - Output: $0.30 per 1M tokens
    """
    
    GEMINI_PRICING = {
        "gemini-2.5-flash-lite": {
            "input": 0.075 / 1_000_000,   # $0.075 per 1M tokens
            "output": 0.30 / 1_000_000     # $0.30 per 1M tokens
        }
    }
    
    def estimate_cost(
        self,
        tokens: int,
        model: str = "gemini-2.5-flash-lite",
        input_ratio: float = 0.7
    ) -> float:
        """
        Estimate cost for token usage.
        
        Args:
            tokens: Total tokens used
            model: Model name
            input_ratio: Percentage of tokens that are input (default 0.7)
        
        Returns:
            Estimated cost in USD
        """
        pricing = self.GEMINI_PRICING.get(
            model,
            self.GEMINI_PRICING["gemini-2.5-flash-lite"]
        )
        
        input_tokens = int(tokens * input_ratio)
        output_tokens = tokens - input_tokens
        
        cost = (input_tokens * pricing["input"]) + (output_tokens * pricing["output"])
        return round(cost, 6)
    
    def get_session_stats(self, log_file: str = "logs/agent_activity.jsonl") -> dict:
        """
        Get cumulative statistics from log file.
        
        Returns:
            Dictionary with total tokens, cost, and agent breakdown
        """
        log_path = Path(log_file)
        
        if not log_path.exists():
            return {
                "total_tokens": 0,
                "total_cost_usd": 0.0,
                "total_calls": 0,
                "by_agent": {}
            }
        
        stats = {
            "total_tokens": 0,
            "total_cost_usd": 0.0,
            "total_calls": 0,
            "by_agent": {}
        }
        
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                    
                entry = json.loads(line)
                agent = entry.get("agent", "unknown")
                tokens = entry.get("tokens_used", 0)
                cost = entry.get("cost_usd", 0.0)
                
                stats["total_tokens"] += tokens
                stats["total_cost_usd"] += cost
                stats["total_calls"] += 1
                
                if agent not in stats["by_agent"]:
                    stats["by_agent"][agent] = {
                        "calls": 0,
                        "tokens": 0,
                        "cost_usd": 0.0
                    }
                
                stats["by_agent"][agent]["calls"] += 1
                stats["by_agent"][agent]["tokens"] += tokens
                stats["by_agent"][agent]["cost_usd"] += cost
        
        stats["total_cost_usd"] = round(stats["total_cost_usd"], 6)
        
        return stats


# Utility functions for viewing logs

def view_recent_logs(limit: int = 10, log_file: str = "logs/agent_activity.jsonl") -> str:
    """
    View recent agent activity.
    
    Args:
        limit: Number of recent entries to show
        log_file: Path to log file
    
    Returns:
        Formatted string with recent activity
    """
    log_path = Path(log_file)
    
    if not log_path.exists():
        return "No logs found. Run agents to generate activity logs."
    
    lines = log_path.read_text(encoding='utf-8').strip().split('\n')
    recent = [line for line in lines if line.strip()][-limit:]
    
    output = f"===== RECENT AGENT ACTIVITY (last {len(recent)}) =====\n\n"
    
    for line in recent:
        try:
            entry = json.loads(line)
            timestamp = entry.get('timestamp', 'Unknown')
            agent = entry.get('agent', 'Unknown')
            action = entry.get('action', 'Unknown')
            tokens = entry.get('tokens_used', 0)
            cost = entry.get('cost_usd', 0.0)
            duration = entry.get('duration_ms', 0)
            status = entry.get('status', 'success')
            
            status_symbol = "✅" if status == "success" else "❌"
            
            output += f"{status_symbol} [{timestamp}] {agent}\n"
            output += f"   Action: {action}\n"
            output += f"   Tokens: {tokens:,} | Cost: ${cost:.6f} | Duration: {duration}ms\n"
            output += f"   Input: {entry.get('input_length', 0)} chars | Output: {entry.get('output_length', 0)} chars\n"
            output += "-" * 70 + "\n"
        except json.JSONDecodeError:
            continue
    
    return output


def get_cost_summary(log_file: str = "logs/agent_activity.jsonl") -> str:
    """
    Get total cost breakdown by agent.
    
    Returns:
        Formatted cost summary
    """
    tracker = TokenTracker()
    stats = tracker.get_session_stats(log_file)
    
    output = "===== COST SUMMARY =====\n\n"
    output += f"Total API Calls: {stats['total_calls']:,}\n"
    output += f"Total Tokens: {stats['total_tokens']:,}\n"
    output += f"Total Cost: ${stats['total_cost_usd']:.6f}\n\n"
    
    if stats['by_agent']:
        output += "Breakdown by Agent:\n"
        output += "-" * 70 + "\n"
        
        # Sort by cost descending
        sorted_agents = sorted(
            stats['by_agent'].items(),
            key=lambda x: x[1]['cost_usd'],
            reverse=True
        )
        
        for agent, data in sorted_agents:
            output += f"\n{agent}:\n"
            output += f"  Calls: {data['calls']:,}\n"
            output += f"  Tokens: {data['tokens']:,}\n"
            output += f"  Cost: ${data['cost_usd']:.6f}\n"
    
    output += "\n" + "=" * 70 + "\n"
    
    return output


# Create singleton logger instance
_global_logger = None

def get_logger() -> AgentLogger:
    """Get global AgentLogger instance (singleton pattern)."""
    global _global_logger
    if _global_logger is None:
        _global_logger = AgentLogger()
    return _global_logger


# Export as ADK tools for agent use
from google.adk.tools import FunctionTool

view_logs_tool = FunctionTool(func=view_recent_logs)
cost_summary_tool = FunctionTool(func=get_cost_summary)
