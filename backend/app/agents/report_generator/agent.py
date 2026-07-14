import os

from app.agents.base_agent import BaseAgent


class ReportGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Report Generator Agent",
            prompt_file=os.path.join(
                os.path.dirname(__file__),
                "prompt.txt",
            ),
        )

    async def analyze(
        self,
        project_data: dict,
        agent_results: dict,
    ) -> dict:
        result = await self.run(
            {
                "project_data": project_data,
                "agent_results": agent_results,
            }
        )

        return result