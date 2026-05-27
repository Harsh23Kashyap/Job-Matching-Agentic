"""Unified resume and JD parse pipeline: clean text, rule extract, optional LLM merge."""
from __future__ import annotations

from core.job_structured_extract import extract_structured_job, merge_job_extraction
from core.profile_quality import analyze_profile_quality, quality_payload_from_extracted
from core.resume_clean import clean_resume_text, resume_preview_excerpt
from core.resume_structured_extract import extract_structured_resume, merge_resume_extraction
from hooks.llm_parser import LlmParseError, LlmParser, LlmUnavailableError


def clean_document_text(text: str) -> str:
    return clean_resume_text(text)


def _attach_profile_quality(result: dict) -> dict:
    extracted = result.get("extracted_fields") or {}
    payload = quality_payload_from_extracted(extracted)
    result["quality"] = analyze_profile_quality(
        payload,
        llm_status=result.get("llm_status"),
        extracted_fields=extracted,
    )
    return result


def parse_resume_document(raw_text: str, llm: LlmParser | None) -> dict:
    cleaned = clean_document_text(raw_text)
    rules = extract_structured_resume(cleaned)
    preview = resume_preview_excerpt(cleaned)

    if llm is None:
        return _attach_profile_quality(
            {
            "extracted_fields": rules,
            "raw_text_preview": preview,
            "cleaned_text": cleaned,
            "llm_status": "unavailable",
            "message": "Automatic extraction unavailable. Review the text preview and fill in details manually.",
            }
        )

    try:
        llm_fields = llm.parse_candidate_from_text(cleaned)
        extracted = merge_resume_extraction(rules, llm_fields)
        return _attach_profile_quality(
            {
            "extracted_fields": extracted,
            "raw_text_preview": preview,
            "cleaned_text": cleaned,
            "llm_status": "ok",
            }
        )
    except LlmUnavailableError:
        return _attach_profile_quality(
            {
            "extracted_fields": rules,
            "raw_text_preview": preview,
            "cleaned_text": cleaned,
            "llm_status": "unavailable",
            "message": "Automatic extraction unavailable. Review the text preview and fill in details manually.",
            }
        )
    except LlmParseError as exc:
        return _attach_profile_quality(
            {
            "extracted_fields": merge_resume_extraction(rules, None),
            "raw_text_preview": preview,
            "cleaned_text": cleaned,
            "llm_status": "parse_failed",
            "message": f"Could not parse resume automatically ({exc}). Fill in details manually.",
            }
        )


def parse_job_document(raw_text: str, llm: LlmParser | None) -> dict:
    cleaned = clean_document_text(raw_text)
    rules = extract_structured_job(cleaned)
    preview = resume_preview_excerpt(cleaned, limit=500)

    if llm is None:
        return {
            "extracted_fields": rules,
            "raw_text_preview": preview,
            "cleaned_text": cleaned,
            "llm_status": "unavailable",
            "message": "Automatic extraction unavailable. Review the text and fill in job details manually.",
        }

    try:
        llm_fields = llm.parse_job_from_text(cleaned)
        extracted = merge_job_extraction(rules, llm_fields)
        return {
            "extracted_fields": extracted,
            "raw_text_preview": preview,
            "cleaned_text": cleaned,
            "llm_status": "ok",
        }
    except LlmUnavailableError:
        return {
            "extracted_fields": rules,
            "raw_text_preview": preview,
            "cleaned_text": cleaned,
            "llm_status": "unavailable",
            "message": "Automatic extraction unavailable. Review the text and fill in job details manually.",
        }
    except LlmParseError as exc:
        return {
            "extracted_fields": merge_job_extraction(rules, None),
            "raw_text_preview": preview,
            "cleaned_text": cleaned,
            "llm_status": "parse_failed",
            "message": f"Could not parse job description automatically ({exc}). Fill in details manually.",
        }
