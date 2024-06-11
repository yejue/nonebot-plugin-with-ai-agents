"""
agents 应该被写成一个目录，而 type 应该是一个 .py 文件
之所以这么写是因为开发时 with_ai_agents 是作为一个 NoneBot 项目的子目录，
为了避免在未知主目录的情况下，子文件引用上一级文件的情况，所以尽量写在了同一级中，
这是一个应该被修正的问题
"""
import re
import subprocess
from nonebot.log import logger

from .config import config
from .utils import prompts, retrievers
from .llms import LLM_TYPE


class BaseType:
    """Agents 基类"""

    async def get_agent_context(self, llm: LLM_TYPE, question: str):
        raise NotImplemented


class Type1(BaseType):
    """提取页面内容"""

    @staticmethod
    def extract_url_without_llm(question: str):
        """不使用 LLM 提取 URL 链接"""
        # 正则匹配 http 或 https 开头的 url
        # url_pattern = r'https?://[-\w.]+(?:[-\w/]|\.(?!\.))+'
        url_pattern = r'https?://[-\w.]+(?:[-\w/]|[-\w/?.&=%+])+'
        # 匹配第一个 URL
        match = re.search(url_pattern, question)
        return match.group(0) if match else None

    @staticmethod
    async def extreact_url_with_llm(llm: LLM_TYPE, question: str):
        """大模型提取 URL"""
        prompt = prompts.get_type1_prompt(question=question)
        url = await llm.ask_model(question=prompt)
        url = url.strip()
        return url

    @staticmethod
    async def summarize_weblink_content(llm: LLM_TYPE, question: str):
        # 从问题中提取 URL
        url = Type1.extract_url_without_llm(question=question)
        logger.info(f"type1 model res：{url}")
        if not url:
            return f"\"{url}\" 的大致内容是：内容提取失败"

        # 提取页面内容
        url_content = await retrievers.get_url_content(url)
        url_content = url_content[:3000]
        result = f"\"{url}\" 的大致内容是：{url_content}"
        return result

    async def get_agent_context(self, llm: LLM_TYPE, question: str):
        url = await self.summarize_weblink_content(llm=llm, question=question)
        return url


class Type2(BaseType):
    """联网查询"""

    @staticmethod
    async def get_search_result(llm: LLM_TYPE, question: str):
        prompt = prompts.get_type2_prompt(question=question)
        llm_res = await llm.ask_model(question=prompt)
        logger.info(f"需要联网搜索，llm_res={llm_res}")

        # 联网搜索
        if config.tavily_api_key:
            search_result = await retrievers.search_tavily(query=llm_res, api_key=config.tavily_api_key)
        else:
            search_result = await retrievers.search_baidu(query=llm_res)
        result = f"\"{llm_res}\" 在搜索引擎的搜索结果是：{search_result}"
        return result

    async def get_agent_context(self, llm: LLM_TYPE, question: str):
        return await self.get_search_result(llm=llm, question=question)


class Type4(BaseType):
    """命令执行"""

    @staticmethod
    def command_execute(cmd):
        """命令执行"""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr

    @staticmethod
    async def get_command_result(llm: LLM_TYPE, question: str):
        prompt = prompts.get_type4_prompt(question)
        llm_res = await llm.ask_model(question=prompt)
        logger.info(f"需要命令执行：{llm_res}")

        llm_res = llm_res.strip()
        cmd_res = Type4.command_execute(llm_res)
        data = f"命令 {llm_res} 在当前服务器的执行结果是：{cmd_res}"
        return data

    async def get_agent_context(self, llm: LLM_TYPE, question: str):
        return await self.get_command_result(llm=llm, question=question)


class Type5(BaseType):
    """你是谁"""

    @staticmethod
    def get_who_you_are():

        if config.custom_soul:
            prompt = config.custom_soul
        else:
            prompt = prompts.get_kurisu_prompt()

        text = f"关于你的信息：{prompt}"
        return text

    async def get_agent_context(self, *args, **kwargs):
        return self.get_who_you_are()


class Type6(BaseType):
    """功能列表"""

    @staticmethod
    def get_ai_abilities():

        text = '''
        当前助手有的功能：
            - 总结网页内容。例子：提取这个页面的内容，www.baidu.com/
            - 天气预报。例子：今天北京的天气怎样
            - 命令执行。例子：执行这条语句，ls -la
            - 聊天。例子：最近有什么新闻？帮我写一个打印 hello world 的代码    
        '''

        return text

    async def get_agent_context(self, *args, **kwargs):
        return self.get_ai_abilities()


class Type8(BaseType):
    """百科搜索能力"""

    async def get_agent_context(self, llm: LLM_TYPE, question: str):
        prompt = prompts.get_type8_prompt(question=question)
        query = await llm.ask_model(question=prompt)
        print(query)
        res = await retrievers.search_baidu_wiki(query)
        res = res[:3000]
        return res


type1 = Type1()
type2 = Type2()
type4 = Type4()
type5 = Type5()
type6 = Type6()
type8 = Type8()
