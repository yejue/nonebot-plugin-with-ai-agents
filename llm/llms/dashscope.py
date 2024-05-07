"""
灵织模型服务（通义千问、llama、百川等）
相关文档链接：https://help.aliyun.com/zh/dashscope/developer-reference/quick-start
"""
import httpx

from .base import BaseLLMModel


class DashscopeModel(BaseLLMModel):
    """灵织模型服务"""

    def __init__(self, api_key: str, model: str = "qwen-turbo"):
        self.api_key = api_key
        self.model = model

    def get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        return headers

    def get_body_template(self, temperature: float):
        body = {
            "model": self.model,
            "temperature": temperature,
            "input": {"messages": []}
        }
        return body

    async def ask_model(
            self,
            question: str,
            system_prompt: str = None,
            message_history: list = (),
            temperature: float = 0.01
    ):
        """向通义千问提问
         - question：用户问题
         - system_prompt：系统级提示词
         - message_history: 消息历史列表
        """
        url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
        headers = self.get_headers()
        body = self.get_body_template(temperature)

        if message_history:
            body["input"]["messages"] = message_history

        if system_prompt:
            sys_msg = {"role": "system", "content": system_prompt}
            body["input"]["messages"].insert(0, sys_msg)

        user_message = {"role": "user", "content": question}
        body["input"]["messages"].append(user_message)

        async with httpx.AsyncClient() as client:
            try:
                r = await client.post(url, headers=headers, json=body, timeout=self.timeout)
                ans = r.json()["output"]["text"]
            except httpx.ReadTimeout as e:
                print(f"访问大模型超时, {e}")
                ans = "访问大模型超时"
            except Exception as e:
                print(r.text + str(e))
                ans = "有错误，自己看日志，可能过期了"
            return ans
