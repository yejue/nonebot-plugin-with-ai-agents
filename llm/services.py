import json

from nonebot.log import logger

from .mem_stores import chat_history
from .config import config
from .utils import prompts
from . import agents
from . import llms


class ChatService:
    """聊天控制类"""

    @staticmethod
    def add_message_to_history(text, role="user"):
        new_message = {"role": role, "content": text}
        chat_history.append(new_message)

    @staticmethod
    def get_history_list():
        return chat_history

    @staticmethod
    def compress_chat_history(max_length: int = 5 * 10000):
        global chat_history
        if len(chat_history) > max_length:
            chat_history = chat_history[-(max_length//2):]

    @staticmethod
    def clear_chat_history():
        global chat_history
        length = len(chat_history)
        chat_history = []
        return length

    @staticmethod
    def get_strategically_chat_history(new_prompt: str, max_length: int):
        """策略获取聊天历史
         - 从最大长度消耗掉 len(new_prompt) 个长度
         - 根据最大长度，从历史列表中提取项目，每提取一条消耗 len(item) 个长度
         - max_length <= 0 后不再继续
        """
        ChatService.compress_chat_history()

        use_chat_history_list = []

        if not chat_history:
            return []

        if len(new_prompt) > max_length:
            return use_chat_history_list

        max_length_count = max_length - len(new_prompt)
        flag = 1

        while max_length_count > 0 and flag <= len(chat_history):
            history_item = chat_history[-flag]
            max_length_count -= len(history_item["content"])
            if max_length_count > 0:
                use_chat_history_list.insert(0, history_item)

            flag += 1

        return use_chat_history_list


class AIService:
    """AI 相关控制类"""

    @staticmethod
    def get_assistant_prompt():
        """获取 AI 默认人格提示词"""
        if config.custom_soul:
            return config.custom_soul
        return prompts.get_kurisu_prompt()

    @staticmethod
    def get_llm():
        """获取大模型的询问工具"""
        platform = config.platform
        api_key = config.api_key
        model = config.model_name
        api_url = config.api_url

        platform_map = {
            "dashscope": llms.DashscopeModel,
            "glm": llms.GLMModel,
            "openai": llms.OpenAIModel,
        }

        platform = platform_map.get(platform, None)
        if not platform:
            return None

        llm = platform(api_key=api_key)

        if model:
            llm.model = model

        if api_url:
            llm.api_url = api_url

        return llm

    @staticmethod
    async def get_question_class(llm: llms.LLM_TYPE, raw_question: str):
        """获取问题分类"""
        # 将用户提问发送到大模型分类器，获取分类列表
        prompt = prompts.get_classifier_prompt(question=raw_question)
        s = prompts.get_classifier_master_prompt()

        try:
            classifier_res = await llm.ask_model(question=prompt, system_prompt=s)
            classifier_res = json.loads(classifier_res)
        except Exception as e:
            return False, str(e)

        return True, classifier_res

    @staticmethod
    async def get_assistant_context(llm: llms.LLM_TYPE, classifier_res: list, raw_question: str):
        """从 Agents 中获取 AI 的上下文"""
        agent_data = ""

        if len(classifier_res) == 1 and classifier_res[0] == 7:
            assemble_prompt = raw_question
        else:
            for num in classifier_res:
                if int(num) == 1:  # 提取页面内容
                    agent_data += await agents.type1.get_agent_context(llm=llm, question=raw_question)
                    agent_data += "\n"
                elif int(num) == 2:  # 联网搜索能力
                    agent_data += await agents.type2.get_agent_context(llm=llm, question=raw_question)
                    agent_data += "\n"
                elif int(num) == 3:  # 某地天气
                    pass
                elif int(num) == 4:  # 执行指令
                    pass
                elif int(num) == 5:  # who are you
                    agent_data += await agents.type5.get_agent_context()
                    agent_data += "\n"
                elif int(num) == 6:  # 功能列表
                    agent_data += await agents.type6.get_agent_context()
                    agent_data += "\n"
                elif int(num) == 8:  # 百科搜索能力
                    agent_data += await agents.type8.get_agent_context(llm=llm, question=raw_question)

            assemble_prompt = prompts.get_assemble_prompt(question=raw_question, agent_data=agent_data)

        return assemble_prompt

    @staticmethod
    async def ask_llm_with_agents(llm: llms.LLM_TYPE, classifier_res: list, raw_question):
        """携带 Agents 上下文向 LLM 提问"""
        try:
            # 获取上下文
            assemble_prompt = await AIService.get_assistant_context(llm, classifier_res, raw_question)
            logger.info("assemble_prompt", assemble_prompt)

            # 获取聊天历史
            chat_history_list = ChatService.get_strategically_chat_history(assemble_prompt, max_length=llm.max_length)

            # 发送正式提问
            s = AIService.get_assistant_prompt()

            assemble_res = await llm.ask_model(
                question=assemble_prompt,
                system_prompt=s,
                message_history=chat_history_list,
                temperature=0.3
            )

            # 将 AI 回答追加到历史
            ChatService.add_message_to_history(text=raw_question, role="user")
            ChatService.add_message_to_history(text=assemble_res, role="assistant")
        except Exception as e:
            return False, str(e)

        return True, assemble_res
