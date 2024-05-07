"""
智普清言 AI 平台
相关文档链接：https://open.bigmodel.cn/dev/howuse/model
"""

import httpx
from .base import BaseLLMModel


class GLMModel(BaseLLMModel):

    def __init__(self, api_key: str, model: str ="glm-3-turbo"):
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
        """向 ChatGLM 提问
         - question：用户问题
         - system_prompt：系统级提示词
         - message_history: 消息历史列表
        """
        url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
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
            except httpx.ReadTimeout as e:
                print(f"访问大模型超时, {e}")
                ans = "访问大模型超时"
            except Exception as e:
                print(r.text + str(e))
                ans = "有错误，自己看日志，可能过期了"
            return ans
