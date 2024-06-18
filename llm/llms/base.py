import httpx

from nonebot.log import logger


class BaseLLMModel:
    """LLM 基类"""

    api_key: str = None
    api_url: str = None  # 大模型 API 访问地址
    default_api_url: str = None  # 大模型 API 默认访问地址
    model: str = None  # 大模型名称
    timeout: int = 30  # 大模型访问过期时间，秒
    max_length = 8000  # 用字符长度简单约束 token 长度

    def get_body_template(self, temperature: float):
        body = {
            "model": self.model,
            "temperature": temperature,
            "messages": []
        }
        return body

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

    async def ask_model(
            self,
            question: str,
            system_prompt: str = None,
            message_history: list = (),
            temperature: float = 0.01
    ):
        """向 ChatGLM 提问
         - question：用户问题
         - system_prompt：系统级提示词
         - message_history: 消息历史列表
        """
        url = self.get_api_url()
        headers = self.get_headers()
        body = self.get_body_template(temperature)

        if message_history:
            body["messages"] = message_history

        if system_prompt:
            sys_msg = {"role": "system", "content": system_prompt}
            body["messages"].insert(0, sys_msg)

        user_message = {"role": "user", "content": question}
        body["messages"].append(user_message)

        async with httpx.AsyncClient() as client:
            try:
                r = await client.post(url, headers=headers, json=body, timeout=self.timeout)
                ans = r.json()["choices"][0]["message"]["content"]
            except httpx.ConnectTimeout as e:
                logger.critical(f"访问大模型超时, {e}")
                raise httpx.ConnectTimeout("访问大模型超时")
            except Exception as e:
                logger.critical(str(e))
                raise
            return ans
