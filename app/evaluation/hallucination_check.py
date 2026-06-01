from pathlib import Path
import json
from datetime import datetime

from app.config import REPORT_DIR
from app.evaluation.evaluator import grounding_score, classify_grounding


def run_hallucination_check() -> dict:
    """
    Demonstrates grounding-quality difference between:
    1. an unguided answer
    2. a retrieval-grounded answer

    This is a lightweight project evaluation showing how retrieved context
    can reduce hallucination risk.
    """

    retrieved_context = """
    Retrieval-Augmented Generation combines a parametric language model
    with non-parametric memory retrieved from an external corpus.
    Relevant documents are retrieved and used as context during generation.
    This helps produce answers that are more factual, specific, and grounded
    in source documents.
    """

    unguided_answer = """
    Retrieval-Augmented Generation is a training algorithm that always updates
    all model weights and guarantees perfectly factual answers without needing
    any external documents or retrieved context.
    """

    grounded_answer = """
    Retrieval-Augmented Generation combines a language model with retrieved
    external documents. The retrieved context is used during generation to make
    answers more factual, specific, and grounded in source documents.
    """

    unguided_score = grounding_score(
        answer=unguided_answer,
        retrieved_context=retrieved_context
    )

    grounded_score = grounding_score(
        answer=grounded_answer,
        retrieved_context=retrieved_context
    )

    report = {
        "generated_at": datetime.now().isoformat(),
        "evaluation_method": "Grounding score based on answer overlap with retrieved context.",
        "retrieved_context": retrieved_context.strip(),
        "unguided_answer": {
            "answer": unguided_answer.strip(),
            "grounding_score": round(unguided_score, 4),
            "grounding_quality": classify_grounding(unguided_score)
        },
        "retrieval_grounded_answer": {
            "answer": grounded_answer.strip(),
            "grounding_score": round(grounded_score, 4),
            "grounding_quality": classify_grounding(grounded_score)
        },
        "grounding_controls": [
            "retrieve top-k chunks before generation",
            "inject retrieved context into the LLM prompt",
            "instruct the model to answer only from retrieved context",
            "separate retrieval and generation layers",
            "evaluate generated answers against retrieved context"
        ]
    }

    Path(REPORT_DIR).mkdir(exist_ok=True)

    report_path = Path(REPORT_DIR) / "hallucination_check.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return report


if __name__ == "__main__":
    report = run_hallucination_check()

    print("\nGrounding / Hallucination Check")
    print("-------------------------------")

    print("\nRetrieved Context:")
    print(report["retrieved_context"])

    print("\nUnguided Answer")
    print("---------------")
    print(report["unguided_answer"]["answer"])
    print(f"Grounding score: {report['unguided_answer']['grounding_score']}")
    print(f"Grounding quality: {report['unguided_answer']['grounding_quality']}")

    print("\nRetrieval-Grounded Answer")
    print("-------------------------")
    print(report["retrieval_grounded_answer"]["answer"])
    print(f"Grounding score: {report['retrieval_grounded_answer']['grounding_score']}")
    print(f"Grounding quality: {report['retrieval_grounded_answer']['grounding_quality']}")

    print("\nGrounding controls used:")
    for control in report["grounding_controls"]:
        print(f"- {control}")

    print("\nSaved report: reports/hallucination_check.json")