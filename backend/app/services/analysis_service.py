import asyncio

from app.agents.accessibility.agent import AccessibilityAgent
from app.agents.architecture_review.agent import (
    ArchitectureReviewAgent,
)
from app.agents.building_code.agent import BuildingCodeAgent
from app.agents.cost.agent import CostAgent
from app.agents.design_analyzer.agent import (
    DesignAnalyzerAgent,
)
from app.agents.energy.agent import EnergyAgent
from app.agents.lighting.agent import LightingAgent
from app.agents.report_generator.agent import (
    ReportGeneratorAgent,
)
from app.agents.sustainability.agent import SustainabilityAgent
from app.agents.ventilation.agent import VentilationAgent


class AnalysisService:
    def __init__(self):
        self.design_agent = DesignAnalyzerAgent()
        self.architecture_agent = ArchitectureReviewAgent()
        self.sustainability_agent = SustainabilityAgent()
        self.energy_agent = EnergyAgent()
        self.ventilation_agent = VentilationAgent()
        self.lighting_agent = LightingAgent()
        self.accessibility_agent = AccessibilityAgent()
        self.building_code_agent = BuildingCodeAgent()
        self.cost_agent = CostAgent()
        self.report_agent = ReportGeneratorAgent()

    async def analyze_project(
        self,
        project_data: dict,
        image_path: str | None = None,
    ) -> dict:
        design_result = await self.design_agent.analyze(
            project_data=project_data,
            image_path=image_path,
        )

        enhanced_project_data = {
            **project_data,
            "design_analysis": design_result,
        }

        results = await asyncio.gather(
            self.architecture_agent.analyze(
                enhanced_project_data
            ),
            self.sustainability_agent.analyze(
                enhanced_project_data
            ),
            self.energy_agent.analyze(
                enhanced_project_data
            ),
            self.ventilation_agent.analyze(
                enhanced_project_data
            ),
            self.lighting_agent.analyze(
                enhanced_project_data
            ),
            self.accessibility_agent.analyze(
                enhanced_project_data
            ),
            self.building_code_agent.analyze(
                enhanced_project_data
            ),
            self.cost_agent.analyze(
                enhanced_project_data
            ),
        )

        agent_results = {
            "design_analyzer": design_result,
            "architecture_review": results[0],
            "sustainability": results[1],
            "energy": results[2],
            "ventilation": results[3],
            "lighting": results[4],
            "accessibility": results[5],
            "building_code": results[6],
            "cost": results[7],
        }

        final_report = await self.report_agent.analyze(
            project_data=enhanced_project_data,
            agent_results=agent_results,
        )

        return {
            "status": "completed",
            "agents": agent_results,
            "final_report": final_report,
        }