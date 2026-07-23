import os
from typing import Any

from app.agents.base_agent import BaseAgent


class ArchitectureReviewAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Architecture Review Agent",
            prompt_file=os.path.join(
                os.path.dirname(__file__),
                "prompt.txt",
            ),
        )

    async def analyze(
        self,
        project_data: dict[str, Any],
        design_analysis: dict[str, Any],
    ) -> dict[str, Any]:
        agent_input = {
            "project_data": project_data,
            "design_analysis": design_analysis,
        }

        result = await self.run(agent_input)

        if not isinstance(result, dict):
            result = {
                "agent": self.name,
                "status": "failed",
                "analysis": {},
                "error": "Architecture review returned an invalid result.",
            }

        return result