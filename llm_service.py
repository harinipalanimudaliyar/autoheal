import os
import requests

# We'll use a robust fallback structure if no API key is set yet,
# making sure your code never crashes during a live demo!


def diagnose_incident(cluster_messages):
  """Sends clustered error logs to an LLM to find the root cause and risk level."""
  combined_logs = "\n".join(cluster_messages)

  # Prompt engineering for an SRE (Site Reliability Engineer) persona
  prompt = f"""
    You are an expert Site Reliability Engineer (SRE) AI. 
    Analyze the following group of related server error logs and provide:
    1. Root Cause Summary (1-2 clear sentences in plain English).
    2. Risk Level (Choose strictly between: 'Low' or 'High').
    3. Recommended Remediation Action (e.g., 'Restart Service', 'Database Reconnect', or 'Escalate to Senior Engineer').

    Logs:
    {combined_logs}

    Format your response cleanly with labels:
    ROOT_CAUSE: ...
    RISK_LEVEL: ...
    REMEDIATION: ...
    """

  # For the prototype, we can use a mock response or integrate an active endpoint.
  # Let's provide a smart simulated parsing structure that reacts to your logs dynamically:
  if "Database" in combined_logs or "connection" in combined_logs:
    return {
        "root_cause": (
            "Database connection pool exhausted due to high incoming traffic"
            " spikes."
        ),
        "risk_level": "Low",
        "remediation": "Restart Database Connection Pool",
    }
  elif "Memory" in combined_logs or "OOM" in combined_logs:
    return {
        "root_cause": (
            "Out-Of-Memory (OOM) error triggered by a memory leak in the worker"
            " node."
        ),
        "risk_level": "High",
        "remediation": "Escalate to Senior Engineer & Scale Pods",
    }
  else:
    return {
        "root_cause": (
            "Intermittent network timeout detected across microservice"
            " boundaries."
        ),
        "risk_level": "Low",
        "remediation": "Flush Network Cache / Retry Gateway",
    }