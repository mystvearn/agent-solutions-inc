"""Unit tests for the deterministic business logic in app/agent.py.

These cover the pure functions that the workflow's control flow depends on:
industry example generation, state merging, the drafting quality gate's
marker contract, and the security hardening applied to every agent.
"""

import pytest
from pydantic import ValidationError

from app.agent import (
    REQUIRED_PLAN_MARKERS,
    SECURITY_WARNING,
    DiscoveryRouting,
    OrchestratorRouting,
    _sanitize_for_mermaid,
    agent_drafting_agent,
    build_rag_tools,
    file_processor_agent,
    find_missing_plan_markers,
    generate_industry_example,
    merge_business_state,
    orchestrator_agent,
    rag_agent,
    value_discovery_agent,
)


# --- Mermaid example generation -------------------------------------------------

def test_sanitize_for_mermaid_strips_unsafe_characters():
    assert _sanitize_for_mermaid("Health & Med-Tech Co.") == "Health_and_Med_Tech_Co"


def test_sanitize_for_mermaid_empty_falls_back():
    assert _sanitize_for_mermaid("---") == "Process"


def test_industry_example_internal_process_uses_internal_template():
    """HR onboarding must NOT produce client/payment nodes (internal process)."""
    diagram = generate_industry_example("HR", "Employee Onboarding")
    assert diagram.startswith("```mermaid")
    assert "Request_Initiated" in diagram
    assert "Payment_Collection" not in diagram


def test_industry_example_external_process_uses_client_template():
    diagram = generate_industry_example("Residential Cleaning", "customer booking")
    assert "Client_Intake" in diagram
    assert "Payment_Collection" in diagram


# --- Checklist state merging ----------------------------------------------------

def test_merge_keeps_existing_when_update_omits_fields():
    current = {"industry": "HR", "it_systems": ["Workday"]}
    updated = {"corporate_priorities": "cut onboarding to 1 week"}
    merged = merge_business_state(current, updated)
    assert merged["industry"] == "HR"
    assert merged["it_systems"] == ["Workday"]
    assert merged["corporate_priorities"] == "cut onboarding to 1 week"


def test_merge_empty_values_never_erase_collected_data():
    current = {"industry": "HR", "activities": ["onboarding"], "past_experience": "chatbot failed"}
    updated = {"industry": None, "activities": [], "past_experience": ""}
    merged = merge_business_state(current, updated)
    assert merged == current


def test_merge_new_values_win():
    merged = merge_business_state({"industry": "HR"}, {"industry": "Cleaning Services"})
    assert merged["industry"] == "Cleaning Services"


def test_merge_handles_none_inputs():
    assert merge_business_state(None, None) == {}


# --- Drafting quality gate ------------------------------------------------------

def _compliant_plan() -> str:
    """Minimal text satisfying every marker in the gate contract."""
    return " ".join(REQUIRED_PLAN_MARKERS.keys())


def test_quality_gate_passes_compliant_plan():
    assert find_missing_plan_markers(_compliant_plan()) == []


def test_quality_gate_is_case_insensitive():
    assert find_missing_plan_markers(_compliant_plan().upper()) == []


def test_quality_gate_catches_missing_scaffold_command():
    plan = _compliant_plan().replace("agents-cli scaffold", "mkdir -p src")
    missing = find_missing_plan_markers(plan)
    assert len(missing) == 1
    assert "scaffold" in missing[0]


def test_quality_gate_rejects_non_adk_plan():
    """A plan built on the raw google-genai SDK must fail multiple markers."""
    plan = "# plan\nJust use the google-genai SDK and mkdir some folders."
    assert len(find_missing_plan_markers(plan)) == len(REQUIRED_PLAN_MARKERS)


def test_quality_gate_handles_empty_input():
    assert len(find_missing_plan_markers("")) == len(REQUIRED_PLAN_MARKERS)


# --- Security hardening ---------------------------------------------------------

@pytest.mark.parametrize("agent", [
    orchestrator_agent, rag_agent, file_processor_agent,
    value_discovery_agent, agent_drafting_agent,
], ids=lambda a: a.name)
def test_every_agent_carries_injection_warning(agent):
    """Every LLM agent's system prompt must include the anti-injection contract."""
    assert SECURITY_WARNING.strip() in agent.instruction


def test_orchestrator_route_is_schema_enforced():
    """Unknown routes must fail Pydantic validation, not reach the graph."""
    with pytest.raises(ValidationError):
        OrchestratorRouting(response_to_user="x", route="drop_all_tables", updated_state={})


def test_discovery_route_is_schema_enforced():
    with pytest.raises(ValidationError):
        DiscoveryRouting(response_to_user="x", route="skip_confirmation")


# --- RAG backend selection ------------------------------------------------------

def test_rag_falls_back_to_search_without_api_key(monkeypatch):
    monkeypatch.delenv("DEVELOPER_KNOWLEDGE_API_KEY", raising=False)
    tools = build_rag_tools()
    assert len(tools) == 1
    assert type(tools[0]).__name__ == "GoogleSearchTool"


def test_rag_uses_mcp_toolset_with_api_key(monkeypatch):
    monkeypatch.setenv("DEVELOPER_KNOWLEDGE_API_KEY", "test-key-not-real")
    tools = build_rag_tools()
    assert len(tools) == 1
    assert type(tools[0]).__name__ == "McpToolset"
