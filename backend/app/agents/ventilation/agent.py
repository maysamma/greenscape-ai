import os

from app.agents.base_agent import BaseAgent
from app.agents.ventilation.tools import (
    calculate_ventilation_score,
)


class VentilationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Ventilation Agent",
            prompt_file=os.path.join(
                os.path.dirname(__file__),
                "prompt.txt",
            ),
        )

    async def analyze(self, project_data: dict) -> dict:
        metrics = calculate_ventilation_score(project_data)

        result = await self.run(
            {
                "project_data": project_data,
                "calculated_metrics": metrics,
            }
        )

        result["metrics"] = metrics

        return result