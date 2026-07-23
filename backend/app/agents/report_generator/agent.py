import os
from typing import Any

from app.agents.base_agent import BaseAgent


class ReportGeneratorAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Report Generator Agent",
            prompt_file=os.path.join(
                os.path.dirname(__file__),
                "prompt.txt",
            ),
        )

    async def analyze(
        self,
        project_data: dict[str, Any],
        agent_results: dict[str, Any],
    ) -> dict[str, Any]:
        result = await self.run(
            {
                "project_data": project_data,
                "agent_results": agent_results,
            }
        )

        if not isinstance(result, dict):
            result = {
                "agent": self.name,
                "status": "failed",
                "analysis": {},
                "error": (
                    "Report generation returned "
                    "an invalid result."
                ),
            }

        return result