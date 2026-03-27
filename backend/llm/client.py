import json
import logging
from decimal import Decimal

import anthropic
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.models import LLMUsage

logger = logging.getLogger(__name__)

# Cost per 1M tokens (as of 2026)
MODEL_COSTS = {
    "claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
}

HAIKU = "claude-haiku-4-5-20251001"
SONNET = "claude-sonnet-4-6"


class LLMClient:
    """Wrapper around Anthropic API with cost tracking."""

    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def complete(
        self,
        prompt: str,
        system: str = "",
        model: str = HAIKU,
        max_tokens: int = 1024,
        temperature: float = 0.0,
        db: AsyncSession | None = None,
        task: str = "",
        article_id: int | None = None,
    ) -> str:
        """Send a completion request and track usage."""
        messages = [{"role": "user", "content": prompt}]

        response = await self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system if system else anthropic.NOT_GIVEN,
            messages=messages,
        )

        result = response.content[0].text
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

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
        model: str = HAIKU,
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

        # Try to extract JSON from response
        text = result.strip()
        # Handle markdown code blocks
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])

        return json.loads(text)


llm_client = LLMClient()
