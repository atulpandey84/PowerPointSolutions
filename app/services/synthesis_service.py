from typing import List, Dict, Any
from app.models.architecture import AgentReview, ArchitectureScores, Severity

class SynthesisService:
    def synthesize(self, agent_reviews: List[AgentReview]) -> Dict[str, Any]:
        all_findings = []
        for review in agent_reviews:
            all_findings.extend(review.findings)

        # Deduplicate and rank findings (simplified)
        deduplicated = self._deduplicate(all_findings)

        # Calculate scores
        scores = self._calculate_scores(agent_reviews)

        summary = {
            "total_findings": len(all_findings),
            "critical_issues": len([f for f in deduplicated if f.severity == Severity.CRITICAL]),
            "high_issues": len([f for f in deduplicated if f.severity == Severity.HIGH]),
            "findings_by_category": self._group_by_category(deduplicated)
        }

        return {
            "summary": summary,
            "scores": scores,
            "findings": deduplicated
        }

    def _deduplicate(self, findings: List[Any]) -> List[Any]:
        # Implementation uses a basic title-based deduplication
        # In a real-world scenario, semantic similarity (embeddings) would be used.
        seen_titles = set()
        unique_findings = []
        for f in findings:
            if f.title.lower() not in seen_titles:
                unique_findings.append(f)
                seen_titles.add(f.title.lower())
        return unique_findings

    def _calculate_scores(self, agent_reviews: List[AgentReview]) -> ArchitectureScores:
        # Placeholder scoring logic
        return ArchitectureScores(
            security=self._score_for_category(agent_reviews, "SECURITY"),
            scalability=self._score_for_category(agent_reviews, "SCALABILITY"),
            reliability=self._score_for_category(agent_reviews, "RELIABILITY"),
            cost=self._score_for_category(agent_reviews, "FINOPS"),
            cloud_native_maturity=self._score_for_category(agent_reviews, "GCP_BEST_PRACTICES")
        )

    def _score_for_category(self, reviews: List[AgentReview], category: str) -> float:
        # Start with 100 and deduct based on severity
        score = 100.0
        for review in reviews:
            for finding in review.findings:
                if finding.category.value == category:
                    if finding.severity == Severity.CRITICAL: score -= 20
                    elif finding.severity == Severity.HIGH: score -= 10
                    elif finding.severity == Severity.MEDIUM: score -= 5
                    elif finding.severity == Severity.LOW: score -= 2
        return max(0.0, score)

    def _group_by_category(self, findings: List[Any]) -> Dict[str, int]:
        counts = {}
        for f in findings:
            counts[f.category.value] = counts.get(f.category.value, 0) + 1
        return counts
