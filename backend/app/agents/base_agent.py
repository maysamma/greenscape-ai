import json
from pathlib import Path
from typing import Any

from app.services.llm import get_llm


class BaseAgent:
    def __init__(
        self,
        name: str,
        prompt_file: str,
    ):
        self.name = name
        self.prompt_file = Path(prompt_file)
        self.llm = get_llm()

        if not self.prompt_file.exists():
            raise FileNotFoundError(
                f"Prompt file not found: {self.prompt_file}"
            )

        self.system_prompt = self.prompt_file.read_text(
            encoding="utf-8"
        )

    async def run(self, input_data: Any) -> dict:
        serialized_input = json.dumps(
            input_data,
            ensure_ascii=False,
            indent=2,
            default=str,
        )

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            {
                "role": "user",
                "content": (
                    "Analyze the following GreenScape AI project data.\n\n"
                    f"{serialized_input}"
                ),
            },
        ]

        try:
            response = await self.llm.ainvoke(messages)

            content = (
                response.content
                if hasattr(response, "content")
                else str(response)
            )

            return {
                "agent": self.name,
                "status": "completed",
                "analysis": self.parse_json_response(content),
            }

        except Exception as error:
            return {
                "agent": self.name,
                "status": "failed",
                "analysis": {},
                "error": str(error),
            }

    @staticmethod
    def parse_json_response(content: str):
        cleaned = content.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]

        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError:
            return {
                "raw_response": content,
                "warning": "The model response was not valid JSON.",
            }