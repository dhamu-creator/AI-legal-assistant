"""
Legal Assistant Evaluation Module
Comprehensive evaluation framework using RAGAS for citation accuracy, faithfulness, and relevance
"""

import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import numpy as np

try:
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    )
    from ragas.langchain import RagasEvaluatorChain
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False
    logging.warning("RAGAS not installed. Install with: pip install ragas")

logger = logging.getLogger(__name__)


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class EvaluationQuestion:
    """Test question for evaluation"""
    question: str
    reference_answer: str
    legal_domain: str  # "ipc_section", "case_law", "act", etc.
    expected_citations: List[str]
    difficulty: str  # "easy", "medium", "hard"


@dataclass
class LegalAnswer:
    """Response from legal assistant"""
    question: str
    answer: str
    citations: List[str]
    sources: List[Dict]
    confidence: float


@dataclass
class CitationAccuracyResult:
    """Citation accuracy evaluation result"""
    correct_citations: int
    total_citations: int
    accuracy: float  # 0.0-1.0
    missed_citations: List[str]
    false_citations: List[str]
    citation_types_covered: Dict[str, int]


@dataclass
class FaithfulnessResult:
    """Faithfulness evaluation result"""
    score: float  # 0.0-1.0
    hallucinations_detected: int
    unsupported_claims: List[str]
    supported_claims: int


@dataclass
class RelevanceResult:
    """Answer relevance evaluation result"""
    score: float  # 0.0-1.0
    relevance_analysis: str
    missing_aspects: List[str]
    extra_information: List[str]


@dataclass
class CompleteLegalEvaluation:
    """Complete evaluation result for legal assistant"""
    question: str
    citation_accuracy: CitationAccuracyResult
    faithfulness: FaithfulnessResult
    relevance: RelevanceResult
    overall_score: float
    evaluation_timestamp: str
    notes: str


# ============================================================================
# CITATION EVALUATION
# ============================================================================

class CitationEvaluator:
    """Evaluate accuracy of extracted citations"""
    
    # Citation type patterns
    CITATION_TYPES = {
        "IPC": r"\bS(?:ection|\.)?\s*\d{1,4}(?:\s*IPC|\b)",
        "CASE": r"\[?\d{4}\]?\s*[A-Z]+\s*\d+(?:\s*\(SC\))?",
        "ACT": r"\b(Indian\s+Penal\s+Code|Criminal\s+Procedure\s+Code|IPC|CrPC)",
        "ARTICLE": r"\bArticle\s+\d{1,3}\b",
        "RULE": r"\bRule\s+\d{1,4}\b",
    }
    
    def __init__(self):
        """Initialize citation evaluator"""
        self.evaluations = []
    
    def evaluate_citations(
        self,
        extracted_citations: List[str],
        reference_citations: List[str]
    ) -> CitationAccuracyResult:
        """
        Evaluate citation accuracy
        
        Args:
            extracted_citations: Citations extracted from answer
            reference_citations: Known correct citations
        
        Returns:
            CitationAccuracyResult with accuracy metrics
        """
        correct = 0
        missed = []
        false_positives = []
        
        # Normalize citations for comparison
        extracted_normalized = [self._normalize_citation(c) for c in extracted_citations]
        reference_normalized = [self._normalize_citation(c) for c in reference_citations]
        
        # Count correct citations
        for ref_cite in reference_normalized:
            if ref_cite in extracted_normalized:
                correct += 1
            else:
                missed.append(ref_cite)
        
        # Identify false positives
        for ext_cite in extracted_normalized:
            if ext_cite not in reference_normalized:
                false_positives.append(ext_cite)
        
        # Calculate accuracy
        total_citations = len(reference_citations)
        accuracy = correct / total_citations if total_citations > 0 else 0.0
        
        # Categorize citations by type
        citation_types = self._categorize_citations(extracted_normalized)
        
        return CitationAccuracyResult(
            correct_citations=correct,
            total_citations=total_citations,
            accuracy=accuracy,
            missed_citations=missed,
            false_citations=false_positives,
            citation_types_covered=citation_types
        )
    
    @staticmethod
    def _normalize_citation(citation: str) -> str:
        """Normalize citation for comparison"""
        # Remove extra whitespace
        normalized = " ".join(citation.split())
        # Convert to lowercase for case-insensitive comparison
        return normalized.lower()
    
    @staticmethod
    def _categorize_citations(citations: List[str]) -> Dict[str, int]:
        """Categorize citations by type"""
        import re
        categories = {
            "IPC": 0,
            "Case": 0,
            "Act": 0,
            "Article": 0,
            "Rule": 0,
            "Other": 0
        }
        
        for citation in citations:
            if re.search(r"section|s\.|ipc", citation, re.I):
                categories["IPC"] += 1
            elif re.search(r"\[\d{4}\]", citation):
                categories["Case"] += 1
            elif re.search(r"act|code", citation, re.I):
                categories["Act"] += 1
            elif re.search(r"article", citation, re.I):
                categories["Article"] += 1
            elif re.search(r"rule", citation, re.I):
                categories["Rule"] += 1
            else:
                categories["Other"] += 1
        
        return categories


# ============================================================================
# FAITHFULNESS EVALUATION
# ============================================================================

class FaithfulnessEvaluator:
    """Evaluate faithfulness of answers to retrieved documents"""
    
    def __init__(self, llm_chain):
        """
        Initialize faithfulness evaluator
        
        Args:
            llm_chain: LegalRAGChain for verification queries
        """
        self.llm_chain = llm_chain
    
    def evaluate_faithfulness(
        self,
        answer: str,
        sources: List[Dict]
    ) -> FaithfulnessResult:
        """
        Evaluate if answer is faithful to sources
        
        Args:
            answer: Generated answer text
            sources: Retrieved source documents
        
        Returns:
            FaithfulnessResult with hallucination analysis
        """
        source_text = " ".join([s.get("text", "") for s in sources])
        
        # Extract key claims from answer
        claims = self._extract_claims(answer)
        
        # Verify each claim against sources
        hallucinations = []
        unsupported = []
        supported = 0
        
        for claim in claims:
            is_supported = self._verify_claim(claim, source_text)
            if not is_supported:
                unsupported.append(claim)
            else:
                supported += 1
        
        # Calculate faithfulness score
        total_claims = len(claims)
        faithfulness_score = supported / total_claims if total_claims > 0 else 1.0
        
        return FaithfulnessResult(
            score=faithfulness_score,
            hallucinations_detected=len(unsupported),
            unsupported_claims=unsupported,
            supported_claims=supported
        )
    
    @staticmethod
    def _extract_claims(text: str) -> List[str]:
        """Extract major claims from text"""
        import nltk
        try:
            sentences = nltk.sent_tokenize(text)
            # Filter short sentences (likely not major claims)
            claims = [s.strip() for s in sentences if len(s.split()) > 5]
            return claims
        except:
            # Fallback: split by period
            return [s.strip() for s in text.split('.') if len(s.split()) > 5]
    
    @staticmethod
    def _verify_claim(claim: str, source_text: str) -> bool:
        """
        Simple claim verification
        Check if key elements of claim appear in source
        """
        import re
        
        # Extract key terms (nouns from claim)
        terms = re.findall(r'\b[A-Z][a-z]+\b', claim)
        
        if not terms:
            return True  # Can't verify, assume true
        
        # Check if key terms appear in source
        for term in terms[:3]:  # Check first 3 key terms
            if term.lower() not in source_text.lower():
                return False
        
        return True


# ============================================================================
# RELEVANCE EVALUATION
# ============================================================================

class RelevanceEvaluator:
    """Evaluate relevance of answers to questions"""
    
    def __init__(self):
        """Initialize relevance evaluator"""
        pass
    
    def evaluate_relevance(
        self,
        question: str,
        answer: str,
        reference_answer: Optional[str] = None
    ) -> RelevanceResult:
        """
        Evaluate answer relevance to question
        
        Args:
            question: User question
            answer: Generated answer
            reference_answer: Optional reference answer for comparison
        
        Returns:
            RelevanceResult with relevance analysis
        """
        # Extract question aspects
        question_aspects = self._extract_aspects(question)
        
        # Check if answer addresses aspects
        covered_aspects = []
        missing_aspects = []
        
        for aspect in question_aspects:
            if self._aspect_in_answer(aspect, answer):
                covered_aspects.append(aspect)
            else:
                missing_aspects.append(aspect)
        
        # Calculate relevance score
        if question_aspects:
            relevance_score = len(covered_aspects) / len(question_aspects)
        else:
            relevance_score = 0.5
        
        # Identify extra information
        extra_info = self._identify_extra_info(question, answer)
        
        analysis = f"Covered {len(covered_aspects)}/{len(question_aspects)} aspects"
        
        return RelevanceResult(
            score=relevance_score,
            relevance_analysis=analysis,
            missing_aspects=missing_aspects,
            extra_information=extra_info
        )
    
    @staticmethod
    def _extract_aspects(question: str) -> List[str]:
        """Extract main aspects/topics from question"""
        import nltk
        
        # Simple approach: extract question words and nouns
        words = question.lower().split()
        question_words = {'what', 'how', 'why', 'when', 'where', 'who'}
        
        aspects = [w for w in words if w not in question_words and len(w) > 3]
        return aspects[:5]  # Top 5 aspects
    
    @staticmethod
    def _aspect_in_answer(aspect: str, answer: str) -> bool:
        """Check if aspect is addressed in answer"""
        return aspect.lower() in answer.lower()
    
    @staticmethod
    def _identify_extra_info(question: str, answer: str) -> List[str]:
        """Identify extra information not asked for"""
        # Simple heuristic: topics in answer but not in question
        q_words = set(question.lower().split())
        a_words = answer.lower().split()
        
        extra = []
        seen = set()
        
        for word in a_words:
            if word not in q_words and word not in seen and len(word) > 4:
                extra.append(word)
                seen.add(word)
        
        return extra[:5]  # Top 5 extra terms


# ============================================================================
# COMPLETE EVALUATOR
# ============================================================================

class LegalAssistantEvaluator:
    """Complete evaluation framework for legal assistant"""
    
    def __init__(self, llm_chain=None):
        """
        Initialize evaluator
        
        Args:
            llm_chain: LegalRAGChain instance (optional)
        """
        self.citation_evaluator = CitationEvaluator()
        self.faithfulness_evaluator = FaithfulnessEvaluator(llm_chain) if llm_chain else None
        self.relevance_evaluator = RelevanceEvaluator()
        self.results = []
    
    def evaluate_answer(
        self,
        question: str,
        answer: LegalAnswer,
        expected_citations: List[str] = None,
        reference_answer: str = None,
        sources: List[Dict] = None
    ) -> CompleteLegalEvaluation:
        """
        Complete evaluation of single answer
        
        Args:
            question: Original question
            answer: LegalAnswer object
            expected_citations: Reference citations for accuracy check
            reference_answer: Reference answer for comparison
            sources: Retrieved source documents
        
        Returns:
            CompleteLegalEvaluation with full metrics
        """
        # Citation accuracy
        expected_cites = expected_citations or []
        citation_result = self.citation_evaluator.evaluate_citations(
            answer.citations,
            expected_cites
        )
        
        # Faithfulness
        sources_data = sources or answer.sources or []
        if self.faithfulness_evaluator:
            faithfulness_result = self.faithfulness_evaluator.evaluate_faithfulness(
                answer.answer,
                sources_data
            )
        else:
            faithfulness_result = FaithfulnessResult(
                score=0.5, hallucinations_detected=0,
                unsupported_claims=[], supported_claims=0
            )
        
        # Relevance
        relevance_result = self.relevance_evaluator.evaluate_relevance(
            question,
            answer.answer,
            reference_answer
        )
        
        # Overall score (weighted average)
        overall_score = (
            citation_result.accuracy * 0.35 +
            faithfulness_result.score * 0.35 +
            relevance_result.score * 0.30
        )
        
        evaluation = CompleteLegalEvaluation(
            question=question,
            citation_accuracy=citation_result,
            faithfulness=faithfulness_result,
            relevance=relevance_result,
            overall_score=overall_score,
            evaluation_timestamp=datetime.now().isoformat(),
            notes=""
        )
        
        self.results.append(evaluation)
        return evaluation
    
    def evaluate_batch(
        self,
        test_questions: List[EvaluationQuestion],
        answer_generator
    ) -> Dict:
        """
        Evaluate multiple questions
        
        Args:
            test_questions: List of EvaluationQuestion
            answer_generator: Function to generate answers
        
        Returns:
            Dict with aggregate metrics
        """
        results = []
        
        for test_q in test_questions:
            try:
                # Generate answer
                answer = answer_generator(test_q.question)
                
                # Evaluate
                evaluation = self.evaluate_answer(
                    test_q.question,
                    answer,
                    expected_citations=test_q.expected_citations,
                    reference_answer=test_q.reference_answer
                )
                
                results.append(evaluation)
            except Exception as e:
                logger.error(f"Error evaluating question: {str(e)}")
        
        # Calculate aggregate metrics
        return self._aggregate_results(results)
    
    def _aggregate_results(self, results: List[CompleteLegalEvaluation]) -> Dict:
        """Aggregate evaluation results"""
        if not results:
            return {}
        
        citation_accuracies = [r.citation_accuracy.accuracy for r in results]
        faithfulness_scores = [r.faithfulness.score for r in results]
        relevance_scores = [r.relevance.score for r in results]
        overall_scores = [r.overall_score for r in results]
        
        return {
            "total_questions": len(results),
            "citation_accuracy": {
                "mean": np.mean(citation_accuracies),
                "std": np.std(citation_accuracies),
                "min": np.min(citation_accuracies),
                "max": np.max(citation_accuracies),
            },
            "faithfulness": {
                "mean": np.mean(faithfulness_scores),
                "std": np.std(faithfulness_scores),
                "min": np.min(faithfulness_scores),
                "max": np.max(faithfulness_scores),
            },
            "relevance": {
                "mean": np.mean(relevance_scores),
                "std": np.std(relevance_scores),
                "min": np.min(relevance_scores),
                "max": np.max(relevance_scores),
            },
            "overall": {
                "mean": np.mean(overall_scores),
                "std": np.std(overall_scores),
                "min": np.min(overall_scores),
                "max": np.max(overall_scores),
            },
        }
    
    def generate_report(self, results: Dict = None) -> str:
        """Generate evaluation report"""
        if not results:
            if not self.results:
                return "No results to report"
            results = self._aggregate_results(self.results)
        
        report = """
╔════════════════════════════════════════════════════════════╗
║           LEGAL ASSISTANT EVALUATION REPORT                ║
╚════════════════════════════════════════════════════════════╝

EVALUATION METRICS:
───────────────────────────────────────────────────────────────

Citation Accuracy:
  • Mean: {citation_mean:.2%}
  • Std Dev: {citation_std:.2%}
  • Range: {citation_min:.2%} - {citation_max:.2%}

Faithfulness:
  • Mean: {faith_mean:.2%}
  • Std Dev: {faith_std:.2%}
  • Range: {faith_min:.2%} - {faith_max:.2%}

Answer Relevance:
  • Mean: {rel_mean:.2%}
  • Std Dev: {rel_std:.2%}
  • Range: {rel_min:.2%} - {rel_max:.2%}

Overall Score:
  • Mean: {overall_mean:.2%}
  • Std Dev: {overall_std:.2%}
  • Range: {overall_min:.2%} - {overall_max:.2%}

───────────────────────────────────────────────────────────────
Total Questions Evaluated: {total}
Timestamp: {timestamp}
        """.format(
            citation_mean=results.get("citation_accuracy", {}).get("mean", 0),
            citation_std=results.get("citation_accuracy", {}).get("std", 0),
            citation_min=results.get("citation_accuracy", {}).get("min", 0),
            citation_max=results.get("citation_accuracy", {}).get("max", 0),
            faith_mean=results.get("faithfulness", {}).get("mean", 0),
            faith_std=results.get("faithfulness", {}).get("std", 0),
            faith_min=results.get("faithfulness", {}).get("min", 0),
            faith_max=results.get("faithfulness", {}).get("max", 0),
            rel_mean=results.get("relevance", {}).get("mean", 0),
            rel_std=results.get("relevance", {}).get("std", 0),
            rel_min=results.get("relevance", {}).get("min", 0),
            rel_max=results.get("relevance", {}).get("max", 0),
            overall_mean=results.get("overall", {}).get("mean", 0),
            overall_std=results.get("overall", {}).get("std", 0),
            overall_min=results.get("overall", {}).get("min", 0),
            overall_max=results.get("overall", {}).get("max", 0),
            total=results.get("total_questions", 0),
            timestamp=datetime.now().isoformat()
        )
        
        return report
    
    def save_results(self, filepath: str) -> None:
        """Save evaluation results to JSON file"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "total_evaluations": len(self.results),
            "aggregate_metrics": self._aggregate_results(self.results),
            "individual_results": [
                {
                    "question": r.question,
                    "citation_accuracy": r.citation_accuracy.accuracy,
                    "faithfulness": r.faithfulness.score,
                    "relevance": r.relevance.score,
                    "overall_score": r.overall_score,
                }
                for r in self.results
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Results saved to {filepath}")


if __name__ == "__main__":
    # Example usage
    from src.utils.citation_tracker import Citation
    
    # Create test data
    question = "What is Section 302 IPC?"
    test_answer = LegalAnswer(
        question=question,
        answer="Section 302 IPC deals with murder and prescribes imprisonment for life.",
        citations=["Section 302 IPC", "[2021] SCC 45"],
        sources=[],
        confidence=0.95
    )
    
    expected_cites = ["Section 302 IPC", "[2021] SCC 45", "AIR 2022 SC 123"]
    
    # Evaluate
    evaluator = LegalAssistantEvaluator()
    result = evaluator.evaluate_answer(
        question,
        test_answer,
        expected_cites
    )
    
    print(f"Citation Accuracy: {result.citation_accuracy.accuracy:.2%}")
    print(f"Faithfulness: {result.faithfulness.score:.2%}")
    print(f"Relevance: {result.relevance.score:.2%}")
    print(f"Overall Score: {result.overall_score:.2%}")
