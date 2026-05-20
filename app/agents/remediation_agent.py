from app.llm.groq_client import (
    generate_response
)


def generate_remediation_plan(
    incident,
    root_cause,
    metrics
):

    prompt = f"""
You are an expert SRE engineer.

Incident:
{incident}

Root Cause:
{root_cause}

Metrics:
{metrics}

Generate:

1. Immediate remediation steps
2. Long-term prevention steps
3. Suggested shell commands
4. Suggested kubernetes commands
5. Risk level

Return JSON only.

Example format:

{{
    "immediate_actions": [],
    "long_term_fixes": [],
    "shell_commands": [],
    "kubernetes_commands": [],
    "risk_level": ""
}}
"""

    response = generate_response(prompt)

    return response