import os

from app.agents.base_agent import BaseAgent
from app.agents.cost.tools import estimate_project_cost


class CostAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Cost Optimization Agent",
            prompt_file=os.path.join(
                os.path.dirname(__file__),
                "prompt.txt",
            ),
        )

    async def analyze(self, project_data: dict) -> dict:
        metrics = estimate_project_cost(project_data)

        result = await self.run(
            {
                "project_data": project_data,
                "calculated_metrics": metrics,
            }
        )

        result["metrics"] = metrics

        return result