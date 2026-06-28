from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Category(str, Enum):
    SECURITY = "SECURITY"
    SCALABILITY = "SCALABILITY"
    RELIABILITY = "RELIABILITY"
    GCP_BEST_PRACTICES = "GCP_BEST_PRACTICES"
    FINOPS = "FINOPS"

class ArchitectureComponent(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)

class DataFlow(BaseModel):
    source: str
    target: str
    protocol: Optional[str] = None
    description: Optional[str] = None

class SystemArchitecture(BaseModel):
    system_name: str
    components: List[ArchitectureComponent]
    data_flows: List[DataFlow]
    dependencies: List[str]
    assumptions: List[str]
    unknowns: List[str]

class Finding(BaseModel):
    category: Category
    severity: Severity
    title: str
    description: str
    recommendation: str

class AgentReview(BaseModel):
    agent_name: str
    findings: List[Finding]

class ArchitectureScores(BaseModel):
    security: float
    scalability: float
    reliability: float
    cost: float
    cloud_native_maturity: float

class CorrectedArchitecture(BaseModel):
    system_name: str
    components: List[ArchitectureComponent]
    data_flows: List[DataFlow]
    changes_made: List[str]
    migration_guidance: List[str] = Field(default_factory=list)

class AnalysisResult(BaseModel):
    original_architecture: SystemArchitecture
    agent_reviews: List[AgentReview]
    synthesis_report: Dict[str, Any]
    scores: ArchitectureScores
    corrected_architecture: CorrectedArchitecture
    mermaid_diagram: str
    graph_model: Dict[str, Any]
    executive_summary: str = ""
