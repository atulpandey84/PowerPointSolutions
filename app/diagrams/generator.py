from typing import Dict, Any, Union
from app.models.architecture import SystemArchitecture, CorrectedArchitecture

class DiagramGenerator:
    def generate_mermaid(self, arch: Union[SystemArchitecture, CorrectedArchitecture]) -> str:
        lines = ["graph TD"]

        # Add nodes
        for comp in arch.components:
            # Clean name for Mermaid compatibility
            safe_id = comp.name.replace(" ", "_").replace("-", "_")
            lines.append(f'    {safe_id}["{comp.name} ({comp.type})"]')

        # Add edges
        for flow in arch.data_flows:
            src_id = flow.source.replace(" ", "_").replace("-", "_")
            tgt_id = flow.target.replace(" ", "_").replace("-", "_")
            label = f"|{flow.protocol}|" if flow.protocol else ""
            lines.append(f'    {src_id} -->{label} {tgt_id}')

        return "\n".join(lines)

    def generate_graph_model(self, arch: Union[SystemArchitecture, CorrectedArchitecture]) -> Dict[str, Any]:
        nodes = []
        for comp in arch.components:
            nodes.append({
                "id": comp.name,
                "label": comp.name,
                "type": comp.type,
                "properties": comp.properties
            })

        edges = []
        for flow in arch.data_flows:
            edges.append({
                "source": flow.source,
                "target": flow.target,
                "protocol": flow.protocol,
                "description": flow.description
            })

        return {
            "nodes": nodes,
            "edges": edges
        }
