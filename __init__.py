from nonebot.plugin import PluginMetadata

from .handler import agents
from .llm.config import Config

__plugin_meta__ = PluginMetadata(
    name="with_ai_agents",
    description="AI 智能体，提供联网学习能力、页面提取能力，以及 AI 能帮你做到的任何事。",
    usage=(
        "无特定用法，聊天即可，例子：\n"
        "https://arxiv.org/abs/2405.04952 这篇文章讲的是什么，是否有向量搜索的实际解决方案\n"
        "查一下最近有什么新闻\n"
    ),
    config=Config,
    homepage="https://github.com/yejue/nonebot-plugin-with-ai-agents",
    type="application"
)
