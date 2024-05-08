from nonebot.plugin import on_message
from nonebot.rule import to_me
from nonebot.adapters import Event

from .llm import central_brain

agents = on_message(rule=to_me(), priority=999, block=True)


@agents.handle()
async def agent_handler(event: Event):
    """中央处理器"""
    question = event.get_message().extract_plain_text()
    ans = await central_brain.ask_central_brain(question)
    await agents.finish(ans)
