"""
控制型 AI：最表层的 AI，用于分类和其他 AI 的调用决策
"""
import json

from . import qwen, agents, glm
from .config import config
from .utils import prompts
from .services import ChatService


def get_llm_model(platform: str = "tongyi", api_key: str = None):
    """获取大模型的询问工具"""
    if platform == "tongyi":
        llm = qwen.QWenModel(api_key=api_key)
        return llm
    elif platform == "glm":
        llm = glm.GLMModel(api_key=api_key)
        return llm
    return None


async def ask_central_brain(raw_question: str):
    """向中心智脑提问"""

    # 选择智脑使用的大模型
    llm = get_llm_model(config.AI_AGENT_PLATFORM, config.AI_AGENT_KEY)

    # 获取聊天历史
    chat_history_list = ChatService.get_history_list()

    # 将用户提问发送到大模型分类器，获取分类列表
    prompt = prompts.get_classifier_prompt().format(question=raw_question)
    s = prompts.get_classifier_master_prompt()
    classifier_res = await llm.ask_model(question=prompt, system_prompt=s)
    print(f"raw_classifier_res: {classifier_res}")
    classifier_res = json.loads(classifier_res)
    print(f"智脑分类结果：{classifier_res}")

    # 遍历分类列表，向 agents 发送任务并获取 context
    agent_data = ""

    for num in classifier_res:
        if int(num) == 1:    # 提取页面内容
            agent_data += await agents.type1.summarize_weblink_content(llm=llm, question=raw_question) + "\n"
        elif int(num) == 2:  # 联网搜索能力
            agent_data += await agents.type2.get_search_result(llm=llm, question=raw_question)
        elif int(num) == 3:  # 某地天气
            pass
        elif int(num) == 4:  # 执行指令
            pass
        elif int(num) == 5:  # who are you
            agent_data += agents.type5.get_who_you_are() + "\n"
        elif int(num) == 6:  # 功能列表
            agent_data += agents.type6.get_ai_abilities() + "\n"

    # 携带 context 向大模型提问 raw_question
    assemble_prompt = prompts.get_assemble_prompt(question=raw_question, agent_data=agent_data)
    print("assemble_prompt", assemble_prompt)
    s = prompts.get_kurisu_prompt()
    assemble_res = await llm.ask_model(question=assemble_prompt, system_prompt=s, message_history=chat_history_list)

    # 将 AI 回答追加到历史
    ChatService.add_message_to_history(text=assemble_prompt, role="user")
    ChatService.add_message_to_history(text=assemble_res, role="assistant")

    return assemble_res
