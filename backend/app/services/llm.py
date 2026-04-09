from __future__ import annotations

import json
import re
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.core.config import settings


class LLMService:
    def __init__(self) -> None:
        self.enabled = bool(settings.openai_api_key)
        self.model = None
        if self.enabled:
            self.model = ChatOpenAI(
                model=settings.openai_model,
                temperature=0.2,
                api_key=settings.openai_api_key,
            )

    def _extract_json(self, text: str) -> dict[str, Any]:
        text = text.strip()

        # Case 1: direct JSON object
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        # Case 2: JSON inside ```json ... ```
        fenced_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
        if fenced_match:
            try:
                parsed = json.loads(fenced_match.group(1))
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        # Case 3: first JSON object-looking block
        object_match = re.search(r"\{.*\}", text, re.DOTALL)
        if object_match:
            try:
                parsed = json.loads(object_match.group(0))
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                pass

        raise ValueError("No valid JSON object found in model response.")

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        fallback: dict[str, Any],
    ) -> dict[str, Any]:
        if not self.enabled or self.model is None:
            return fallback

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
            response = self.model.invoke(messages)
            content = response.content if isinstance(response.content, str) else str(response.content)
            return self._extract_json(content)
        except Exception:
            return fallback


llm_service = LLMService()