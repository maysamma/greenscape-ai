import os

from app.agents.base_agent import BaseAgent
from app.agents.building_code.tools import (
    run_basic_code_checks,
)


class BuildingCodeAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Building Code Agent",
            prompt_file=os.path.join(
                os.path.dirname(__file__),
                "prompt.txt",
            ),
        )

    async def analyze(self, project_data: dict) -> dict:
        checks = run_basic_code_checks(project_data)

        result = await self.run(
            {
                "project_data": project_data,
                "preliminary_checks": checks,
            }
        )

        result["code_checks"] = checks

        return result