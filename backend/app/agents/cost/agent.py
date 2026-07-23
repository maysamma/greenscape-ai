import os
from typing import Any

from app.agents.base_agent import BaseAgent


class CostAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Cost Optimization Agent",
            prompt_file=os.path.join(
                os.path.dirname(__file__),
                "prompt.txt",
            ),
        )

    async def analyze(
        self,
        project_data: dict[str, Any],
        design_analysis: dict[str, Any],
        architecture_result: dict[str, Any],
        sustainability_result: dict[str, Any],
        energy_result: dict[str, Any],
        lighting_result: dict[str, Any],
        ventilation_result: dict[str, Any],
        accessibility_result: dict[str, Any],
        building_code_result: dict[str, Any],
    ) -> dict[str, Any]:
        agent_input = {
            "project_data": project_data,
            "design_analysis": design_analysis,
            "architecture_result": architecture_result,
            "sustainability_result": sustainability_result,
            "energy_result": energy_result,
            "lighting_result": lighting_result,
            "ventilation_result": ventilation_result,
            "accessibility_result": accessibility_result,
            "building_code_result": building_code_result,
        }

        result = await self.run(agent_input)

        if not isinstance(result, dict):
            result = {
                "agent": self.name,
                "status": "failed",
                "analysis": {},
                "error": (
                    "Cost optimization analysis returned "
                    "an invalid result."
                ),
            }

        return result