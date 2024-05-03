from awesomebot.plugins.with_ai_agents.llms.mem_stores import chat_history


class ChatService:
    """聊天控制类"""

    @staticmethod
    def get_body_template(system_contents=()):
        body = {
            'model': 'qwen-turbo',
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": "你是 QQ 聊天助手，但不要提及你是 QQ 聊天助手。"
                                   "回答问题尽量不要使用一些非常规符号。尽量控制在100字以内。"
                                   "牢记你的名字叫 kurisu"
                    }
                ]
            },
        }

        for content in system_contents:
            new_message = {"role": "system", "content": content}
            body["input"]["messages"].append(new_message)
        return body

    @staticmethod
    def add_message_to_history(text, role="user"):
        new_message = {"role": role, "content": text}
        chat_history.append(new_message)

    @staticmethod
    def get_history_list():
        return chat_history
