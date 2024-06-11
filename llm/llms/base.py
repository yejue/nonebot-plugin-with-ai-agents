class BaseLLMModel:
    """LLM 基类"""

    api_key: str = None
    api_url: str = None  # 大模型 API 访问地址
    default_api_url: str = None  # 大模型 API 默认访问地址
    model: str = None  # 大模型名称
    timeout: int = 30  # 大模型访问过期时间，秒
    max_length = 8000  # 用字符长度简单约束 token 长度

    def get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        return headers

    def get_api_url(self):
        if not self.api_url:
            return self.default_api_url
        return self.api_url

    async def ask_model(self, *args, **kwargs):
        raise NotImplemented("ask_model 需要被覆写")
