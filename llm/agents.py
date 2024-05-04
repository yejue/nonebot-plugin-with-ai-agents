"""
agents 应该被写成一个目录，而 type 应该是一个 .py 文件
之所以这么写是因为开发时 with_ai_agents 是作为一个 NoneBot 项目的子目录，
为了避免在未知主目录的情况下，子文件引用上一级文件的情况，所以尽量写在了同一级中，
这是一个应该被修正的问题
"""
from typing import Union

from .config import config
from .utils import prompts, retrievers
from .llms import BaseLLMModel, DashscopeModel, GLMModel


class Type1:
    """提取页面内容"""

    @staticmethod
    async def summarize_weblink_content(
            llm: Union[DashscopeModel, BaseLLMModel, GLMModel],
            question: str
    ):
        prompt = f'''
            请从我的问题中提取出网页链接，不要有其他信息。
            我的要求是:
            1. 如果有多个链接，只需要提取出第一个
            2. 如果没有链接，你可以回答"无"
            3. 下面是个例子：
                用户问题是: 总结下里面的内容： https://www.baidu.com
                你要回答: https://www.baidu.com
            
            我的问题是: 
            """
            {question}
            """
        '''
        url = await llm.ask_model(question=prompt)
        url = url.strip()
        print(f"type1 model res：{url}")

        url_content = await retrievers.get_url_content(url)
        url_content = url_content[:400]  # 最大 400 个字符
        print(f"提取页面内容：{url_content}")
        result = f"\"{url}\" 的大致内容是：{url_content}"
        return result


class Type2:
    """联网查询"""

    @staticmethod
    async def get_search_result(
            llm: Union[DashscopeModel, BaseLLMModel, GLMModel],
            question: str
    ):
        prompt = f'''
        请从我的问题中提出要搜索的内容，不要有其他信息。
        我的要求是：
        1. 回答只有一句话，20字以内
        2. 搜索的内容应该是你所不清楚的
        3. 下面是个例子：
            用户问题是：看一下最近有什么新闻呢
            你要回答：最近有什么新闻
            
        我的问题是：
        """
        {question}
        """
        '''
        llm_res = await llm.ask_model(question=prompt)
        print(f"需要联网搜索，llm_res={llm_res}")

        # 联网搜索
        if config.TAVILY_API_KEY:
            search_result = await retrievers.search_tavily(query=llm_res, api_key=config.TAVILY_API_KEY)
        else:
            search_result = await retrievers.search_bing(query=llm_res)
        result = f"\"{llm_res}\" 在搜索引擎的搜索结果是：{search_result}"
        return result


class Type5:
    """你是谁"""

    @staticmethod
    def get_who_you_are():
        text = f"关于你的信息：{prompts.get_kurisu_prompt()}"
        return text


class Type6:
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


type1 = Type1()
type2 = Type2()
type5 = Type5()
type6 = Type6()
