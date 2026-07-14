import os

from app.agents.accessibility.tools import (
    calculate_accessibility_score,
)
from app.agents.base_agent import BaseAgent


class AccessibilityAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Accessibility Agent",
            prompt_file=os.path.join(
                os.path.dirname(__file__),
                "prompt.txt",
            ),
        )

    async def analyze(self, project_data: dict) -> dict:
        metrics = calculate_accessibility_score(project_data)

        result = await self.run(
            {
                "project_data": project_data,
                "calculated_metrics": metrics,
            }
        )

        result["metrics"] = metrics

        return result