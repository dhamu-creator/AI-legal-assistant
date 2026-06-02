"""
STEP 8: Comprehensive Evaluation Script
Demonstrates RAGAS integration with citation accuracy, faithfulness, and relevance metrics
"""

import sys
import os
import json
from datetime import datetime

# Add project to path
sys.path.insert(0, '.')

from src.evaluation.evaluator import (
    EvaluationQuestion,
    LegalAnswer,
    LegalAssistantEvaluator,
    CitationEvaluator,
    RelevanceEvaluator,
)

# ============================================================================
# TEST DATASET
# ============================================================================

def create_legal_test_dataset():
    """Create comprehensive test dataset for evaluation"""
    
    test_questions = [
        # IPC Section Questions
        EvaluationQuestion(
            question="What is Section 302 IPC and what is the punishment?",
            reference_answer="Section 302 of the Indian Penal Code deals with murder. It prescribes imprisonment for life or death penalty, and may also include fine.",
            legal_domain="ipc_section",
            expected_citations=["Section 302 IPC", "[2021] SCC 45", "AIR 2022 SC 123"],
            difficulty="easy"
        ),
        
        # Case Law Questions
        EvaluationQuestion(
            question="What is the significance of AIR 2022 SC 123 in bail proceedings?",
            reference_answer="This landmark judgment clarifies the principles for granting bail in serious crimes, emphasizing the presumption of innocence.",
            legal_domain="case_law",
            expected_citations=["AIR 2022 SC 123", "SCC (2022) 4", "Supreme Court"],
            difficulty="medium"
        ),
        
        # Act Inquiry
        EvaluationQuestion(
            question="How does the Criminal Procedure Code differ from IPC in handling investigations?",
            reference_answer="CrPC governs procedural aspects of criminal law including investigation, arrest, bail, and trial, while IPC defines substantive crimes and punishments.",
            legal_domain="act",
            expected_citations=["Criminal Procedure Code", "IPC", "CrPC"],
            difficulty="medium"
        ),
        
        # Punishment Questions
        EvaluationQuestion(
            question="What is the maximum punishment for cheating under Section 420 IPC?",
            reference_answer="Section 420 IPC prescribes imprisonment up to 7 years and/or fine up to Rs 1 Lakh for cheating.",
            legal_domain="punishment",
            expected_citations=["Section 420 IPC", "7 years imprisonment"],
            difficulty="easy"
        ),
        
        # Bail Questions
        EvaluationQuestion(
            question="Can bail be granted in murder cases?",
            reference_answer="Bail in murder cases is discretionary. While serious crimes attract stricter bail conditions, courts consider factors like evidence strength, criminal history, and flight risk.",
            legal_domain="bail",
            expected_citations=["Bail provisions", "Section 437 CrPC", "Discretionary bail"],
            difficulty="hard"
        ),
    ]
    
    return test_questions


def create_sample_answers():
    """Create sample AI responses for testing"""
    
    answers = [
        LegalAnswer(
            question="What is Section 302 IPC?",
            answer="Section 302 of the Indian Penal Code deals with murder. It provides for punishment including life imprisonment or death penalty. The section is extensively used in Indian criminal law for prosecuting serious homicide cases. A landmark judgment [2021] SCC 45 clarifies the interpretation of 'murder'.",
            citations=["Section 302 IPC", "[2021] SCC 45"],
            sources=[
                {"case_name": "Landmark Murder Case", "court": "Supreme Court", "year": 2021, "text": "Section 302 covers..." }
            ],
            confidence=0.92
        ),
        
        LegalAnswer(
            question="How does CrPC differ from IPC?",
            answer="The Criminal Procedure Code (CrPC) is the procedural law governing criminal investigations, arrests, bail, and trials in India. The Indian Penal Code (IPC) on the other hand defines substantive crimes and prescribes punishments. CrPC essentially provides the framework for applying IPC. Key differences include investigation procedures, bail conditions, and trial processes.",
            citations=["Criminal Procedure Code", "IPC", "Procedural law"],
            sources=[],
            confidence=0.88
        ),
        
        LegalAnswer(
            question="What about bail in murder cases?",
            answer="Bail in murder cases is discretionary under Section 437 of CrPC. While murder is a serious crime, courts have authority to grant bail considering factors such as strength of evidence, criminal history, and flight risk. Courts balance between personal liberty and public safety in such cases.",
            citations=["Section 437 CrPC", "Murder cases", "Discretionary bail"],
            sources=[],
            confidence=0.85
        ),
    ]
    
    return answers


# ============================================================================
# EVALUATION DEMONSTRATIONS
# ============================================================================

def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_citation_evaluation():
    """Demonstrate citation accuracy evaluation"""
    print_section("DEMO 1: CITATION ACCURACY EVALUATION")
    
    evaluator = CitationEvaluator()
    
    # Test Case 1: Perfect match
    extracted = ["Section 302 IPC", "[2021] SCC 45", "AIR 2022 SC 123"]
    reference = ["Section 302 IPC", "[2021] SCC 45", "AIR 2022 SC 123"]
    
    result1 = evaluator.evaluate_citations(extracted, reference)
    print("Test Case 1: Perfect Match")
    print(f"  Accuracy: {result1.accuracy:.2%}")
    print(f"  Correct: {result1.correct_citations}/{result1.total_citations}")
    print()
    
    # Test Case 2: Partial match with false positives
    extracted = ["Section 302 IPC", "[2021] SCC 45", "Section 420 IPC"]
    reference = ["Section 302 IPC", "[2021] SCC 45", "AIR 2022 SC 123"]
    
    result2 = evaluator.evaluate_citations(extracted, reference)
    print("Test Case 2: Partial Match")
    print(f"  Accuracy: {result2.accuracy:.2%}")
    print(f"  Correct: {result2.correct_citations}/{result2.total_citations}")
    print(f"  Missed: {result2.missed_citations}")
    print(f"  False Positives: {result2.false_citations}")
    print()
    
    # Test Case 3: Poor accuracy
    extracted = ["Article 21", "IPC 123"]
    reference = ["Section 302 IPC", "[2021] SCC 45"]
    
    result3 = evaluator.evaluate_citations(extracted, reference)
    print("Test Case 3: Poor Accuracy")
    print(f"  Accuracy: {result3.accuracy:.2%}")
    print(f"  Correct: {result3.correct_citations}/{result3.total_citations}")
    print(f"  Citation Types: {result3.citation_types_covered}")
    print()


def demo_relevance_evaluation():
    """Demonstrate relevance evaluation"""
    print_section("DEMO 2: RELEVANCE EVALUATION")
    
    evaluator = RelevanceEvaluator()
    
    # Test Case 1: Highly relevant
    q1 = "What is Section 302 IPC?"
    a1 = "Section 302 of the Indian Penal Code deals with murder. It prescribes death penalty or life imprisonment, with or without fine."
    
    result1 = evaluator.evaluate_relevance(q1, a1)
    print("Test Case 1: Highly Relevant Answer")
    print(f"  Question: {q1}")
    print(f"  Relevance Score: {result1.score:.2%}")
    print(f"  Analysis: {result1.relevance_analysis}")
    print()
    
    # Test Case 2: Partially relevant
    q2 = "How does bail work in criminal cases?"
    a2 = "Bail is provided under CrPC. Murder is a serious crime. Section 302 deals with murder. Criminal law is complex."
    
    result2 = evaluator.evaluate_relevance(q2, a2)
    print("Test Case 2: Partially Relevant Answer")
    print(f"  Question: {q2}")
    print(f"  Relevance Score: {result2.score:.2%}")
    print(f"  Missing Aspects: {result2.missing_aspects}")
    print()


def demo_complete_evaluation():
    """Demonstrate complete answer evaluation"""
    print_section("DEMO 3: COMPLETE ANSWER EVALUATION")
    
    evaluator = LegalAssistantEvaluator()
    
    # Create test answer
    question = "What is Section 302 IPC?"
    answer = LegalAnswer(
        question=question,
        answer="Section 302 of the Indian Penal Code deals with murder. It prescribes death penalty or life imprisonment. More information about punishment can be found in criminal law literature.",
        citations=["Section 302 IPC", "[2021] SCC 45"],
        sources=[{"text": "Section 302 deals with murder and prescribes..."}],
        confidence=0.90
    )
    
    expected_citations = ["Section 302 IPC", "[2021] SCC 45", "AIR 2022 SC 123"]
    
    # Evaluate
    result = evaluator.evaluate_answer(
        question,
        answer,
        expected_citations=expected_citations,
        sources=answer.sources
    )
    
    print(f"Question: {question}\n")
    print("Evaluation Results:")
    print(f"  Citation Accuracy: {result.citation_accuracy.accuracy:.2%}")
    print(f"    Correct: {result.citation_accuracy.correct_citations}/{result.citation_accuracy.total_citations}")
    print(f"    Missed: {result.citation_accuracy.missed_citations}")
    print()
    print(f"  Faithfulness Score: {result.faithfulness.score:.2%}")
    print(f"    Unsupported Claims: {len(result.faithfulness.unsupported_claims)}")
    print()
    print(f"  Relevance Score: {result.relevance.score:.2%}")
    print(f"    Missing Aspects: {result.relevance.missing_aspects}")
    print()
    print(f"  >>> OVERALL SCORE: {result.overall_score:.2%} <<<")
    print()


def demo_batch_evaluation():
    """Demonstrate batch evaluation"""
    print_section("DEMO 4: BATCH EVALUATION")
    
    evaluator = LegalAssistantEvaluator()
    test_dataset = create_legal_test_dataset()
    
    # Simple answer generator (in production would use full RAG chain)
    def simple_answer_generator(question):
        return LegalAnswer(
            question=question,
            answer=f"Answer to: {question}",
            citations=["Section 302 IPC", "[2021] SCC 45"],
            sources=[],
            confidence=0.8
        )
    
    print(f"Evaluating {len(test_dataset)} test questions...")
    results = evaluator.evaluate_batch(test_dataset, simple_answer_generator)
    
    print("\nBatch Evaluation Results:")
    print(f"  Total Questions: {results.get('total_questions', 0)}")
    print()
    print("  Citation Accuracy:")
    print(f"    Mean: {results.get('citation_accuracy', {}).get('mean', 0):.2%}")
    print(f"    Range: {results.get('citation_accuracy', {}).get('min', 0):.2%} - {results.get('citation_accuracy', {}).get('max', 0):.2%}")
    print()
    print("  Faithfulness:")
    print(f"    Mean: {results.get('faithfulness', {}).get('mean', 0):.2%}")
    print()
    print("  Relevance:")
    print(f"    Mean: {results.get('relevance', {}).get('mean', 0):.2%}")
    print()
    print("  Overall Score:")
    print(f"    Mean: {results.get('overall', {}).get('mean', 0):.2%}")
    print()


def demo_report_generation():
    """Demonstrate report generation"""
    print_section("DEMO 5: EVALUATION REPORT GENERATION")
    
    evaluator = LegalAssistantEvaluator()
    
    # Create sample evaluation result
    sample_result = {
        "total_questions": 5,
        "citation_accuracy": {
            "mean": 0.85,
            "std": 0.10,
            "min": 0.67,
            "max": 1.00,
        },
        "faithfulness": {
            "mean": 0.82,
            "std": 0.12,
            "min": 0.60,
            "max": 0.95,
        },
        "relevance": {
            "mean": 0.88,
            "std": 0.09,
            "min": 0.75,
            "max": 1.00,
        },
        "overall": {
            "mean": 0.85,
            "std": 0.10,
            "min": 0.68,
            "max": 0.99,
        },
    }
    
    report = evaluator.generate_report(sample_result)
    print(report)


def demo_integration_with_rag():
    """Demonstrate integration with RAG chain"""
    print_section("DEMO 6: INTEGRATION WITH RAG CHAIN")
    
    print("""
To integrate evaluation with your RAG chain:

1. Setup RAG System:
   ─────────────────
   from src.generation.llm_chain import build_rag_chain
   chain = build_rag_chain(retriever)

2. Create Evaluator:
   ─────────────────
   from src.evaluation.evaluator import LegalAssistantEvaluator
   evaluator = LegalAssistantEvaluator(chain)

3. Evaluate Questions:
   ───────────────────
   test_questions = [
       EvaluationQuestion(
           question="What is Section 302?",
           reference_answer="...",
           legal_domain="ipc_section",
           expected_citations=["Section 302 IPC"],
           difficulty="easy"
       ),
       ...
   ]
   
4. Run Batch Evaluation:
   ─────────────────────
   def answer_generator(q):
       answer = chain.query(q)
       return LegalAnswer(
           question=q,
           answer=answer.answer,
           citations=answer.citations,
           sources=answer.sources,
           confidence=answer.confidence_score
       )
   
   results = evaluator.evaluate_batch(test_questions, answer_generator)

5. Generate Reports:
   ──────────────────
   report = evaluator.generate_report(results)
   print(report)
   evaluator.save_results("evaluation_results.json")

METRICS EXPLAINED:
─────────────────
• Citation Accuracy: % of expected citations correctly extracted
• Faithfulness: % of claims supported by retrieved documents  
• Relevance: % of question aspects addressed in answer
• Overall Score: Weighted average (35% citation + 35% faithful + 30% relevant)
    """)


def demo_best_practices():
    """Best practices for evaluation"""
    print_section("DEMO 7: EVALUATION BEST PRACTICES")
    
    practices = """
BEST PRACTICES FOR EVALUATING LEGAL QA SYSTEMS:
───────────────────────────────────────────────

1. DIVERSE TEST SETS
   ✓ Include easy, medium, hard questions
   ✓ Cover different legal domains (IPC, CrPC, Acts)
   ✓ Test both simple and complex scenarios
   ✓ Include edge cases and ambiguous questions

2. CITATION EVALUATION
   ✓ Verify citations exist in source documents
   ✓ Check citation formatting accuracy
   ✓ Evaluate citation relevance to answer
   ✓ Monitor for hallucinated citations

3. FAITHFULNESS TESTING
   ✓ Compare answers against source documents
   ✓ Identify unsupported claims
   ✓ Check for answer hallucinations
   ✓ Verify legal accuracy of generated text

4. RELEVANCE ASSESSMENT
   ✓ Ensure all question aspects addressed
   ✓ Check for unnecessary information
   ✓ Verify answer completeness
   ✓ Assess answer clarity and structure

5. CONTINUOUS MONITORING
   ✓ Track metrics over time
   ✓ Compare performance across LLM versions
   ✓ Identify degradation patterns
   ✓ Set performance baselines and thresholds

6. INTERACTIVE EVALUATION
   ✓ Manual review of edge cases
   ✓ Expert legal review for accuracy
   ✓ User feedback integration
   ✓ A/B testing of different approaches

7. PERFORMANCE TARGETS
   ✓ Citation Accuracy: Target > 85%
   ✓ Faithfulness: Target > 80%
   ✓ Relevance: Target > 85%
   ✓ Overall Score: Target > 83%

8. QUALITY THRESHOLDS
   ✓ High Quality: Score > 0.90
   ✓ Good Quality: Score 0.80-0.90
   ✓ Fair Quality: Score 0.70-0.80
   ✓ Poor Quality: Score < 0.70
    """
    
    print(practices)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all evaluation demonstrations"""
    
    print("\n" + "=" * 80)
    print("  STEP 8: COMPREHENSIVE LEGAL ASSISTANT EVALUATION")
    print("  RAGAS Integration & Evaluation Framework Demo")
    print("=" * 80)
    
    demos = [
        ("Citation Accuracy Evaluation", demo_citation_evaluation),
        ("Relevance Evaluation", demo_relevance_evaluation),
        ("Complete Answer Evaluation", demo_complete_evaluation),
        ("Batch Evaluation", demo_batch_evaluation),
        ("Report Generation", demo_report_generation),
        ("RAG Integration", demo_integration_with_rag),
        ("Best Practices", demo_best_practices),
    ]
    
    for demo_name, demo_func in demos:
        try:
            demo_func()
            input("\n▶️  Press Enter to continue... ")
        except KeyboardInterrupt:
            print("\n\n❌ Demo interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "=" * 80)
    print("  STEP 8 EVALUATION FRAMEWORK COMPLETE")
    print("=" * 80)
    print("\n✅ Evaluation system is ready for use!")
    print("📊 Integration:")
    print("   - Citation accuracy evaluation")
    print("   - Faithfulness assessment")
    print("   - Relevance scoring")
    print("   - Batch processing")
    print("   - Report generation")
    print("\n📈 Next: Integrate with your RAG chain for continuous monitoring")
    print("\n")


if __name__ == "__main__":
    main()
