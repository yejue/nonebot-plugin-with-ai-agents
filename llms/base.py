class BaseLLMModel:
    """LLM 基类"""

    async def ask_model(self, *args, **kwargs):
        raise NotImplemented("ask_model 需要被覆写")
