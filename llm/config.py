from pydantic import BaseModel, Field
from nonebot import get_plugin_config


BaseModel.model_config["protected_namespaces"] = ()


class ScopedConfig(BaseModel):
    api_key: str = Field(None, doc="大模型 api_key")
    platform: str = Field(None, doc="大模型访问平台")
    model_name: str = Field(None, doc="选用的大模型名称")
    tavily_api_key: str = Field(None, doc="Tavily 聚合搜索 api_key，但准备弃用")


class Config(BaseModel):
    """AI Agents"""
    with_ai_agents: ScopedConfig


plugin_config = get_plugin_config(Config).with_ai_agents
config = plugin_config

print("With_AI_Agents: api_key=", config.api_key)
print("With_AI_Agents: platform=", config.platform)
print("With_AI_Agents: model_name=", config.model_name)
print("With_AI_Agents：tavily_api_key=", config.tavily_api_key)
