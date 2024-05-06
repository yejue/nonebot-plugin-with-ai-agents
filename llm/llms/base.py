class BaseLLMModel:
    """LLM 基类"""

    api_key: str = None
    model: str = None

    def get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        return headers

    async def ask_model(self, *args, **kwargs):
        raise NotImplemented("ask_model 需要被覆写")
