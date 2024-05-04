from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg

from .llm import central_brain

agents = on_command("", rule=to_me(), priority=999, block=True)


@agents.handle()
async def agent_handler(args: Message = CommandArg()):
    """中央处理器"""
    if not args:
        return
    question = args.extract_plain_text()
    ans = await central_brain.ask_central_brain(question)
    await agents.finish(ans)
