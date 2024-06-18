"""
智普清言 AI 平台
相关文档链接：https://open.bigmodel.cn/dev/howuse/model
"""

from .base import BaseLLMModel


class GLMModel(BaseLLMModel):

    def __init__(self, api_key: str, model: str ="glm-3-turbo"):
        self.api_key = api_key
        self.model = model
        self.default_api_url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'

