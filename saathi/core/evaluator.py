"""
Saathi AI 2.0 — Answer Self-Evaluation & Critique Pipeline
"""

from typing import Dict, Any, Optional

class ResponseEvaluator:
    """Evaluates generated responses for correctness, completeness, citations, and syntax consistency."""

    def __init__(self, max_iterations: int = 2):
        self.max_iterations = max_iterations

    def evaluate(self, task: str, response: str) -> Dict[str, Any]:
        issues = []
        score = 1.0

        if not response or len(response.strip()) < 10:
            issues.append("Response is excessively brief or empty.")
            score -= 0.5

        if "Error" in response or "Exception" in response:
            issues.append("Response contains unhandled error or exception trace.")
            score -= 0.3

        if ("research" in task.lower() or "search" in task.lower()) and "Source" not in response and "http" not in response:
            issues.append("Research response lacks explicit source citations.")
            score -= 0.2

        passed = (score >= 0.7) and (len(issues) == 0)

        return {
            "passed": passed,
            "score": max(0.0, score),
            "issues": issues,
            "recommendation": "APPROVED" if passed else f"REVISE: {'; '.join(issues)}"
        }

