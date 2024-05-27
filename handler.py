from nonebot.plugin import on_message, on_command
from nonebot.rule import to_me, regex
from nonebot.adapters import Event

from .llm import central_brain
from .llm.services import ChatService
from .llm.config import config

agents = on_message(rule=to_me() & regex(fr"^{config.message_start}.*"), priority=config.priority, block=True)
command = on_command("清理AI聊天记录", priority=13, block=True)


@agents.handle()
async def agent_handler(event: Event):
    """中央处理器"""
    question = event.get_message().extract_plain_text()
    ans = await central_brain.ask_central_brain(question)
    await agents.finish(ans)


@command.handle()
async def command_handler():
    count = ChatService.clear_chat_history()
    result = f"OK, 共清理 {count} 条记录"
    await command.finish(result)
