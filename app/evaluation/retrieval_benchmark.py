from pathlib import Path
import json
from datetime import datetime

from app.config import (
    UPLOAD_DIR,
    REPORT_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K
)

from app.ingestion.pdf_loader import load_pdfs
from app.ingestion.chunker import chunk_documents
from app.retrieval.retriever import ResearchRetriever
from app.evaluation.evaluator import keyword_match_score

from app.evaluation.benchmark_question import test_cases


def evaluate_retrieval(
    chunks: list[dict],
    top_k: int,
    questions: list[dict]
) -> dict:
    """
    Build retriever and evaluate retrieval relevance using benchmark questions.
    """
    print("Building temporary FAISS index for benchmark...")

    retriever = ResearchRetriever()
    retriever.build_index(chunks)

    scores = []
    detailed_results = []

    print(f"Evaluating {len(questions)} benchmark questions...")

    for index, case in enumerate(questions, start=1):
        question = case["question"]
        expected_keywords = case["expected_keywords"]

        retrieved_chunks = retriever.retrieve(
            query=question,
            top_k=top_k
        )

        retrieved_context = " ".join(
            [chunk["text"] for chunk in retrieved_chunks]
        )

        score = keyword_match_score(
            text=retrieved_context,
            expected_keywords=expected_keywords
        )

        matched_keywords = [
            keyword for keyword in expected_keywords
            if keyword.lower() in retrieved_context.lower()
        ]

        scores.append(score)

        detailed_results.append({
            "question_number": index,
            "question": question,
            "expected_keywords": expected_keywords,
            "matched_keywords": matched_keywords,
            "score_percent": round(score * 100, 2),
            "retrieved_sources": [
                {
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"]
                }
                for chunk in retrieved_chunks
            ]
        })

        print(
            f"Question {index}/{len(questions)} "
            f"score: {round(score * 100, 2)}%"
        )

    average_score = sum(scores) / len(scores) if scores else 0.0

    return {
        "questions_evaluated": len(questions),
        "average_retrieval_relevance_percent": round(average_score * 100, 2),
        "detailed_results": detailed_results
    }


def run_retrieval_benchmark() -> dict:
    """
    Compare baseline retrieval setup against optimized retrieval setup.
    """
    print("\nLoading PDFs from papers folder...")

    pdf_texts = load_pdfs(UPLOAD_DIR)

    if not pdf_texts:
        raise FileNotFoundError(
            "No PDF files found in papers folder. Upload PDFs first."
        )

    print(f"Documents loaded: {len(pdf_texts)}")

    print("\nCreating baseline chunks...")
    baseline_chunks = chunk_documents(
        pdf_texts=pdf_texts,
        chunk_size=500,
        overlap=100
    )

    print(f"Baseline chunks: {len(baseline_chunks)}")

    baseline_eval = evaluate_retrieval(
        chunks=baseline_chunks,
        top_k=5,
        questions=test_cases
    )

    print("\nCreating optimized chunks...")
    optimized_chunks = chunk_documents(
        pdf_texts=pdf_texts,
        chunk_size=CHUNK_SIZE,
        overlap=CHUNK_OVERLAP
    )

    print(f"Optimized chunks: {len(optimized_chunks)}")

    optimized_eval = evaluate_retrieval(
        chunks=optimized_chunks,
        top_k=TOP_K,
        questions=test_cases
    )

    baseline_score = baseline_eval["average_retrieval_relevance_percent"]
    optimized_score = optimized_eval["average_retrieval_relevance_percent"]

    benchmark = {
        "generated_at": datetime.now().isoformat(),
        "benchmark_dataset": "app/evaluation/benchmark_question.py",
        "total_questions": len(test_cases),
        "baseline": {
            "chunk_size": 300,
            "chunk_overlap": 50,
            "top_k": 2,
            "total_chunks": len(baseline_chunks),
            "retrieval_relevance_percent": baseline_score
        },
        "optimized": {
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP,
            "top_k": TOP_K,
            "total_chunks": len(optimized_chunks),
            "retrieval_relevance_percent": optimized_score
        },
        "improvement_percentage_points": round(
            optimized_score - baseline_score,
            2
        ),
        "baseline_details": baseline_eval["detailed_results"],
        "optimized_details": optimized_eval["detailed_results"]
    }

    Path(REPORT_DIR).mkdir(exist_ok=True)

    report_path = Path(REPORT_DIR) / "retrieval_benchmark.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(benchmark, file, indent=4)

    return benchmark


if __name__ == "__main__":
    benchmark = run_retrieval_benchmark()

    print("\nRetrieval Benchmark")
    print("-------------------")
    print(f"Questions evaluated: {benchmark['total_questions']}")
    print(f"Baseline chunks: {benchmark['baseline']['total_chunks']}")
    print(f"Optimized chunks: {benchmark['optimized']['total_chunks']}")
    print(f"Baseline relevance: {benchmark['baseline']['retrieval_relevance_percent']}%")
    print(f"Optimized relevance: {benchmark['optimized']['retrieval_relevance_percent']}%")
    print(f"Improvement: {benchmark['improvement_percentage_points']} percentage points")
    print("\nSaved report: reports/retrieval_benchmark.json")