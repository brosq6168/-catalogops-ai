import os
import pytest
from pydantic import BaseModel
from services.ai_assistant import process_catalog_exception, get_ai_mode, OperationalDraft

@pytest.fixture
def mock_exception_data():
    return {
        "sku": "TEST-SKU-99",
        "issue_type": "Invalid Price",
        "severity": "high",
        "issue_description": "The item price is set to a negative integer.",
        "suggested_action": "Contact vendor to confirm accurate pricing matrix."
    }

def test_fallback_mode_generation_contract(mock_exception_data, monkeypatch):
    """
    Ensure that when no API key is present, the failover path 
    fires seamlessly and returns the strict Pydantic OperationalDraft model.
    """
    # Force environmental state to simulate an unconfigured layout
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("AI_MODE", "production")
    
    # Run pipeline execution 
    result = process_catalog_exception(mock_exception_data)
    
    # Assert structural type constraints
    assert isinstance(result, OperationalDraft)
    assert isinstance(result, BaseModel)
    
    # Verify core business payload properties are intact
    assert "TEST-SKU-99" in result.subject
    assert "Invalid Price" in result.summary
    assert "high priority" in result.summary.lower()
    assert "Contact vendor" in result.summary

def test_ai_mode_string_leakage(monkeypatch):
    """Verify system reporting metrics match configurations exactly."""
    # Test Fallback Reporting
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert "Fallback" in get_ai_mode()
    
    # Test Production Mode Mapping
    monkeypatch.setenv("OPENAI_API_KEY", "sk-mock-key-string-payload")
    monkeypatch.setenv("AI_MODE", "production")
    assert "Production Mode" in get_ai_mode()
