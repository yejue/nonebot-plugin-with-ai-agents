from .mem_stores import chat_history


class ChatService:
    """聊天控制类"""

    @staticmethod
    def add_message_to_history(text, role="user"):
        new_message = {"role": role, "content": text}
        chat_history.append(new_message)

    @staticmethod
    def get_history_list():
        return chat_history

    @staticmethod
    def compress_chat_history(max_length: int = 5 * 10000):
        global chat_history
        if len(chat_history) > max_length:
            chat_history = chat_history[-(max_length//2):]

    @staticmethod
    def clear_chat_history():
        global chat_history
        length = len(chat_history)
        chat_history = []
        return length

    @staticmethod
    def get_strategically_chat_history(new_prompt: str, max_length: int):
        """策略获取聊天历史
         - 从最大长度消耗掉 len(new_prompt) 个长度
         - 根据最大长度，从历史列表中提取项目，每提取一条消耗 len(item) 个长度
         - max_length <= 0 后不再继续
        """
        ChatService.compress_chat_history()

        use_chat_history_list = []

        if not chat_history:
            return []

        if len(new_prompt) > max_length:
            return use_chat_history_list

        max_length_count = max_length - len(new_prompt)
        flag = 1

        while max_length_count > 0 and flag <= len(chat_history):
            history_item = chat_history[-flag]
            max_length_count -= len(history_item["content"])
            if max_length_count > 0:
                use_chat_history_list.insert(0, history_item)

            flag += 1

        return use_chat_history_list
