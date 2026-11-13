import json
import logging
import urllib.request
from typing import Any

from providers import register_provider
from providers.base import ProviderProfile

logger = logging.getLogger(__name__)

_USER_AGENT = "hermes-morph/1.0.0"


class MorphProfile(ProviderProfile):
    def fetch_models(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 8.0,
    ) -> list[str] | None:
        """Chat models only.

        Morph's ``/models`` also lists its Fast Apply, WarpGrep and compaction
        models, which cannot drive an agent loop. The gateway marks chat models
        by publishing ``supported_parameters`` on their rows.
        """
        effective_base = (base_url or "").strip() or self.base_url
        req = urllib.request.Request(effective_base.rstrip("/") + "/models")
        if api_key:
            req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", _USER_AGENT)
        try:
            from hermes_cli.urllib_security import open_credentialed_url

            with open_credentialed_url(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode())
        except Exception as exc:
            logger.debug("fetch_models(%s): %s", self.name, exc, exc_info=True)
            return None
        items = data if isinstance(data, list) else data.get("data", [])
        models = [
            item["id"]
            for item in items
            if isinstance(item, dict)
            and item.get("id")
            and item.get("supported_parameters")
        ]
        return models or None

    def build_api_kwargs_extras(
        self,
        *,
        reasoning_config: dict | None = None,
        **context: Any,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Forward an explicit reasoning choice as top-level ``reasoning_effort``.

        Unset leaves each model on its served default.
        """
        if not isinstance(reasoning_config, dict):
            return {}, {}
        if reasoning_config.get("enabled") is False:
            return {}, {"reasoning_effort": "none"}
        effort = str(reasoning_config.get("effort") or "").strip().lower()
        return {}, ({"reasoning_effort": effort} if effort else {})


morph = MorphProfile(
    name="morph",
    aliases=("morphllm",),
    display_name="Morph",
    description="Morph: open models (Kimi, GLM, DeepSeek, Qwen, MiniMax) on an OpenAI-compatible API",
    signup_url="https://www.morphllm.com/dashboard/api-keys",
    env_vars=("MORPH_API_KEY", "MORPH_BASE_URL"),
    base_url="https://api.morphllm.com/v1",
    default_headers={"User-Agent": _USER_AGENT},
)

register_provider(morph)
