from pydantic import BaseModel
from nonebot import get_driver

global_config = get_driver().config


class Config(BaseModel):
    """AI Agents"""

    AI_AGENT_KEY: str = getattr(global_config, "ai_agent_key", None)
    AI_AGENT_PLATFORM: str = getattr(global_config, "ai_agent_platform", None)
    TAVILY_API_KEY: str = getattr(global_config, "tavily_api_key", None)


config = Config()
