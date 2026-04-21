import os
import torch
from functools import lru_cache
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

from app.config import (
    BASE_MODEL_NAME,
    FINETUNED_ADAPTER_PATH,
    MAX_NEW_TOKENS,
    TEMPERATURE,
    TOP_P,
)


def _chunk_to_text(chunk):
    """
    Supports:
    - plain strings
    - metadata dicts: {"chunk": ..., "pdf": ..., "page": ...}
    """
    if isinstance(chunk, str):
        return chunk

    if isinstance(chunk, dict):
        text = chunk.get("chunk", "")
        pdf = chunk.get("pdf", "unknown.pdf")
        page = chunk.get("page", "N/A")
        return f"[Source: {pdf}, Page: {page}]\n{text}"

    return str(chunk)


def _build_prompt(context_chunks, query):
    context = "\n\n".join([_chunk_to_text(c) for c in context_chunks])

    prompt = f"""
You are a research paper assistant.

Answer the user's question using ONLY the retrieved context below.
If the context is insufficient, say that clearly.
Do not invent facts.

Retrieved Context:
{context}

Question:
{query}

Return the answer in EXACTLY this format:

Summary:
<2-4 grounded sentences>

Method:
<brief methodology description if available in context; otherwise say not clearly specified>

Key Findings:
- finding 1
- finding 2
- finding 3

Limitations:
<limitations, caveats, or missing details from context>

Conclusion:
<final grounded answer>
"""
    return prompt.strip()


@lru_cache(maxsize=1)
def _load_base_model():
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto"
    )
    return tokenizer, model


@lru_cache(maxsize=1)
def _load_finetuned_model():
    tokenizer, base_model = _load_base_model()

    if not os.path.exists(FINETUNED_ADAPTER_PATH):
        return tokenizer, base_model, False

    ft_model = PeftModel.from_pretrained(base_model, FINETUNED_ADAPTER_PATH)
    return tokenizer, ft_model, True


def generate_answer(context_chunks, query, mode="base"):
    prompt = _build_prompt(context_chunks, query)

    if mode == "finetuned":
        tokenizer, model, loaded = _load_finetuned_model()
        if not loaded:
            tokenizer, model = _load_base_model()
    else:
        tokenizer, model = _load_base_model()

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=True,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            pad_token_id=tokenizer.eos_token_id,
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if prompt in decoded:
        decoded = decoded.replace(prompt, "").strip()

    return decoded.strip()