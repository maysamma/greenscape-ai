import os
from typing import Any

from app.agents.base_agent import BaseAgent


class SustainabilityAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Sustainability Agent",
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
    ) -> dict[str, Any]:
        agent_input = {
            "project_data": project_data,
            "design_analysis": design_analysis,
            "architecture_result": architecture_result,
        }

        result = await self.run(agent_input)

        if not isinstance(result, dict):
            result = {
                "agent": self.name,
                "status": "failed",
                "analysis": {},
                "error": (
                    "Sustainability analysis returned "
                    "an invalid result."
                ),
            }

        return result