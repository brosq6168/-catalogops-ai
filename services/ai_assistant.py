import os
from typing import Dict, Optional
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI

# 1. Define strict schemas for the AI's output to prevent text hallucinations
class OperationalDraft(BaseModel):
    subject: str = Field(description="Professional, concise email subject line referencing the SKU.")
    body: str = Field(description="Polished, clear email body explaining the catalog discrepancies and required actions.")
    summary: str = Field(description="A concise 1-sentence analytical summary of the issue for the internal operations log.")

def get_ai_client() -> Optional[instructor.Instructor]:
    """Initializes the patched OpenAI client if an API key is present."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        return instructor.from_openai(OpenAI(api_key=api_key))
    except Exception:
        return None

def process_catalog_exception(exception: Dict) -> OperationalDraft:
    """
    Orchestrates the AI generation layer. 
    Dynamically switches between production LLM endpoints and a local failover system.
    """
    sku = exception.get("sku", "Unknown SKU")
    issue_type = exception.get("issue_type", "Catalog Discrepancy")
    severity = exception.get("severity", "Medium")
    description = exception.get("issue_description", "The catalog record needs clarification.")
    action = exception.get("suggested_action", "Review the record.")

    client = get_ai_client()
    
    # --- PRODUCTION MODE: Live LLM Processing ---
    if client and os.getenv("AI_MODE", "production") == "production":
        try:
            # Force the model to return structured data matching our Pydantic schema
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_model=OperationalDraft,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an elite E-commerce AI Operations assistant. Draft professional, clear communications to suppliers regarding inventory anomalies."
                    },
                    {
                        "role": "user", 
                        "content": f"SKU: {sku}\nIssue Type: {issue_type}\nSeverity: {severity}\nDescription: {description}\nRecommended Action: {action}"
                    }
                ],
                temperature=0.2 # Keep creativity low for reliable operational summaries
            )
            return response
        except Exception:
            # Silent failover to fallback mode if the network or API keys fail
            pass

    # --- FAILOVER MODE: Deterministic Fallback Engine ---
    fallback_subject = f"Subject: Clarification needed for {sku}"
    fallback_body = (
        f"Hello,\n\nWe are reviewing the catalog record for {sku}. "
        f"{description} Please confirm the correct information so we can complete the catalog record.\n\n"
        "Kind regards,\nCatalog Operations"
    )
    fallback_summary = f"{issue_type} ({severity} priority). Recommended action: {action}"
    
    return OperationalDraft(
        subject=fallback_subject,
        body=fallback_body,
        summary=fallback_summary
    )

def get_ai_mode() -> str:
    """Dynamically returns the operational state of the AI framework."""
    if os.getenv("OPENAI_API_KEY") and os.getenv("AI_MODE", "production") == "production":
        return "Production Mode (OpenAI GPT-4o-mini)"
    return "Local Fallback Mode (Deterministic)"
