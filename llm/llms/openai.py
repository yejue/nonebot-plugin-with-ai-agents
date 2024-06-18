"""
OpenAI 平台（提供 ChatGPT 系列模型）
相关文档链接：https://platform.openai.com/docs/quickstart
"""

from .base import BaseLLMModel


class OpenAIModel(BaseLLMModel):

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo-0125"):
        self.api_key = api_key
        self.model = model

        temp = 'https://gateway.ai.cloudflare.com/v1/269867777450cd358cac180511da1722/openai-01/openai/chat/completions'
        self.default_api_url = temp
