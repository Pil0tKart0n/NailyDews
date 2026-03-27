import json
import logging
from decimal import Decimal

import httpx
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.models import LLMUsage

logger = logging.getLogger(__name__)

# Cost per 1M tokens
MODEL_COSTS = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
}

# Model aliases for easy switching
CHEAP = "gemini-2.0-flash"   # Filter, categorize, confidence (free tier)
QUALITY = "gpt-4o-mini"       # Summaries, headlines, editorial


class GeminiClient:
    """Google Gemini API client (REST, no SDK needed)."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.http = httpx.AsyncClient(timeout=60.0)

    async def complete(self, prompt: str, system: str = "", model: str = "gemini-2.0-flash",
                       max_tokens: int = 1024, temperature: float = 0.0) -> tuple[str, int, int]:
        """Send request to Gemini. Returns (text, input_tokens, output_tokens)."""
        url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"

        contents = []
        if system:
            contents.append({"role": "user", "parts": [{"text": system}]})
            contents.append({"role": "model", "parts": [{"text": "Understood. I will follow these instructions."}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        body = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "responseMimeType": "application/json",
            },
        }

        response = await self.http.post(url, json=body)
        response.raise_for_status()
        data = response.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]
        usage = data.get("usageMetadata", {})
        input_tokens = usage.get("promptTokenCount", 0)
        output_tokens = usage.get("candidatesTokenCount", 0)

        return text, input_tokens, output_tokens


class LLMClient:
    """Unified LLM client: Gemini Flash for cheap tasks, GPT-4o-mini for quality tasks."""

    def __init__(self):
        self.openai = AsyncOpenAI(api_key=settings.openai_api_key)
        self.gemini = GeminiClient(api_key=settings.gemini_api_key)

    async def complete(
        self,
        prompt: str,
        system: str = "",
        model: str = CHEAP,
        max_tokens: int = 1024,
        temperature: float = 0.0,
        db: AsyncSession | None = None,
        task: str = "",
        article_id: int | None = None,
    ) -> str:
        """Send completion to appropriate provider based on model."""

        if model.startswith("gpt"):
            # OpenAI
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            response = await self.openai.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                response_format={"type": "json_object"},
            )

            result = response.choices[0].message.content or ""
            input_tokens = response.usage.prompt_tokens if response.usage else 0
            output_tokens = response.usage.completion_tokens if response.usage else 0

        elif model.startswith("gemini"):
            # Google Gemini
            result, input_tokens, output_tokens = await self.gemini.complete(
                prompt=prompt,
                system=system,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
            )

        else:
            raise ValueError(f"Unknown model: {model}")

        # Track costs
        if db and task:
            costs = MODEL_COSTS.get(model, {"input": 0, "output": 0})
            cost_usd = (
                (input_tokens * costs["input"] / 1_000_000)
                + (output_tokens * costs["output"] / 1_000_000)
            )
            db.add(LLMUsage(
                model=model,
                task=task,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=Decimal(str(round(cost_usd, 6))),
                article_id=article_id,
            ))

        return result

    async def complete_json(
        self,
        prompt: str,
        system: str = "",
        model: str = CHEAP,
        max_tokens: int = 1024,
        db: AsyncSession | None = None,
        task: str = "",
        article_id: int | None = None,
    ) -> dict | list:
        """Send completion and parse JSON response."""
        result = await self.complete(
            prompt=prompt,
            system=system,
            model=model,
            max_tokens=max_tokens,
            db=db,
            task=task,
            article_id=article_id,
        )

        text = result.strip()
        # Handle markdown code blocks
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])

        return json.loads(text)


llm_client = LLMClient()
