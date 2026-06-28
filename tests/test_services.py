import pytest
from app.models.architecture import SystemArchitecture, ArchitectureComponent, DataFlow, AgentReview, Finding, Category, Severity
from app.services.synthesis_service import SynthesisService
from app.diagrams.generator import DiagramGenerator

def test_synthesis_score_calculation():
    service = SynthesisService()
    findings = [
        Finding(
            category=Category.SECURITY,
            severity=Severity.CRITICAL,
            title="Test",
            description="Test",
            recommendation="Test"
        )
    ]
    review = AgentReview(agent_name="Security", findings=findings)
    scores = service._calculate_scores([review])
    assert scores.security == 80.0
    assert scores.scalability == 100.0

def test_diagram_generation():
    generator = DiagramGenerator()
    arch = SystemArchitecture(
        system_name="Test",
        components=[
            ArchitectureComponent(name="A", type="GCE"),
            ArchitectureComponent(name="B", type="Cloud SQL")
        ],
        data_flows=[
            DataFlow(source="A", target="B", protocol="SQL")
        ],
        dependencies=[],
        assumptions=[],
        unknowns=[]
    )
    mermaid = generator.generate_mermaid(arch)
    assert "graph TD" in mermaid
    assert "A" in mermaid
    assert "B" in mermaid
    assert "SQL" in mermaid

def test_graph_model_generation():
    generator = DiagramGenerator()
    arch = SystemArchitecture(
        system_name="Test",
        components=[
            ArchitectureComponent(name="A", type="GCE")
        ],
        data_flows=[],
        dependencies=[],
        assumptions=[],
        unknowns=[]
    )
    model = generator.generate_graph_model(arch)
    assert len(model["nodes"]) == 1
    assert model["nodes"][0]["id"] == "A"
