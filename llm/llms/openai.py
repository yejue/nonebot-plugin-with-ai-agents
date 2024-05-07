"""
OpenAI 平台（提供 ChatGPT 系列模型）
相关文档链接：https://platform.openai.com/docs/quickstart
"""

import httpx
from .base import BaseLLMModel


class OpenAIModel(BaseLLMModel):

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo-0125"):
        self.api_key = api_key
        self.model = model

    def get_body_template(self, temperature: float):
        body = {
            "model": self.model,
            "temperature": temperature,
            "messages": []
        }
        return body

    async def ask_model(
            self,
            question: str,
            system_prompt: str = None,
            message_history: list = (),
            temperature: float = 0.01
    ):
        """向 OpenAI 提问
         - question：用户问题
         - system_prompt：系统级提示词
         - message_history: 消息历史列表
        """
        url = 'https://gateway.ai.cloudflare.com/v1/269867777450cd358cac180511da1722/openai-01/openai/chat/completions'
        headers = self.get_headers()
        body = self.get_body_template(temperature)

        if message_history:
            body["messages"] = message_history

        if system_prompt:
            sys_msg = {"role": "system", "content": system_prompt}
            body["messages"].insert(0, sys_msg)

        user_message = {"role": "user", "content": question}
        body["messages"].append(user_message)
        print("openai body: ", body)

        async with httpx.AsyncClient() as client:
            r = await client.post(url, headers=headers, json=body, timeout=self.timeout)

            try:
                ans = r.json()["choices"][0]["message"]["content"]
            except httpx.ReadTimeout as e:
                print(f"访问大模型超时, {e}")
                ans = "访问大模型超时"
            except Exception as e:
                print(r.text + str(e))
                ans = "有错误，自己看日志"
            return ans
