class BaseLLMModel:
    """LLM 基类"""

    api_key: str = None
    model: str = None
    timeout: int = 30  # 大模型访问过期时间，秒

    def get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        return headers

    async def ask_model(self, *args, **kwargs):
        raise NotImplemented("ask_model 需要被覆写")
