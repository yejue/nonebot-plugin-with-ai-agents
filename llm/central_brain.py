"""
控制型 AI：最表层的 AI，用于分类和其他 AI 的调用决策
"""
from nonebot.log import logger

from .config import config
from .utils import prompts
from .services import ChatService, AIService


async def ask_central_brain(raw_question: str):
    """向中心智脑提问"""
    if not config:
        return "WITH_AI_AGENTS 配置获取失败，请检查配置。配置文档参考：https://github.com/yejue/nonebot-plugin-with-ai-agents"

    # 选择智脑使用的大模型
    llm = AIService.get_llm()
    if not llm:
        return "WITH_AI_AGENTS 大模型获取失败，请检查配置。配置文档参考：https://github.com/yejue/nonebot-plugin-with-ai-agents"

    # 获取分类信息
    try:
        classifier_res = await AIService.get_question_class(llm=llm, raw_question=raw_question)
    except Exception as e:
        logger.critical(e)
        return "分类失败，建议尝试更好的模型"
    logger.info(f"智脑分类结果：{classifier_res}")

    # 获取上下文
    assemble_prompt = await AIService.get_assistant_context(llm, classifier_res, raw_question)
    logger.info("assemble_prompt", assemble_prompt)

    # 获取聊天历史
    chat_history_list = ChatService.get_strategically_chat_history(assemble_prompt, max_length=llm.max_length)

    # 发送正式提问
    s = prompts.get_kurisu_prompt()
    assemble_res = await llm.ask_model(
        question=assemble_prompt,
        system_prompt=s,
        message_history=chat_history_list,
        temperature=0.3
    )

    # 将 AI 回答追加到历史
    ChatService.add_message_to_history(text=raw_question, role="user")
    ChatService.add_message_to_history(text=assemble_res, role="assistant")

    return assemble_res


async def ask_simple_llm(raw_question: str):
    """向普通 LLM 提问"""
    if not config:
        return "WITH_AI_AGENTS 配置获取失败，请检查配置。配置文档参考：https://github.com/yejue/nonebot-plugin-with-ai-agents"

    # 选择智脑使用的大模型
    llm = AIService.get_llm()
    if not llm:
        return "WITH_AI_AGENTS 大模型获取失败，请检查配置。配置文档参考：https://github.com/yejue/nonebot-plugin-with-ai-agents"

    # Chat History 策略获取
    chat_history_list = ChatService.get_strategically_chat_history(raw_question, max_length=llm.max_length)
    s = prompts.get_usagi_mini_prompt()
    assemble_res = await llm.ask_model(
        question=raw_question,
        system_prompt=s,
        message_history=chat_history_list,
        temperature=0.3
    )

    # 将 AI 回答追加到历史
    ChatService.add_message_to_history(text=raw_question, role="user")
    ChatService.add_message_to_history(text=assemble_res, role="assistant")

    return assemble_res
