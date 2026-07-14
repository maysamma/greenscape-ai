import os

from app.agents.architecture_review.tools import (
    calculate_space_efficiency,
)
from app.agents.base_agent import BaseAgent


class ArchitectureReviewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Architecture Review Agent",
            prompt_file=os.path.join(
                os.path.dirname(__file__),
                "prompt.txt",
            ),
        )

    async def analyze(self, project_data: dict) -> dict:
        metrics = calculate_space_efficiency(project_data)

        result = await self.run(
            {
                "project_data": project_data,
                "calculated_metrics": metrics,
            }
        )

        result["metrics"] = metrics

        return result