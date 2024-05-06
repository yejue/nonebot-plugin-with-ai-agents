from nonebot.plugin import PluginMetadata

from .handler import agents
from .llm.config import Config

__plugin_meta__ = PluginMetadata(
    name="with_ai_agents",
    description="AI 智能体，提供 AI 本身的通用聊天功能与诸如联网、网页内容总结等附加能力",
    usage="无特定用法，聊天即可，可以通过询问功能来查看有哪些用法",
    config=Config,
)
